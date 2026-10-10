#!/usr/bin/env python3
"""accepted.py [--rev REV] [--list] [--selftest]: which accepted lessons may be published from REV (default HEAD; "." is
the working tree).

Reads lessons/ACCEPTED at REV. A lesson is publishable when its lesson.md, vectors.txt and
fmt-vectors.txt at REV equal those at the last commit its line names (the accepted commit, or the
last change abacus has seen), the front matter's status, requires and tools lines aside (tools: by
abacus #6101: site metadata that graph.py checks). --selftest plants changes in a copy of a lesson. --list prints the publishable ids,
one a line, for the site's build; otherwise each lesson is reported. Exit 1 if any listed lesson is
held back or unknown, 0 if all are publishable."""
import argparse
import re
import subprocess
import sys

FILES = ("lesson.md", "vectors.txt", "fmt-vectors.txt")


def git(*args, ok=(0,)):
    r = subprocess.run(["git", *args], capture_output=True, text=True, encoding="utf-8")
    if r.returncode not in ok:
        raise SystemExit(f"accepted: git {' '.join(args)}: {r.stderr.strip()}")
    return r


def show(rev, path):
    """The file at rev (the working tree for "."), or None if it is not there."""
    if rev == ".":
        try:
            return open(path, encoding="utf-8").read()  # as git stores it: LF
        except FileNotFoundError:
            return None
    r = git("show", f"{rev}:{path}", ok=(0, 128))
    return r.stdout if r.returncode == 0 else None


BOOKKEEPING = ("status:", "requires:", "tools:")


def sans_status(text):
    """The text with the front matter's status, requires and tools lines removed: the lesson's
    bookkeeping, which may change without abacus (its accuracy read covers the prose, keys and values).
    Only those lines, and only in the front matter: any other change still holds the lesson."""
    if text is None:
        return None
    m = re.match(r"^---\n(.*?\n)---\n", text, re.S)
    if not m:
        return text
    head = "".join(l for l in m.group(1).splitlines(True) if not l.startswith(BOOKKEEPING))
    return "---\n" + head + "---\n" + text[m.end():]


def lesson_dirs(rev):
    """id -> lessons/<dir> or placement/<dir> at rev, read from each one's front matter. A placement
    check is accepted and held like a lesson (abacus #5355)."""
    out = {}
    paths = []
    for top in ("lessons/", "placement/"):
        found = git("ls-files", top).stdout.split() if rev == "." else \
            git("ls-tree", "--name-only", rev, top).stdout.split()
        if rev == ".":
            found = sorted({"/".join(p.split("/")[:2]) for p in found if p.count("/") >= 2})
        paths += found
    for path in paths:
        text = show(rev, f"{path}/lesson.md")
        m = text and re.search(r"^id:\s*(\S+)", text, re.M)
        if m:
            out[m.group(1)] = path
    return out


def read_list(rev):
    text = show(rev, "lessons/ACCEPTED")
    if text is None:
        raise SystemExit(f"accepted: no lessons/ACCEPTED at {rev}")
    rows = []
    for n, line in enumerate(text.splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) != 4 or not re.fullmatch(r"#\d+", parts[1]) or not re.fullmatch(r"[0-9a-f]{7,40}", parts[2]):
            raise SystemExit(f"accepted: lessons/ACCEPTED:{n}: expected 'id | #msg | commit | [#msg @ commit, ...]'")
        seen = re.findall(r"(#\d+)\s*@\s*([0-9a-f]{7,40})", parts[3])
        if parts[3] and len(seen) != len([s for s in parts[3].split(",") if s.strip()]):
            raise SystemExit(f"accepted: lessons/ACCEPTED:{n}: later changes must read '#msg @ commit'")
        rows.append((parts[0], parts[1], parts[2], seen))
    return rows


def selftest():
    """Each planted change must hold the lesson or pass it, as named; a plant that does not change the
    text is an error, not a pass."""
    text = open("lessons/angle-01-points-lines-and-angles/lesson.md", encoding="utf-8").read()
    word = "A point marks a place and has no size."
    tools = re.search(r"^tools:.*$", text, re.M).group(0)
    retool = text.replace(tools, "tools: point straightedge ruler", 1)
    plants = [
        ("a tools: edit alone passes", retool, False),
        ("a status: edit alone passes", re.sub(r"^status:.*$", "status: planted", text, count=1, flags=re.M), False),
        ("a tools: edit beside a changed word of prose holds",
         retool.replace(word, "A point marks a place and has no width.", 1), True),
        ("a tools: line added in the prose, outside the front matter, holds",
         text.replace("\n## Angles\n", "\ntools: compass\n## Angles\n", 1), True),
        ("a changed front matter line that is not bookkeeping holds",
         text.replace("display: FIX 4\n", "display: FIX 2\n", 1), True),
    ]
    red = 0
    for name, planted, hold in plants:
        if planted == text:
            print(f"FAIL {name}: the plant did not apply")
            continue
        held = sans_status(planted) != sans_status(text)
        print(f"{'ok  ' if held == hold else 'FAIL'} {name}")
        red += held == hold
    print(f"{red}/{len(plants)} acceptance controls as planted")
    return 0 if red == len(plants) else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rev", default="HEAD")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    dirs = lesson_dirs(a.rev)
    rows = read_list(a.rev)
    good, bad = [], []
    for lid, msg, commit, seen in rows:
        if lid not in dirs:
            bad.append(f"{lid}: no such lesson at {a.rev}")
            continue
        last = seen[-1][1] if seen else commit
        d = dirs[lid]
        changed = [f for f in FILES if sans_status(show(last, f"{d}/{f}")) != sans_status(show(a.rev, f"{d}/{f}"))]
        if changed:
            bad.append(f"{lid}: held back, {', '.join(changed)} changed since {last} (abacus has not seen it)")
        else:
            good.append(lid)
    for lid in sorted(set(dirs) - {r[0] for r in rows}):
        print(f"not accepted: {lid}", file=sys.stderr)
    if a.list:
        print("\n".join(good))
    else:
        for lid in good:
            print(f"ok   {lid}")
    for b in bad:
        print(f"HELD {b}", file=sys.stderr)
    print(f"{len(good)}/{len(rows)} accepted lessons publishable at {a.rev}", file=sys.stderr)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
