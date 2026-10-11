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
    out = []
    for line in open(os.path.join(ROOT, "courses", f"{course}.course"), encoding="utf-8"):
        p = [x.strip() for x in line.split("|")]
        if p[0] == "lesson":
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


def expression(s, i, inner=False):
    """The end of an expression at i: an operand, then (operator operand)*. A space either side of an operator is
    allowed; an ASCII - is an operator only with a space on both sides."""
    j = operand(s, i, inner)
    if j is None:
        return None
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
        if e is None:
            return j
        j = e


def runs(s):
    """Every maximal expression in a masked stretch, as (start, end)."""
    out, i = [], 0
    while i < len(s):
        ch = s[i]
        if (ch.isalnum() or ch in "−-√∠(") and (i == 0 or not (s[i - 1].isalnum() or s[i - 1] in "_'’.")):
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
    if re.search(rf"[{re.escape(OPS)}]|\^", t.lstrip("−-")) or re.search(rf"[{SUPS}√′″]", t) or re.search(r"[A-Za-z]\(", t):
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
    o = r"\d+(?:\.\d+)?|(?<![A-Za-z])[A-Za-z](?![A-Za-z])|\([^()]*\)"
    t = re.sub(rf"(?<![\w.)])({o})/({o})(?![\w.(])",
               lambda m: r"\frac{" + re.sub(r"^\((.*)\)$", r"\1", m.group(1)) + "}{" + re.sub(r"^\((.*)\)$", r"\1", m.group(2)) + "}", t)
    t = re.sub(rf"(?<![A-Za-z\\])({'|'.join(check.MATHS_OPERATORS)})(?![A-Za-z])", r"\\operatorname{\1}", t)
    t = re.sub(f"[{SUPS}]+", lambda m: "^{" + "".join(SUP_BACK[c] for c in m.group(0)) + "}", t)
    t = re.sub(r"\^\(([^()]*)\)", lambda m: "^{" + m.group(1) + "}", t)
    t = re.sub(r"\^([\d.]+)", lambda m: "^{" + m.group(1) + "}", t)
    t = t.replace("″", "''").replace("′", "'").replace("%", r"\%")
    return re.sub(r"∠", r"\\angle ", t)


def plan(text, geometry, keys):
    """(the spans to write as (start, end, tex), a Counter of what was left plain, the unsettled letters as
    (line number, context))."""
    masked = mask(text)
    found = []
    for a, b in zones(text):
        for s, e in runs(masked[a:b]):
            found.append((a + s, a + e, text[a + s:a + e]))
    left, unsettled, spans = collections.Counter(), [], []

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
    for s, e, t, key in found:
        k = kind_of(t)
        before, after = text[max(0, s - 24):s], text[e:e + 12]
        if key:
            left["key name"] += 1
            continue
        if k == "expr":
            if re.search(r"(?<![A-Za-z])[XYZT](?![A-Za-z(])", t) and not re.search(r"[a-z]", t):
                left["register in an expression"] += 1
                unsettled.append((text.count("\n", 0, s) + 1, f"register: {t}"))
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
            elif t not in letters and not (geometry and t.islower() and t != "a"):
                left["letter not in the lesson's maths"] += 1  # (in geometry a small letter is an angle: p, v, w)
            elif t in ("a", "A", "I") and re.match(r"\s+(?!(?:times|plus|minus|is|squared|cubed|and|or)\b)[a-z]{2,}", after):
                left["the word a, A or I"] += 1         # an article before its noun: "a number", "a customer"
            elif t in ("a", "A", "I"):
                left["unsettled letter"] += 1
                unsettled.append((text.count("\n", 0, s) + 1, f"{t}: …{before[-20:]}[{t}]{after}…".replace("\n", " ")))
            else:
                spans.append((s, e, t))
        else:
            left[{"number": "lone number", "angle": "lone ∠ name"}.get(k, "lone name (LCM, GCF)")] += 1
    return [(s, e, to_tex(t)) for s, e, t in spans], left, unsettled


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
    if len(sys.argv) < 3 or sys.argv[1] not in ("rewrap", "convert", "report"):
        print(__doc__)
        return 2
    step, course, dry = sys.argv[1], sys.argv[2], "--dry" in sys.argv
    geometry = course == "geometry"
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
            spans, left, unsettled = plan(body, geometry, keys)
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
