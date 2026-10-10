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
ITEM_FIELDS = ("prompt", "topics", "answer", "calculator", "keys", "places", "working", "slip")
# A typed answer that is computed is made by the core too, as vector <ID>W beside the typed one (abacus #6439).
# The lessons and placement files whose typed items predate that rule; the sweep (decision 76) takes each off
# as its unit's batch gives every computed item its working. A listed file whose items all have it is refused,
# so the list cannot outlive its need.
WORKING_PENDING = {"der-03", "int-01", "lim-02", "num-04", "parallel-01",
                   "prob-01b", "sys-02", "trig-04", "place-algebra-to-calculus"}


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
KEYS_FENCE = re.compile(r"^```keys[ \t]+[^\s=]+(?:[ \t]+(?:after|mode|entry)=\S+)*[ \t]*$")
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
            if k not in ("after", "mode", "entry") and report:
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
        for pid in sorted(set(re.findall(r"\b([a-z]+-\d{2}[a-z]?)['’]s\b", body))):     # straight or curly
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
