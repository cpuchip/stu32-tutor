#!/usr/bin/env python3
"""accepted.py [--rev REV] [--list]: which accepted lessons may be published from REV (default HEAD; "." is
the working tree).

Reads lessons/ACCEPTED at REV. A lesson is publishable when its lesson.md, vectors.txt and
fmt-vectors.txt at REV equal those at the last commit its line names (the accepted commit, or the
last change abacus has seen), the front matter's status and requires lines aside. --list prints the publishable ids,
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


def sans_status(text):
    """The text with the front matter's status and requires lines removed: the lesson's bookkeeping,
    which may change without abacus (its accuracy read covers the prose, keys and values)."""
    if text is None:
        return None
    m = re.match(r"^---\n(.*?\n)---\n", text, re.S)
    if not m:
        return text
    head = "".join(l for l in m.group(1).splitlines(True) if not l.startswith(("status:", "requires:")))
    return "---\n" + head + "---\n" + text[m.end():]


def lesson_dirs(rev):
    """id -> lessons/<dir> at rev, read from each lesson's front matter."""
    out = {}
    paths = git("ls-files", "lessons/").stdout.split() if rev == "." else \
        git("ls-tree", "--name-only", rev, "lessons/").stdout.split()
    if rev == ".":
        paths = sorted({"/".join(p.split("/")[:2]) for p in paths if p.count("/") >= 2})
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rev", default="HEAD")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
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
