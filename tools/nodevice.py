"""nodevice.py: the checks for a lesson with no device (T65, the computer science course; front matter
`device: none`), called by check.py in place of the calculator's. docs/lesson-format.md, "A lesson with no device".

Such a lesson has no setup, no modes or entries, no keys blocks and no quoted displays. What it has:

- items whose answer is typed text (`answer: text`) or a table's blank cells (`answer: table`, with `table:` and
  `row:` lines), each judged by tools/judge.c from an expectation in vectors.txt: `ID | note | - | TEXT=...`,
  `BASE=b:digits` or `GRID=c,c,...` (judge.h);
- docs/evidence/<id>.py, a recomputation of every expectation that never calls judge.c, whose printed lines must be
  vectors.txt's exactly;
- ```quote``` blocks, each a passage from a source in sources/SOURCES.tsv, whose words must be in that source's
  cached text (scripts/fetch-sources.py), on the page the block names when the text marks its pages.
"""
import hashlib
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ITEM_BLOCK = re.compile(r"^[ \t]*```item[ \t]+(\S+)[ \t]*\n(.*?)^[ \t]*```[ \t]*$", re.M | re.S)
QUOTE_BLOCK = re.compile(r"^[ \t]*```quote[ \t]+(\S+)[ \t]*([^\n]*)\n(.*?)^[ \t]*```[ \t]*$", re.M | re.S)
FIELDS = ("prompt", "topics", "answer", "calculator", "table", "row", "slip")
FORM = re.compile(r"^(TEXT|BASE|GRID)=(\S+)$")
BASE_CELL = re.compile(r"^(2|8|10|16):([0-9A-Za-z]+)$")
REFUSED_META = ("setup", "modes", "modes_reason", "entries", "display", "voices")
REFUSED_BODY = (("```keys", "a keys block"), ("<disp", "a <disp> quote"), ("```widget", "a widget"), ("```why", "a why block"),
                ("<mode", "a <mode> span"), ("<entry", "an <entry> span"), ("<voice", "a <voice> span"))


def cells(text):
    return [c.strip() for c in text.split("|")]


def parse_items(body):
    """(id, start, fields, rows, slips, problems) for each item."""
    out = []
    for m in ITEM_BLOCK.finditer(body):
        iid, fields, rows, slips, problems = m.group(1), {}, [], [], []
        for raw in m.group(2).splitlines():
            line = raw.strip()
            if not line:
                continue
            k, sep, v = line.partition(":")
            k, v = k.strip(), v.strip()
            if not sep or k not in FIELDS:
                problems.append(f"item {iid}: a line not one of {', '.join(FIELDS)}: '{line}'")
            elif k == "slip":
                parts = [p.strip() for p in v.split("|")]
                if len(parts) != 3 or not all(parts):
                    problems.append(f"item {iid}: a slip is 'slip: VID | name | hint': '{line}'")
                else:
                    slips.append(tuple(parts))
            elif k == "row":
                rows.append(cells(v))
            elif k in fields:
                problems.append(f"item {iid}: {k} given twice")
            else:
                fields[k] = v
        for k in ("prompt", "topics", "answer", "calculator"):
            if not fields.get(k):
                problems.append(f"item {iid}: no {k}:")
        kind = fields.get("answer")
        if kind and kind not in ("text", "table"):
            problems.append(f"item {iid}: answer: is text or table in a lesson with no device")
        if fields.get("calculator") not in (None, "no"):
            problems.append(f"item {iid}: calculator: is no in a lesson with no device")
        if kind == "text" and ("table" in fields or rows):
            problems.append(f"item {iid}: a text answer has no table: or row:")
        if kind == "table":
            head = cells(fields.get("table", ""))
            if "table" not in fields or not all(head):
                problems.append(f"item {iid}: a table answer needs `table: head | head | ...`, every head named")
            if not rows:
                problems.append(f"item {iid}: a table answer needs its rows, `row: cell | cell | ...`")
            for r in rows:
                if len(r) != len(head):
                    problems.append(f"item {iid}: a row of {len(r)} cells under a head of {len(head)}: {' | '.join(r)}")
                if any(not c for c in r):
                    problems.append(f"item {iid}: an empty cell (a blank for the learner is ?): {' | '.join(r)}")
            if rows and not any(c == "?" for r in rows for c in r):
                problems.append(f"item {iid}: a table with no ? cell asks nothing")
        out.append((iid, m.start(), fields, rows, slips, problems))
    return out


def blanks(rows):
    return sum(c == "?" for r in rows for c in r)


def canonical(exp):
    """The learner's answer that exp means exactly: the text a right answer is typed as."""
    kind, v = FORM.match(exp).groups()
    if kind == "BASE":
        return v.split(":", 1)[1]
    if kind == "GRID":
        return ",".join(BASE_CELL.match(c).group(2) if BASE_CELL.match(c) else c for c in v.split(","))
    return v


def form_problems(vid, exp):
    m = FORM.match(exp)
    if not m:
        return [f"{vid}: the expectation is one of TEXT=, BASE=b:digits or GRID=c,c,... (got '{exp}')"]
    kind, v = m.groups()
    if kind == "BASE":
        b = BASE_CELL.match(v)
        if not b or any(int(ch, 36) >= int(b.group(1)) for ch in b.group(2)):
            return [f"{vid}: BASE= is a base (2, 8, 10 or 16), a colon and that base's digits (got '{v}')"]
    if kind == "GRID":
        if any(not c for c in v.split(",")):
            return [f"{vid}: GRID= has an empty cell"]
        for c in v.split(","):
            b = BASE_CELL.match(c)
            if b and any(int(ch, 36) >= int(b.group(1)) for ch in b.group(2)):
                return [f"{vid}: GRID= cell '{c}' has a digit its base does not"]
    return []


def judge(pairs, judge_bin):
    """judge_expect for each (expectation, answer), through tools/judge_test (the page's own judge)."""
    if not pairs:
        return []
    r = subprocess.run([judge_bin], input="".join(f"{e}\t{g}\n" for e, g in pairs), capture_output=True, text=True,
                       encoding="utf-8")
    out = r.stdout.split()
    if r.returncode != 0 or len(out) != len(pairs):
        raise ValueError(f"judge_test answered {len(out)} of {len(pairs)} (rc {r.returncode}): {r.stderr.strip()}")
    return [int(x) for x in out]


def norm_quote(s):
    """A passage as words: TeX's quotes and markup dropped, curly quotes straightened, spaces collapsed."""
    s = s.replace("``", '"').replace("''", '"').replace("“", '"').replace("”", '"').replace("’", "'").replace("‘", "'")
    s = re.sub(r"\\[a-zA-Z]+\{([^{}]*)\}", r"\1", s).replace("$", "")
    return re.sub(r"\s+", " ", s).strip()


def sources():
    rows = {}
    path = os.path.join(ROOT, "sources", "SOURCES.tsv")
    for line in open(path, encoding="utf-8"):
        if line.startswith("#") or not line.strip():
            continue
        f = line.rstrip("\n").split("\t")
        rows[f[0]] = f
    return rows


def quote_problems(body):
    out = []
    table = None
    for m in QUOTE_BLOCK.finditer(body):
        sid, where, words = m.group(1), m.group(2).strip(), norm_quote(m.group(3))
        if table is None:
            table = sources()
        if sid not in table:
            out.append(f"quote from {sid}: not a source in sources/SOURCES.tsv")
            continue
        if not where:
            out.append(f"quote from {sid}: the fence names where in the source it is (```quote {sid} p. 224)")
        if len(words) < 12:
            out.append(f"quote from {sid}: too short to find: '{words}'")
            continue
        p = os.path.join(ROOT, "sources", "cache", f"{sid}.txt")
        if not os.path.exists(p):
            out.append(f"quote from {sid}: sources/cache/{sid}.txt is not fetched (python3 scripts/fetch-sources.py)")
            continue
        raw = open(p, "rb").read()
        if hashlib.sha256(raw).hexdigest() != table[sid][-1]:
            out.append(f"quote from {sid}: the cached text is not the one read (its sha256 is not SOURCES.tsv's)")
            continue
        text = raw.decode("utf-8")
        flat = norm_quote(text)
        i = flat.find(words)
        if i < 0:
            out.append(f"quote from {sid}: not in the source: '{words[:80]}'")
            continue
        pages = re.findall(r"\[p\. (\d+)\]", flat[:i])
        if pages and where != f"p. {pages[-1]}":
            out.append(f"quote from {sid}: it is on p. {pages[-1]}, the fence says '{where}'")
    return out


def topics_known():
    known = set()
    for line in open(os.path.join(ROOT, "lessons", "TOPICS"), encoding="utf-8"):
        if line.strip() and not line.startswith("#"):
            known.add(line.split("|", 1)[0].strip())
    return known


def evidence_problems(lesson_id, vectors):
    path = os.path.join(ROOT, "docs", "evidence", f"{lesson_id}.py")
    if not os.path.exists(path):
        return [f"no recomputation of the expectations: docs/evidence/{lesson_id}.py"]
    r = subprocess.run([sys.executable, "-I", path], capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        return [f"docs/evidence/{lesson_id}.py failed: {r.stderr.strip()[-300:]}"]
    got = {}
    for line in r.stdout.splitlines():
        if line.strip():
            vid, _, exp = line.partition(" | ")
            got[vid.strip()] = exp.strip()
    want = {vid: parts[3] for vid, parts, _ in vectors}
    out = []
    for vid in sorted(set(want) | set(got)):
        if vid not in got:
            out.append(f"evidence: {vid} is not recomputed by docs/evidence/{lesson_id}.py")
        elif vid not in want:
            out.append(f"evidence: {vid} is recomputed but not in vectors.txt")
        elif got[vid] != want[vid]:
            out.append(f"evidence: {vid}: vectors.txt says {want[vid]}, the recomputation {got[vid]}")
    return out


def problems(lesson_dir, meta, body, vectors, judge_bin):
    """Everything wrong with a lesson with no device, and the notes for its line."""
    out, notes = [], []
    for k in REFUSED_META:
        if k in meta:
            out.append(f"front matter `{k}:` in a lesson with no device")
    for tok, what in REFUSED_BODY:
        if tok in body:
            out.append(f"{what} in a lesson with no device")
    items = parse_items(body)
    if not items:
        out.append("a lesson with no device keeps at least one item (the route map counts it done by them)")
    known = topics_known()
    vec = {}
    for vid, parts, _ in vectors:
        if parts[2] != "-":
            out.append(f"{vid}: keys are - in a lesson with no device (got '{parts[2]}')")
        exps = parts[3].split()
        if len(exps) != 1:
            out.append(f"{vid}: one expectation, not {len(exps)}")
            continue
        out += form_problems(vid, exps[0])
        vec[vid] = exps[0]
    used, pairs, why = set(), [], []
    ids = [i[0] for i in items]
    for dup in sorted({i for i in ids if ids.count(i) > 1}):
        out.append(f"item {dup} appears more than once")
    for iid, start, fields, rows, slips, probs in items:
        out += probs
        for t in fields.get("topics", "").split():
            if t not in known:
                out.append(f"item {iid}: topic {t} is not in lessons/TOPICS")
        if iid not in vec:
            out.append(f"item {iid}: no vector {iid} for its answer")
            continue
        used.add(iid)
        ans = vec[iid]
        kind = FORM.match(ans).group(1) if FORM.match(ans) else None
        if fields.get("answer") == "table" and kind != "GRID":
            out.append(f"item {iid}: a table answer's vector is GRID=")
        if fields.get("answer") == "text" and kind not in ("TEXT", "BASE"):
            out.append(f"item {iid}: a text answer's vector is TEXT= or BASE=")
        if kind == "GRID" and fields.get("answer") == "table" and len(ans[5:].split(",")) != blanks(rows):
            out.append(f"item {iid}: GRID= gives {len(ans[5:].split(','))} cells, the table has {blanks(rows)} blanks")
        if form_problems(iid, ans):
            continue
        pairs.append((ans, canonical(ans)))
        why.append((1, f"item {iid}: its own answer, {canonical(ans)}, is not judged right"))
        # Nothing before an item shows its answer (as for the calculator's items).
        a = canonical(ans)
        if kind != "GRID" and len(a) >= 3 and re.search(rf"(?<![0-9A-Za-z]){re.escape(a)}(?![0-9A-Za-z])", body[:start]):
            out.append(f"item {iid}: its answer {a} is in the lesson before the item")
        for vid, name, _ in slips:
            if vid not in vec:
                out.append(f"item {iid}: no vector {vid} for its slip ({name})")
                continue
            used.add(vid)
            if form_problems(vid, vec[vid]):
                continue
            skind = FORM.match(vec[vid]).group(1)
            if (kind == "GRID") != (skind == "GRID"):
                out.append(f"item {iid}: slip {vid} is not the answer's kind ({skind}= beside {kind}=)")
                continue
            # The page shows a slip's hint when the learner's answer is judged right against the slip's expectation:
            # the slip's own value must be, and the item's answer must not take it.
            pairs.append((ans, canonical(vec[vid])))
            why.append((0, f"item {iid}: slip {vid} ({name}) gives the answer itself"))
            pairs.append((vec[vid], canonical(vec[vid])))
            why.append((1, f"item {iid}: slip {vid} ({name}): its own value, {canonical(vec[vid])}, is not judged its"))
    for vid in sorted(set(vec) - used):
        out.append(f"vector {vid} is no item's answer and no slip's")
    if pairs:
        for v, (want, msg) in zip(judge(pairs, judge_bin), why):
            if v != want:
                out.append(msg)
    out += evidence_problems(meta.get("id", os.path.basename(lesson_dir)), vectors)
    quotes = len(QUOTE_BLOCK.findall(body))
    out += quote_problems(body)
    notes.append(f"no device: {len(items)} items judged by judge.c, {len(vectors)} expectations recomputed, "
                 f"{quotes} quotes found in their sources")
    return out, notes
