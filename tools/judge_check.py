#!/usr/bin/env python3
"""judge_check.py: proves tools/judge.c judges an answer as the firmware's vector runner does.

    tools/judge_check.py --core build/core-PIN [lessons/*/]

For every exact expectation (X=, Y=, Z=, T=, N=) in every lesson's vectors.txt, in the 33s mode a
vector runs in, three answers are planted against the value the core really produced (the vector
passes, so the core's value is the expectation's): the same number written another way (the core's
own E-form, and a trailing zero), and one unit off in the 34th significant digit. Each planted
expectation runs on the firmware's runner and through judge.c, and the two must give the same verdict:
right for the first two, wrong for the third. Then judge.c's tolerance (X#c,t) is checked against exact
decimal arithmetic at, inside and outside its edges. A disagreement, or a planted miss the runner
passes, fails the check.
"""
import argparse
import glob
import os
import re
import subprocess
import sys
import tempfile
from decimal import Decimal, getcontext

sys.stdout.reconfigure(encoding="utf-8")
getcontext().prec = 200
EXACT = re.compile(r"^([XYZTN])=([+-]?\d+(?:\.\d+)?(?:E[+-]?\d+)?)$")


def eform(v):
    """The core's VAL form: sign, the digits, E and the exponent (keyrun's +12002E-3)."""
    d = Decimal(v)
    sign, digits, exp = d.as_tuple()
    if not any(digits):
        return "+0E+0"
    return ("-" if sign else "+") + "".join(map(str, digits)) + f"E{exp:+d}"


def trailing(v):
    return v + "0" if "." in v and "E" not in v else (v + ".0" if "E" not in v else v)


def nudge(v):
    """One unit in the 34th significant digit above v (for 0: 1E-33)."""
    d = Decimal(v)
    if d == 0:
        return "1E-33"
    sign, digits, exp = d.normalize().as_tuple()
    top = len(digits) + exp                       # d is below 10^top
    unit = Decimal(1).scaleb(top - 34)
    return format(d + unit, "f") if abs(unit.adjusted()) < 60 else str(d + unit)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--core", required=True)
    ap.add_argument("lessons", nargs="*")
    a = ap.parse_args()
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.dirname(here)
    lessons = a.lessons or sorted(glob.glob(os.path.join(root, "lessons", "*", "")))
    judge = os.path.join(root, "build", "judge_test")
    sys.path.insert(0, here)
    import check                                  # the lesson's own mode and entry, as check.py runs them
    cases = []                                    # (vector line, judge expectation, the core's value, want)
    for d in lessons:
        path = os.path.join(d, "vectors.txt")
        if not os.path.exists(path):
            continue
        meta, _ = check.front_matter(open(os.path.join(d, "lesson.md"), encoding="utf-8").read())
        md = check.lesson_modes(meta)[0][0]
        entry = check.lesson_entries(meta, check.lesson_modes(meta)[0])[0][0]
        for vid, parts, _ in check.vectors_for_mode(check.read_vectors(path, 4), md, None, entry):
            parts = check.variant(parts, md, False, entry).split(" | ")
            exps = parts[3].split()
            for i, e in enumerate(exps):
                m = EXACT.match(e)
                if not m:
                    continue
                reg, v = m.groups()
                for tag, planted, want in (("e", eform(v), 1), ("z", trailing(v), 1), ("n", nudge(v), 0)):
                    tok = f"{reg}={planted}"
                    rest = exps[:i] + [tok] + exps[i + 1:]
                    cid = f"{os.path.basename(d.rstrip('/'))}.{vid}.{i}{tag}"   # no colon: the runner ends an ID with one
                    vline = " | ".join([cid, "judge_check", parts[2], " ".join(rest)])
                    cases.append((vline, tok, v, want))
    if not cases:
        print("judge: no expectations found")
        return 1
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as t:
        t.write("\n".join(c[0] for c in cases) + "\n")
    try:
        r = subprocess.run([f"{a.core}/build/vectors", t.name], capture_output=True, text=True, encoding="utf-8")
    finally:
        os.unlink(t.name)
    failed = {m.group(1) for m in re.finditer(r"^FAIL ([^\s:]+):", r.stdout, re.M)}
    bad = []
    # An instrument that never sees a failure would agree with anything (it did once: IDs with a colon
    # were cut at it, and every planted miss read as a pass).
    if not failed:
        bad.append("the runner failed no planted answer: the instrument cannot see a failure")
    jin = "\n".join(f"{tok}\t{v}" for _, tok, v, _ in cases) + "\n"
    j = subprocess.run([judge], input=jin, capture_output=True, text=True, encoding="utf-8")
    verdicts = j.stdout.split()
    for (vline, tok, v, want), jv in zip(cases, verdicts):
        cid = vline.split(" | ", 1)[0]
        runner = 0 if cid in failed else 1
        judged = int(jv)
        if runner != want:
            bad.append(f"runner: {cid} {tok} against {v}: {'passed' if runner else 'failed'}, planted to {'pass' if want else 'fail'}")
        if judged != runner:
            bad.append(f"disagree: {cid} {tok} against {v}: runner {runner}, judge {judged}")
    if len(verdicts) != len(cases):
        bad.append(f"judge answered {len(verdicts)} of {len(cases)}")
    # The tolerance against exact arithmetic: at the edges, inside and just outside.
    tcases = []
    for c, t in (("0.5", "0.5"), ("2", "1E-15"), ("12.36361580643337667476963084402730302448", "1E-20"),
                 ("-1", "1E-15"), ("0", "1E-33"), ("1E6", "0.001")):
        C, T = Decimal(c), Decimal(t)
        for got, want in ((C + T, 1), (C - T, 1), (C, 1), (C + T + T / 1000, 0), (C - T - T / 1000, 0),
                          (C + T - T / 1000, 1)):
            tcases.append((f"X#{c},{t}", str(got), want))
    j2 = subprocess.run([judge], input="\n".join(f"{e}\t{g}" for e, g, _ in tcases) + "\n",
                        capture_output=True, text=True, encoding="utf-8")
    for (e, g, want), jv in zip(tcases, j2.stdout.split()):
        if int(jv) != want:
            bad.append(f"tolerance: {e} against {g}: judge {jv}, exact arithmetic {want}")
    for b in bad[:20]:
        print("FAIL " + b)
    n_exp = len(cases) // 3
    print(f"judge: {len(cases)} planted answers on {n_exp} expectations, runner and judge.c agree on "
          f"{len(cases) - sum(1 for b in bad if b.startswith('disagree'))}; {len(tcases)} tolerance cases"
          + ("" if not bad else f"; {len(bad)} problems"))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
