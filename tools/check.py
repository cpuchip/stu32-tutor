#!/usr/bin/env python3
"""check.py: every lesson's examples, run on the pinned core. The rules are docs/lesson-format.md.

    tools/check.py --core build/core-PIN lessons/*/

A lesson offers modes (front matter `modes:`, default all three: 33s 35s STU; decision 56), and is
checked in each of them on its own view: the keys blocks for that mode (a shared block, or the
variant that names the mode), the <mode m="..."> spans and <disp m="..."> quotes for that mode, and
the vectors for that mode (a vector applies to every mode, or to those named after an @ in its ID;
its first token, MODE33, is set to the mode's own). For each lesson and each offered mode:
  1. the vectors run on the firmware's vector runner, from a fresh core and from a used one (DIRTY:
     the stack full, LAST x set, RAD), and must pass.
  2. fmt-vectors.txt runs on the firmware's display runner (once: the formatter is every mode's).
  3. The ```keys setup``` block is the front matter's setup, with {mode} for the MODE soft key. Every
     other block in the view, after that setup with the mode filled in, is pressed on the device's
     key layer (keyrun) and must issue the same ops as its vector, leave the same core state, and
     leave the device at rest. Every vector of the mode is shown by a block of the view.
  4. Every <disp v="ID">text</disp> of the view sits after block ID and before the next block, is the
     text the device's screen shows after those keys in that mode, and (for a value) is the text of
     display vector D-ID@mode if there is one, else D-ID, of vector ID's exact X result.
  5. No em-dash anywhere in lesson.md, as a character or an entity.
  6. A student working through, in that mode: the setup once, then every block of the view in order
     on one device with nothing reset (student_sequence); every exact X, Y, Z, T and every quoted
     display must hold for that student too.
A lesson may also offer entries (front matter `entries:`, the default first: rpn, alg; decision 63).
Entry is a second axis built like modes: the setup presses {entry} right after {mode}, a keys block
may be a variant for `entry=alg`, a span is <entry e="alg">, a quote <disp ... e="alg">, a vector
ID@alg, and every step above runs once for each (mode, entry). A lesson with no `entries:` is RPN
and its setup has no {entry}. Algebraic entry is STU mode's alone (firmware 029 rule 2), so a lesson
offering alg offers STU mode only.
A file with no vectors, or a vector with no expectation, fails: a check that checks nothing is
not a pass.
"""
import argparse
import os
import re
import subprocess
import sys
import tempfile
from decimal import Decimal, InvalidOperation

sys.stdout.reconfigure(encoding="utf-8")

# The modes a lesson can offer, by the MODE menu's labels, and the vector token that sets each.
MODES = {"33s": "MODE33", "35s": "MODE35", "STU": "STU"}
ALL_MODES = ["33s", "35s", "STU"]
# The entries a lesson can offer, by name, and the MODE menu's soft key (and vector token) for each.
ENTRIES = {"rpn": "RPN", "alg": "ALG"}
ALL_ENTRIES = ["rpn", "alg"]
SETTING = re.compile(r"^(FIX|SCI|ENG)(\d+)$|^ALL$")
DISP = re.compile(r'<disp v="([^"]+)"(?: kind="(view|prompt|message|entry|status|eqn|program|row|line|readout|xmin|xmax|ymin|ymax|note)")?>(.*?)</disp>', re.S)
# A <disp> as written, attributes in any order (v, kind, m); mode_view rewrites it to DISP's form.
DISP_ANY = re.compile(r'<disp((?:\s+[a-z]+="[^"]*")*)\s*>(.*?)</disp>', re.S)
ATTR = re.compile(r'([a-z]+)="([^"]*)"')
MODE_SPAN = re.compile(r'<mode m="([^"]*)">(.*?)</mode>', re.S)
ENTRY_SPAN = re.compile(r'<entry e="([^"]*)">(.*?)</entry>', re.S)
# ```item ID```: a quiz or checkpoint item (docs/lesson-format.md, Items). Its fields, one a line:
# prompt, topics, answer (type or work), calculator (yes or no), keys (the working, needed for work),
# places (in a placement file: the unit it shows a learner is ready for), working (none: a typed answer
# that is counted or recalled, not computed), and any number of slip lines, "slip: VID | name | hint".
ITEM_BLOCK = re.compile(r"^[ \t]*```item[ \t]+(\S+)[ \t]*\n(.*?)^[ \t]*```[ \t]*$", re.M | re.S)
ITEM_FIELDS = ("prompt", "topics", "answer", "calculator", "keys", "places", "working", "slip", "twin")
# A typed answer that is computed is made by the core too, as vector <ID>W beside the typed one (abacus #6439).
# The lessons and placement files whose typed items predate that rule; the sweep (decision 76) takes each off
# as its unit's batch gives every computed item its working. A listed file whose items all have it is refused,
# so the list cannot outlive its need.
WORKING_PENDING = set()             # empty since the sweep reached the placement file (decision 76)


def parse_items(view):
    """(id, start, fields, slips, problems) for each item block of a view."""
    out = []
    for m in ITEM_BLOCK.finditer(view):
        fields, slips, problems = {}, [], []
        for raw in m.group(2).splitlines():
            line = raw.strip()
            if not line:
                continue
            k, sep, v = line.partition(":")
            k, v = k.strip(), v.strip()
            if not sep or k not in ITEM_FIELDS:
                problems.append(f"item {m.group(1)}: a line not one of {', '.join(ITEM_FIELDS)}: '{line}'")
            elif k == "slip":
                parts = [p.strip() for p in v.split("|")]
                if len(parts) != 3 or not all(parts):
                    problems.append(f"item {m.group(1)}: a slip is 'slip: VID | name | hint': '{line}'")
                else:
                    slips.append(tuple(parts))
            elif k in fields:
                problems.append(f"item {m.group(1)}: {k} given twice")
            else:
                fields[k] = v
        for k in ("prompt", "topics", "answer", "calculator"):
            if not fields.get(k):
                problems.append(f"item {m.group(1)}: no {k}:")
        if fields.get("answer") not in (None, "type", "work"):
            problems.append(f"item {m.group(1)}: answer: is type or work")
        if fields.get("calculator") not in (None, "yes", "no"):
            problems.append(f"item {m.group(1)}: calculator: is yes or no")
        if fields.get("answer") == "work" and not fields.get("keys"):
            problems.append(f"item {m.group(1)}: answer: work needs the working, as keys:")
        if fields.get("working") not in (None, "none"):
            problems.append(f"item {m.group(1)}: working: is none (a count or a concept), or left out")
        elif fields.get("working") == "none" and fields.get("answer") != "type":
            problems.append(f"item {m.group(1)}: working: none is for a typed answer; a worked item's keys are its working")
        out.append((m.group(1), m.start(), fields, slips, problems))
    return out


def answer_of(parts, result):
    """A vector's answer, as an item judges it: ("exact", value) from its last result= expectation, or
    ("within", center, tol) from result#c,t; None when it has neither."""
    exps = parts[3].split()
    within = [e for e in exps if re.match(rf"^{result}#[^,]+,\S+$", e)]
    exact = [e for e in exps if e.startswith(f"{result}=")]
    try:
        if exact:
            return ("exact", Decimal(exact[-1].split("=", 1)[1]))
        if within:
            c, t = within[-1][2:].split(",", 1)
            return ("within", Decimal(c), Decimal(t))
    except InvalidOperation:
        return None
    return None
# A graph's texts as screen.c draws them (unit 033b; keyrun's GRAPH line): the trace readout, the window labels
# and the plotted form's note.
GRAPH_KINDS = ("readout", "xmin", "xmax", "ymin", "ymax", "note")
FRAC_SETTINGS = {"/C", "SF:7", "CF:7", "SF:8", "CF:8", "SF:9", "CF:9"}  # change the fraction display
# ```keys ID``` or ```keys ID after=PREV```: a continuation holds only the keys pressed after block
# PREV, which must be the block just before it (in the mode's view); its full keys are PREV's full
# keys and then its own. KEYS_BLOCK reads the view; KEYS_ANY reads the lesson as written, with
# mode= variants.
KEYS_BLOCK = re.compile(r"^[ \t]*```keys[ \t]+([^\s=]+)(?:[ \t]+after=(\S+))?[ \t]*\n(.*?)^[ \t]*```[ \t]*$", re.M | re.S)
KEYS_ANY = re.compile(r"^([ \t]*)```keys[ \t]+([^\s=]+)((?:[ \t]+[a-z]+=\S+)*)[ \t]*\n(.*?)^[ \t]*```[ \t]*$", re.M | re.S)
KEYS_FENCE = re.compile(r"^```keys[ \t]+[^\s=]+(?:[ \t]+(?:after|mode|entry|twin|fade)=\S+)*[ \t]*$")
SHOWS = re.compile(r"\b(shows?|showed|showing|shown|displays?|displayed|screen|reads|appears?)\b", re.I)
FENCE = re.compile(r"^[ \t]*(```|~~~)(.*)$", re.M)
# A used calculator: every variable A-Z holds 7, RAD, the stack full, lift enabled, LAST x 6.
DIRTY = " ".join(["RAD"] + [f"7 STO:{v}" for v in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"] + "9 ENTER 8 ENTER 7 ENTER 6 SQRT".split())
DEVICE_WIDTH = "w=21"                           # the X line's width on the device (screen.c FMT_WIDTH)
MAX_EXPECT = 64                                # the runner keeps no more than this per vector
EM_DASH = ("—", "&mdash;", "&#8212;", "&#x2014;", "&#X2014;")


def front_matter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}, text
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta, text[m.end():]


def read_vectors(path, nfields):
    """(id, fields, line) for each vector line; comments and blanks skipped."""
    out = []
    with open(path, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            s = line.rstrip("\n")
            if not s.strip() or s.lstrip().startswith("#"):
                continue
            parts = [p.strip() for p in s.split("|")]
            if len(parts) != nfields:
                raise ValueError(f"{path}:{n}: {len(parts)} fields, expected {nfields}")
            out.append((parts[0], parts, s))
    return out


# Voices (decision 71; docs/proposals/voices.md): a lesson may offer a story reading and a plain one of the same
# skeleton, `voices: story plain` in its front matter (the default first). Text inside <voice v="story">…</voice>
# or <voice v="plain">…</voice> belongs to that voice; everything outside is shared. A span holds prose only, so
# every voice has the same keys blocks, quotes, items and sections; check_voices proves it on the readings.
VOICES = ("story", "plain")
VOICE_SPAN = re.compile(r'<voice v="([^"]*)">(.*?)</voice>', re.S)
VOICE_HOLDS_NOT = (("```keys", "a keys block"), ("```item", "an item"), ("```why", "a why block"), ("<disp", "a <disp> quote"),
                   ("<mode", "a <mode> span"), ("<entry", "an <entry> span"), ("<voice", "a <voice> span"))
SKELETON = re.compile(r"^[ \t]*```(?:keys|item|why)\b.*?^[ \t]*```[ \t]*$|<disp\b[^>]*>.*?</disp>|^## [^\n]*$", re.M | re.S)
# ```why```: a "Why?" prompt under a worked example (decision 76, step 4): `ask:` the question, `because:` the reason
# the page reveals on request. The words are the non-author read's; the numbers are checked: every number in a why
# block is one its example shows (its keys, its prose, its quoted displays), so a reason cannot cite a number the
# core did not make.
WHY_BLOCK = re.compile(r"^[ \t]*```why[ \t]*\n(.*?)^[ \t]*```[ \t]*$", re.M | re.S)

# Maths (docs/proposals/maths-markup.md; TeX with primer #6738, everything typeset by Michael #6967): an inline span
# is $...$ on one line with TeX inside, a ```math fence holds one display equation, and a $ that is not maths is
# written \$. The page renders the TeX with KaTeX. check.py reads each span back to the plain text the lessons wrote
# before the markup (maths_text, over a closed list of commands), and every other check reads that text, so the
# markup changes nothing a check sees.
MATHS_FENCE = re.compile(r"^[ \t]*```math[ \t]*\n(.*?)^[ \t]*```[ \t]*$", re.M | re.S)
MATHS_TAG = re.compile(r"</?(?:voice|mode|entry|disp)\b[^>]*>")
MATHS_KEEP, MATHS_END = "", ""      # around a span's reading, so seen() strips no tag or id inside it
SUP_CHARS = "0123456789-+()nxytrkabcdeimhT"        # the letters the lessons write raised: eˣ, (eʳ)ᵗ, 1.04ᵀ (abacus #7274)
SUP_FORMS = "⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺⁽⁾ⁿˣʸᵗʳᵏᵃᵇᶜᵈᵉⁱᵐʰᵀ"
SUP = str.maketrans(SUP_CHARS, SUP_FORMS)
MATHS_COMMANDS = {r"\times": "×", r"\div": "÷", r"\le": "≤", r"\ge": "≥", r"\pm": "±", r"\neq": "≠", r"\cdot": "·",
                  r"\pi": "π", r"\theta": "θ", r"\infty": "∞", r"\,": "", r"\left": "", r"\right": "",
                  r"\%": "%", r"\angle": "∠",         # \% and \angle: abacus #7218
                  r"\dots": "…"}                      # a sum's ellipsis, 1 + 2 + … + 10
MATHS_VULGAR = {("1", "2"): "½", ("1", "4"): "¼", ("3", "4"): "¾"}   # \dfrac{1}{2} reads as ½ (KaTeX refuses ½ itself;
#   \dfrac as the page sets every fraction, primer #7286: \tfrac would be text-size, which abacus ruled too small)
MATHS_OPERATORS = ("LCM", "GCF")                      # \operatorname{...}: upright names (abacus #7227)
MATHS_FUNCTIONS = ("sin", "cos", "tan", "log", "ln")  # \sin ...: KaTeX's own names (abacus #7263); unlike other
#                                                       letter commands the space after one is kept: "sin x"
MATHS_KEY_NAMES = ("SIN", "COS", "TAN", "LOG", "LN", "ABS", "ASIN", "ACOS", "ATAN")   # keys: never in a span


class MathsRefused(ValueError):
    pass


def maths_group(tex, i):
    """(the text of the {...} group or the single character at i, the index after it)."""
    if i >= len(tex):
        raise MathsRefused("a command is missing its argument")
    if tex[i] == "{":
        depth, j = 1, i + 1
        while depth:
            if j >= len(tex):
                raise MathsRefused("an unclosed {")
            depth += {"{": 1, "}": -1}.get(tex[j], 0)
            j += 1
        return tex[i + 1:j - 1], j
    if tex[i] in "}\\":
        raise MathsRefused("a command is missing its argument")
    return tex[i], i + 1


def maths_wrap(s):
    return s if re.fullmatch(r"[\w.]+", s) else f"({s})"


def maths_text(tex):
    """A maths span's TeX read as the plain text the lessons write: ^2 as ², ^{r × t} as ^(r × t), ^{2.5} as ^2.5,
    \\frac{1}{4} as 1/4, \\frac{1 + 3}{4 + 8} as (1 + 3)/(4 + 8), \\sqrt{x} as √x, ' as ′, \\operatorname{LCM} as LCM
    (MATHS_OPERATORS only), and MATHS_COMMANDS as their symbols. Anything else is taken as
    written. A command off the list, a bare brace or a missing argument is refused (MathsRefused)."""
    out, i = [], 0
    while i < len(tex):
        c = tex[i]
        if c == "\\":
            m = re.match(r"\\([A-Za-z]+|.)", tex[i:], re.S)
            name = "\\" + m.group(1)
            i += len(m.group(0))
            if m.group(1) in MATHS_FUNCTIONS:
                out.append(m.group(1))              # sin, cos ...: the space after is kept, as the lessons write it
                continue
            if m.group(1) == "dots":
                out.append("…")                     # and after the ellipsis: "… + 44"
                continue
            if m.group(1).isalpha() and i < len(tex) and tex[i] == " ":
                i += 1                              # TeX drops one space after a letter command
            if name == r"\frac":
                a, i = maths_group(tex, i)
                b, i = maths_group(tex, i)
                out.append(f"{maths_wrap(maths_text(a))}/{maths_wrap(maths_text(b))}")
            elif name == r"\sqrt":
                if tex[i:i + 1] == "[":
                    raise MathsRefused(r"\sqrt[n] is not on the list")
                a, i = maths_group(tex, i)
                out.append("√" + maths_wrap(maths_text(a)))
            elif name == r"\dfrac":
                a, i = maths_group(tex, i)
                b, i = maths_group(tex, i)
                if (a, b) not in MATHS_VULGAR:
                    raise MathsRefused(f"\\dfrac{{{a}}}{{{b}}} is not on the list: \\dfrac writes ½ ¼ ¾ only; a fraction is \\frac")
                out.append(MATHS_VULGAR[(a, b)])
            elif name == r"\text":
                a, i = maths_group(tex, i)          # words in a formula, sin A = \text{opposite} (abacus #7274)
                if not re.fullmatch(r"[A-Za-z]+(?: [A-Za-z]+)*", a):
                    raise MathsRefused(f"\\text{{{a}}} holds words only: letters and single spaces, no digit")
                out.append(a)
            elif name == r"\operatorname":
                a, i = maths_group(tex, i)
                if a not in MATHS_OPERATORS:
                    raise MathsRefused(f"\\operatorname{{{a}}} is not on the list ({', '.join(MATHS_OPERATORS)})")
                out.append(a)
            elif name in MATHS_COMMANDS:
                out.append(MATHS_COMMANDS[name])
            else:
                raise MathsRefused(f"{name} is not on the list")
        elif c == "^":
            a, i = maths_group(tex, i + 1)
            body = maths_text(a)
            plain = body.replace("−", "-")
            if plain and all(ch in SUP_CHARS for ch in plain):
                out.append(plain.translate(SUP))
            elif re.fullmatch(r"[\d.]+", body):
                out.append("^" + body)              # no superscript for the point: the lessons write 0.5^2.5
            else:
                out.append(f"^({body})")            # nor for letters: the lessons write e^(r × t)
        elif tex.startswith("''", i):
            out.append("″")
            i += 2
        elif c == "'":
            out.append("′")
            i += 1
        elif tex.startswith("{,}", i):
            out.append(",")                         # a thousands comma, 10{,}000: no space after it
            i += 3
        elif c in "{}":
            raise MathsRefused("a bare brace")
        elif c == "%":
            raise MathsRefused(r"a bare % (TeX takes it as a comment and drops the rest of the span): write \%")
        else:
            out.append(c)
            i += 1
    return "".join(out)


def maths_scan(text):
    """(the inline maths spans of a text, each (start, end, tex) with start at its opening $ and end after its
    closing $; the problems with its $ marks). A span opens at a $ and closes at the next $ on the same line; it is
    not empty and neither starts nor ends with a space. \\$ is a dollar, not a mark."""
    spans, out, at = [], [], 0
    for line in text.splitlines(keepends=True):
        marks = [m.start() for m in re.finditer(r"(?<!\\)\$", line)]
        if len(marks) % 2:
            out.append(f"a $ with no closing $ on its line: '{line.strip()[:80]}'")
            marks = marks[:-1]
        for a, b in zip(marks[::2], marks[1::2]):
            tex = line[a + 1:b]
            if not tex:
                out.append(f"an empty maths span ($$) in '{line.strip()[:80]}': display maths is a ```math fence")
            elif tex != tex.strip():
                out.append(f"a maths span that starts or ends with a space: '${tex}$'")
            else:
                spans.append((at + a, at + b + 1, tex))
        at += len(line)
    return spans, out


def maths_spans(text):
    """The inline maths spans of a text, each (start, end, tex): the page's `maths` question (primer)."""
    return maths_scan(text)[0]


def check_maths(body):
    """Problems with a lesson's maths: the $ marks; a span where maths may not go (a heading, a keys block, a <disp>
    quote, a tag, a ```math fence, an item's field other than prompt: and slip:); a span across a tag (a voice span's
    included); a span written before the word "key" (a key's name is plain: "the x² key"); a ```math fence that is not
    one line of TeX; and any TeX maths_text refuses."""
    spans, out = maths_scan(body)
    places = [(m.start(), m.end(), what) for pattern, what in
              ((re.compile(r"^#+ [^\n]*$", re.M), "a heading"), (KEYS_ANY, "a keys block"), (DISP_ANY, "a <disp> quote"),
               (MATHS_TAG, "a tag"), (MATHS_FENCE, "a ```math fence (it holds TeX without $)"))
              for m in pattern.finditer(body)]
    slips = []
    for m in ITEM_BLOCK.finditer(body):
        at = m.start(2)
        for line in m.group(2).splitlines(keepends=True):
            if line.split(":", 1)[0].strip() not in ("prompt", "slip"):
                places.append((at, at + len(line), "an item's field other than prompt and slip"))
            elif line.split(":", 1)[0].strip() == "slip":
                slips.append((at, at + len(line)))
            at += len(line)
    for a, b, tex in spans:
        where = next((what for s, e, what in places if s <= a < e), None)
        if where:
            out.append(f"a maths span in {where}: '${tex}$'")
            continue
        if "|" in tex and any(s <= a < e for s, e in slips):
            out.append(f"a | inside a maths span on a slip line: '${tex}$'; | separates a slip's fields, so write the "
                       f"absolute value in words there")
            continue
        if MATHS_TAG.search(tex):
            out.append(f"a maths span across a tag: '${tex}$'; a span lies wholly inside one <voice> span or outside them all")
            continue
        if re.match(r"\s*key", body[b:b + 6]):
            out.append(f"a maths span names a key: '${tex}$ key'; write a key's name plain, as in 'the x² key'")
        if r"\text" in tex and not re.search(rf"[=+−×÷<>≤≥≠±]|\\(?:{'|'.join(MATHS_FUNCTIONS)})\b",
                                             re.sub(r"\\text\{[^}]*\}", "", tex)):
            out.append(f"a \\text with no function, operator or relation beside it: '${tex}$'; words alone are prose")
        named = re.findall(rf"(?<![A-Za-z\\])({'|'.join(MATHS_KEY_NAMES)})(?![A-Za-z])", tex)
        if named:
            maths = {"ABS": "|x|", "ASIN": "\\sin^{-1}", "ACOS": "\\cos^{-1}", "ATAN": "\\tan^{-1}"}.get(
                named[0], "\\" + named[0].lower())
            out.append(f"a maths span holds the key name {named[0]}: '${tex}$'; a key's name is plain, and in maths "
                       f"the function is written {maths}")
        try:
            maths_text(tex)
        except MathsRefused as e:
            out.append(f"the maths span '${tex}$': {e}")
    # A half-span (abacus #7274, its maths_halfspan detector): an operator in the prose touching a span, as in
    # "eˣ = $3x$" or "$500 × 1.04$ᵀ = 1000", means part of one expression was left out of it. Tags are masked first
    # (a voice tag's < is not an operator); keys blocks, quotes and math fences are not prose.
    hidden = body
    for rx in (KEYS_ANY, DISP_ANY, MATHS_FENCE, MATHS_TAG):
        hidden = rx.sub(lambda m: "\x00" * len(m.group(0)), hidden)
    for a, b, tex in spans:
        left, right = hidden[max(0, a - 2):a], hidden[b:b + 2]
        if re.search(r"[=+−×÷<>≤≥≠±] ?\Z", left) or re.match(r" ?[=+−×÷<>≤≥≠±]", right) \
                or re.search(rf"[\w{SUP_FORMS}′)]\Z", left) or re.match(rf"[{SUP_FORMS}(]|(?!s\b)\w", right):
            # (a plural s is English: "how many $\frac{2}{10}$s make")
            out.append(f"a maths span touching more maths outside it: '{hidden[max(0, a - 12):a]}${tex}${hidden[b:b + 12]}'"
                       f"; put the whole expression in the span")
    for m in MATHS_FENCE.finditer(body):
        lines = [l for l in m.group(1).splitlines() if l.strip()]
        if len(lines) != 1 or "$" in m.group(1):
            out.append(f"a ```math fence holds one equation on one line, with no $: {lines}")
            continue
        try:
            maths_text(lines[0].strip())
        except MathsRefused as e:
            out.append(f"the ```math fence '{lines[0].strip()}': {e}")
    return out


def maths_read(body):
    """The lesson as every other check reads it: each maths span and ```math fence replaced by its reading (between
    MATHS_KEEP and MATHS_END), and \\$ by $. A span check_maths refused is left as written."""
    def fence(m):
        try:
            return MATHS_KEEP + maths_text(m.group(1).strip()) + MATHS_END
        except MathsRefused:
            return m.group(0)
    body = MATHS_FENCE.sub(fence, body)
    for a, b, tex in reversed(maths_spans(body)):
        try:
            body = body[:a] + MATHS_KEEP + maths_text(tex) + MATHS_END + body[b:]
        except MathsRefused:
            pass
    return body.replace("\\$", "$")


def maths_plain(text):
    """A read text with the marks around each span's reading dropped: the text the lessons wrote before the markup."""
    return text.replace(MATHS_KEEP, "").replace(MATHS_END, "")


def numbers_in(text):
    """The numbers written in a text, as values (commas dropped), so 12 and 12.0000 are one number."""
    out = set()
    for n in re.findall(r"\d+(?:[.,]\d+)*", text):
        try:
            out.add(Decimal(n.replace(",", "")))
        except InvalidOperation:
            pass
    return out


def lead_in(body, blocks, i):
    """The example's lead-in (abacus #6632): the prose paragraph directly above its first keys block, a run of its
    variants (mode= or entry=) taken as one block, or "" when that paragraph is a heading or another fence."""
    while i > 0 and blocks[i - 1].group(2) == blocks[i].group(2) and not body[blocks[i - 1].end():blocks[i].start()].strip():
        i -= 1
    para = body[:blocks[i].start()].rstrip().split("\n\n")[-1]
    if re.search(r"^## ", para, re.M) or para.strip().endswith("```"):
        return ""
    return para


def seen(text):
    """What a learner reads of a stretch of lesson: no keys fence's info line, no tag's attributes, and no lesson id
    (the page shows sys-01 as its title, abacus #5459). An ID such as L02, <disp v="S01"> or rpn-01 is not a number
    the example shows, nor one a why block names. A maths span's reading is lifted out first and put back whole, so
    "x < 2 ... >" is not taken for a tag nor "x-10" for a lesson id (docs/proposals/maths-markup.md §3)."""
    lifted = []

    def lift(m):
        lifted.append(m.group(1))
        return f"{len(lifted) - 1}"
    text = re.sub(f"{MATHS_KEEP}(.*?){MATHS_END}", lift, text, flags=re.S)
    text = re.sub(r"<[^>]*>", " ", re.sub(r"^[ \t]*```keys[^\n]*\n", "", text, flags=re.M))
    text = re.sub(r"\b[a-z]+-\d{2}[a-z]?\b", " ", text)
    return re.sub("(\\d+)", lambda m: " " + lifted[int(m.group(1))] + " ", text)


def check_why(body):
    """Problems with a lesson's why blocks: each holds ask: and because: and nothing else, sits under a worked example
    (the nearest keys block above it other than the setup, with no ## heading between), and names only numbers that
    example shows: its lead-in paragraph, its keys, and its prose and displays below (abacus #6632)."""
    out = []
    for m in WHY_BLOCK.finditer(body):
        fields, bad_lines = {}, []
        for raw in m.group(1).splitlines():
            line = raw.strip()
            if not line:
                continue
            k, sep, v = line.partition(":")
            if not sep or k.strip() not in ("ask", "because") or k.strip() in fields:
                bad_lines.append(line)
            else:
                fields[k.strip()] = v.strip()
        if bad_lines or not fields.get("ask") or not fields.get("because"):
            out.append(f"a why block needs one ask: and one because: line and nothing else: {bad_lines or sorted(fields)}")
            continue
        blocks = list(KEYS_ANY.finditer(body))
        above = [i for i, k in enumerate(blocks) if k.end() <= m.start() and k.group(2) != "setup"]
        if not above:
            out.append(f"a why block with no worked example above it: '{fields['ask']}'")
            continue
        last = blocks[above[-1]]
        example = body[last.start():m.start()]
        if re.search(r"^## ", example, re.M):
            out.append(f"a why block with a ## heading between it and its example ({last.group(2)}): '{fields['ask']}'")
            continue
        missing = sorted(numbers_in(seen(fields["ask"] + " " + fields["because"]))
                         - numbers_in(seen(example)) - numbers_in(seen(lead_in(body, blocks, above[-1]))))
        if missing:
            out.append(f"a why block under {last.group(2)} names {', '.join(str(x) for x in missing)}, which its "
                       f"example does not show")
    return out


SHIFTS = ("GOLD", "BLUE")                             # a shift and its key are one keystroke for fading


def operands(text):
    """The numbers of a text, sorted, as values: a twin and an item collide when these are equal (in any order)."""
    return sorted(Decimal(n) for n in re.findall(r"(?<![\w.])\d+(?:\.\d+)?(?![\w.])", text))


def problem_operands(prompt):
    """A prompt's problem, as operands: its first maths span (a read prompt keeps it between MATHS_KEEP and MATHS_END),
    so "Work out $37 × 24$ in parts: $37 × 4$, then ..." is [24, 37], not its helper parts too; a prompt with no
    span gives all its numbers."""
    m = re.search(f"{MATHS_KEEP}(.*?){MATHS_END}", prompt)
    return operands(m.group(1) if m else prompt)


def unit_problems(lesson_dir, lesson_id):
    """Every problem a learner meets in the lesson's unit (abacus #7310): each item's prompt, as (ID, operands), and
    each Exercises line, as ("lesson exercise N", operands), over the lessons the course files put in its unit. The
    unit is found by the lesson's id in this repository's courses; the lesson itself is read from lesson_dir (a
    control's planted copy is what is checked), its siblings from lessons/."""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    folders = [d for d in os.listdir(os.path.join(root, "lessons")) if os.path.isdir(os.path.join(root, "lessons", d))]
    me = next((f for f in folders if f == lesson_id or f.startswith(f"{lesson_id}-")), None)
    unit = None
    for path in sorted(os.listdir(os.path.join(root, "courses"))):
        here, members = None, {}
        for line in open(os.path.join(root, "courses", path), encoding="utf-8"):
            p = [x.strip() for x in line.split("|")]
            if p[0] == "unit":
                here = p[1]
            elif p[0] == "lesson":
                d = next((f for f in folders if f == p[1] or f.startswith(p[1] + "-")), None)
                members.setdefault(here, []).append(d)
        for u, ds in members.items():
            if me in ds:
                unit = ds
    out = []
    for d in unit or [me]:
        path = os.path.join(lesson_dir, "lesson.md") if d == me or d is None else os.path.join(root, "lessons", d, "lesson.md")
        meta, body = front_matter(open(path, encoding="utf-8").read())
        voices = lesson_voices(meta)[0]
        body = maths_read(body if voices == [None] else voice_view(body, voices[0]))   # the default reading
        for m in ITEM_BLOCK.finditer(body):
            prompt = next((l.split(":", 1)[1] for l in m.group(2).splitlines() if l.strip().startswith("prompt:")), "")
            if not re.search(r"^[ \t]*twin:", m.group(2), re.M):
                out.append((m.group(1), problem_operands(prompt)))
        ex = re.search(r"^## Exercises\n(.*?)(?=^## |\Z)", body, re.M | re.S)
        for n, item in re.findall(r"^(\d+)\. (.*?)(?=^\d+\. |\Z)", ex.group(1) if ex else "", re.M | re.S):
            out.append((f"{d[:8]} exercise {n}", operands(maths_plain(item))))
    return out


def check_worked(body, unit=()):
    """Problems with a lesson's twins and faded blocks (docs/proposals/worked-examples.md, abacus #7299, primer
    #7300). A twin names an earlier keys block: an item with `twin:` (answer: type, calculator: no) after it and
    before the next block, or a keys block with `twin=` that has prose of its own (its prompt) after it; neither
    leaves its section, and neither works the example's own operands. `fade=N` hides a block's last N keystrokes:
    at least one and not all, not on the setup, never splitting a shift from its key, and never on a twin."""
    out = []
    blocks = list(KEYS_ANY.finditer(body))
    first, last = {}, {}
    for m in blocks:
        first.setdefault(m.group(2), m)
        last[m.group(2)] = m

    def collides(who, ops):
        """A twin whose operands are an item's or an exercise's in the unit hands the learner that answer."""
        for label, other in unit:
            if other == ops and len(ops) >= 2:
                out.append(f"{who} works the same operands as {label} in its unit; a twin's numbers are its own")
                return

    def section_between(a, b):
        return bool(re.search(r"^## ", body[a:b], re.M))
    for m in blocks:
        bid, attrs, keys = m.group(2), dict(re.findall(r"([a-z]+)=(\S+)", m.group(3))), m.group(4)
        if "fade" in attrs:
            toks = keys.split()
            n = int(attrs["fade"]) if attrs["fade"].isdigit() else 0
            if "twin" in attrs:
                out.append(f"keys block {bid} is both twin= and fade=; a twin hides all its keys already")
            elif bid == "setup":
                out.append("the setup block may not be faded")
            elif not 1 <= n < len(toks):
                out.append(f"keys block {bid}: fade={attrs['fade']} must hide at least one keystroke and leave one shown "
                           f"(the block has {len(toks)})")
            elif toks[len(toks) - n - 1] in SHIFTS:
                out.append(f"keys block {bid}: fade={n} splits {toks[len(toks) - n - 1]} from its key; a shift and its "
                           f"key are one keystroke")
        if "twin" in attrs:
            ex = attrs["twin"]
            if ex not in first or first[ex].start() >= m.start():
                out.append(f"keys block {bid}: twin={ex} names no keys block before it")
                continue
            gap = body[last[ex].end():m.start()]
            if section_between(last[ex].end(), m.start()):
                out.append(f"keys block {bid}: twin of {ex} in another section; a twin follows its example")
            paras = [p for p in re.split(r"\n[ \t]*\n", KEYS_ANY.sub("", gap)) if re.sub(r"<[^>]*>|\s", "", p)]
            if len(paras) < 2:
                # the first paragraph after the example is the example's own ("X holds 4."); the twin's prompt is
                # a paragraph after it (primer #7300)
                out.append(f"keys block {bid}: twin of {ex} with no prose of its own before it; its prompt is a "
                           f"paragraph after the example's own lines")
            if operands(keys) == operands(last[ex].group(4)):
                out.append(f"keys block {bid}: twin of {ex} works the example's own operands; a twin has new numbers")
            collides(f"keys block {bid}", operands(keys))
    for m in ITEM_BLOCK.finditer(body):
        iid, f = m.group(1), {}
        for line in m.group(2).splitlines():
            k, sep, v = line.strip().partition(":")
            if sep and k.strip() not in f:
                f[k.strip()] = v.strip()
        ex = f.get("twin")
        if ex is None:
            continue
        if ex not in first or first[ex].start() >= m.start():
            out.append(f"item {iid}: twin: {ex} names no keys block before it")
            continue
        later = [b for b in blocks if last[ex].end() <= b.start() < m.start() and b.group(2) != ex
                 and dict(re.findall(r"([a-z]+)=(\S+)", b.group(3))).get("after") != ex]   # (a continuation is the example's)
        if later or section_between(last[ex].end(), m.start()):
            out.append(f"item {iid}: twin of {ex} is not right after it (a keys block or a ## heading comes between)")
        if f.get("answer") != "type" or f.get("calculator") != "no":
            out.append(f"item {iid}: a twin item is answer: type and calculator: no (it leaves the device alone)")
        ops = problem_operands(f.get("prompt", ""))
        if ops == operands(last[ex].group(4)):
            out.append(f"item {iid}: twin of {ex} works the example's own operands; a twin has new numbers")
        collides(f"item {iid}", ops)
    return out


def lesson_voices(meta):
    """(the lesson's voices, the default first, or [None]; a problem or None)."""
    if "voices" not in meta:
        return [None], None
    vs = meta["voices"].split()
    if len(vs) < 2 or len(set(vs)) != len(vs) or any(v not in VOICES for v in vs):
        return [None], f"`voices: {meta['voices']}` must name two or more of {' '.join(VOICES)}, each once"
    return vs, None


def voice_view(body, voice):
    """The lesson as read in one voice: that voice's spans kept (their text), the others removed."""
    return VOICE_SPAN.sub(lambda m: m.group(2) if m.group(1) == voice else "", body)


def prose_numbers(text):
    """The numerals a reading writes in its prose (outside its keys blocks, items, quotes and headings), in order:
    a voice may reword a problem's setup, never its numbers (abacus #6550)."""
    return re.findall(r"\d+(?:[.,]\d+)*", SKELETON.sub(" ", text))


def check_voices(meta, body):
    """Problems with a lesson's voices: the spans as written, and the proof that every reading has the default's
    skeleton (keys blocks, items, quotes and ## headings, in order) and its prose's numbers."""
    voices, why = lesson_voices(meta)
    if why:
        return [why]
    spans = list(VOICE_SPAN.finditer(body))
    rest = VOICE_SPAN.sub("", body)
    out = []
    if "<voice" in rest or "</voice>" in rest:
        out.append('a <voice> tag not in the form <voice v="...">...</voice>')
    if voices == [None]:
        if spans:
            out.append("a <voice> span, but the front matter offers no `voices:`")
        return out
    for m in spans:
        v, inner = m.group(1), m.group(2)
        if v not in voices:
            out.append(f'<voice v="{v}">: {v} is not one of the lesson\'s voices ({" ".join(voices)})')
        for token, what in VOICE_HOLDS_NOT:
            if token in inner:
                out.append(f'<voice v="{v}"> holds {what}; a voice span holds prose only, so every voice has the same skeleton')
        if re.search(r"^## ", inner, re.M):
            out.append(f'<voice v="{v}"> holds a ## heading; sections are shared by every voice')
    for v in voices:
        if not any(m.group(1) == v for m in spans):
            out.append(f"`voices:` offers {v}, but no <voice v=\"{v}\"> span says anything in it")
    base = voice_view(body, voices[0])
    for v in voices[1:]:
        reading = voice_view(body, v)
        if SKELETON.findall(reading) != SKELETON.findall(base):
            out.append(f"the {v} reading's keys blocks, items, quotes or sections differ from the {voices[0]} reading's")
        a, b = prose_numbers(reading), prose_numbers(base)
        if a != b:
            i = next((k for k, (x, y) in enumerate(zip(a, b)) if x != y), min(len(a), len(b)))
            out.append(f"the {v} reading's prose has other numbers than the {voices[0]} reading's: at numeral "
                       f"{i + 1}, {a[i] if i < len(a) else 'none'} against {b[i] if i < len(b) else 'none'}")
    return out


def lesson_modes(meta):
    """The modes a lesson offers (all three unless its front matter lists fewer), and any problem."""
    modes = meta.get("modes", " ".join(ALL_MODES)).split()
    if not modes or any(m not in MODES for m in modes) or len(set(modes)) != len(modes):
        return ALL_MODES, f"front matter `modes: {meta.get('modes')}`: give some of 33s 35s STU, once each"
    if sorted(modes) != sorted(ALL_MODES) and not meta.get("modes_reason"):
        return modes, "front matter offers fewer than all three modes without a `modes_reason`"
    return [m for m in ALL_MODES if m in modes], None


def lesson_entries(meta, modes):
    """The entries a lesson offers, the default first, and any problem. A lesson with no `entries:`
    gives [None]: RPN, with no {entry} in its setup and no entry token in its vectors."""
    if "entries" not in meta:
        return [None], None
    entries = meta["entries"].split()
    if not entries or any(e not in ENTRIES for e in entries) or len(set(entries)) != len(entries):
        return [None], f"front matter `entries: {meta['entries']}`: give some of rpn alg, once each, the default first"
    if "alg" in entries and modes != ["STU"]:
        return entries, ("front matter offers alg in a mode other than STU: algebraic entry is STU mode's alone "
                         "(firmware 029 rule 2), so the lesson gives `modes: STU` and a `modes_reason`")
    return entries, None


def mode_list(text):
    return [m.strip() for m in text.split(",") if m.strip()]


def scope_fit(modes, entries, mode, entry):
    """How a variant scoped to some modes and entries (None: any) fits (mode, entry): None if it does
    not apply there, else the number of axes it names, so that the narrower variant wins."""
    if modes is not None and mode not in modes:
        return None
    if entries is not None and (entry or "rpn") not in entries:
        return None
    return (modes is not None) + (entries is not None)


def pick(cands, mode, entry, what, problems):
    """The candidate that fits (mode, entry) most narrowly, from (modes, entries, item) triples; two
    that fit equally narrowly are a problem (appended once per pair, when problems is given)."""
    fits = [(scope_fit(ms, es, mode, entry), item) for ms, es, item in cands]
    fits = [(f, item) for f, item in fits if f is not None]
    if not fits:
        return None
    best = max(f for f, _ in fits)
    top = [item for f, item in fits if f == best]
    if len(top) > 1 and problems is not None:
        where = mode + (f" {entry}" if entry else "")
        problems.append(f"{what}: {len(top)} variants for {where}")
    return top[0]


def mode_view(body, mode, problems, entry=None):
    """The lesson as read in one mode and entry (None: a lesson that offers none): each block ID's
    variant for them (or its shared block), the <mode> and <entry> spans for them, the <disp> quotes
    for them in DISP's form. Problems with the variants and attributes as written are appended to
    problems (once, for the first mode and entry)."""
    report = problems is not None
    found = list(KEYS_ANY.finditer(body))
    # Group the blocks by ID, in order, and check the variants as written.
    groups, order = {}, []
    for i, m in enumerate(found):
        indent, bid, attrs, keys = m.group(1), m.group(2), m.group(3), m.group(4)
        a = dict(re.findall(r"([a-z]+)=(\S+)", attrs))
        for k in a:
            if k not in ("after", "mode", "entry", "twin", "fade") and report:
                problems.append(f"keys block {bid}: unknown attribute {k}=")
        ms = mode_list(a["mode"]) if "mode" in a else None
        es = mode_list(a["entry"]) if "entry" in a else None
        if report:
            for x in ms or []:
                if x not in MODES:
                    problems.append(f"keys block {bid}: mode={a['mode']} names {x}, not one of 33s 35s STU")
            for x in es or []:
                if x not in ENTRIES:
                    problems.append(f"keys block {bid}: entry={a['entry']} names {x}, not one of rpn alg")
        if bid not in groups:
            groups[bid] = []
            order.append(bid)
        elif report and found[i - 1].group(2) != bid:
            problems.append(f"keys block {bid}: its variants must follow it at once")
        groups[bid].append((m, ms, es, a.get("after"), indent, keys))
    if report:
        for bid, g in groups.items():
            shared = [x for x in g if x[1] is None and x[2] is None]
            if len(shared) > 1:
                problems.append(f"keys block {bid}: {len(shared)} shared blocks (no mode= or entry=)")
    # Rewrite: the chosen block in the plain form, every other block of the ID removed. Two variants
    # that fit this mode and entry equally narrowly are a problem here (the caller views each pair
    # the lesson offers).
    out, pos = [], 0
    for m in found:
        out.append(body[pos:m.start()])
        pos = m.end()
        bid = m.group(2)
        g = groups[bid]
        chosen = pick([(x[1], x[2], x) for x in g], mode, entry, f"keys block {bid}", problems)
        if chosen is None or chosen[0] is not m:
            continue
        after = chosen[3] or next((x[3] for x in g if x[1] is None and x[2] is None and x[3]), None)
        indent = chosen[4]
        head = f"{indent}```keys {bid}" + (f" after={after}" if after else "")
        keys_text = chosen[5]
        out.append(f"{head}\n{keys_text}{indent}```")
    out.append(body[pos:])
    view = "".join(out)
    # Spans: kept (their text) in their modes or entries, removed in the others. No span inside a
    # span of its own kind; a <mode> span may hold an <entry> span, and the reverse.

    def span_of(kind, attr, names, here):
        def span(m):
            ms = mode_list(m.group(1))
            if report:
                for x in ms:
                    if x not in names:
                        problems.append(f'<{kind} {attr}="{m.group(1)}">: {x} is not one of {" ".join(names)}')
                if f"<{kind}" in m.group(2):
                    problems.append(f"a <{kind}> span inside a <{kind}> span")
            return m.group(2) if here in ms else ""
        return span
    view = MODE_SPAN.sub(span_of("mode", "m", list(MODES), mode), view)
    view = ENTRY_SPAN.sub(span_of("entry", "e", ALL_ENTRIES, entry or "rpn"), view)
    if report and ("<mode" in view or "</mode>" in view):
        problems.append("a <mode> tag not in the form <mode m=\"...\">...</mode>")
    if report and ("<entry" in view or "</entry>" in view):
        problems.append("an <entry> tag not in the form <entry e=\"...\">...</entry>")

    # Quotes: those for this mode and entry, in DISP's form (v, then kind).
    def disp(m):
        a = dict(ATTR.findall(m.group(1)))
        for k in a:
            if k not in ("v", "kind", "m", "e") and report:
                problems.append(f"<disp> with unknown attribute {k}=")
        for attr, names, here in (("m", MODES, mode), ("e", ENTRIES, entry or "rpn")):
            if attr in a:
                ms = mode_list(a[attr])
                if report:
                    for x in ms:
                        if x not in names:
                            problems.append(f'<disp v="{a.get("v")}" {attr}="{a[attr]}">: {x} is not one of {" ".join(names)}')
                if here not in ms:
                    return ""
        kind = f' kind="{a["kind"]}"' if "kind" in a else ""
        return f'<disp v="{a.get("v", "")}"{kind}>{m.group(2)}</disp>'
    return DISP_ANY.sub(disp, view)


def split_scope(text):
    """ID@33s,alg -> (ID, modes or None, entries or None, unknown names)."""
    base, _, sc = text.partition("@")
    names = mode_list(sc)
    ms = [x for x in names if x in MODES] or None
    es = [x for x in names if x in ENTRIES] or None
    return base, ms, es, [x for x in names if x not in MODES and x not in ENTRIES]


def vectors_for_mode(vectors, mode, problems=None, entry=None):
    """The vectors that apply in a mode and entry, by their plain ID: a vector ID@m1,e1 applies in
    the modes and entries it names (either axis left out: any) and replaces a broader one there."""
    by_base = {}
    for vid, parts, line in vectors:
        base, ms, es, unknown = split_scope(vid)
        if problems is not None:
            for x in unknown:
                problems.append(f"vector {vid}: {x} is not one of 33s 35s STU rpn alg")
        by_base.setdefault(base, []).append((ms, es, (base, parts, line)))
    out = []
    for base, cands in by_base.items():
        v = pick(cands, mode, entry, f"vector {base}", problems)
        if v is not None:
            out.append(v)
    return out


def variant(parts, mode, dirty, entry=None):
    """A vector line in a mode and entry, from a fresh or a used core: its first token, MODE33, set to
    the mode's, and the entry's token after it when the lesson offers entries (as its setup presses
    them, the entry right after the mode)."""
    toks = parts[2].split()
    toks[0] = MODES[mode]
    if entry:
        toks.insert(1, ENTRIES[entry])
    if dirty:
        toks = DIRTY.split() + toks
    return " | ".join(parts[:2] + [" ".join(toks)] + parts[3:])


def view_blocks(view):
    """(id, own keys, full keys, start, end, after) for each block of a view, and the problems with
    its chain (a continuation must follow its PREV at once)."""
    found = [(m.group(1), " ".join(m.group(3).split()), m.start(), m.end(), m.group(2))
             for m in KEYS_BLOCK.finditer(view)]
    out, full, problems = [], {}, []
    for i, (bid, keys, s0, e0, after) in enumerate(found):
        if after:
            prev = found[i - 1][0] if i > 0 else None
            if after != prev or prev == "setup":
                problems.append(f"keys block {bid} continues {after}, but the block just before it is {prev}")
                full[bid] = keys
            else:
                full[bid] = f"{full[prev]} {keys}"
        else:
            full[bid] = keys
        out.append((bid, keys, full[bid], s0, e0, after))
    return out, problems


def student_sequence(lesson_dir, mode, entry=None):
    """The keys a student presses working through a lesson in a mode and entry, as keyrun --sequence
    reads them: "setup<TAB>keys", then "ID<TAB>keys" for every block of the view in order. The
    learning page's gate calls this (primer #4513), so the page and the checker press the same keys.
    With no entry given, a lesson that offers entries is worked in its default (the first listed)."""
    text = open(os.path.join(lesson_dir, "lesson.md"), encoding="utf-8").read()
    meta, body = front_matter(text)
    if entry is None and meta.get("entries", "").split():
        entry = meta["entries"].split()[0]
    setup = " ".join(meta.get("setup", "").split()).replace("{mode}", mode)
    if entry:
        setup = setup.replace("{entry}", ENTRIES[entry])
    blocks, _ = view_blocks(mode_view(body, mode, None, entry))
    lines = [f"setup\t{setup}"] + [f"{bid}\t{own}" for bid, own, _, _, _, _ in blocks if bid != "setup"]
    return "\n".join(lines) + "\n"


class Lesson:
    def __init__(self, d, core):
        self.d = d.rstrip("/")
        self.name = os.path.basename(self.d)
        self.core = core
        self.fail = []
        self.notes = []

    def bad(self, msg):
        if msg not in self.fail:
            self.fail.append(msg)

    def run(self, *cmd, env=None):
        e = dict(os.environ)
        e.update(env or {})
        return subprocess.run(cmd, capture_output=True, text=True, env=e, encoding="utf-8")

    def run_vectors(self, lines, env=None):
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as t:
            t.write("\n".join(lines) + "\n")
        try:
            return self.run(f"{self.core}/build/vectors", t.name, env=env)
        finally:
            os.unlink(t.name)

    def check(self):
        lesson_md = os.path.join(self.d, "lesson.md")
        vec_path = os.path.join(self.d, "vectors.txt")
        fmt_path = os.path.join(self.d, "fmt-vectors.txt")
        for p in (lesson_md, vec_path):
            if not os.path.exists(p):
                self.bad(f"missing {p}")
        if self.fail:
            return
        text = open(lesson_md, encoding="utf-8").read()
        meta, body = front_matter(text)
        # Maths: the spans as written; then every check below reads each one as its plain text (maths_read).
        for p in check_maths(body):
            self.bad(p)
        body = maths_read(body)
        # Voices: the spans and the same-skeleton proof first; then every check below reads the default voice,
        # which the proof shows has every other voice's examples, quotes and items.
        for p in check_voices(meta, body):
            self.bad(p)
        body_all = body
        voices = lesson_voices(meta)[0]
        if voices != [None]:
            body = voice_view(body, voices[0])
            self.notes.append(f"voices: {' '.join(voices)}, one skeleton")
        for p in check_worked(body, unit_problems(self.d, meta.get("id", ""))):
            self.bad(p)
        for p in check_why(body):
            self.bad(p)
        vectors = read_vectors(vec_path, 4)
        fmts = read_vectors(fmt_path, 6) if os.path.exists(fmt_path) else []

        # A check that checks nothing is not a pass.
        if not vectors:
            self.bad("vectors.txt has no vectors")
        ids = [v[0] for v in vectors]
        for dup in sorted({i for i in ids if ids.count(i) > 1}):
            self.bad(f"vector {dup} appears more than once")
        settings = set()
        for vid, parts, _ in vectors:
            exps = parts[3].split()
            if not exps:
                self.bad(f"{vid}: no expectation")
            if len(exps) > MAX_EXPECT:
                self.bad(f"{vid}: {len(exps)} expectations; the runner keeps {MAX_EXPECT}")
            toks = parts[2].split()
            # Every vector sets its mode and its display, so nothing depends on how the core began.
            if len(toks) < 2 or toks[0] != "MODE33" or not SETTING.match(toks[1]):
                self.bad(f"{vid}: keys must begin MODE33 and a display setting (FIXn, SCIn, ENGn, ALL)")
                continue
            settings.add(toks[1])
            if any(t in ("STU", "ALG", "RPN") or t.startswith("MODE") for t in toks[1:]):
                self.bad(f"{vid}: the mode is set only by the first key")
        modes, why = lesson_modes(meta)
        if why:
            self.bad(why)
        setup_t = " ".join(meta.get("setup", "").split())
        if not setup_t:
            self.bad("front matter has no `setup:` keys (the mode and the display setting, as pressed)")
        elif setup_t.split().count("{mode}") != 1:
            self.bad("the setup must press MODE's soft key as {mode}, once (the page and the checker fill it in)")
        entries, why = lesson_entries(meta, lesson_modes(meta)[0])
        if why:
            self.bad(why)
        st = setup_t.split()
        if entries == [None]:
            if "{entry}" in st:
                self.bad("the setup presses {entry}, but the front matter offers no `entries:`")
        elif st.count("{entry}") != 1 or "{mode}" not in st:
            self.bad("the setup must press MODE's soft key as {entry}, once, right after {mode}")
        else:
            # The vectors set the entry right after the mode (variant), so the setup presses it there:
            # the same shift and MODE key again, then {entry}.
            i = st.index("{mode}")
            if i < 2 or st[i + 1:i + 4] != st[i - 2:i] + ["{entry}"]:
                self.bad(f"the setup must press the entry right after the mode, "
                         f"'{' '.join(st[max(i - 2, 0):i])} {{mode}} {' '.join(st[max(i - 2, 0):i])} {{entry}}'")
        for m in FENCE.finditer(body):
            line = m.group(0).strip()           # a fence may be indented (in a list item)
            if "key" in m.group(2).lower() and not KEYS_FENCE.match(line):
                self.bad(f"a fence that looks like keys but is not checked: '{line}'")
        problems = []
        for mode in modes:
            for entry in entries:
                mode_view(body, mode, problems, entry)
                vectors_for_mode(vectors, mode, problems, entry)
        for p in dict.fromkeys(problems):
            self.bad(p)
        if self.fail:
            return

        # 2. The displays, once.
        if fmts:
            r = self.run(f"{self.core}/build/fmt_vectors", fmt_path)
            out = r.stdout.strip().splitlines()
            if r.returncode != 0 or not out:
                self.bad(f"display vectors:\n{r.stdout}{r.stderr}")
            else:
                self.notes.append("displays: " + out[-1].split(": ", 1)[-1])
        self.quoted = 0
        self.working_pending = set()
        for mode in modes:
            for entry in entries:
                self.check_mode(mode, entry, meta, body, vectors, fmts, settings, setup_t)
        self.notes.append(f"displays quoted: {self.quoted} (all modes)")
        if meta.get("id") in WORKING_PENDING:
            if self.working_pending:
                self.notes.append(f"{len(self.working_pending)} typed answers still without their working (WORKING_PENDING)")
            else:
                self.bad(f"{meta['id']} is in WORKING_PENDING, but every computed answer has its working: take it off")
        self.notes.append("worked through in order in each mode" + (" and entry" if entries != [None] else ""))

        # 5. Voice, the front matter included.
        dashes = sum(text.count(d) for d in EM_DASH)
        if dashes:
            self.bad(f"{dashes} em-dash(es) in lesson.md")
        # The page renders a lesson id in prose as its linked title (abacus #5459), so a possessive id
        # ("lim-02's ball") reads as "[Rates of change]'s ball" (primer #5463): name the thing, then the
        # lesson ("the ball from lim-02").
        for pid in sorted(set(re.findall(r"\b([a-z]+-\d{2}[a-z]?)['’]s\b", body_all))):     # straight or curly, in every voice
            self.bad(f"lesson id {pid} written as a possessive ({pid}'s): the page renders it as a title; "
                     f"write 'the … from {pid}'")

    def check_mode(self, md, entry, meta, body, all_vectors, fmts, settings, setup_t):
        # md is the mode; `mode` names the mode and entry in messages ("33s", or "STU alg").
        mode = md if entry is None else f"{md} {entry}"
        view = mode_view(body, md, None, entry)
        vectors = vectors_for_mode(all_vectors, md, None, entry)
        ids = [v[0] for v in vectors]
        setup = setup_t.replace("{mode}", md).replace("{entry}", ENTRIES[entry] if entry else "")
        # An ALG result is ANS, shown in X's place; the stack is untouched (firmware 029 rule 6), so
        # its vectors expect N= where an RPN vector expects X=.
        result = "N" if entry == "alg" else "X"

        # 1. The maths, from a fresh core and from a used one.
        for dirty in (False, True):
            r = self.run_vectors([variant(v[1], md, dirty, entry) for v in vectors])
            where = f"{mode} mode, {'a used' if dirty else 'a fresh'} core"
            if r.returncode != 0:
                self.bad(f"vectors in {where}:\n{r.stdout}{r.stderr}")
            elif not dirty:
                last = (r.stdout.strip().splitlines() or ["(no output)"])[-1]
                self.notes.append(f"{mode}: {last.split(': ', 1)[-1]}")

        # 3. The printed keys against the vectors.
        found, chain_problems = view_blocks(view)
        for p in chain_problems:
            self.bad(f"{p} (in {mode})")
        blocks = [(bid, full, s0, e0) for bid, _, full, s0, e0, _ in found]
        own_keys = {bid: own for bid, own, _, _, _, _ in found}
        continued = {after for (_, _, _, _, _, after) in found if after}
        byid = {v[0]: v for v in vectors}
        shown, screen, screen_y, status, graph = set(), {}, {}, {}, {}

        def line_says(xline, yline, qkind, text):
            # A prompt for a variable (INPUT's or an equation's "X?") takes the Y line (screen.h);
            # STO's "STO _" takes X. Every other kind is the X line.
            if qkind == "prompt":
                return any(k == "prompt" and t.strip() == text for k, t in (xline, yline))
            # TABLE's selected row is on the X line: the variable's value, then the equation's,
            # spaced to the line's width; the prose writes them with single spaces between.
            if qkind == "row":
                return xline[0] == "value" and " ".join(xline[1].split()) == text
            # The algebraic line as typed sits in Y's place above its result (firmware 029, proposal 3),
            # an equation line to keyrun.
            if qkind == "line":
                return yline[0] == "eqn" and yline[1].strip() == text
            return xline[0] == qkind and xline[1].strip() == text
        for bid, keys, _, _ in blocks:
            if bid == "setup":                  # the setup as printed for the student, {mode} and all
                if keys != setup_t:
                    self.bad(f"the setup block '{keys}' is not the front matter's setup '{setup_t}'")
                continue
            if bid not in byid:
                self.bad(f"keys block {bid} names no vector in {mode} mode")
                continue
            shown.add(bid)
            fd, trace = tempfile.mkstemp(suffix=".trace")
            os.close(fd)
            r = self.run_vectors([variant(byid[bid][1], md, False, entry)], env={"STU_TRACE": trace})
            if r.returncode != 0:
                os.unlink(trace)
                self.bad(f"{bid}: vector fails alone in {mode} mode:\n{r.stdout}")
                continue
            # A block the next one continues may stop at a prompt the continuation answers.
            cont = {"KEYRUN_OPEN_PROMPT": "1"} if bid in continued else {}
            k = self.run(f"{self.core}/build/keyrun", f"{setup} {keys}", trace, env=cont)
            os.unlink(trace)
            if k.returncode != 0:
                self.bad(f"{bid}: printed keys and vector disagree in {mode} mode: "
                         f"{k.stdout.strip()}{k.stderr.strip()}")
                continue
            xl = [l.split("\t") for l in k.stdout.splitlines() if l.startswith("X\t")]
            sl = [l.split("\t", 1)[1] for l in k.stdout.splitlines() if l.startswith("STATUS\t")]
            yl = [l.split("\t") for l in k.stdout.splitlines() if l.startswith("YL\t")]
            if xl and len(xl[0]) == 3:
                screen[bid] = (xl[0][1], xl[0][2])
                screen_y[bid] = (yl[0][1], yl[0][2]) if yl and len(yl[0]) == 3 else ("?", "")
                status[bid] = sl[0].split() if sl else []
                gl = [l.split("\t") for l in k.stdout.splitlines() if l.startswith("GRAPH\t")]
                graph[bid] = dict(zip(GRAPH_KINDS, gl[0][2:8])) if gl and len(gl[0]) == 8 else {}
        # 3b. Items (docs/lesson-format.md, Items): the answer and each slip are vectors of this view;
        # the working printed with an item presses to its answer's ops; each slip's value is not the
        # answer; and nothing shows the answer or a slip before the item asks it. The page reveals an
        # item's working after the attempt, so its vectors need no keys block.
        items = parse_items(view)
        quotes_at = [(q.group(1), q.start()) for q in DISP.finditer(view)]
        placement = meta.get("kind") == "placement"
        for iid, at, fields, slips, problems in items:
            for p in problems:
                self.bad(p)
            # A placement file's items each place a unit (graph.py checks the unit and its topics);
            # elsewhere an item places nothing.
            if placement and not re.fullmatch(r"\d+", fields.get("places", "")):
                self.bad(f"item {iid}: a placement item needs places: and a unit number")
            if not placement and "places" in fields:
                self.bad(f"item {iid}: places: is for placement files (front matter kind: placement)")
            if iid not in byid:
                self.bad(f"item {iid} names no vector in {mode} mode")
                continue
            want = answer_of(byid[iid][1], result)
            if want is None:
                self.bad(f"item {iid}: its vector has no {result}= or {result}# answer in {mode} mode")
                continue
            shown.add(iid)
            for sid, name, _ in slips:
                if sid not in byid:
                    self.bad(f"item {iid}: slip {sid} names no vector in {mode} mode")
                    continue
                shown.add(sid)
                got = answer_of(byid[sid][1], result)
                if got is None or got[0] != "exact":
                    self.bad(f"item {iid}: slip {sid} needs an exact {result}= value")
                    continue
                v = got[1]
                same = v == want[1] if want[0] == "exact" else abs(v - want[1]) <= want[2]
                if same:
                    self.bad(f"item {iid}: slip {sid} ({name}) gives the answer itself, {v} ({mode})")
            # A computed typed answer has its working on the core, vector <ID>W, whose answer is the typed
            # one: a wrong typed answer then fails here and not only in a reader's eye (abacus #6439).
            wid = iid + "W"
            working = []
            if fields.get("answer") == "type" and fields.get("working") != "none":
                if wid in byid:
                    working = [wid]
                    shown.add(wid)
                    got = answer_of(byid[wid][1], result)
                    if got is None:
                        same = False
                    elif want[0] == "exact":
                        same = got[0] == "exact" and got[1] == want[1]
                    else:
                        same = abs(got[1] - want[1]) <= want[2]
                    if not same:
                        self.bad(f"item {iid}: its working {wid} gives {got[1] if got else 'no answer'}, not the "
                                 f"typed answer {want[1]} ({mode})")
                elif meta.get("id") in WORKING_PENDING:
                    self.working_pending.add(iid)
                else:
                    self.bad(f"item {iid}: a computed answer needs its working, vector {wid}, made by the core "
                             f"(or working: none, for a count or a concept) ({mode})")
            elif fields.get("working") == "none" and wid in byid:
                self.bad(f"item {iid}: working: none, but vector {wid} is there as its working ({mode})")
            for name in [iid] + working + [s[0] for s in slips]:
                if any(b[0] == name and b[2] < at for b in blocks) or any(v == name and p < at for v, p in quotes_at):
                    self.bad(f"item {iid}: {name} is shown before the item asks it ({mode})")
            if fields.get("keys"):
                keys = " ".join(fields["keys"].split())
                fd, trace = tempfile.mkstemp(suffix=".trace")
                os.close(fd)
                r = self.run_vectors([variant(byid[iid][1], md, False, entry)], env={"STU_TRACE": trace})
                if r.returncode != 0:
                    os.unlink(trace)
                    self.bad(f"item {iid}: vector fails alone in {mode} mode:\n{r.stdout}")
                    continue
                k = self.run(f"{self.core}/build/keyrun", f"{setup} {keys}", trace)
                os.unlink(trace)
                if k.returncode != 0:
                    self.bad(f"item {iid}: its keys and vector disagree in {mode} mode: "
                             f"{k.stdout.strip()}{k.stderr.strip()}")
        for vid in ids:
            if vid not in shown:
                self.bad(f"vector {vid} is shown by no keys block in {mode} mode")
        self.notes.append(f"{mode} keys: {len(blocks)} blocks, {len(shown)} of {len(ids)} vectors shown"
                          + (f", {len(items)} items" if items else ""))

        # 4. Quoted displays: beside their example, on the device's screen, verified by the formatter.
        fmt_scoped = {}
        for fid, fparts, _ in fmts:
            base, ms, es, _ = split_scope(fid)
            fmt_scoped.setdefault(base, []).append((ms, es, fparts))

        def spelled(tok):                       # FIX4 -> "FIX 4", the display vectors' form
            m = SETTING.match(tok)
            return f"{m.group(1)} {m.group(2)}" if m.group(1) else "ALL"

        # Every vector starts at the setup's setting; a lesson may change it within an example
        # (rpn-03 does), and a quoted display is judged at the setting its own example ends in.
        if len(settings) > 1:
            self.bad(f"the vectors start at {len(settings)} display settings; the setup sets one")
        want = spelled(sorted(settings)[0]) if settings else ""
        if meta.get("display") and meta["display"] != want:
            self.bad(f"front matter `display: {meta['display']}`, but the vectors set {want}")

        def final_setting(toks):
            # FDISP toggles Fraction display on and off; choosing FIX, SCI, ENG or ALL turns it off
            # (unit 007). The maximum denominator and the format are left at their defaults, so a
            # vector that changes them cannot have its display judged here.
            setting, frac = None, False
            for t in toks:
                if SETTING.match(t):
                    setting, frac = spelled(t), False
                elif t == "FDISP":
                    frac = not frac
                elif t in FRAC_SETTINGS:
                    return None
            return "FRAC 4095 P" if frac else setting

        ends_at = {v[0]: final_setting(v[1][2].split()) for v in vectors}
        quotes = list(DISP.finditer(view))
        self.quoted += len(quotes)
        if view.count("<disp") != len(quotes):
            self.bad(f"{view.count('<disp')} <disp tags, {len(quotes)} of the checked form <disp v=\"ID\">text</disp>")
        for q in quotes:
            vid, qkind, shown_text = q.group(1), q.group(2) or "value", q.group(3)
            before = [b for b in blocks if b[3] <= q.start() and b[0] != "setup"]
            if not before or before[-1][0] != vid:
                self.bad(f'<disp v="{vid}"> is not under its own example '
                         f'(it follows {before[-1][0] if before else "no example"}) in {mode} mode')
            if qkind == "status":
                # An annunciator (the fraction indicator, RAD, ...): a token of the status band.
                if shown_text not in status.get(vid, []):
                    self.bad(f"{vid}: the status band shows {status.get(vid, [])}, without '{shown_text}' ({mode})")
                continue
            if qkind in GRAPH_KINDS:
                got = graph.get(vid, {}).get(qkind)
                if got != shown_text:
                    self.bad(f"{vid}: the graph's {qkind} shows '{got if got is not None else '(no graph)'}', "
                             f"the prose '{shown_text}' ({mode})")
                continue
            if qkind != "value":
                # A VIEW's "B=49.75" is no value the formatter's vectors cover: the device's own
                # screen line is the check, kind and text both.
                kind, stext = screen.get(vid, ("?", ""))
                if not line_says((kind, stext), screen_y.get(vid, ("?", "")), qkind, shown_text):
                    if qkind == "line":                 # the algebraic line is in Y's place: say what is there
                        kind, stext = screen_y.get(vid, ("?", ""))
                    where = "line above X" if qkind == "line" else "X line"
                    self.bad(f"{vid}: the device's {where} shows '{stext}' ({kind}), the prose '{shown_text}' ({qkind}) ({mode})")
                continue
            # A quote that differs by mode or entry (33s's real part against 35s's a i b) has its own
            # display vector, D-ID@mode (or @entry, or both), as a vector has ID@modes; the narrowest
            # that fits serves, else the one display vector D-ID.
            f = pick(fmt_scoped.get("D-" + vid, []), md, entry, f"display vector D-{vid}", None)
            if not f:
                self.bad(f'<disp v="{vid}"> has no display vector D-{vid}')
                continue
            # A fraction's text may end in its accuracy indicator (" v" below, " ^" above), which the
            # device draws in the status band, not on the X line: the prose quotes the X line, and
            # the status band must carry the matching arrow, or none when the fraction is exact.
            ftext, ind = f[5], ""
            if f[3].startswith("FRAC") and ftext.endswith((" v", " ^")):
                ftext, ind = ftext[:-2], ftext[-1]
            if ftext != shown_text:
                self.bad(f"D-{vid}: the prose shows '{shown_text}', the display vector '{f[5]}'")
            if f[3].startswith("FRAC"):
                arrows = [a for a in ("▼", "▲") if a in status.get(vid, [])]
                need = {"v": ["▼"], "^": ["▲"], "": []}[ind]
                if arrows != need:
                    self.bad(f"D-{vid}: the display vector's indicator is '{ind or 'none'}', the status band has {arrows or 'none'}")
            if f[3] != ends_at.get(vid, want):
                self.bad(f"D-{vid}: display vector at '{f[3]}', vector {vid} ends at '{ends_at.get(vid, want)}'")
            # The device formats X at 21 cells (firmware/screen.c FMT_WIDTH, "ours, v0"); the display
            # runner's default is 22, which agrees for short values only. The screen-line comparison
            # below is the backstop if FMT_WIDTH changes.
            if f[4] not in ("", DEVICE_WIDTH):
                self.bad(f"D-{vid}: display options '{f[4]}'; a quoted display uses the device's ('{DEVICE_WIDTH}' or none)")
            v = byid.get(vid)
            xs = re.findall(r"(?:^|\s)%s=(\S+)" % result, v[1][3]) if v else []
            if not xs or xs[-1] != f[2]:
                self.bad(f"D-{vid}: value {f[2]} is not vector {vid}'s exact {result} result ({xs[-1] if xs else 'none'})")
            kind, stext = screen.get(vid, ("?", ""))
            if kind != "value" or stext.strip() != shown_text:
                self.bad(f"D-{vid}: the device's X line shows '{stext}' ({kind}), the prose '{shown_text}' ({mode})")
        # A sentence that says what the screen shows, with a number in the display's own form
        # (FIX n places) outside a tag, is a display claim nothing checked. A number given as an
        # input ("a 7.25 item") is not a claim about the screen, so only such sentences count.
        m = SETTING.match(sorted(settings)[0]) if settings else None
        if m and m.group(1) == "FIX" and int(m.group(2)) > 0:
            prose = DISP.sub("", KEYS_BLOCK.sub("", view))
            fixed = re.compile(r"(?<![\d.])-?\d+\.\d{%d}(?!\d|\.\d)" % int(m.group(2)))
            for sentence in re.split(r"(?<=[.!?:])\s+", prose):
                if SHOWS.search(sentence):
                    for n in fixed.findall(sentence):
                        self.bad(f"'{n}' looks like a display at {want} but is not in a <disp> tag")

        # 6. A student working through: the setup once, then every block in lesson order on ONE
        # device, nothing reset between them. Each example above is judged from the setup; a student
        # carries whatever the last example left (a display setting, Fraction display, a number still
        # being typed), so every quoted display must also be what that student sees.
        with tempfile.NamedTemporaryFile("w", suffix=".seq", delete=False, encoding="utf-8") as t:
            t.write(student_sequence(self.d, md, entry))
        r = self.run(f"{self.core}/build/keyrun", "--sequence", t.name)
        os.unlink(t.name)
        seq_x, seq_y, seq_st, seq_val, seq_graph = {}, {}, {}, {}, {}
        for l in r.stdout.splitlines():
            p = l.split("\t")
            if p[0] == "X" and len(p) == 4:
                seq_x[p[1]] = (p[2], p[3])
            elif p[0] == "YL" and len(p) == 4:
                seq_y[p[1]] = (p[2], p[3])
            elif p[0] == "STATUS" and len(p) == 3:
                seq_st[p[1]] = p[2].split()
            elif p[0] == "VAL" and len(p) == 6:
                seq_val[p[1]] = dict(zip("XYZT", p[2:6]))
            elif p[0] == "GRAPH" and len(p) == 8:
                seq_graph[p[1]] = dict(zip(GRAPH_KINDS, p[2:8]))
        if r.returncode != 0:
            self.bad(f"a student working through in {mode} mode cannot press the keys in order: {r.stdout.strip()}")
        # Every example's exact X, Y, Z and T expectations, not only the quoted displays: the
        # prose says "X holds 23" and "Y holds 2" too.
        for bid, _, _, _ in blocks:
            if bid not in byid or bid not in seq_val:
                continue
            for level, want_v in re.findall(r"(?:^|\s)([XYZT])=(\S+)", byid[bid][1][3]):
                got = seq_val[bid].get(level, "")
                # A complex value is its two parts joined by "i" (the vectors' and keyrun's form);
                # each part must be equal, so a real never passes for a complex or the reverse.
                try:
                    gp, wp = got.split("i"), want_v.split("i")
                    same = len(gp) == len(wp) and all(Decimal(g) == Decimal(w) for g, w in zip(gp, wp))
                except InvalidOperation:
                    same = False
                if not same:
                    self.bad(f"{bid}: working through in order, {level} holds {got or '(not a real)'}, "
                             f"the vector says {want_v} ({mode})")
        for q in quotes:
            vid, qkind, shown_text = q.group(1), q.group(2) or "value", q.group(3)
            if qkind == "status":
                if shown_text not in seq_st.get(vid, []):
                    self.bad(f"{vid}: working through in order, the status band shows {seq_st.get(vid, [])}, "
                             f"without '{shown_text}' ({mode})")
                continue
            if qkind in GRAPH_KINDS:
                got = seq_graph.get(vid, {}).get(qkind)
                if got != shown_text:
                    self.bad(f"{vid}: working through in order, the graph's {qkind} shows "
                             f"'{got if got is not None else '(no graph)'}', the prose '{shown_text}' ({mode})")
                continue
            kind, stext = seq_x.get(vid, ("?", ""))
            if not line_says((kind, stext), seq_y.get(vid, ("?", "")), qkind, shown_text):
                if qkind == "line":
                    kind, stext = seq_y.get(vid, ("?", ""))
                where = "the line above X" if qkind == "line" else "X"
                self.bad(f"{vid}: working through in order, {where} shows '{stext}' ({kind}), the prose '{shown_text}' ({mode})")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--core", required=True)
    ap.add_argument("lessons", nargs="*")
    a = ap.parse_args()
    if not a.lessons:
        print("check: no lessons")
        return 1
    failed = 0
    for d in a.lessons:
        L = Lesson(d, a.core)
        try:
            L.check()
        except (ValueError, OSError) as e:
            L.bad(f"{type(e).__name__}: {e}")
        status = "FAIL" if L.fail else "ok"
        print(f"{status:4} {L.name}: " + "; ".join(L.notes))
        for f in L.fail:
            print("     " + f.replace("\n", "\n     "))
        failed += bool(L.fail)
    print(f"{len(a.lessons) - failed}/{len(a.lessons)} lessons pass")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
