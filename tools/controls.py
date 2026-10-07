#!/usr/bin/env python3
"""controls.py: proves check.py can fail. Each control plants one fault in a copy of a lesson and
requires check.py to fail with the message that names it; the clean copy must pass first.

    tools/controls.py --core build/core-PIN lessons/rpn-01-the-stack

A planted fault that does not change the file is an error, not a pass (a mutant counts only when it
applies), and so is a control that fails for some other reason than its own.
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile

sys.stdout.reconfigure(encoding="utf-8")

# (name, file, old, new, env, text the failure must contain)
CONTROLS = [
    ("a printed key does something else", "lesson.md", "3 ENTER 4 + 5 ×", "3 ENTER 4 + 5 +", {},
     "S06: printed keys and vector disagree in 33s mode: DIFF"),
    ("a shifted legend printed without its shift", "lesson.md", "4 ÷ GOLD LASTx\n", "4 ÷ LASTx\n", {},
     "S11: printed keys and vector disagree in 33s mode: KEY"),
    ("a legend no key carries", "lesson.md", "5 ENTER 20 x↔y ÷", "5 ENTER 20 SWAP ÷", {},
     "S09: printed keys and vector disagree in 33s mode: KEY"),
    ("the printed setup is not the setup", "lesson.md", "```keys setup\nBLUE MODE 33s", "```keys setup\nBLUE MODE 35s", {},
     "the setup block"),
    ("the setup pressed is not the vectors' setup", "lesson.md", "setup: BLUE MODE 33s GOLD DISP FIX 4",
     "setup: BLUE MODE 33s GOLD DISP FIX 2", {}, "printed keys and vector disagree in 33s mode: DIFF"),
    ("a wrong expected value", "vectors.txt", "5 + | X=12\n", "5 + | X=13\n", {}, "vectors in 33s mode"),
    ("a vector right in 33s mode only (the 35s's key after a message only clears it)", "vectors.txt",
     "S01 | ENTER separates two numbers; + uses both | MODE33 FIX4 7 ENTER 5 + | X=12",
     "S01 | ENTER separates two numbers; + uses both | MODE33 FIX4 7 ENTER 5 + | X=12\n"
     "S99 | planted | MODE33 FIX4 1 ENTER 0 / 5 | ERR X=5", {}, "vectors in 35s mode"),
    ("a vector no printed keys show", "vectors.txt", "5 + | X=12\n", "5 + | X=12\nS98 | planted | MODE33 FIX4 1 ENTER 1 + | X=2\n",
     {}, "vector S98 is shown by no keys block"),
    ("a vector with no expectation", "vectors.txt", "5 + | X=12\n", "5 + | \n", {}, "S01: no expectation"),
    ("a vector that does not set its mode", "vectors.txt", "MODE33 FIX4 7 ENTER 5 + |", "FIX4 7 ENTER 5 + |", {},
     "S01: keys must begin MODE33"),
    ("a keys block naming no vector", "lesson.md", "```keys S02\n", "```keys S2\n", {}, "keys block S2 names no vector"),
    ("a quoted display the display vector does not show", "lesson.md", '<disp v="S01">12.0000</disp>',
     '<disp v="S01">12.000</disp>', {}, "D-S01: the prose shows"),
    ("a display vector of another value", "fmt-vectors.txt", "| 12 | FIX 4 |  | 12.0000", "| 13 | FIX 4 |  | 13.0000", {},
     "D-S01: value 13"),
    ("a display vector at another setting", "fmt-vectors.txt", "| 2.5 | FIX 4 |  | 2.5000", "| 2.5 | FIX 2 |  | 2.50", {},
     "D-S03: display vector at 'FIX 2'"),
    ("a quoted display with no display vector", "lesson.md", "X shows <disp v=\"S03\">", "X shows <disp v=\"S05\">", {},
     "no display vector D-S05"),
    ("an em-dash in the prose", "lesson.md", "## Two numbers, one operation", "## Two numbers \u2014 one operation", {},
     "em-dash"),
    ("the same ops from a different state (planted CLx behind the trace)", None, None, None, {"KEYRUN_FAULT": "state"},
     "STATE: the same"),
    # From the 2026-10-06 outside review (docs/evidence/rpn-01.md), one control per finding fixed.
    ("the quoted displays at a setting the student never pressed",
     [("lesson.md", "display: FIX 4", "display: FIX 2"), ("lesson.md", '<disp v="S01">12.0000</disp>', '<disp v="S01">12.00</disp>'),
      ("fmt-vectors.txt", "| 12 | FIX 4 |  | 12.0000", "| 12 | FIX 2 |  | 12.00")], None, None, {},
     "front matter `display: FIX 2`, but the vectors set FIX 4"),
    ("a display vector with options the device does not use", "fmt-vectors.txt", "| 12 | FIX 4 |  | 12.0000",
     "| 12 | FIX 4 | sep=off | 12.0000", {}, "display options 'sep=off'"),
    ("a quoted display of a number still being typed",
     [("vectors.txt", "5 + | X=12\n", "5 + | X=12\nS97 | planted | MODE33 FIX4 6 ENTER 5 | X=5\n"),
      ("lesson.md", "## Two numbers, one operation\n", "## Two numbers, one operation\n\n```keys S97\n6 ENTER 5\n```\n\n<disp v=\"S97\">5.0000</disp>\n"),
      ("fmt-vectors.txt", "D-S03 |", "D-S97 | planted | 5 | FIX 4 |  | 5.0000\nD-S03 |")], None, None, {},
     "D-S97: the device's X line shows"),
    ("a quoted display under another example", "lesson.md", 'X shows <disp v="S01">12.0000</disp>',
     'X shows <disp v="S03">2.5000</disp>', {}, "is not under its own example (it follows S01)"),
    ("a keys fence the checker would not read", "lesson.md", "```keys S02\n", "```keys S02 alt\n", {},
     "a fence that looks like keys but is not checked"),
    ("a display tag in a form the checker would not read", "lesson.md", '<disp v="S01">', "<disp v='S01'>", {},
     "<disp tags"),
    ("an example that needs an empty stack",
     [("vectors.txt", "5 + | X=12\n", "5 + | X=12\nS96 | planted | MODE33 FIX4 4 + | X=4\n"),
      ("lesson.md", "## Two numbers, one operation\n", "## Two numbers, one operation\n\n```keys S96\n4 +\n```\n")], None, None, {},
     "vectors in 33s mode, a used core"),
    ("an empty modes line", "lesson.md", "display: FIX 4\n", "display: FIX 4\nmodes:\n", {}, "give 33, 35 or both"),
    ("modes named as models", "lesson.md", "display: FIX 4\n", "display: FIX 4\nmodes: 33s 35s\nmodes_reason: planted\n", {},
     "give 33, 35 or both"),
    ("a second mode key inside a vector", "vectors.txt", "MODE33 FIX4 7 ENTER 5 - |", "MODE33 FIX4 MODE33 7 ENTER 5 - |", {},
     "S02: the mode is set only by the first key"),
    ("keys that end with a shift armed", "lesson.md", "4 ÷ GOLD LASTx ×\n", "4 ÷ GOLD LASTx × GOLD\n", {},
     "LEFT: the keys end with a shift armed"),
    ("a display written in the prose without its tag", "lesson.md", "scientific form.\n",
     "decimal places, so 12 appears as 12.0000.\n", {}, "'12.0000' looks like a display at FIX 4"),
    ("an em-dash written as an entity", "lesson.md", "## Two numbers, one operation", "## Two numbers &mdash; one operation", {},
     "em-dash"),
]


# Negative controls: harmless changes that must still pass, so a red above is not a check that
# fails on everything near it. (The first em-dash check counted the text "2014".)
GREENS = [
    ("a year in the prose is not an em-dash", "lesson.md", "## Two numbers, one operation",
     "## Two numbers, one operation (CODATA 2014, 2018 and 2022)"),
    ("a hyphen is not an em-dash", "lesson.md", "## Two numbers, one operation", "## Two numbers - one operation"),
    ("a number in other than the display's form is not a display", "lesson.md", "scientific form.\n",
     "scientific form. A price of 1.05 or 21.5 is fine to write.\n"),
    ("an input written in the display's form, in a sentence about no screen", "lesson.md", "scientific form.\n",
     "scientific form. A rate of 0.0825 is typed as it is written.\n"),
]


# Controls that need a lesson's own content (rpn-02's VIEW line). A lesson not named here gets the
# lists above, which are anchored on rpn-01.
CONTROLS_FOR = {
    "rpn-02-storing-numbers": [
        ("a quoted VIEW line the screen does not show", "lesson.md", 'kind="view">B=49.75<', 'kind="view">B=49.70<', {},
         "V06: the device's X line shows 'B=49.75' (view), the prose 'B=49.70' (view)"),
        ("a VIEW line quoted as a value", "lesson.md", '<disp v="V06" kind="view">', '<disp v="V06">', {},
         "has no display vector D-V06"),
        ("a quoted line of the wrong kind", "lesson.md", 'kind="view">B=49.75<', 'kind="prompt">B=49.75<', {},
         "(view), the prose 'B=49.75' (prompt)"),
        ("a stored value shown rounded but quoted whole", "lesson.md", '<disp v="V01">0.08</disp>', '<disp v="V01">0.0825</disp>',
         {}, "D-V01: the prose shows '0.0825'"),
        ("a variable key that is not the letter's", "lesson.md", "0.0825 STO A 40 RCL × A\n", "0.0825 STO A 40 RCL × B\n", {},
         "V03: printed keys and vector disagree in 33s mode: DIFF"),
    ],
}
GREENS_FOR = {
    "rpn-02-storing-numbers": [
        ("a price written in prose at the display's places", "lesson.md", "## A running total\n",
         "## A running total\n\nA 12.50 lunch and a 7.25 coffee are typed as 12.5 and 7.25.\n"),
    ],
}


def run_check(core, lesson, env):
    e = dict(os.environ)
    e.update(env)
    here = os.path.dirname(os.path.abspath(__file__))
    r = subprocess.run([sys.executable, os.path.join(here, "check.py"), "--core", core, lesson],
                       capture_output=True, text=True, encoding="utf-8", env=e)
    return r.returncode, r.stdout + r.stderr


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--core", required=True)
    ap.add_argument("lesson")
    a = ap.parse_args()
    lesson = a.lesson.rstrip("/")
    controls = CONTROLS_FOR.get(os.path.basename(lesson), CONTROLS)
    greens = GREENS_FOR.get(os.path.basename(lesson), GREENS)
    bad = 0
    with tempfile.TemporaryDirectory() as tmp:
        clean = os.path.join(tmp, "clean")
        shutil.copytree(lesson, clean)
        rc, out = run_check(a.core, clean, {})
        if rc != 0:
            print("FAIL the clean lesson does not pass, so no control means anything:\n" + out)
            return 1
        print("ok   the clean lesson passes")
        for name, fn, old, new, env, want in controls:
            d = os.path.join(tmp, "c")
            shutil.rmtree(d, ignore_errors=True)
            shutil.copytree(lesson, d)
            edits = fn if isinstance(fn, list) else ([(fn, old, new)] if fn else [])
            applied = True
            for efn, eold, enew in edits:
                p = os.path.join(d, efn)
                s = open(p, encoding="utf-8").read()
                if s.count(eold) != 1:
                    print(f"FAIL {name}: the fault did not apply to {efn} ({s.count(eold)} matches)")
                    applied = False
                    break
                open(p, "w", encoding="utf-8").write(s.replace(eold, enew))
            if not applied:
                bad += 1
                continue
            rc, out = run_check(a.core, d, env)
            if rc == 0:
                print(f"FAIL {name}: check.py PASSED a lesson with this fault")
                bad += 1
            elif want not in out:
                print(f"FAIL {name}: check.py failed, but not for this fault:\n{out}")
                bad += 1
            else:
                line = next(l.strip() for l in out.splitlines() if want in l)
                print(f"ok   {name}\n       -> {line[:150]}")
        greens_bad = 0
        for name, fn, old, new in greens:
            d = os.path.join(tmp, "g")
            shutil.rmtree(d, ignore_errors=True)
            shutil.copytree(lesson, d)
            p = os.path.join(d, fn)
            s = open(p, encoding="utf-8").read()
            if s.count(old) != 1:
                print(f"FAIL {name}: the change did not apply")
                greens_bad += 1
                continue
            open(p, "w", encoding="utf-8").write(s.replace(old, new))
            rc, out = run_check(a.core, d, {})
            if rc != 0:
                print(f"FAIL {name}: check.py failed a harmless change:\n{out}")
                greens_bad += 1
            else:
                print(f"ok   {name} (still passes)")
    print(f"{len(controls) - bad}/{len(controls)} controls red as planted; "
          f"{len(greens) - greens_bad}/{len(greens)} harmless changes still green")
    bad += greens_bad
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
