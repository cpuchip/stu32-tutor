#!/usr/bin/env python3
"""maths_convert.py: puts the lessons' maths in $TeX$ spans, a course at a time (docs/proposals/maths-markup.md §6,
approved by abacus #7218). Two steps, each its own commit with its own oracle:

    tools/maths_convert.py rewrap  COURSE   move each hard wrap out of an expression (a span may not cross a
                                            line); oracle: every paragraph's text, whitespace collapsed, unchanged
    tools/maths_convert.py convert COURSE   write the spans; oracle: for every lesson, check.py's reading of the
                                            new text (maths_plain(maths_read(...))) is the old text byte for byte,
                                            and check_maths finds nothing
    tools/maths_convert.py report  COURSE   what was spanned and what was left plain, per lesson, by kind

Add --dry to rewrap or convert to check without writing. The rules (§6):
  - an expression or relation is one span, arithmetic too: operands joined by + − × ÷ = < > ≤ ≥ ≠ ± / ·, with
    products (2t², 4ac), powers, roots, primes, function notation and ∠ angles; a power, root, prime or function
    alone is a span;
  - a lone number stays plain (3, −4, 6%, 90°); a lone ∠B stays plain, like a point;
  - a sign, ° and % sit inside (% written \\%); a word unit stays outside;
  - a lone letter is a span when the same letter is in the lesson's expressions, except the registers X Y Z T,
    a memory letter after STO or RCL, a geometry lesson's capital (a point), and the words a, A and I, which a
    lesson using that letter as a variable gets listed for a decision by hand;
  - a key's name beside "key" or "press", and any run that is a keys block's legend, stays plain;
  - nothing in a heading, keys block, <disp> quote, tag, inline code, link, front matter, or an item field other
    than prompt and a slip's hint, or a why block's ask and because.
"""
import collections
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import check  # noqa: E402

SUPS = "⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺⁽⁾ⁿ"
SUP_BACK = dict(zip(SUPS, "0123456789-+()n"))
OPS = "+−×÷=<>≤≥≠±/·"
UNIT_WORDS = ("cm", "m", "km", "kg", "g", "mm", "ml", "l")
FENCE = re.compile(r"^([ \t]*)```(\w*)[^\n]*\n(.*?)^\1```[ \t]*$", re.M | re.S)
MASKS = (re.compile(r"<disp\b[^>]*>.*?</disp>", re.S), re.compile(r"</?(?:voice|mode|entry)\b[^>]*>"),
         re.compile(r"`[^`\n]*`"), re.compile(r"\[[^\]\n]*\]\([^)\n]*\)"), re.compile(r"<!--.*?-->", re.S))
HOLE = "\x00"
LIST_MARK = re.compile(r"[ \t]*(?:[-*] |\d+\. )")


def course_lessons(course):
    """The lesson.md paths of a course in order, or of one unit with COURSE:UNIT (algebra:0)."""
    course, _, unit = course.partition(":")
    out, here = [], None
    for line in open(os.path.join(ROOT, "courses", f"{course}.course"), encoding="utf-8"):
        p = [x.strip() for x in line.split("|")]
        if p[0] == "unit":
            here = p[1]
        if p[0] == "lesson" and (not unit or here == unit):
            d = next(x for x in os.listdir(os.path.join(ROOT, "lessons")) if x == p[1] or x.startswith(p[1] + "-"))
            out.append(os.path.join(ROOT, "lessons", d, "lesson.md"))
    return out


def legends():
    """Every keys block's tokens that hold a letter or a maths sign (R/S, 1/x, √x, x², x↔y): a key's name."""
    out = set()
    for d in os.listdir(os.path.join(ROOT, "lessons")):
        p = os.path.join(ROOT, "lessons", d, "lesson.md")
        if os.path.isfile(p):
            for m in check.KEYS_ANY.finditer(open(p, encoding="utf-8").read()):
                out |= {t for t in m.group(4).split() if re.search(r"[A-Za-z√²ˣ↔/]", t) and not re.fullmatch(r"[\d.]+", t)}
    return out


def zones(text):
    """(start, end) of every stretch of the lesson a span may go in, as offsets into text: prose lines outside
    fences, headings and front matter, and the value of an item's prompt:, a slip's hint, and a why's ask: and
    because:. Masked stretches (quotes, tags, code, links) are cut out later by mask()."""
    fm = re.match(r"\A---\n.*?\n---\n", text, re.S)
    start = fm.end() if fm else 0
    fences = [(m.start(), m.end(), m.group(2), m) for m in FENCE.finditer(text, start)]
    out, at = [], start
    for a, b, kind, m in fences + [(len(text), len(text), None, None)]:
        pos, prev = at, ""
        for line in text[at:a].splitlines(keepends=True):
            body = line.rstrip("\n")
            if body.strip() and not body.lstrip().startswith("#"):
                lead = re.match(r"[ \t]*(?:[-*] )?", body).end()          # a list mark is not maths
                if not prev.strip() or LIST_MARK.match(prev):              # "5400. " mid-paragraph is not a list
                    lead = max(lead, re.match(r"[ \t]*(?:\d+\. )?", body).end())
                out.append((pos + lead, pos + len(body)))
            pos += len(line)
            prev = body
        if kind in ("item", "why"):
            pos = m.start(3)
            for line in m.group(3).splitlines(keepends=True):
                k, sep, v = line.partition(":")
                key = k.strip()
                if sep and key in ("prompt", "ask", "because"):
                    vs = pos + len(k) + 1 + (len(v) - len(v.lstrip()))
                    out.append((vs, pos + len(line.rstrip("\n"))))
                elif sep and key == "slip":
                    bars = [i for i, ch in enumerate(line) if ch == "|"]
                    if len(bars) >= 2:
                        hs = bars[1] + 1
                        hs += len(line[hs:]) - len(line[hs:].lstrip())
                        out.append((pos + hs, pos + len(line.rstrip("\n"))))
                pos += len(line)
        at = b
    return out


def mask(text):
    """text with every masked stretch replaced by holes of the same length (offsets kept)."""
    for rx in MASKS:
        text = rx.sub(lambda m: HOLE * len(m.group(0)), text)
    return text


# ---- the expression scanner: s is a masked stretch; every function returns an end index or None ----

def _num(s, i):
    m = re.compile(r"\d+(?:[.,]\d+)*").match(s, i)
    if not m:
        return None
    j = m.end()
    if s[j:j + 1] == "," and re.match(r",\d", s[j:j + 2]):
        return None
    return j


def _paren(s, i, commas=False):
    """The end of a ( ... ) group starting at i whose content is maths, or None. Commas between expressions only
    for a call's arguments (LCM(4, 8), P(10, 3)): a bare group with commas is a list, each item its own span."""
    if s[i:i + 1] != "(":
        return None
    j = i + 1
    while True:
        while s[j:j + 1] == " ":
            j += 1
        k = expression(s, j, inner=True)
        if k is None:
            return None
        j = k
        while s[j:j + 1] == " ":
            j += 1
        if s[j:j + 1] == "," and commas:
            j += 1
            continue
        if s[j:j + 1] == ")":
            return j + 1
        return None


def _post(s, j):
    """Superscripts, primes, a caret power, ° and % after an operand."""
    while j < len(s):
        if s[j] in SUPS:
            j += 1
        elif s[j] == "^":
            k = _paren(s, j + 1) or _num(s, j + 1)
            if k is None:
                m = re.compile(r"[a-z](?![A-Za-z])").match(s, j + 1)
                k = m.end() if m else None
            if k is None:
                return j
            j = k
        elif s[j] in "°%":
            j += 1
        elif s[j] == "!" and s[j + 1:j + 2] != "=" and (s[j - 1].isdigit() or s[j - 1] == ")"):
            # a factorial: 5!, (n + 1)!; only after a digit or a bracket, so "Found!" never spans (abacus #7263)
            j += 1
        else:
            return j
    return j


def operand(s, i, inner=False):
    """The end of one operand at i: a number (with a letter product: 2t, 4ac), a single letter, a call f(x) or
    f′(a), a root, a ( ) group, or ∠ and a point's letters; with a sign before and powers after; or None."""
    j = i
    if s[j:j + 1] == "−" or (s[j:j + 1] == "-" and re.match(r"-[\d(]", s[j:j + 2]) and (j == 0 or s[j - 1] in " (")):
        j += 1
    if s[j:j + 1] == "√":
        k = operand(s, j + 1, inner)
        if k is None:
            return None
        return k
    if s[j:j + 1] == "∠":
        m = re.compile(r"∠[A-Za-z]{1,3}(?![A-Za-z])").match(s, j)
        return _post(s, m.end()) if m else None
    if s[j:j + 1] == "|" and s[j + 1:j + 2] not in (" ", "|", "-", "") and not s.lstrip(" \t").startswith("|"):
        k = expression(s, j + 1, inner=True)         # an absolute value, |x| or |x − 3|: no space inside the bars,
        if k is not None and s[k:k + 1] == "|" and s[k - 1] != " ":   # and never on a table row
            return _post(s, k + 1)
        return None
    m = re.compile(rf"(?<![A-Za-z])(?:{'|'.join(check.MATHS_FUNCTIONS)})[{SUPS}]*(?![A-Za-z])").match(s, j)
    if m:                                             # sin 30°, cos A, ln 2, sin⁻¹ 0.5: a function and its argument
        k = m.end() + (s[m.end():m.end() + 1] == " ")
        e = operand(s, k, inner)
        return e if e is not None else None           # a name alone ("the sine, sin,") stays plain
    m = re.compile(rf"(?<![A-Za-z])(?:{'|'.join(check.MATHS_OPERATORS)})(?![A-Za-z])").match(s, j)
    if m:                                             # LCM(4, 8), GCF: an upright name (abacus #7227)
        return _post(s, _paren(s, m.end(), commas=True) or m.end())
    k = _paren(s, j)
    if k is None:
        k = _num(s, j)
        if k is not None:
            mixed = re.compile(r" \d+/\d+(?![\w/]|\.\d)").match(s, k)
            if mixed:                                 # a mixed number, 1 1/8, is one operand
                return _post(s, mixed.end())
            m = re.compile(r"(?:[a-z](?![a-z]*['’]))+(?![A-Za-z])").match(s, k)
            if m and not re.fullmatch(r"st|nd|rd|th|s|am|pm", m.group(0)):
                k = m.end()
        else:
            m = re.compile(r"(?<![A-Za-z'’])[A-Za-zπθ][′″]{0,2}(?![A-Za-z'’])").match(s, j)
            if not m:
                return None
            k = m.end()
            if s[k:k + 1] == "(":
                c = _paren(s, k, commas=True)          # a call: f(x), P(10, 3)
                if c is not None:
                    k = c
    k = _post(s, k)
    while s[k:k + 1] == "(":                          # a product by a group: 2(x + 1), a(a + h), (x − 1)(x + 1)
        c = _paren(s, k)
        if c is None:
            break
        k = _post(s, c)
    return k


WORDS2 = {"is", "an", "of", "to", "in", "it", "be", "by", "or", "on", "at", "as", "if", "up", "so", "do", "no", "we",
          "me", "he", "us", "am", "go", "my", "the", "and", "for", "but", "not", "are", "was", "has", "its", "one",
          "two", "six", "ten", "all", "any", "can", "you", "let", "put", "set", "get", "new", "now", "how", "why",
          "who", "own", "per", "via", "yet", "off", "out", "too", "use", "see", "say", "way", "end", "top", "row",
          "key", "box", "pie", "bun", "day", "car", "map", "cm", "km", "kg", "mm", "ml", "add", "sum", "few", "low",
          "big", "old", "far", "ago", "act", "lot", "had", "did", "may", "our", "his", "her", "him", "she", "each"}


def _product(s, j):
    """The end of a product of letters at j, mx or abc (two or three small letters, not a word), or None."""
    m = re.compile(rf"(?<![A-Za-z'’])([a-z]{{2,3}})[{SUPS}]*(?![A-Za-z'’(])").match(s, j)
    return m.end() if m and m.group(1) not in WORDS2 else None


def expression(s, i, inner=False):
    """The end of an expression at i: an operand, then (operator operand)*. A space either side of an operator is
    allowed; an ASCII - is an operator only with a space on both sides. A product of letters (y = mx + b) is an
    operand only where an operator touches it, so a word is never read as one."""
    j = operand(s, i, inner)
    if j is None:
        k = _product(s, i)
        if k is None or not re.match(rf" ?[{re.escape(OPS)}]", s[k:]):
            return None
        j = _post(s, k)
    while True:
        k = j
        while s[k:k + 1] == " ":
            k += 1
        if k < len(s) and s[k] in OPS:
            op = k
            k += 1
        elif s[k:k + 2] == "- " and k > j:
            op = k
            k += 1
        else:
            return j
        # a − or + spaced on one side only is the next number's sign ("a −4"), not an operator
        if s[op] in "−+-" and (op > j) != (s[k:k + 1] == " "):
            return j
        while s[k:k + 1] == " ":
            k += 1
        e = operand(s, k, inner)
        if e is None and _product(s, k) is not None:
            e = _post(s, _product(s, k))              # after an operator: y = mx + b
        if e is None:
            return j
        j = e


def runs(s):
    """Every maximal expression in a masked stretch, as (start, end)."""
    out, i = [], 0
    while i < len(s):
        ch = s[i]
        if (ch.isalnum() or ch in "−-√∠(|") and (i == 0 or not (s[i - 1].isalnum() or s[i - 1] in "_'’.")):
            e = expression(s, i)
            if e is not None and e > i:
                while e > i and s[e - 1] in " ":
                    e -= 1
                out.append((i, e))
                i = e
                continue
        i += 1
    return out


def kind_of(t):
    """'expr' for a run that is maths on its own, else what kind of lone thing it is. A run that is one ( ) group is
    the kind of what it holds: "(28)" is a lone number."""
    if re.fullmatch(r"\((?:[^()]|\([^()]*\))*\)", t):
        return kind_of(t[1:-1].strip())
    if re.match(rf"[−-]?(?:{'|'.join(check.MATHS_FUNCTIONS)})(?![A-Za-z])", t):
        return "expr"                                  # sin 30°, log 1.04: a function applied
    if re.fullmatch(r"[−-](?:\d+(?:\.\d+)?)?[A-Za-zθπ]", t) and not t.endswith("i"):
        return "expr"                                  # a signed letter or term, −b, −4z, −θ (not −4i, a number)
    if re.search(rf"[{re.escape(OPS)}]|\^", t.lstrip("−-")) or re.search(rf"[{SUPS}√′″|!]", t) or re.search(r"[A-Za-z]\(", t):
        return "expr"
    if re.fullmatch(r"[−-]?\d+(?:[.,]\d+)*[%°]?", t):
        return "number"
    if t.startswith("∠"):
        return "angle"
    if re.fullmatch(r"\d+(?:[.,]\d+)*[a-z]+", t):
        return "expr"                                  # a product: 3x, 4ac
    if re.fullmatch(r"[A-Za-zπθ]", t):
        return "letter"
    return "other"


def to_tex(u):
    """A run's Unicode as TeX that check.maths_text reads back to it (the round trip is the proof)."""
    t = re.sub(r"√\(([^()]*(?:\([^()]*\)[^()]*)*)\)", lambda m: r"\sqrt{" + m.group(1) + "}", u)
    t = re.sub(r"√([\w.]+)", lambda m: r"\sqrt{" + m.group(1) + "}", t)
    # every operand over an operand is stacked, a bracket group included (abacus #7227): 1/4, x/2, (1 + 3)/(4 + 8)
    o = rf"(?:\d+(?:\.\d+)?|(?<![A-Za-z])[A-Za-z](?![A-Za-z])|\([^()]*\))[{SUPS}]*"     # 1/2³ too
    t = re.sub(rf"(?<![\w.)])({o})/({o})(?![\w.(])",
               lambda m: r"\frac{" + re.sub(r"^\((.*)\)$", r"\1", m.group(1)) + "}{" + re.sub(r"^\((.*)\)$", r"\1", m.group(2)) + "}", t)
    t = re.sub(rf"(?<![A-Za-z\\])({'|'.join(check.MATHS_OPERATORS)})(?![A-Za-z])", r"\\operatorname{\1}", t)
    t = re.sub(rf"(?<![A-Za-z\\])({'|'.join(check.MATHS_FUNCTIONS)})(?![A-Za-z])", r"\\\1", t)
    t = re.sub(r"(?<=\d),(?=\d{3}(?!\d))", "{,}", t)  # 10,000: TeX would space a bare comma
    t = re.sub(f"[{SUPS}]+", lambda m: "^{" + "".join(SUP_BACK[c] for c in m.group(0)) + "}", t)
    t = re.sub(r"\^\(([^()]*)\)", lambda m: "^{" + m.group(1) + "}", t)
    t = re.sub(r"\^([\d.]+)", lambda m: "^{" + m.group(1) + "}", t)
    t = t.replace("″", "''").replace("′", "'").replace("%", r"\%")
    return re.sub(r"∠", r"\\angle ", t)


HAND_FILE = os.path.join(HERE, "maths_hand.txt")


def hand_decisions(lesson):
    """The recorded hand decisions for a lesson (tools/maths_hand.txt: lesson TAB span|plain TAB context), as
    {context: decision}. The context is the report's own, so a decision applies to exactly the place it names."""
    out = {}
    if os.path.exists(HAND_FILE):
        for line in open(HAND_FILE, encoding="utf-8"):
            if line.strip() and not line.startswith("#"):
                l, decision, ctx = line.rstrip("\n").split("\t", 2)
                if l == lesson:
                    assert decision in ("span", "plain"), line
                    out[ctx] = decision
    return out


def plan(text, geometry, keys, hand=None):
    """(the spans to write as (start, end, tex), a Counter of what was left plain, the undecided places as (line
    number, context)). `hand` is the lesson's recorded decisions; a place it does not name stays plain and is listed."""
    hand = hand or {}
    masked = mask(text)
    found = []
    for a, b in zones(text):
        for s, e in runs(masked[a:b]):
            found.append((a + s, a + e, text[a + s:a + e]))
    left, unsettled, spans, deferred = collections.Counter(), [], [], []

    def ask(s, e, t, ctx):
        """A place the rules leave to a person: the recorded decision, or listed as undecided (and plain)."""
        d = hand.get(ctx)
        if d == "span":
            left["span by hand"] += 1
            spans.append((s, e, t))
        elif d == "plain":
            left["plain by hand"] += 1
        else:
            left["UNDECIDED"] += 1
            unsettled.append((text.count("\n", 0, s) + 1, ctx))

    def key_name(s, e, t):
        """A key's name: a legend, the whole word around the run a legend (x↔y), or beside "key" or "press"."""
        a = s
        while a > 0 and not text[a - 1].isspace():
            a -= 1
        b = e
        while b < len(text) and not text[b].isspace():
            b += 1
        word = text[a:b].strip(".,;:!?()")
        # a one-character legend (the memory letters A-Z, b, i, m, r) is a key's name only beside "key" or "press"
        return ((len(t) > 1 and t in keys) or (len(word) > 1 and word in keys) or re.match(r"\s*keys?\b", text[e:e + 12])
                or re.search(r"\bpress(?:es|ed|ing)?\s+(?:the\s+)?$", text[max(0, s - 24):s]))
    found = [(s, e, t, bool(key_name(s, e, t))) for s, e, t in found]
    letters = set()
    for s, e, t, key in found:
        if kind_of(t) == "expr" and not key:
            letters |= set(re.findall(r"(?<![\\A-Za-z])[A-Za-z](?![A-Za-z(])", re.sub(r"[A-Za-z][′″]?\(", "(", t)))
            # a letter used as a function counts too, so "the domain of $r$" matches its $r(x)$ (abacus #7268); not
            # a, A or I, where "a(a + h)" is a product and a lone a is the article rule's
            letters |= set(re.findall(r"(?<![\\A-Za-z])([A-Za-z])[′″]?\(", t)) - {"a", "A", "I"}
    # a product of the lesson's letters standing alone ("Take mx from both sides") is not a run, so it is listed
    for za, zb in zones(text):
        for m in re.finditer(r"(?<![A-Za-z'’$\\])[a-z]{2}(?![A-Za-z'’(])", masked[za:zb]):   # two letters: "add" is a word
            s, e, t = za + m.start(), za + m.end(), m.group(0)
            if t not in WORDS2 and set(t) <= letters and not any(a <= s < b for a, b, _, _ in found):
                ask(s, e, t, f"product: …{text[max(0, s - 20):s]}[{t}]{text[e:e + 12]}…".replace("\n", " "))
    for s, e, t, key in found:
        k = kind_of(t)
        before, after = text[max(0, s - 24):s], text[e:e + 12]
        if key:
            left["key name"] += 1
            continue
        if k == "expr":
            if re.search(r"(?<![A-Za-z])[XYZT](?![A-Za-z(])", t) and not re.search(r"[a-z]", t):
                ask(s, e, t, f"register: {t}")          # X Y Z T in an expression: registers, or a formula's T
                continue
            if re.match(rf" ?[{re.escape(OPS)}] ?(?:the |that |its )?[A-Za-z]{{2,}}", masked[e:e + 12]) and not key:
                # an expression an operator joins to a word, "sin A = opposite ÷ hypotenuse": spanning it would
                # leave the rest of the formula plain, so it is a decision by hand
                ask(s, e, t, f"word formula: {t}{after}".replace("\n", " "))
                continue
            if re.match(rf"\s?(?:{'|'.join(UNIT_WORDS)})\b", after) or re.match(r"\s?[a-z]{3,}", after):
                left["word after, kept outside"] += 1
            if re.fullmatch(r"\((?:[^()]|\([^()]*\))*\)", t):   # an aside's brackets are prose: "(2 2/3)"
                s, e, t = s + 1, e - 1, t[1:-1]
            spans.append((s, e, t))
        elif k == "letter":
            if t in "XYZT":
                left["register"] += 1
            elif re.search(r"\b(?:STO|RCL)\s*$", before):
                left["memory letter"] += 1
            elif geometry and t.isupper():
                left["point"] += 1
            elif t in ("a", "A", "I"):
                deferred.append((s, e, t, before, after))   # decided once the other spans are known
            elif t not in letters and not (geometry and t.islower()):
                left["letter not in the lesson's maths"] += 1  # (in geometry a small letter is an angle: p, v, w)
            elif t.isupper() and t in keys:
                # a capital the lesson's maths uses that is also a memory letter: a variable ("3.5 in W") or the
                # calculator's letter ("W is on the 5 key"); never decided silently
                ask(s, e, t, f"{t}: …{before[-20:]}[{t}]{after}…".replace("\n", " "))
            else:
                spans.append((s, e, t))
        else:
            left[{"number": "lone number", "angle": "lone ∠ name"}.get(k, "lone name (LCM, GCF)")] += 1
    # A lone a, A or I in a sentence that also holds a one-letter span, or a span using that letter as a variable,
    # is always listed for a decision by hand, never decided (abacus #7248: angle-02's "a with c"). Elsewhere it is
    # the word, or listed when the lesson uses it as a variable and no noun follows.
    lspans = [x for x in spans if re.fullmatch(r"[A-Za-z]", x[2]) or re.search(r"(?<![\\A-Za-z])[aAI](?![A-Za-z])", x[2])]
    # a deferred letter decided a span by hand counts too ("here $A$" lists the "a formula" in its sentence)
    lspans += [(s, e, t) for s, e, t, before, after in deferred
               if hand.get(f"{t}: …{before[-20:]}[{t}]{after}…".replace("\n", " ")) == "span"]
    for s, e, t, before, after in deferred:
        a, b = sentence(text, s)
        if any(a <= x[0] < b for x in lspans) or (t in letters and not re.match(
                r"\s+(?!(?:times|plus|minus|is|squared|cubed|and|or)\b)[a-z]{2,}", after)):
            ask(s, e, t, f"{t}: …{before[-20:]}[{t}]{after}…".replace("\n", " "))
        elif t not in letters:
            left["letter not in the lesson's maths"] += 1
        else:
            left["the word a, A or I"] += 1             # an article before its noun: "a number", "a customer"
    return [(s, e, to_tex(t)) for s, e, t in spans], left, unsettled


def sentence(text, i):
    """(start, end) of the sentence around offset i: from after the last . ! ? (then a space) or blank line before
    it to the next one after it."""
    a = max([m.end() for m in re.finditer(r"[.!?](?=\s)|\n[ \t]*\n", text[:i])] or [0])
    m = re.compile(r"[.!?](?=\s|$)|\n[ \t]*\n").search(text, i)
    return a, m.end() if m else len(text)


def letter_spans(text):
    """The spans of a text whose TeX is one letter ($c$), or which use the letter a, A or I as a variable ($a = 5$),
    as (start, end, tex)."""
    return [(a, b, t) for a, b, t in check.maths_spans(text)
            if re.fullmatch(r"[A-Za-z]", t) or re.search(r"(?<![\\A-Za-z])[aAI](?![A-Za-z])", t)]


def ambiguous_articles(text, extra=()):
    """Each lone a, A or I (outside spans, in a place maths may go) in a sentence that also holds a one-letter span or a
    span using a, A or I as a variable (abacus #7248): never decided silently, always listed. `extra` adds spans
    planned but not yet written, as (start, end, tex). As (offset, the letter)."""
    spans = check.maths_spans(text)
    lspans = letter_spans(text) + [x for x in extra if re.fullmatch(r"[A-Za-z]", x[2])
                                   or re.search(r"(?<![\\A-Za-z])[aAI](?![A-Za-z])", x[2])]
    masked = mask(text)
    out = []
    for za, zb in zones(text):
        for m in re.finditer(r"(?<![\w'’$\\])[aAI](?![\w'’$])", masked[za:zb]):
            i = za + m.start()
            if any(a <= i < b for a, b, _ in spans):
                continue
            s, e = sentence(text, i)
            if any(s <= a < e for a, b, _ in lspans):
                out.append((i, m.group(0)))
    return out


def apply(text, spans):
    for s, e, tex in sorted(spans, reverse=True):
        text = text[:s] + "$" + tex + "$" + text[e:]
    return text


def wrapped(text):
    """Expressions a hard wrap splits: in each paragraph of prose, the lines joined (each newline and the next line's
    indent read as one space at the same offsets), an expression holding a newline. As (start, end) in text."""
    out = []
    masked = mask(text)
    zs = zones(text)
    i = 0
    while i < len(zs):
        a, b = zs[i]
        j = i
        while j + 1 < len(zs) and not text[zs[j][1]:zs[j + 1][0]].strip() and text[zs[j][1]:zs[j + 1][0]].count("\n") == 1:
            j += 1                                     # a list item's mark sits between zones, so items never join
        if j > i:
            a, b = zs[i][0], zs[j][1]
            joined = re.sub(r"\n[ \t]*", lambda m: " " * len(m.group(0)), masked[a:b])
            for s, e in runs(joined):
                if "\n" in text[a + s:a + e] and kind_of(re.sub(r"\s+", " ", text[a + s:a + e])) == "expr":
                    out.append((a + s, a + e))
        i = j + 1
    return out


def rewrap(text):
    """Move each wrap out of an expression: the line breaks just before the expression instead (or, at a line's
    start, the lines join), the next line's indent kept."""
    for s, e in sorted(wrapped(text), reverse=True):
        piece = text[s:e]
        indent = re.search(r"\n([ \t]*)", piece).group(1)
        flat = re.sub(r"[ \t]*\n[ \t]*", " ", piece)
        line_start = text.rfind("\n", 0, s) + 1
        if text[line_start:s].strip():
            pre = text[:s].rstrip(" ")
            text = pre + "\n" + indent + flat + text[e:]
        else:
            text = text[:s] + flat + text[e:]
    return text


def collapse(text):
    return [re.sub(r"\s+", " ", p).strip() for p in re.split(r"\n[ \t]*\n", text)]


def main():
    if len(sys.argv) >= 2 and sys.argv[1] == "selftest":
        # The scanner's rules on lines whose right runs are known (abacus #7263's controls among them): each case
        # is the line and the runs the scanner must find, so a rule that slips shows as a FAIL.
        cases = [("written |x|, is its distance: |5| and |−5| are both 5.", ["|x|", "|5|", "|−5|", "5"]),
                 ("So |x − 3| = 5 says", ["|x − 3| = 5"]),
                 ("| x | 0 | 1 | 2 |", ["x", "0", "1", "2"]),             # a table row is never read as bars
                 ("| q(x) | 3 | −1 |", ["q(x)", "3", "−1"]),
                 ("that is 5! = 120, and 0! is 1.", ["5! = 120", "0!", "1"]),
                 ("Found! It works!", []),                                # a prose exclamation never spans
                 ("n! is gold, above ×", ["n"]),                          # a letter's ! is the key's legend: no factorial
                 ("so 2⁻³ is 1/2³, which is 1/8.", ["2⁻³", "1/2³", "1/8"]),
                 ("LCM(5, 2) = 10 and (90 = 2 × 45, 45 = 3 × 15)", ["LCM(5, 2) = 10", "90 = 2 × 45", "45 = 3 × 15"]),
                 ("which is 1 1/8. Then a −4 is", ["1 1/8", "a", "−4"])]  # a sign spaced one side is not a minus
        bad = 0
        for line, want in cases:
            got = [line[a:b] for a, b in runs(line)]
            ok = got == want and all(check.maths_text(to_tex(g)) == g for g in got)
            bad += not ok
            print(f"{'ok  ' if ok else 'FAIL'} {line!r}: {got}" + ("" if ok else f" (want {want})"))
        print(f"{len(cases) - bad}/{len(cases)} scanner cases")
        return 1 if bad else 0
    if len(sys.argv) >= 3 and sys.argv[1] == "scan":
        # On converted lessons: every lone a, A or I in a sentence with a one-letter span (abacus #7248).
        n = 0
        for p in course_lessons(sys.argv[2]):
            t = open(p, encoding="utf-8").read()
            for i, w in ambiguous_articles(t):
                n += 1
                s, e = sentence(t, i)
                print(f"{os.path.basename(os.path.dirname(p))}:{t.count(chr(10), 0, i) + 1}: [{w}] in "
                      f"'{re.sub(r'\s+', ' ', t[s:e]).strip()[:160]}'")
        print(f"{sys.argv[2]}: {n} lone a/A/I in a sentence with a one-letter span")
        return 0
    if len(sys.argv) < 3 or sys.argv[1] not in ("rewrap", "convert", "report"):
        print(__doc__)
        return 2
    step, course, dry = sys.argv[1], sys.argv[2], "--dry" in sys.argv
    geometry = course.partition(":")[0] == "geometry"
    keys = legends()
    bad = 0
    total = collections.Counter()
    for p in course_lessons(course):
        name = os.path.basename(os.path.dirname(p))
        old = open(p, encoding="utf-8").read()
        meta, body = check.front_matter(old)
        head = old[:len(old) - len(body)]
        if step == "rewrap":
            new = head + rewrap(body)
            ok = collapse(new) == collapse(old) and "$" not in new
            n = len(wrapped(body))
            print(f"{'ok  ' if ok else 'FAIL'} {name}: {n} expression(s) rewrapped; paragraphs (whitespace collapsed) "
                  f"{'unchanged' if ok else 'CHANGED'}; {len(wrapped(rewrap(body)))} left wrapped")
        else:
            if wrapped(body):
                print(f"FAIL {name}: {len(wrapped(body))} expression(s) still wrapped; rewrap first")
                bad += 1
                continue
            spans, left, unsettled = plan(body, geometry, keys, hand_decisions(name))
            nb = apply(body, spans)
            new = head + nb
            back = check.maths_plain(check.maths_read(nb))
            probs = check.check_maths(nb)
            ok = back == body and not probs
            total["spans"] += len(spans)
            total.update(left)
            plain = ", ".join(f"{v} {k}" for k, v in sorted(left.items(), key=lambda x: -x[1]))
            print(f"{'ok  ' if ok else 'FAIL'} {name}: {len(spans)} spans; left plain: {plain or 'nothing'}; round trip "
                  f"{'byte for byte' if back == body else 'DIFFERS'}; check_maths {'clean' if not probs else probs[:3]}")
            if back != body:
                i = next(k for k, (x, y) in enumerate(zip(back, body)) if x != y) if back[:len(body)] != body[:len(back)] else min(len(back), len(body))
                print(f"     first difference at {i}: read {back[max(0, i - 30):i + 30]!r}\n     was  {body[max(0, i - 30):i + 30]!r}")
            for ln, ctx in unsettled:
                print(f"     line {ln + old[:len(head)].count(chr(10))}: {ctx}")
            if step == "report":
                for s, e, tex in spans:
                    print(f"     ${tex}$")
        if not ok:
            bad += 1
        elif not dry and step != "report" and new != old:
            open(p, "w", encoding="utf-8", newline="").write(new)
    if step != "rewrap":
        print("total: " + ", ".join(f"{v} {k}" for k, v in total.most_common()))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
