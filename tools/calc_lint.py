#!/usr/bin/env python3
"""calc_lint.py [--selftest]: lists, and never fails on, the keys blocks in an astronomy course's lessons that ask the
calculator for arithmetic a head can do (docs/courses/astronomy-shape.md; abacus #12375, from Michael's worry about
"teaching to the calculator"). A block is listed when its only operations are + − × ÷ on whole numbers under 100,
with no function key, and its lesson's front matter has no `calculator_reason:` line saying why the calculator earns
it. The listing is for abacus's review; the exit is 0 either way. --selftest plants a block of each kind."""
import glob
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SUBJECT = "astronomy"
KEYS = re.compile(r"^[ \t]*```keys[ \t]+(\S+)([^\n]*)\n(.*?)^[ \t]*```", re.M | re.S)
OPS = {"+", "−", "-", "×", "÷", "ENTER"}


def front_matter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    meta = {}
    for line in (m.group(1).splitlines() if m else []):
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta


def plain(keys):
    """True when the keys are only whole numbers under 100 and + − × ÷ ENTER."""
    toks = keys.split()
    nums = [t for t in toks if t not in OPS]
    return bool(nums) and len(nums) < len(toks) and all(t.isdigit() and int(t) < 100 for t in nums)


def listed(text):
    """[(block id, keys)] a lesson's text gives the listing, or [] when its front matter gives a reason."""
    if front_matter(text).get("calculator_reason"):
        return []
    out = {}                                   # an example's entry and mode variants are one example
    for m in KEYS.finditer(text):
        if m.group(1) != "setup" and plain(m.group(3)):
            out.setdefault(m.group(1), " ".join(m.group(3).split()))
    return list(out.items())


def astronomy_lessons(root):
    """{lesson id: lesson.md path} for the lessons listed in a course whose subject is astronomy."""
    ids = set()
    for p in glob.glob(os.path.join(root, "courses", "*.course")):
        text = open(p, encoding="utf-8").read()
        if re.search(rf"^subject \| {SUBJECT}\s*$", text, re.M):
            ids |= set(re.findall(r"^lesson \| (\S+)\s*$", text, re.M))
    out = {}
    for p in glob.glob(os.path.join(root, "lessons", "*", "lesson.md")):
        lid = front_matter(open(p, encoding="utf-8").read()).get("id")
        if lid in ids:
            out[lid] = p
    return out


def selftest():
    lesson = "---\nid: zz-01\n{reason}---\n\n```keys setup\nBLUE MODE {{mode}} GOLD DISP FIX 4\n```\n\n{block}"
    cases = [
        ("sky-01's 40 + 25, algebraic", lesson.format(reason="", block="```keys D01 entry=alg\n40 + 25 ENTER\n```\n"), 1),
        ("sky-01's 40 + 25, RPN", lesson.format(reason="", block="```keys D01 entry=rpn\n40 ENTER 25 +\n```\n"), 1),
        ("both entries of one example, listed once", lesson.format(
            reason="", block="```keys D01 entry=alg\n40 + 25 ENTER\n```\n\n```keys D01 entry=rpn\n40 ENTER 25 +\n```\n"), 1),
        ("par-01's TAN chain", lesson.format(reason="", block="```keys P01\n0.3136 ENTER 3600 ÷ TAN 1/x\n```\n"), 0),
        ("a number of 100 or more (90 + 25 listed, 125 not)",
         lesson.format(reason="", block="```keys A\n90 + 25 ENTER\n```\n\n```keys B\n125 − 60 ENTER\n```\n"), 1),
        ("a decimal, 5.37 − 5", lesson.format(reason="", block="```keys S01\n5.37 − 5 ENTER\n```\n"), 0),
        ("a block with a reason in the front matter",
         lesson.format(reason="calculator_reason: the learner's first keys, before any measurement\n",
                       block="```keys D01\n40 + 25 ENTER\n```\n"), 0),
        ("the setup alone", lesson.format(reason="", block=""), 0),
    ]
    ok = True
    for name, text, want in cases:
        got = len(listed(text))
        good = got == want
        ok = ok and good
        print(f"{'ok  ' if good else 'FAIL'} {name}: {got} listed, {want} expected")
    # The real tree: no astronomy lesson is listed since sky-01 and sky-02 went without the calculator (abacus
    # #12844), so the planted cases above are the positive controls; par-01's TAN chain is not listed either.
    real = astronomy_lessons(ROOT)
    for lid, want in (("par-01", False), ("sky-01", False), ("sky-02", False)):
        if lid in real:
            got = bool(listed(open(real[lid], encoding="utf-8").read()))
            ok = ok and got == want
            print(f"{'ok  ' if got == want else 'FAIL'} {lid} in the tree: {'listed' if got else 'not listed'}")
    print(f"calc-lint selftest: {'all as planted' if ok else 'a case went wrong'}")
    return ok


def main():
    if "--selftest" in sys.argv:
        return 0 if selftest() else 1
    total = 0
    for lid, p in sorted(astronomy_lessons(ROOT).items()):
        for bid, keys in listed(open(p, encoding="utf-8").read()):
            total += 1
            print(f"calc-lint: {lid} {bid}: arithmetic a head can do ({keys}); for abacus's review, or a "
                  f"calculator_reason: line in its front matter")
    print(f"calc-lint: {total} block(s) listed (a listing, not a failure)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
