#!/usr/bin/env python3
"""records.py FILE.jsonl ...: checks problem records (abacus #5698, #5737), one JSON object per line.

A problem record is a problem from a book, with the book's printed answer, and the same answer worked by the STU-32's
core (through stu32-calc) and by mpmath (outside the image). This checks each record's fields, recomputes its verdict
from its three values, and refuses a record whose written verdict differs. Exit 1 if any record is refused.

THE COMPARISON RULES (pinned by abacus, #5737):
  printed against core   at the book's printed precision: the core's value is rounded to the printed digits (2.718 in
                         the book matches e at 3 decimals; half up or half even, which differ only on a tie). A
                         printed fraction compares exactly: the core must hold the fraction's own value, correctly
                         rounded to its 34 digits.
  core against mpmath    a relative difference of at most 1E-30, or the same exact value where both are exact. The core
                         is correctly rounded at 34 digits, so a larger difference is the core's or the record's fault.
THE VERDICT follows from those two comparisons and nothing else:
  OK        printed = core and core = mpmath
  CALC      core != mpmath, whatever the book says: a calculator bug or a wrong record; it goes to abacus and soroban
  FLAGGED   printed != core = mpmath: our extraction error or the book's erratum. A person decides which, and writes
            "resolution": {"cause": "extraction" | "erratum", "by": ..., "note": ...}. It is never dropped.
THE KEYS ARE THE PROBLEM'S OWN WORKING (abacus #5513, held for lessons; #pd-books #5962): every number the keys type
comes from the problem (its text, problem_latex, problem_expr(s), values) or from how.constants, each with its source
(a number from the working, such as the 1 in (1 + ln 3)/3, is a constant whose source names the step); and the printed
answer is never typed as a literal unless it is itself a given. Keys that type the answer reproduce it and prove
nothing, so such a record is refused, whatever its verdict.
WHAT THIS CANNOT CATCH: the mpmath expression is written separately from the STU-32 keys, but by the same extractor,
reading the same problem. A misreading of the problem can therefore hide in both, and the two will agree with each
other and with nothing in the book. That is what FLAGGED and the human spot-check against a printed copy are for:
agreement between the core and mpmath shows the calculation, not the reading.

A RECORD (fields; "?" optional):
  id                     unique in the file
  book                   {title, author, edition, year, source}: the edition read from the copy itself
  page                   the page (or section) the problem is on
  problem                the problem's text, as the quote gate passed it
  printed_answer         the book's answer, verbatim
  printed_value          {kind: integer | decimal | fraction | symbolic, text}: the answer as a value; for a fraction
                         "p/q" or "a b/c"; for symbolic, in Casimir's notation
  how                    {kind: keys, mode, entry?, angle?, fix?, steps: [...], constants?: [{value, source}]} or
                         {kind: casim, op, args: [...]}
  problem_latex?, problem_expr?, problem_exprs?, values?
                         the problem as printed (LaTeX), as SymPy, and its givens ({symbol: value as printed}): the
                         numbers the keys may type, beside the problem's text
  core                   {status: "OK", value, display?, pins}: stu32-calc's answer. value is exact text (the stack's
                         X, or Casimir's text); pins as the call returned them
  core.equiv?            symbolic only: {op: "simplify", text: "(printed)-(core)", result}: Casimir's own check that
                         the printed answer and its own are the same expression; "0" when they are
  mpmath                 {version, dps >= 40, expression, value} for a number; for symbolic, {version, dps,
                         expression, samples: [{at: {X: ...}, expected, core}]}: expected is the problem's own
                         mathematics evaluated by mpmath (for a derivative, mpmath.diff), core is the core's expression
                         evaluated at the same point
  verdict                OK | CALC | FLAGGED
  resolution?            for FLAGGED, as above
"""
import json
import re
import sys
from decimal import ROUND_HALF_EVEN, ROUND_HALF_UP, Context, Decimal, InvalidOperation
from fractions import Fraction

REL = Decimal("1E-30")
CORE = Context(prec=34, rounding=ROUND_HALF_EVEN)
KINDS = ("integer", "decimal", "fraction", "symbolic")
VERDICTS = ("OK", "CALC", "FLAGGED")


def num(text):
    """A number as the core or mpmath writes it ("+5331E+0", "2.718281828...", "-1.5"), or None."""
    try:
        d = Decimal(str(text).strip())
    except InvalidOperation:
        return None
    return d if d.is_finite() else None


def fraction_of(text):
    """ "p/q", "-p/q" or a mixed "a b/c" as a Fraction, or None."""
    t = text.strip().replace("−", "-")
    try:
        if " " in t:
            whole, part = t.split(None, 1)
            f = Fraction(part)
            w = int(whole)
            return w - f if w < 0 or whole.startswith("-") else w + f
        return Fraction(t)
    except (ValueError, ZeroDivisionError):
        return None


def close(a, b):
    """core against mpmath: the same value, or within a relative 1E-30."""
    if a == b:
        return True
    scale = max(abs(a), abs(b))
    return abs(a - b) <= REL * scale


def printed_matches(pv, core_value):
    kind, text = pv["kind"], pv["text"]
    c = num(core_value)
    if c is None:
        return False, f"the core's value {core_value!r} is not a number"
    if kind == "fraction":
        f = fraction_of(text)
        if f is None:
            return False, f"{text!r} is not a fraction"
        want = CORE.divide(Decimal(f.numerator), Decimal(f.denominator))
        return CORE.plus(c) == want, f"the fraction {text} is {want} at 34 digits; the core holds {c}"
    p = num(text.replace("−", "-").replace(",", ""))
    if p is None:
        return False, f"{text!r} is not a number"
    q = Decimal(1).scaleb(p.as_tuple().exponent)
    ups, evens = c.quantize(q, ROUND_HALF_UP), c.quantize(q, ROUND_HALF_EVEN)
    return p in (ups, evens), f"the core rounded to the printed digits is {evens}" + \
        ("" if ups == evens else f" (half up {ups})")


NUMBER = re.compile(r"\d*\.?\d+")
SETTING = {"FIX", "SCI", "ENG", "ALL"}      # the number after one of these is a display setting, not a value


def numbers_in(text):
    """The numbers written in a text, as Decimals (4.50 and 4.5 are one number)."""
    out = set()
    for m in NUMBER.findall(str(text)):
        try:
            out.add(Decimal(m).normalize())
        except InvalidOperation:
            pass
    return out


def keyed_numbers(steps):
    """(number, step) for each number typed in the steps: a token of digits and points ("4.5", ".5", "2.3.8",
    a 33s fraction, gives each part), the number after FIX, SCI, ENG or ALL left out."""
    out = []
    for step in steps:
        toks = step.split("\t")[-1].split()
        for i, tok in enumerate(toks):
            if i and toks[i - 1] in SETTING:
                continue
            if re.fullmatch(r"[\d.]+", tok) and any(c.isdigit() for c in tok):
                parts = tok.split(".") if tok.count(".") > 1 else [tok]
                out += [(Decimal(p).normalize(), step) for p in parts if p]
    return out


def own_working(rec):
    """The keys must be the problem's own working (abacus #5513, for lessons; #pd-books #5962): every number keyed
    comes from the problem (its text, problem_latex, problem_expr(s), values) or from how.constants, each with its
    source; and the printed answer is never keyed as a literal, unless it is itself a given."""
    bad = []
    givens = numbers_in(rec.get("problem", "")) | numbers_in(rec.get("problem_latex", ""))
    for f in ("problem_expr", "problem_exprs"):
        givens |= numbers_in(json.dumps(rec.get(f, "")))
    givens |= numbers_in(json.dumps(rec.get("values", {})))
    consts = rec["how"].get("constants", [])
    for c in consts:
        if not str(c.get("source", "")).strip():
            bad.append(f"how.constants: {c.get('value')!r} has no source")
    allowed = givens | {n for c in consts for n in numbers_in(c.get("value", ""))}
    answer = numbers_in(rec["printed_value"].get("text", "")) if rec["printed_value"].get("kind") != "symbolic" else set()
    for n, step in keyed_numbers(rec["how"].get("steps", [])):
        if n in answer and n not in givens:
            bad.append(f"keys type the printed answer's {n} ({step!r}): the keys must work it, not type it")
        elif n not in allowed:
            bad.append(f"keys type {n} ({step!r}), which is not in the problem: give it in how.constants with its "
                       f"source, or work it")
    return bad


def check(rec, seen):
    """(problems, the verdict the values give)."""
    bad = []
    for f in ("id", "book", "page", "problem", "printed_answer", "printed_value", "how", "core", "mpmath", "verdict"):
        if f not in rec:
            bad.append(f"no {f}")
    if bad:
        return bad, None
    if rec["id"] in seen:
        bad.append(f"id {rec['id']} appears twice")
    seen.add(rec["id"])
    for f in ("title", "author", "edition", "year", "source"):
        if not str(rec["book"].get(f, "")).strip():
            bad.append(f"book has no {f}")
    pv, core, mp = rec["printed_value"], rec["core"], rec["mpmath"]
    if pv.get("kind") not in KINDS:
        bad.append(f"printed_value.kind is one of {' '.join(KINDS)}")
    if rec["how"].get("kind") not in ("keys", "casim"):
        bad.append("how.kind is keys or casim")
    if core.get("status") != "OK":
        bad.append(f"core.status is {core.get('status')!r}: a record is made from a call that ran (fix the keys first)")
    if not core.get("pins", {}).get("firmware"):
        bad.append("core.pins has no firmware: say which core checked it")
    if rec["verdict"] not in VERDICTS:
        bad.append(f"verdict is one of {' '.join(VERDICTS)}")
    if not str(mp.get("expression", "")).strip():
        bad.append("mpmath.expression is empty: mpmath works the problem itself, not the core's value")
    if not str(mp.get("version", "")).strip():
        bad.append("mpmath.version is empty")
    if not isinstance(mp.get("dps"), int) or mp["dps"] < 40:
        bad.append("mpmath.dps is below 40")
    if rec["how"].get("kind") == "keys":
        bad += own_working(rec)
    if bad:
        return bad, None

    if pv["kind"] == "symbolic":
        eq = core.get("equiv") or {}
        if eq.get("op") != "simplify" or "result" not in eq:
            return [f"symbolic: core.equiv is Casimir's simplify of (printed)-(core)"], None
        printed_ok, why_p = eq["result"].strip() == "0", f"simplify of the difference gives {eq['result']!r}"
        samples = mp.get("samples") or []
        if len(samples) < 3:
            return ["symbolic: mpmath.samples needs at least 3 points"], None
        core_ok, why_c = True, ""
        for s in samples:
            e, c = num(s.get("expected")), num(s.get("core"))
            if e is None or c is None:
                return [f"symbolic: a sample without numbers: {s}"], None
            if not close(c, e):
                core_ok, why_c = False, f"at {s.get('at')} mpmath gives {e}, the core's expression {c}"
                break
    else:
        m, c = num(mp.get("value")), num(core.get("value"))
        if m is None:
            return [f"mpmath.value {mp.get('value')!r} is not a number"], None
        if c is None:
            return [f"core.value {core.get('value')!r} is not a number"], None
        if str(mp.get("value")).strip() == str(core.get("value")).strip() and len(str(c.normalize())) > 20:
            bad.append("mpmath.value is the core's text character for character, a long value: worked, or copied?")
        core_ok, why_c = close(c, m), f"core {c}, mpmath {m}"
        printed_ok, why_p = printed_matches(pv, core["value"])
    verdict = "CALC" if not core_ok else "OK" if printed_ok else "FLAGGED"
    if verdict != rec["verdict"]:
        bad.append(f"the values give {verdict}, the record says {rec['verdict']} ({why_c}; {why_p})")
    if verdict == "FLAGGED" and "resolution" in rec:
        r = rec["resolution"]
        if r.get("cause") not in ("extraction", "erratum") or not r.get("by"):
            bad.append("resolution needs cause extraction or erratum, and by whom")
    return bad, verdict


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    refused = total = 0
    counts = {v: 0 for v in VERDICTS}
    for path in sys.argv[1:]:
        seen = set()
        with open(path, encoding="utf-8") as f:
            for n, line in enumerate(f, 1):
                if not line.strip():
                    continue
                total += 1
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError as e:
                    print(f"REFUSED {path}:{n}: not JSON ({e})")
                    refused += 1
                    continue
                bad, verdict = check(rec, seen)
                rid = rec.get("id", f"line {n}")
                if bad:
                    refused += 1
                    for b in bad:
                        print(f"REFUSED {path}:{n} {rid}: {b}")
                else:
                    counts[verdict] += 1
                    open_flag = verdict == "FLAGGED" and "resolution" not in rec
                    print(f"{verdict:8} {rid}" + ("  (awaiting a person's resolution)" if open_flag else ""))
    print(f"{total} records: " + ", ".join(f"{counts[v]} {v}" for v in VERDICTS) + f", {refused} refused")
    return 1 if refused else 0


if __name__ == "__main__":
    sys.exit(main())
