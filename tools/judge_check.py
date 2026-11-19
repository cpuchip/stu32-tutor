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


DIGITS = "0123456789abcdefghijklmnopqrstuvwxyz"
BASE_CELL = re.compile(r"^(2|8|10|16):([0-9A-Za-z]+)$")


def squash(s):
    return "".join(s.split()).lower()


def m_text(w, g):
    w = squash(w)
    return -1 if not w else int(w == squash(g))


def m_base(b, d, g):
    """A number in base b, by value: the model's own reading, Python's int over digits it has checked first."""
    if b not in (2, 8, 10, 16) or not d or any(c not in DIGITS[:b] for c in d.lower()):
        return -1
    g = squash(g)
    if not g or any(c not in DIGITS[:b] for c in g):
        return 0
    return int(int(d, b) == int(g, b))


def m_cell(w, g):
    m = BASE_CELL.match(w)
    return m_base(int(m.group(1)), m.group(2), g) if m else m_text(w, g)


def model(exp, got):
    """judge.h's rules for the forms with no device (TEXT=, BASE=, GRID=, and a CELL i of a grid), written again."""
    if exp.startswith("CELL "):
        i, grid = exp[5:].split("\t", 1)
        ws = grid.split(",")
        return m_cell(ws[int(i)], got) if 0 <= int(i) < len(ws) else -1
    kind, v = exp.split("=", 1)
    if kind == "TEXT":
        return m_text(v, got)
    if kind == "BASE":
        b, _, d = v.partition(":")
        return m_base(int(b), d, got) if b.isdigit() else -1
    ws, gs = v.split(","), got.split(",")
    if any(m_cell(w, "") < 0 for w in ws):
        return -1
    return int(len(ws) == len(gs) and all(m_cell(w, g) == 1 for w, g in zip(ws, gs)))


def to_base(n, b):
    s = ""
    while True:
        s = DIGITS[n % b] + s
        n //= b
        if not n:
            return s


def other(c):
    return {"0": "1", "1": "0"}.get(c, "z" if c != "z" else "y")


def plants(exp):
    """(expectation, answer, verdict meant) for one expectation: right, right written another way, wrong."""
    kind, v = exp.split("=", 1)
    if kind == "TEXT":
        return [(exp, v, 1), (exp, " ".join(v).upper(), 1), (exp, v[:-1] + other(v[-1]), 0), (exp, v + v[-1], 0)]
    if kind == "BASE":
        b, d = v.split(":", 1)
        b, n = int(b), int(d, int(b))
        return [(exp, d, 1), (exp, "00" + d.upper(), 1), (exp, " " + d.lower() + " ", 1), (exp, to_base(n + 1, b), 0),
                (exp, d + DIGITS[b], 0), (exp, "", 0),
                (f"BASE={b}:{d}{DIGITS[b]}", d, -1)]       # an expectation with a digit its base lacks is not read
    ws = v.split(",")
    right = [BASE_CELL.match(w).group(2) if BASE_CELL.match(w) else w for w in ws]
    out = [(exp, ",".join(right), 1), (exp, ", ".join(right), 1), (exp, ",".join(right[:-1]), 0),
           (exp, ",".join(right + right[-1:]), 0)]
    for i, w in enumerate(ws):
        wrong = right[:i] + [other(right[i][-1]) if not BASE_CELL.match(w) else
                             to_base(int(right[i], int(BASE_CELL.match(w).group(1))) + 1, int(BASE_CELL.match(w).group(1)))] + right[i + 1:]
        out.append((exp, ",".join(wrong), 0))
        out.append((f"CELL {i}\t{v}", right[i], 1))
        out.append((f"CELL {i}\t{v}", wrong[i], 0))
    out.append((f"CELL {len(ws)}\t{v}", right[0], -1))
    return out


def nodevice_cases(lessons):
    """Every no-device expectation's planted answers, each checked against the model before judge.c sees it: a plant
    the model does not judge as meant is a fault in the model or the plant, and is raised, not counted."""
    out = []
    for d in lessons:
        for line in open(os.path.join(d, "vectors.txt"), encoding="utf-8"):
            if line.lstrip().startswith("#") or line.count("|") < 3:
                continue
            exp = line.rstrip("\n").split("|")[3].strip()
            if not re.match(r"^(TEXT|BASE|GRID)=", exp):
                continue
            for e, g, want in plants(exp):
                if model(e, g) != want:
                    raise SystemExit(f"judge_check: the model judges {e!r} against {g!r} as {model(e, g)}, "
                                     f"planted as {want}")
                out.append((e, g, want))
    return out


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
    nodevice_lessons = []
    for d in lessons:
        path = os.path.join(d, "vectors.txt")
        if not os.path.exists(path):
            continue
        meta, _ = check.front_matter(open(os.path.join(d, "lesson.md"), encoding="utf-8").read())
        if "device" in meta:
            nodevice_lessons.append(d)            # no core runs it: judged against the model below
            continue
        md, entry = check.lesson_pairs(meta)[0]
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
    # The forms with no device (T65): every TEXT=, BASE= and GRID= expectation of a lesson with no device, against a
    # model of the rules written here in Python, with answers planted right, right written another way, and wrong.
    ncases = nodevice_cases(nodevice_lessons)
    if nodevice_lessons and not ncases:
        bad.append("no-device: lessons with no device, but no expectation of theirs was planted")
    jn = subprocess.run([judge], input="".join(f"{e}\t{g}\n" for e, g, _ in ncases), capture_output=True, text=True,
                        encoding="utf-8")
    nv = jn.stdout.split()
    if len(nv) != len(ncases):
        bad.append(f"no-device: judge answered {len(nv)} of {len(ncases)}")
    for (e, g, want), jv in zip(ncases, nv):
        if int(jv) != want:
            bad.append(f"no-device: {e} against '{g}': judge {jv}, the model {want}")
    for b in bad[:20]:
        print("FAIL " + b)
    n_exp = len(cases) // 3
    print(f"judge: {len(cases)} planted answers on {n_exp} expectations, runner and judge.c agree on "
          f"{len(cases) - sum(1 for b in bad if b.startswith('disagree'))}; {len(tcases)} tolerance cases; "
          f"{len(ncases)} no-device cases"
          + ("" if not bad else f"; {len(bad)} problems"))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
