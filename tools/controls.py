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
    ("the printed setup is not the setup", "lesson.md", "```keys setup\nBLUE MODE {mode}", "```keys setup\nBLUE MODE 35s", {},
     "the setup block"),
    ("the setup pressed is not the vectors' setup", "lesson.md", "setup: BLUE MODE {mode} GOLD DISP FIX 4",
     "setup: BLUE MODE {mode} GOLD DISP FIX 2", {}, "printed keys and vector disagree in 33s mode: DIFF"),
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
    ("an empty modes line", "lesson.md", "display: FIX 4\n", "display: FIX 4\nmodes:\n", {}, "give some of 33s 35s STU"),
    ("modes named by number, not by the MODE menu's labels", "lesson.md", "display: FIX 4\n", "display: FIX 4\nmodes: 33 35\nmodes_reason: planted\n", {},
     "give some of 33s 35s STU"),
    ("fewer than three modes without a reason", "lesson.md", "display: FIX 4\n", "display: FIX 4\nmodes: 33s 35s\n", {},
     "offers fewer than all three modes without a `modes_reason`"),
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
CONTROLS_FOR["rpn-03-the-display"] = [
    ("a quote verified at the setup's setting while its example ends at another",
     [("fmt-vectors.txt", "| SCI 3 |  | 6.667E-1", "| FIX 4 |  | 0.6667"),
      ("lesson.md", '<disp v="P04">6.667E-1</disp>', '<disp v="P04">0.6667</disp>')], None, None, {},
     "D-P04: display vector at 'FIX 4', vector P04 ends at 'SCI 3'"),
    ("a long display verified at the runner's width (22), not the device's (21)",
     [("fmt-vectors.txt", "| ALL | w=21 | 0.6666666666666666667", "| ALL |  | 0.66666666666666666667"),
      ("lesson.md", '<disp v="P08B">0.6666666666666666667</disp>', '<disp v="P08B">0.66666666666666666667</disp>')],
     None, None, {}, "D-P08B: the device's X line shows '0.6666666666666666667'"),
    ("a screen claim worded with 'showed'", "lesson.md", "## ALL: no padding\n",
     "## ALL: no padding\n\nAt FIX 4 the screen showed 0.1250 for it.\n", {},
     "'0.1250' looks like a display at FIX 4"),
]
CONTROLS_FOR["num-02-fractions"] = [
    ("the other arrow quoted", "lesson.md", 'kind="status">▲</disp>', 'kind="status">▼</disp>', {},
     "E01: the status band shows"),
    ("a display vector whose indicator disagrees with the device's arrow", "fmt-vectors.txt",
     "| w=21 | 0 5/6 v", "| w=21 | 0 5/6 ^", {}, "D-G04: the display vector's indicator is '^', the status band has"),
    ("a display vector that drops an inexact fraction's indicator", "fmt-vectors.txt",
     "| w=21 | 0 5/6 v", "| w=21 | 0 5/6", {}, "D-G04: the display vector's indicator is 'none', the status band has"),
    ("a fraction quoted after the fraction key turned it off",
     [("fmt-vectors.txt", "D-G07 | after G07 | 2.375 | FIX 4 | w=21 | 2.3750", "D-G07 | after G07 | 2.375 | FRAC 4095 P | w=21 | 2 3/8"),
      ("lesson.md", '<disp v="G07">2.3750</disp>', '<disp v="G07">2 3/8</disp>')], None, None, {},
     "D-G07: display vector at 'FRAC 4095 P', vector G07 ends at 'FIX 4'"),
    ("an example that turns Fraction display on again, though the one before left it on",
     [("lesson.md", "```keys G06 after=G05\n.3.4 ENTER .2.3 ×\n", "```keys G06 after=G05\n.3.4 ENTER .2.3 × BLUE →FRAC\n"),
      ("vectors.txt", "FDISP .3.4 ENTER .2.3 * | X=0.5", "FDISP .3.4 ENTER .2.3 * FDISP | X=0.5")], None, None, {},
     "D-G06: display vector at 'FRAC 4095 P', vector G06 ends at 'FIX 4'"),
]
CONTROLS_FOR["num-01-order-of-operations"] = [
    ("a stopping point's example written in full again (the student's half-typed 5 strands it)", "lesson.md",
     "```keys N01 after=N01A\n× +\n", "```keys N01\n3 ENTER 4 ENTER 5 × +\n", {},
     "N01: working through in order, X holds"),
    ("a continuation of a block that is not the one just before it", "lesson.md",
     "```keys N08T after=N08S\n", "```keys N08T after=N05A\n", {},
     "keys block N08T continues N05A, but the block just before it is N08S"),
    ("a stray digit that still lands on the right X (only Y shows it)", "lesson.md",
     "```keys N08T after=N08S\n+ GOLD x² ×\n", "```keys N08T\n2 ENTER 3 ENTER 4 ENTER 1 + GOLD x² ×\n", {},
     "N08T: working through in order, Y holds"),
]
CONTROLS_FOR["num-03-powers-and-roots"] = [
    ("the 35s message rule taken out of keyrun (KEYRUN_FAULT=no-m35-rule)", None, None, None,
     {"KEYRUN_FAULT": "no-m35-rule"}, "R07E: printed keys and vector disagree in 35s mode: DIFF"),
    ("a quoted error message the screen does not show", "lesson.md", 'kind="message">INVALID yˣ<',
     'kind="message">INVALID ˣ√y<', {}, "R07D: the device's X line shows 'INVALID yˣ' (message)"),
]
CONTROLS_FOR["eq-01-equations"] = [
    ("a variant naming a mode that does not exist", "lesson.md", "```keys Q06B after=Q06 mode=33s,35s\n",
     "```keys Q06B after=Q06 mode=33s,36s\n", {}, "mode=33s,36s names 36s"),
    ("STU's own vector missing: the shared one (SYNTAX ERROR) run in STU", "vectors.txt", "Q06@STU |", "Q06Z@STU |", {},
     "vectors in STU mode"),
    ("a quoted equation the screen does not show", "lesson.md", 'v="Q01" kind="eqn">2×X+3=11<', 'v="Q01" kind="eqn">2×X+3=12<', {},
     "Q01: the device's X line shows '2×X+3=11' (eqn)"),
    ("a quoted prompt the screen does not show", "lesson.md", 'kind="prompt">X?<', 'kind="prompt">Y?<', {},
     "Q02: the device's X line shows"),
    ("an equation-bar key the bar does not have", "lesson.md", "GOLD EQN 2 × RCL X + 3 = 11 ENTER\n```",
     "GOLD EQN 2 × RCL X + 3 EQUALS 11 ENTER\n```", {}, "Q01: printed keys and vector disagree in 33s mode: KEY"),
    ("a stopping point left at a prompt that no continuation answers", "lesson.md", "```keys Q05 after=Q05A\nX\n```",
     "```keys Q05\nGOLD EQN 2 × RCL X + 3 = 11 ENTER GOLD SOLVE X\n```", {},
     "Q05A: printed keys and vector disagree in 33s mode: LEFT: the keys end with a prompt waiting"),
    ("checking a second value without showing the equation again", "lesson.md", "```keys Q04 after=Q03\nGOLD EQN XEQ 5 R/S\n",
     "```keys Q04 after=Q03\nXEQ 5 R/S\n", {}, "Q04: printed keys and vector disagree in 33s mode"),
    ("← over SOLVE's view quoted as clearing X too", "lesson.md", 'v="Q05C">4.0000<', 'v="Q05C">0.0000<', {},
     "D-Q05C: the prose shows '0.0000'"),
]
CONTROLS_FOR["fn-01-functions-as-programs"] = [
    ("a 35s-only quote wrong in its own mode", "lesson.md", 'm="35s">F001 LBL F ·35<', 'm="35s">F001 LBL F ·33<', {},
     "F01B: the device's X line shows 'F001 LBL F ·35' (program), the prose 'F001 LBL F ·33' (program) (35s)"),
    ("a quoted program line the screen does not show", "lesson.md", 'kind="program">K004 3<', 'kind="program">K004 +<', {},
     "M02: the device's X line shows 'K004 3' (program)"),
    ("program entry quoted as resuming at F's last line after a run", "lesson.md", 'v="G01A" kind="program">PRGM TOP<',
     'v="G01A" kind="program">F006 RTN<', {}, "G01A: the device's X line shows 'PRGM TOP' (program)"),
    ("a program entered with the wrong key", "lesson.md", "```keys F01C after=F01B\n2 × 3 +\n", "```keys F01C after=F01B\n2 × 3 −\n", {},
     "F01C: printed keys and vector disagree in 33s mode: DIFF"),
]
CONTROLS_FOR["num-04-percent-and-powers-of-ten"] = [
    ("a small number quoted in FIX form, where the display falls back to scientific", "lesson.md",
     'v="C06">4.00E-3<', 'v="C06">0.00<', {}, "D-C06: the prose shows '0.00'"),
    ("% keyed as %CHG", "lesson.md", "```keys C01\n80 ENTER 15 GOLD %\n", "```keys C01\n80 ENTER 15 BLUE %CHG\n", {},
     "C01: printed keys and vector disagree in 33s mode"),
]
CONTROLS_FOR["eq-02-formulas"] = [
    ("a SOLVE root's view under the wrong letter", "lesson.md", 'kind="view">W=3.5000<', 'kind="view">A=3.5000<', {},
     "S01: the device's X line shows 'W=3.5000' (view)"),
    ("a SOLVE root quoted as a plain value (before firmware 035)", "lesson.md",
     'The X line shows <disp v="S01" kind="view">W=3.5000</disp>', 'X shows <disp v="S01">3.5000</disp>', {},
     "S01: working through in order, X shows 'W=3.5000' (view), the prose '3.5000'"),
    ("solved for the wrong letter", "lesson.md", "GOLD EQN GOLD SOLVE F 100 R/S", "GOLD EQN GOLD SOLVE C 100 R/S", {},
     "T02: printed keys and vector disagree in 33s mode"),
]
CONTROLS_FOR["eq-03-two-answers-and-inequalities"] = [
    ("the other root quoted", "lesson.md", 'kind="view">X=8.0000<', 'kind="view">X=-2.0000<', {},
     "A03: the device's X line shows 'X=8.0000' (view)"),
    ("a guess keyed without its sign", "lesson.md", "```keys A04 after=A03\n0 STO X 10 +/− ",
     "```keys A04 after=A03\n0 STO X 10 ", {}, "A04: printed keys and vector disagree in 33s mode"),
]
CONTROLS_FOR["lin-01-slope-and-intercept"] = [
    ("the slope keyed run over rise", "lesson.md", "```keys L01\n13 ENTER 9 − 5 ENTER 3 − ÷\n",
     "```keys L01\n5 ENTER 3 − 13 ENTER 9 − ÷\n", {}, "L01: printed keys and vector disagree in 33s mode"),
    ("a vertical line's message misquoted", "lesson.md", 'v="L07" kind="message">DIVIDE BY 0<',
     'v="L07" kind="message">INVALID DATA<', {}, "L07: the device's X line shows 'DIVIDE BY 0' (message)"),
    ("the intercept quoted as the slope", "lesson.md", 'v="L03">3.0000<', 'v="L03">2.0000<', {},
     "D-L03: the prose shows '2.0000'"),
]
CONTROLS_FOR["lin-02-lines-through-data"] = [
    ("a point entered x first (the Σ+ order reversed)", "lesson.md", "```keys D01\nGOLD CLEAR Σ 3 ENTER 1 Σ+\n",
     "```keys D01\nGOLD CLEAR Σ 1 ENTER 3 Σ+\n", {}, "D01: printed keys and vector disagree in 33s mode"),
    ("the statistics not cleared first", "lesson.md", "```keys D01\nGOLD CLEAR Σ 3 ENTER 1 Σ+\n",
     "```keys D01\n3 ENTER 1 Σ+\n", {}, "D01: printed keys and vector disagree in 33s mode"),
    ("r quoted with the sign of the falling set", "lesson.md", 'v="D05">0.9851<', 'v="D05">-0.9851<', {},
     "D-D05: the prose shows '-0.9851'"),
    ("Σ− taken as removing the last point, whatever its values", "lesson.md", "```keys W02A after=W01\n11 ENTER 5 GOLD Σ−\n",
     "```keys W02A after=W01\nGOLD Σ−\n", {}, "W02A: printed keys and vector disagree in 33s mode"),
]
CONTROLS_FOR["lin-03-when-a-line-does-not-fit"] = [
    ("q(2) keyed as 1, its sign lost", "lesson.md", "0 ENTER 1 Σ+ 1 +/− ENTER 2 Σ+", "0 ENTER 1 Σ+ 1 ENTER 2 Σ+", {},
     "Q01: printed keys and vector disagree in 33s mode"),
    ("the curve's r quoted as a weak rising fit", "lesson.md", 'v="Q02">0.0000<', 'v="Q02">0.3000<', {},
     "D-Q02: the prose shows '0.3000'"),
    ("the doubling estimate quoted as the doubling", "lesson.md", 'v="E01D">34.0000<', 'v="E01D">64.0000<', {},
     "D-E01D: the prose shows '64.0000'"),
    ("flat data's r quoted as 0 instead of the refusal", "lesson.md", 'v="F01" kind="message">STAT ERROR<',
     'v="F01">0.0000<', {}, "F01: working through in order, X shows 'STAT ERROR' (message)"),
]
CONTROLS_FOR["poly-01-evaluating-a-polynomial"] = [
    ("the stack filled with two ENTERs, not three", "lesson.md", "```keys H02\n2 ENTER ENTER ENTER 2 ×",
     "```keys H02\n2 ENTER ENTER 2 ×", {}, "H02: printed keys and vector disagree in 33s mode"),
    ("a coefficient's sign lost (+ 3 for − 3)", "lesson.md", "```keys H01B after=H01C\n−\n",
     "```keys H01B after=H01C\n+\n", {}, "H01B: printed keys and vector disagree in 33s mode"),
    ("the missing power's 0 left out", "lesson.md", "   2 ENTER ENTER ENTER 1 × 0 + × 2 − × 1 +\n",
     "   2 ENTER ENTER ENTER 1 × 2 − × 1 +\n", {}, "E01: printed keys and vector disagree in 33s mode"),
]
CONTROLS_FOR["poly-02-roots-with-solve"] = [
    ("a <mode> span naming a mode that does not exist", "lesson.md", '<mode m="35s,STU">: in this mode', '<mode m="35s,STV">: in this mode', {},
     "STV is not one of 33s 35s STU"),
    ("the message left showing before the next example (the 35s and STU key only clears it)", "lesson.md",
     "```keys N02 after=N01\nC\n```\n", "", {}, "E01A: working through in order, X holds +1E+0, the vector says -1 (35s)"),
    ("guesses that straddle two roots (0 and 2.5) quoted as the first", "lesson.md",
     "```keys S01 after=R05\n0 STO X 1.5 GOLD EQN", "```keys S01 after=R05\n0 STO X 2.5 GOLD EQN", {},
     "S01: printed keys and vector disagree in 33s mode"),
    ("a sign misread in the table of values", "lesson.md", 'v="R04">-0.3750<', 'v="R04">0.3750<', {},
     "D-R04: the prose shows '0.3750'"),
    ("x² + 1 quoted as having a root", "lesson.md", 'v="N01" kind="message">NO ROOT FND<',
     'v="N01" kind="view">X=0.0000<', {}, "N01: the device's X line shows 'NO ROOT FND' (message)"),
]
CONTROLS_FOR["poly-03-the-quadratic-formula"] = [
    ("b stored without its sign", "lesson.md", "```keys Q01\n1 STO A 4 +/− STO B 3 STO C\n",
     "```keys Q01\n1 STO A 4 STO B 3 STO C\n", {}, "Q01: printed keys and vector disagree in 33s mode"),
    ("dividing by 2 instead of 2a in the exercise", "lesson.md", "```keys E01B after=E01\nRCL B +/− RCL D √x + 2 RCL A × ÷\n",
     "```keys E01B after=E01\nRCL B +/− RCL D √x + 2 ÷\n", {}, "E01B: printed keys and vector disagree in 33s mode"),
    ("a negative discriminant's refusal misquoted", "lesson.md", 'v="N02" kind="message">SQRT(NEG)<',
     'v="N02" kind="message">INVALID DATA<', {}, "N02: the device's X line shows 'SQRT(NEG)' (message)"),
]
CONTROLS_FOR["poly-04-complex-roots"] = [
    ("33s: a pair typed real part first", "lesson.md", "```keys C01A mode=33s\n1 ENTER 0\n",
     "```keys C01A mode=33s\n0 ENTER 1\n", {}, "C01A: printed keys and vector disagree in 33s mode"),
    ("33s: the imaginary part quoted as the X line", "lesson.md", '<disp v="R01" m="33s">-1.0000<',
     '<disp v="R01" m="33s">2.0000<', {}, "D-R01: the prose shows '2.0000'"),
    ("a root's i part quoted with the wrong sign", "lesson.md", 'v="R01" m="35s,STU">-1.0000i2.0000<', 'v="R01" m="35s,STU">-1.0000i-2.0000<', {},
     "D-R01: the prose shows '-1.0000i-2.0000'"),
    ("−b typed without ENTER (the −2 runs into the 0 of 0 i 4)", "lesson.md", "```keys R01\n2 +/− ENTER 0 BLUE CMPLX i 4 + 2 ÷\n",
     "```keys R01\n2 +/− 0 BLUE CMPLX i 4 + 2 ÷\n", {}, "R01: printed keys and vector disagree in 35s mode"),
    ("the conjugate checked with its i part's sign lost", "lesson.md", "```keys H02A\n1 +/− BLUE CMPLX i 2 +/−\n",
     "```keys H02A\n1 +/− BLUE CMPLX i 2\n", {}, "H02A: printed keys and vector disagree in 35s mode"),
]
CONTROLS_FOR["exp-01-growth-and-decay"] = [
    ("4% growth keyed as a factor of 0.04", "lesson.md", "```keys G01\n500 ENTER 1.04 ENTER 10 yˣ ×\n",
     "```keys G01\n500 ENTER 0.04 ENTER 10 yˣ ×\n", {}, "G01: printed keys and vector disagree in 33s mode"),
    ("15% loss keyed as a factor of 1.15", "lesson.md", "   18000 ENTER 0.85 ENTER 4 yˣ ×\n",
     "   18000 ENTER 1.15 ENTER 4 yˣ ×\n", {}, "E02: printed keys and vector disagree in 33s mode"),
    ("the decay quoted as halfway between 20 and 10", "lesson.md", 'v="D01">14.1421<', 'v="D01">15.0000<', {},
     "D-D01: the prose shows '15.0000'"),
]
CONTROLS_FOR["exp-02-the-number-e"] = [
    ("a monthly rate keyed as the yearly one (no ÷ 12)", "lesson.md", "```keys C02\n1000 ENTER 0.06 ENTER 12 ÷ 1 + 12 yˣ ×\n",
     "```keys C02\n1000 ENTER 0.06 1 + 12 yˣ ×\n", {}, "C02: printed keys and vector disagree in 33s mode"),
    ("continuous growth keyed with 10ˣ for eˣ", "lesson.md", "```keys G01\n1000 ENTER 0.06 eˣ ×\n",
     "```keys G01\n1000 ENTER 0.06 GOLD 10ˣ ×\n", {}, "G01: printed keys and vector disagree in 33s mode"),
    ("the limit quoted as e to more places than FIX 4 shows", "lesson.md", 'v="L03">2.7183<', 'v="L03">2.71828<', {},
     "D-L03: the prose shows '2.71828'"),
]
CONTROLS_FOR["exp-03-logarithms"] = [
    ("the division the wrong way round (log 1.04 ÷ log 2)", "lesson.md", "```keys S01\n2 GOLD LOG 1.04 GOLD LOG ÷\n",
     "```keys S01\n1.04 GOLD LOG 2 GOLD LOG ÷\n", {}, "S01: printed keys and vector disagree in 33s mode"),
    ("LOG keyed without its gold shift", "lesson.md", "```keys L01\n1000 GOLD LOG\n", "```keys L01\n1000 LOG\n", {},
     "'LOG': no key has that legend on its face"),
    ("the half-life quoted as negative", "lesson.md", 'v="H01">6.5788<', 'v="H01">-6.5788<', {},
     "D-H01: the prose shows '-6.5788'"),
]
CONTROLS_FOR["exp-04-exponential-equations"] = [
    ("EXP( typed without ▶ out of its parentheses", "lesson.md", "```keys Q01\nGOLD EQN eˣ RCL X ▶ = 3 × RCL X ENTER\n",
     "```keys Q01\nGOLD EQN eˣ RCL X = 3 × RCL X ENTER\n", {}, "Q01: printed keys and vector disagree in 33s mode"),
    ("guesses that straddle both roots (0 and 2)", "lesson.md", "```keys S01 after=Q04\n0 STO X 1 GOLD EQN",
     "```keys S01 after=Q04\n0 STO X 2 GOLD EQN", {}, "S01: printed keys and vector disagree in 33s mode"),
    ("a sign misread at x = 1", "lesson.md", 'v="Q03">-0.2817<', 'v="Q03">0.2817<', {}, "D-Q03: the prose shows '0.2817'"),
]
CONTROLS_FOR["trig-01-degrees-and-radians"] = [
    ("the radians example quoted as if still in degrees", "lesson.md", 'v="A02">-0.9880<', 'v="A02">0.5000<', {},
     "D-A02: the prose shows '0.5000'"),
    ("the status band quoted as DEG", "lesson.md", 'v="A02" kind="status">RAD<', 'v="A02" kind="status">DEG<', {},
     "A02: the status band shows"),
    ("the exercise's sine left in radians (DEG not set)", "lesson.md", "   BLUE ∡MODE DEG 45 SIN\n", "   45 SIN\n", {},
     "E03: printed keys and vector disagree in 33s mode"),
]
CONTROLS_FOR["trig-02-right-triangles"] = [
    ("the ladder's height taken with cos (the adjacent side)", "lesson.md", "```keys L01\n5 ENTER 70 SIN ×\n",
     "```keys L01\n5 ENTER 70 COS ×\n", {}, "L01: printed keys and vector disagree in 33s mode"),
    ("an angle from SIN instead of ASIN", "lesson.md", "```keys A01\n3 ENTER 5 ÷ GOLD ASIN\n", "```keys A01\n3 ENTER 5 ÷ SIN\n", {},
     "A01: printed keys and vector disagree in 33s mode"),
    ("the tree's height quoted from the wrong ratio (12 ÷ tan 35)", "lesson.md", 'v="T01">8.4025<', 'v="T01">17.1378<', {},
     "D-T01: the prose shows '17.1378'"),
]
CONTROLS_FOR["trig-03-the-unit-circle"] = [
    ("cos 120 quoted with the sign of the right-hand side", "lesson.md", 'v="U01">-0.5000<', 'v="U01">0.5000<', {},
     "D-U01: the prose shows '0.5000'"),
    ("ASIN 0.5 quoted as the other angle", "lesson.md", 'v="U07">30.0000<', 'v="U07">150.0000<', {},
     "D-U07: the prose shows '150.0000'"),
    ("a negative angle keyed without its sign", "lesson.md", "```keys U09\n30 +/− SIN\n", "```keys U09\n30 SIN\n", {},
     "U09: printed keys and vector disagree in 33s mode"),
]
CONTROLS_FOR["trig-04-polar-and-rectangular"] = [
    ("->POL with x and y the wrong way round", "lesson.md", "```keys P01\n4 ENTER 3 BLUE ANGLE →POL\n",
     "```keys P01\n3 ENTER 4 BLUE ANGLE →POL\n", {}, "P01: printed keys and vector disagree in 33s mode"),
    ("the second-quadrant angle quoted as ATAN gives it", "lesson.md", 'v="Q01">126.8699<', 'v="Q01">-53.1301<', {},
     "D-Q01: the prose shows '-53.1301'"),
    ("->REC with r and the angle the wrong way round", "lesson.md", "```keys R01\n30 ENTER 10 BLUE ANGLE →REC\n",
     "```keys R01\n10 ENTER 30 BLUE ANGLE →REC\n", {}, "R01: printed keys and vector disagree in 33s mode"),
]
CONTROLS_FOR["sys-01-two-equations-at-once"] = [
    ("a pair that fits one equation quoted as fitting both", "lesson.md", 'v="C01">40.0000<', 'v="C01">37.0000<', {},
     "D-C01: the prose shows '37.0000'"),
    ("elimination done the wrong way round: (37 - 15) x 2", "lesson.md", "```keys L01\n37 ENTER 2 ENTER 15 × −\n",
     "```keys L01\n37 ENTER 15 − 2 ×\n", {}, "L01: printed keys and vector disagree in 33s mode"),
    ("no solution read off a 0 = 0", "lesson.md", 'v="E02">3.0000<', 'v="E02">0.0000<', {},
     "D-E02: the prose shows '0.0000'"),
    ("the fruit's bottom taken the wrong way round: 0.75 - 1.25", "lesson.md", "6 × − 1.25 ENTER 0.75 − ÷\n```\n\nX shows",
     "6 × − 0.75 ENTER 1.25 − ÷\n```\n\nX shows", {}, "F01: printed keys and vector disagree in 33s mode"),
]
CONTROLS_FOR["sys-02-the-built-in-solvers"] = [
    ("A and B typed the wrong way round", "lesson.md", "```keys T01 after=T01B\n2 R/S 3 R/S 37 R/S",
     "```keys T01 after=T01B\n3 R/S 2 R/S 37 R/S", {}, "T01: printed keys and vector disagree in 35s mode"),
    ("y quoted as x's value", "lesson.md", 'kind="view">Y=7.0000<', 'kind="view">Y=8.0000<', {},
     "T02: the device's X line shows 'Y=7.0000' (view)"),
    ("the list opened without NEW (only right on a fresh list)", "lesson.md", "```keys T01Z\nGOLD EQN NEW\n",
     "```keys T01Z\nGOLD EQN\n", {}, "T01Z: printed keys and vector disagree in 35s mode"),
    ("one line twice quoted as no solution", "lesson.md", 'kind="message">MULT SOLUTION<',
     'kind="message">NO SOLUTION<', {}, "N02: the device's X line shows 'MULT SOLUTION' (message)"),
]
CONTROLS_FOR["seq-01-sequences-and-sums"] = [
    ("the nth term with n steps, not n - 1", "lesson.md", "```keys A01\n20 ENTER 14 ENTER 2 × +\n",
     "```keys A01\n20 ENTER 15 ENTER 2 × +\n", {}, "A01: printed keys and vector disagree in 33s mode"),
    ("the geometric sum quoted as the next term", "lesson.md", 'v="G02">3,069.0000<', 'v="G02">3,072.0000<', {},
     "D-G02: the prose shows '3,072.0000'"),
    ("the loop's row k as 20 + 2k (one row out)", "lesson.md", "IP 2 × 18 + STO + T BLUE ISG I GOLD GTO W RCL T",
     "IP 2 × 20 + STO + T BLUE ISG I GOLD GTO W RCL T", {}, "P01B: printed keys and vector disagree in 33s mode"),
]
CONTROLS_FOR["cnt-01-counting"] = [
    ("a team counted with order (Pn,r for Cn,r)", "lesson.md", "```keys C01\n10 ENTER 3 BLUE PROB Cn,r\n",
     "```keys C01\n10 ENTER 3 BLUE PROB Pn,r\n", {}, "C01: printed keys and vector disagree in 33s mode"),
    ("n and r typed the wrong way round", "lesson.md", "```keys P01\n10 ENTER 3 BLUE PROB Pn,r\n",
     "```keys P01\n3 ENTER 10 BLUE PROB Pn,r\n", {}, "P01: printed keys and vector disagree in 33s mode"),
    ("52! quoted with one power of ten too many", "lesson.md", 'v="F02">8.0658E67<', 'v="F02">8.0658E68<', {},
     "D-F02: the prose shows '8.0658E68'"),
]
CONTROLS_FOR["prob-01-probability"] = [
    ("the die game quoted as fair (expected value 0)", "lesson.md", 'v="X01">-0.1667<', 'v="X01">0.0000<', {},
     "D-X01: the prose shows '0.0000'"),
    ("not worked the wrong way round: 1/6 - 1", "lesson.md", "```keys N01\n1 ENTER 1 ENTER 6 ÷ −\n",
     "```keys N01\n1 ENTER 6 ÷ 1 −\n", {}, "N01: printed keys and vector disagree in 33s mode"),
    ("at least one 6 quoted without the not: (5/6)^4", "lesson.md", 'v="A02">0.5177<', 'v="A02">0.4823<', {},
     "D-A02: the prose shows '0.4823'"),
    ("the same seed shown without seeding again", "lesson.md",
     "7 BLUE SEED GOLD RAND STO A 7 BLUE SEED GOLD RAND RCL A −", "7 BLUE SEED GOLD RAND STO A GOLD RAND RCL A −",
     {}, "S01: printed keys and vector disagree in 33s mode"),
    ("a die face claimed far outside 1 to 6 (the tolerance is checked)", "vectors.txt", "| X#3.5,2.5", "| X#10,0.5", {},
     "R02"),
]
CONTROLS_FOR["lim-01-approaching-a-limit"] = [
    ("program L without x<>y: (x^2 - 1) divided the wrong way", "lesson.md",
     "GOLD LBL L ENTER GOLD x² 1 − x↔y 1 − ÷ BLUE RTN", "GOLD LBL L ENTER GOLD x² 1 − 1 − ÷ BLUE RTN", {},
     "P01A: printed keys and vector disagree in 33s mode"),
    ("two sides that disagree quoted as agreeing", "lesson.md", 'v="N04">-1.0000<', 'v="N04">1.0000<', {},
     "D-N04: the prose shows '1.0000'"),
    ("sin(x)/x quoted at FIX 4, hiding the approach", "lesson.md", 'v="S02">0.999983333<', 'v="S02">1.0000<', {},
     "D-S02: the prose shows '1.0000'"),
    ("the limit from below quoted as from above", "lesson.md", 'v="L04">1.9000<', 'v="L04">2.1000<', {},
     "D-L04: the prose shows '2.1000'"),
]
CONTROLS_FOR["lim-02-rates-of-change"] = [
    ("program D without taking away d(1)", "lesson.md", "GOLD LBL D STO H 1 + GOLD x² 2 × 2 − RCL H ÷ BLUE RTN",
     "GOLD LBL D STO H 1 + GOLD x² 2 × RCL H ÷ BLUE RTN", {}, "P01A: printed keys and vector disagree in 33s mode"),
    ("the cancelled h = 1E-34 quoted as if it still gave 4", "lesson.md", 'v="D05">0.0000<', 'v="D05">4.0000<', {},
     "D-D05: the prose shows '4.0000'"),
    ("the average speed quoted as the speed at an instant", "lesson.md", 'v="A01">8.0000<', 'v="A01">4.0000<', {},
     "D-A01: the prose shows '4.0000'"),
]
CONTROLS_FOR["int-01-area-under-a-curve"] = [
    ("the strips' heights at their left ends (k - 1)", "lesson.md",
     "GOLD LBL B RCL I BLUE POW IP 3 × RCL N ÷ GOLD x² 3 × RCL N ÷ STO + T BLUE ISG I GOLD GTO B RCL T",
     "GOLD LBL B RCL I BLUE POW IP 1 − 3 × RCL N ÷ GOLD x² 3 × RCL N ÷ STO + T BLUE ISG I GOLD GTO B RCL T", {},
     "P01A: printed keys and vector disagree in 33s mode"),
    ("three rectangles quoted as the true area", "lesson.md", 'v="A01">14.0000<', 'v="A01">9.0000<', {},
     "D-A01: the prose shows '9.0000'"),
    ("the integral's limits the wrong way round", "lesson.md", "GOLD EQN 0 ENTER 3 GOLD EQN GOLD ∫ X",
     "GOLD EQN 3 ENTER 0 GOLD EQN GOLD ∫ X", {}, "I01B: printed keys and vector disagree in 33s mode"),
]
CONTROLS_FOR["prob-01b-loot-boxes"] = [
    ("at least one in 100 quoted as 1 in 100 makes it certain", "lesson.md", 'v="P03">0.6340<', 'v="P03">1.0000<', {},
     "D-P03: the prose shows '1.0000'"),
    ("the pity timer's sum without taking 0.99^90 from 1", "lesson.md", "```keys T01\n1 ENTER 0.99 ENTER 90 yˣ − 0.01 ÷\n",
     "```keys T01\n0.99 ENTER 90 yˣ 0.01 ÷\n", {}, "T01: printed keys and vector disagree in 33s mode"),
    ("exactly one without the C(100, 1) ways", "lesson.md", "```keys K01\n100 ENTER 1 BLUE PROB Cn,r 0.01 × 0.99 ENTER 99 yˣ ×\n",
     "```keys K01\n0.01 0.99 ENTER 99 yˣ ×\n", {}, "K01: printed keys and vector disagree in 33s mode"),
]
CONTROLS_FOR["fn-02-a-table-of-values"] = [
    ("a label's line numbered from the program's top, not its own label", "lesson.md", 'kind="program">U008 RTN<',
     'kind="program">T022 RTN<', {}, "T01B: the device's X line shows 'U008 RTN' (program)"),
    ("the loop entered without IP", "lesson.md", "GOLD LBL U RCL I BLUE POW IP XEQ Q R/S", "GOLD LBL U RCL I XEQ Q R/S", {},
     "T01B: printed keys and vector disagree in 33s mode: DIFF"),
    ("a TABLE row misquoted (q(0) where q(1) is)", "lesson.md", 'kind="row">1.0000 0.0000<', 'kind="row">1.0000 3.0000<',
     {}, "B05: the device's X line shows"),
    ("a graph readout misquoted (the trace at x = 2.02 read as the lowest point)", "lesson.md",
     'kind="readout">x=2.0200 y=-0.9996<', 'kind="readout">x=2.0200 y=-1.0000<', {},
     "W03: the graph's readout shows 'x=2.0200 y=-0.9996'"),
    ("the fitted y axis misquoted", "lesson.md", 'kind="ymin">-1.8000<', 'kind="ymin">-1.0000<', {},
     "W02: the graph's ymin shows '-1.8000'"),
]
CONTROLS_FOR["fn-03-domain"] = [
    ("a stopped program quoted as stopped after the line that refused", "lesson.md",
     'v="S05" kind="program">S004 √x<', 'v="S05" kind="program">S005 RTN<', {},
     "S05: the device's X line shows 'S004 √x' (program)"),
    ("program entry quoted at the top while a program is stopped", "lesson.md",
     'v="D04" kind="program">R002 1/x<', 'v="D04" kind="program">PRGM TOP<', {},
     "D04: the device's X line shows 'R002 1/x' (program)"),
    ("the wrong error message", "lesson.md", 'v="S03" kind="message">SQRT(NEG)<',
     'v="S03" kind="message">DIVIDE BY 0<', {}, "S03: the device's X line shows 'SQRT(NEG)' (message)"),
    ("a negative input keyed with − instead of +/−", "lesson.md", "2 +/− XEQ R\n", "2 − XEQ R\n", {},
     "E01: printed keys and vector disagree in 33s mode"),
    ("GTO . with one dot: the prompt left waiting", "lesson.md", "```keys S07 after=S06\nGOLD GTO . .\n",
     "```keys S07 after=S06\nGOLD GTO .\n", {}, "S07: printed keys and vector disagree in 33s mode"),
]
# The entry axis (decision 63), proven on the first lesson to offer entries.
CONTROLS_FOR["frac-01-equivalent-fractions"] = [
    ("algebraic entry offered in the 33s and 35s modes, which refuse ALG", "lesson.md", "modes: STU\n", "", {},
     "algebraic entry is STU mode's alone"),
    ("the entry pressed after the display setting, not right after the mode", "lesson.md",
     "setup: BLUE MODE {mode} BLUE MODE {entry} GOLD DISP FIX 4 BLUE →FRAC",
     "setup: BLUE MODE {mode} GOLD DISP FIX 4 BLUE MODE {entry} BLUE →FRAC", {},
     "the setup must press the entry right after the mode"),
    ("a lesson offering entries whose setup presses none", "lesson.md",
     "setup: BLUE MODE {mode} BLUE MODE {entry} GOLD DISP FIX 4 BLUE →FRAC",
     "setup: BLUE MODE {mode} GOLD DISP FIX 4 BLUE →FRAC", {}, "as {entry}, once"),
    ("an entry the core has not", "lesson.md", "entries: alg rpn\n", "entries: alg rpn tex\n", {},
     "give some of rpn alg"),
    ("an algebraic result expected in X (the line leaves the stack alone)", "vectors.txt",
     "ENTER | N=0.5 %LINE=2÷4", "ENTER | X=0.5 %LINE=2÷4", {}, "vectors in STU alg mode"),
    ("RPN keys printed in the algebraic block", "lesson.md", "```keys Q03 entry=alg\n6 ÷ 8 ENTER\n",
     "```keys Q03 entry=alg\n6 ENTER 8 ÷\n", {}, "Q03: printed keys and vector disagree in STU alg mode"),
    ("algebraic keys printed in the RPN block", "lesson.md", "```keys Q05 entry=rpn\n8 ENTER 37 ×\n",
     "```keys Q05 entry=rpn\n8 × 37 ENTER\n", {}, "Q05: printed keys and vector disagree in STU rpn mode"),
    ("the typed line misquoted", "lesson.md", 'kind="line">2÷4<', 'kind="line">2/4<', {},
     "the prose '2/4' (line) (STU alg)"),
    ("the line's sentence left in the RPN reading, which has no line",
     [("lesson.md", '<entry e="alg">The line you typed', "The line you typed"),
      ("lesson.md", '>2÷4</disp>.</entry>', '>2÷4</disp>.')], None, None, {},
     "the prose '2÷4' (line) (STU rpn)"),
    ("an RPN vector missing: the RPN block shows nothing", "vectors.txt", "Q04@rpn |", "Q04@35s |", {},
     "keys block Q04 names no vector in STU rpn mode"),
    ("two algebraic variants of one block", "lesson.md", "```keys Q05 entry=rpn", "```keys Q05 entry=alg", {},
     "2 variants for STU alg"),
    ("a keys variant naming no entry", "lesson.md", "```keys E01 entry=rpn", "```keys E01 entry=rnp", {},
     "not one of rpn alg"),
    ("an <entry> span naming no entry", "lesson.md", '<entry e="rpn">In RPN', '<entry e="RPN">In RPN', {},
     "RPN is not one of rpn alg"),
    ("fraction display left out of the setup: the student sees decimals", "lesson.md",
     "setup: BLUE MODE {mode} BLUE MODE {entry} GOLD DISP FIX 4 BLUE →FRAC\n",
     "setup: BLUE MODE {mode} BLUE MODE {entry} GOLD DISP FIX 4\n", {},
     "printed keys and vector disagree in STU alg mode"),
]
CONTROLS_FOR["start-01-the-calculator"] = [
    ("the setup printed without its entry", "lesson.md", "```keys setup\nBLUE MODE {mode} BLUE MODE {entry} GOLD DISP FIX 4\n",
     "```keys setup\nBLUE MODE {mode} GOLD DISP FIX 4\n", {}, "the setup block"),
    ("an answer quoted without FIX 4's digits", "lesson.md", '<disp v="C01">12.0000<', '<disp v="C01">12<', {},
     "D-C01: the prose shows '12'"),
    ("ANS's line misquoted", "lesson.md", 'kind="line">ANS×2<', 'kind="line">2×ANS<', {},
     "the prose '2×ANS' (line) (STU alg)"),
    ("LASTx printed without its shift", "lesson.md", "100 − GOLD LASTx ENTER", "100 − LASTx ENTER", {},
     "C03: printed keys and vector disagree in STU alg mode: KEY"),
    ("the RPN subtraction without x↔y (24 − 100)", "lesson.md", "100 x↔y −\n", "100 −\n", {},
     "C03: printed keys and vector disagree in STU rpn mode"),
    ("fraction display turned on as a fresh example, not carrying on", "lesson.md", "```keys F02 after=F01\n",
     "```keys F02\n", {}, "F02: printed keys and vector disagree"),
    ("the arrow quoted the wrong way", "lesson.md", 'kind="status">▼<', 'kind="status">▲<', {},
     "F03: the status band shows"),
    ("exercise 2 without fraction display turned on", "lesson.md", "BLUE →FRAC 9 ÷ 4 ENTER\n", "9 ÷ 4 ENTER\n", {},
     "E02: printed keys and vector disagree in STU alg mode"),
]
CONTROLS_FOR["der-01-the-derivative"] = [
    ("d(a) in program V not doubled", "lesson.md", "RCL A GOLD x² 2 × − RCL H", "RCL A GOLD x² − RCL H", {},
     "V01A: printed keys and vector disagree in 33s mode"),
    ("the speed at t = 3 quoted as exactly 12", "lesson.md", '<disp v="D01">12.0020<', '<disp v="D01">12.0000<', {},
     "D-D01: the prose shows '12.0000'"),
    ("h from below keyed with − instead of +/−", "lesson.md", "```keys D02 after=D01\n0.001 +/− XEQ V\n",
     "```keys D02 after=D01\n0.001 − XEQ V\n", {}, "D02: printed keys and vector disagree in 33s mode"),
    ("D/DX answered with X, not the equation's T", "lesson.md", "CAS D/DX T\n", "CAS D/DX X\n", {},
     "B01: printed keys and vector disagree in STU mode"),
    ("Casimir's result misquoted", "lesson.md", 'kind="eqn">4×T<', 'kind="eqn">4T<', {},
     "B01: the device's X line shows '4×T' (eqn)"),
    ("Equation mode left on before exercise 3", "lesson.md", "   ```keys E02C after=E02B mode=STU\n   GOLD EQN\n   ```\n", "", {},
     "E03: working through in order"),
]
CONTROLS_FOR["der-02-the-power-rule"] = [
    ("the cube's x↔y left out (4 x 2.001^3 taken)", "lesson.md", "2.001 ENTER ENTER 3 yˣ x↔y 4 ×", "2.001 ENTER ENTER 3 yˣ 4 ×", {},
     "P01: printed keys and vector disagree in 33s mode"),
    ("an average quoted as the exact 8", "lesson.md", '<disp v="P01">8.0060<', '<disp v="P01">8.0000<', {},
     "D-P01: the prose shows '8.0000'"),
    ("Casimir's 3x² − 4 misquoted", "lesson.md", 'kind="eqn">3×X^2-4<', 'kind="eqn">3X^2-4<', {},
     "B01: the device's X line shows '3×X^2-4' (eqn)"),
    ("1/x's average with + for −", "lesson.md", "2.001 1/x 0.5 − 0.001 ÷", "2.001 1/x 0.5 + 0.001 ÷", {},
     "R01: printed keys and vector disagree in 33s mode"),
    ("exercise 2 with no ENTER: 1.001 squared in the typing", "lesson.md", "1.001 ENTER GOLD x²", "1.001 GOLD x²", {},
     "E02: printed keys and vector disagree in 33s mode"),
    ("Equation mode left on after D/DX of 1/x", "lesson.md", "```keys R03 after=R02 mode=STU\nGOLD EQN\n```\n", "", {},
     "E01: working through in order"),
]
CONTROLS_FOR["der-03-using-the-derivative"] = [
    ("the tangent's value quoted as the curve's", "lesson.md", '<disp v="T02">0.2000<', '<disp v="T02">0.2100<', {},
     "D-T02: the prose shows '0.2100'"),
    ("SOLVE answered with the wrong variable", "lesson.md", "4 ENTER GOLD SOLVE X\n", "4 ENTER GOLD SOLVE Y\n", {},
     "S01: printed keys and vector disagree in 33s mode"),
    ("f(−1) keyed as f(1): the +/− left out", "lesson.md", "```keys C01\n1 +/− ENTER ENTER", "```keys C01\n1 ENTER ENTER", {},
     "C01: printed keys and vector disagree in 33s mode"),
    ("EXTR's readout misquoted", "lesson.md", 'kind="readout">EXTRM: 2.0000<', 'kind="readout">EXTRM: 1.9999<', {},
     "G03: the graph's readout shows 'EXTRM: 2.0000'"),
    ("TANL pressed without its gold shift", "lesson.md", "```keys G05 after=G04 mode=STU\nGOLD TANL\n", "```keys G05 after=G04 mode=STU\nTANL\n", {},
     "G05: printed keys and vector disagree in STU mode"),
    ("the trace left at x = 2: EXTR has nothing to find", "lesson.md", "BLUE GRAPH GO 6 6 6 6 6\n", "BLUE GRAPH GO\n", {},
     "G02: printed keys and vector disagree in STU mode"),
    ("the graph left open before the exercises", "lesson.md", "```keys G06 after=G05 mode=STU\nC\n```\n", "", {},
     "E01: working through in order"),
    # Items (decision 67): the checkpoint's rules.
    ("a slip that is the answer itself", "lesson.md", "slip: K01A | the −2x term dropped", "slip: K01 | the −2x term dropped", {},
     "item K01: slip K01 (the −2x term dropped) gives the answer itself"),
    ("a slip that names no vector", "lesson.md", "slip: K02B |", "slip: K02Z |", {},
     "item K02: slip K02Z names no vector"),
    ("a worked item's keys that make another number", "lesson.md", "keys: 3 ENTER GOLD x² x↔y 6 × − 10 +",
     "keys: 3 ENTER GOLD x² x↔y 6 × + 10 +", {}, "item K03: its keys and vector disagree"),
    ("a worked item with no working", "lesson.md", "keys: 3 ENTER GOLD x² x↔y 6 × − 10 +\n", "", {},
     "item K03: answer: work needs the working"),
    ("an item with no answer: line", "lesson.md", "answer: type\ncalculator: no\nslip: K02A", "calculator: no\nslip: K02A", {},
     "item K02: no answer:"),
    ("an item's answer quoted before it asks", "lesson.md", "## Checkpoint\n", "## Checkpoint\n\nX shows <disp v=\"K01\">10.0000</disp>.\n", {},
     "item K01: K01 is shown before the item asks it"),
]
CONTROLS_FOR["algebra-to-calculus"] = [    # placement/algebra-to-calculus (graph.py --selftest plants the course rules)
    ("a placement item with no places:", "lesson.md", "calculator: no\nplaces: 2\n```\n\n```item U2B", "calculator: no\n```\n\n```item U2B", {},
     "item U2A: a placement item needs places:"),
    ("a wrong answer", "vectors.txt", "MODE33 FIX4 19 | X=19", "MODE33 FIX4 19 | X=18", {}, "vectors in 33s mode"),
]
CONTROLS_FOR["whole-01-adding-and-subtracting"] = [
    ("a carry dropped in the quoted sum", "lesson.md", '<disp v="A01">5,331.0000<', '<disp v="A01">5,231.0000<', {},
     "D-A01: the prose shows '5,231.0000'"),
    ("a quote without the device's comma", "lesson.md", '<disp v="A03">4,331.0000<', '<disp v="A03">4331.0000<', {},
     "D-A03: the prose shows '4331.0000'"),
    ("RPN's subtraction in the wrong order", "lesson.md", "```keys A02 entry=rpn\n5000 ENTER 2768 −\n",
     "```keys A02 entry=rpn\n2768 ENTER 5000 −\n", {}, "A02: printed keys and vector disagree in STU rpn mode"),
    ("the algebraic line added where it should take away", "lesson.md", "```keys A02 entry=alg\n5000 − 2768 ENTER\n",
     "```keys A02 entry=alg\n5000 + 2768 ENTER\n", {}, "A02: printed keys and vector disagree in STU alg mode"),
]
CONTROLS_FOR["whole-02-multiplying-and-dividing"] = [
    ("INT÷ pressed without its gold shift", "lesson.md", "```keys D02 entry=alg\nGOLD INT÷ 59", "```keys D02 entry=alg\nINT÷ 59", {},
     "D02: printed keys and vector disagree in STU alg mode"),
    ("RPN's Rmdr with the divisor first", "lesson.md", "```keys D03 entry=rpn\n59 ENTER 9 BLUE Rmdr\n",
     "```keys D03 entry=rpn\n9 ENTER 59 BLUE Rmdr\n", {}, "D03: printed keys and vector disagree in STU rpn mode"),
    ("the comma left out of RMDR(1000,7)", "lesson.md", "BLUE Rmdr 1000 GOLD , 7 ▶ ENTER", "BLUE Rmdr 1000 7 ▶ ENTER", {},
     "D05: printed keys and vector disagree in STU alg mode"),
    ("the remainder misquoted", "lesson.md", '<disp v="D03">5.0000<', '<disp v="D03">4.0000<', {},
     "D-D03: the prose shows '4.0000'"),
]
CONTROLS_FOR["expr-01-letters-for-numbers"] = [
    ("the number typed where RCL X should be", "lesson.md", "```keys V02 entry=alg after=V01\n3 × RCL N + 5 ENTER\n",
     "```keys V02 entry=alg after=V01\n3 × 4 + 5 ENTER\n", {}, "V02: printed keys and vector disagree in STU alg mode"),
    ("the number stored under the wrong letter", "lesson.md", "```keys V01\n4 STO N\n", "```keys V01\n4 STO A\n", {},
     "V01: printed keys and vector disagree"),
    ("the line quoted without its ×", "lesson.md", 'kind="line">3×N+5<', 'kind="line">3N+5<', {},
     "the prose '3N+5' (line) (STU alg)"),
    ("RPN adding before it multiplies", "lesson.md", "```keys V02 entry=rpn after=V01\n3 ENTER RCL N × 5 +\n",
     "```keys V02 entry=rpn after=V01\n3 ENTER RCL N 5 + ×\n", {}, "V02: printed keys and vector disagree in STU rpn mode"),
]
CONTROLS_FOR["expr-02-solving-by-undoing"] = [
    ("the ×3 undone before the +5", "lesson.md", "```keys U01 entry=alg\n20 − 5 ENTER\n", "```keys U01 entry=alg\n20 ÷ 3 ENTER\n", {},
     "U01: printed keys and vector disagree in STU alg mode"),
    ("the answer misquoted", "lesson.md", '<disp v="U02">5.0000<', '<disp v="U02">6.0000<', {},
     "D-U02: the prose shows '6.0000'"),
    ("the check adding before it multiplies", "lesson.md", "```keys C01 entry=rpn\n3 ENTER 5 × 5 +\n",
     "```keys C01 entry=rpn\n3 ENTER 5 + 5 ×\n", {}, "C01: printed keys and vector disagree in STU rpn mode"),
    ("the ÷4 undone by dividing again", "lesson.md", "```keys U04 entry=alg after=U03\n× 4 ENTER\n",
     "```keys U04 entry=alg after=U03\n÷ 4 ENTER\n", {}, "U04: printed keys and vector disagree in STU alg mode"),
]
CONTROLS_FOR["rpn-03-the-display"].append(
    ("an example that relies on a setting the one before it changed", "lesson.md",
     "```keys P01\nGOLD DISP FIX 4 2 ENTER 3 ÷\n", "```keys P01\n2 ENTER 3 ÷\n", {},
     "P01: working through in order"))
GREENS_FOR = {
    "frac-01-equivalent-fractions": [
        ("a block's RPN variant written before its algebraic one", "lesson.md",
         "```keys Q02 entry=alg\n1 ÷ 2 ENTER\n```\n\n```keys Q02 entry=rpn\n1 ENTER 2 ÷\n```\n",
         "```keys Q02 entry=rpn\n1 ENTER 2 ÷\n```\n\n```keys Q02 entry=alg\n1 ÷ 2 ENTER\n```\n"),
    ],
    "num-02-fractions": [
        ("an input written in the display's form, in a sentence about no screen", "lesson.md",
         "## Typing a fraction\n", "## Typing a fraction\n\nA board 0.3750 inches thick is typed as .3.8.\n"),
    ],
    "rpn-03-the-display": [
        ("an input written in the display's form, in a sentence about no screen", "lesson.md",
         "## ALL: no padding\n", "## ALL: no padding\n\nA rate of 0.0825 is typed as it is written.\n"),
    ],
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
    # The lists above are anchored on rpn-01's text; another lesson gets only its own, never a
    # silent borrow of rpn-01's (which would fail as "did not apply" and prove nothing).
    name = os.path.basename(lesson)
    controls = CONTROLS if name == "rpn-01-the-stack" else CONTROLS_FOR.get(name)
    greens = GREENS if name == "rpn-01-the-stack" else GREENS_FOR.get(name, [])
    if not controls:
        print(f"FAIL no controls are defined for {name}")
        return 1
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
