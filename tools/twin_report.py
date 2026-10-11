#!/usr/bin/env python3
"""twin_report.py: a unit's twins beside every problem in the unit, by operands (abacus #7317), so the clearance can
be seen as well as trusted. For each twin: the example it twins, its operands, and the example's; then every item and
exercise of the unit with its operands. check.py refuses a twin whose operands equal any of these.

    tools/twin_report.py COURSE:UNIT ...      (e.g. pre-algebra:1)
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check  # noqa: E402
import maths_convert as mc  # noqa: E402


def fmt(ops):
    return "[" + ", ".join(str(x) for x in ops) + "]"


def main():
    for arg in sys.argv[1:]:
        paths = mc.course_lessons(arg)
        print(f"== {arg}")
        problems = None
        for p in paths:
            d = os.path.dirname(p)
            meta, body = check.front_matter(open(p, encoding="utf-8").read())
            if problems is None:
                problems = check.unit_problems(d, meta.get("id", ""))
            voices = check.lesson_voices(meta)[0]
            body = check.maths_read(body if voices == [None] else check.voice_view(body, voices[0]))
            blocks = {m.group(2): m for m in check.KEYS_ANY.finditer(body)}
            vec = os.path.join(d, "vectors.txt")
            vt = open(vec, encoding="utf-8").read() if os.path.exists(vec) else ""
            for m in check.KEYS_ANY.finditer(body):
                a = dict(re.findall(r"([a-z]+)=(\S+)", m.group(3)))
                if "twin" in a and a.get("entry", "rpn") == "rpn":
                    ex = blocks.get(a["twin"])
                    print(f"  twin {meta['id']} {m.group(2)} (keys, twins {a['twin']}): {fmt(check.operands(m.group(4)))}"
                          f"  answer {check.item_answer(vt, m.group(2))}  example {fmt(check.operands(ex.group(4)) if ex else [])}")
                if "fade" in a:
                    print(f"  fade {meta['id']} {m.group(2)}: last {a['fade']} keystrokes of '{' '.join(m.group(4).split())}'")
            for m in check.ITEM_BLOCK.finditer(body):
                f = dict(re.findall(r"^[ \t]*(\w+):[ \t]*(.*)$", m.group(2), re.M))
                if "twin" in f:
                    ex = blocks.get(f["twin"])
                    print(f"  twin {meta['id']} {m.group(1)} (item, twins {f['twin']}): "
                          f"{fmt(check.problem_operands(f.get('prompt', '')))}  answer {check.item_answer(vt, m.group(1))}  "
                          f"example {fmt(check.operands(ex.group(4)) if ex else [])}")
        print("  the unit's problems (a twin may equal none of these):")
        for label, ops, ans in problems or []:
            print(f"    {label:22} {fmt(ops)}  answer {ans if ans is not None else '?'}")


if __name__ == "__main__":
    main()
