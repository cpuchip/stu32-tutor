#!/usr/bin/env python3
"""check.py: every lesson's examples, run on the pinned core. The rules are docs/lesson-format.md.

    tools/check.py --core build/core-PIN lessons/*/

For each lesson:
  1. vectors.txt runs on the firmware's vector runner in 33s mode as written and with its MODE33
     made MODE35 (unless the front matter limits `modes:` with a `modes_reason:`), each from a
     fresh core and from a used one (DIRTY: the stack full, LAST x set, RAD), and must pass in all.
  2. fmt-vectors.txt runs on the firmware's display runner.
  3. The ```keys setup``` block is the front matter's setup. Every other ```keys ID``` block, after
     the setup, is pressed on the device's key layer (keyrun) in each mode, and must issue the same
     ops as vector ID, leave the same core state, and leave the device at rest. Every vector is
     shown by at least one block.
  4. Every <disp v="ID">text</disp> sits after block ID and before the next block, is the text the
     device's screen shows on X after those keys (a value, not an entry or a message), and is the
     text of display vector D-ID at the setting the vectors set, of vector ID's exact X result.
  5. No em-dash anywhere in lesson.md, as a character or an entity.
  6. A student working through: the setup once, then every block in order on one device with
     nothing reset (a continuation, ```keys ID after=PREV```, presses only its own keys); every
     exact X, Y, Z, T and every quoted display must hold for that student too.
A file with no vectors, or a vector with no expectation, fails: a check that checks nothing is
not a pass.
"""
import argparse
import os
import re
import subprocess
import sys
import tempfile
from decimal import Decimal, InvalidOperation

sys.stdout.reconfigure(encoding="utf-8")

SETTING = re.compile(r"^(FIX|SCI|ENG)(\d+)$|^ALL$")
DISP = re.compile(r'<disp v="([^"]+)"(?: kind="(view|prompt|message|entry|status|eqn)")?>(.*?)</disp>', re.S)
FRAC_SETTINGS = {"/C", "SF:7", "CF:7", "SF:8", "CF:8", "SF:9", "CF:9"}  # change the fraction display
# ```keys ID``` or ```keys ID after=PREV```: a continuation holds only the keys pressed after block
# PREV, which must be the block just before it; its full keys are PREV's full keys and then its own.
KEYS_BLOCK = re.compile(r"^[ \t]*```keys[ \t]+([^\s=]+)(?:[ \t]+after=(\S+))?[ \t]*\n(.*?)^[ \t]*```[ \t]*$", re.M | re.S)
SHOWS = re.compile(r"\b(shows?|showed|showing|shown|displays?|displayed|screen|reads|appears?)\b", re.I)
FENCE = re.compile(r"^[ \t]*(```|~~~)(.*)$", re.M)
# A used calculator: every variable A-Z holds 7, RAD, the stack full, lift enabled, LAST x 6.
DIRTY = " ".join(["RAD"] + [f"7 STO:{v}" for v in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"] + "9 ENTER 8 ENTER 7 ENTER 6 SQRT".split())
DEVICE_WIDTH = "w=21"                           # the X line's width on the device (screen.c FMT_WIDTH)
MAX_EXPECT = 64                                # the runner keeps no more than this per vector
EM_DASH = ("\u2014", "&mdash;", "&#8212;", "&#x2014;", "&#X2014;")


def front_matter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}, text
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta, text[m.end():]


def read_vectors(path, nfields):
    """(id, fields, line) for each vector line; comments and blanks skipped."""
    out = []
    with open(path, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            s = line.rstrip("\n")
            if not s.strip() or s.lstrip().startswith("#"):
                continue
            parts = [p.strip() for p in s.split("|")]
            if len(parts) != nfields:
                raise ValueError(f"{path}:{n}: {len(parts)} fields, expected {nfields}")
            out.append((parts[0], parts, s))
    return out


def variant(parts, mode, dirty):
    """A vector line in a mode (33 or 35), from a fresh or a used core."""
    toks = parts[2].split()
    toks[0] = f"MODE{mode}"
    if dirty:
        toks = DIRTY.split() + toks
    return " | ".join(parts[:2] + [" ".join(toks)] + parts[3:])


class Lesson:
    def __init__(self, d, core):
        self.d = d.rstrip("/")
        self.name = os.path.basename(self.d)
        self.core = core
        self.fail = []
        self.notes = []

    def bad(self, msg):
        self.fail.append(msg)

    def run(self, *cmd, env=None):
        e = dict(os.environ)
        e.update(env or {})
        return subprocess.run(cmd, capture_output=True, text=True, env=e, encoding="utf-8")

    def run_vectors(self, lines, env=None):
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as t:
            t.write("\n".join(lines) + "\n")
        try:
            return self.run(f"{self.core}/build/vectors", t.name, env=env)
        finally:
            os.unlink(t.name)

    def check(self):
        lesson_md = os.path.join(self.d, "lesson.md")
        vec_path = os.path.join(self.d, "vectors.txt")
        fmt_path = os.path.join(self.d, "fmt-vectors.txt")
        for p in (lesson_md, vec_path):
            if not os.path.exists(p):
                self.bad(f"missing {p}")
        if self.fail:
            return
        text = open(lesson_md, encoding="utf-8").read()
        meta, body = front_matter(text)
        vectors = read_vectors(vec_path, 4)
        fmts = read_vectors(fmt_path, 6) if os.path.exists(fmt_path) else []

        # A check that checks nothing is not a pass.
        if not vectors:
            self.bad("vectors.txt has no vectors")
        ids = [v[0] for v in vectors]
        for dup in sorted({i for i in ids if ids.count(i) > 1}):
            self.bad(f"vector {dup} appears more than once")
        settings = set()
        for vid, parts, _ in vectors:
            exps = parts[3].split()
            if not exps:
                self.bad(f"{vid}: no expectation")
            if len(exps) > MAX_EXPECT:
                self.bad(f"{vid}: {len(exps)} expectations; the runner keeps {MAX_EXPECT}")
            toks = parts[2].split()
            # Every vector sets its mode and its display, so nothing depends on how the core began.
            if len(toks) < 2 or toks[0] != "MODE33" or not SETTING.match(toks[1]):
                self.bad(f"{vid}: keys must begin MODE33 and a display setting (FIXn, SCIn, ENGn, ALL)")
                continue
            settings.add(toks[1])
            if any(t.startswith("MODE") for t in toks[1:]):
                self.bad(f"{vid}: the mode is set only by the first key")
        if self.fail:
            return

        # 1. The maths, in each mode, from a fresh core and from a used one.
        modes = meta.get("modes", "33 35").split()
        if not modes or any(m not in ("33", "35") for m in modes) or len(set(modes)) != len(modes):
            self.bad(f"front matter `modes: {meta.get('modes')}`: give 33, 35 or both")
            modes = ["33", "35"]
        if modes != ["33", "35"] and not meta.get("modes_reason"):
            self.bad("front matter limits `modes` without a `modes_reason`")
        for mode in modes:
            for dirty in (False, True):
                r = self.run_vectors([variant(v[1], mode, dirty) for v in vectors])
                where = f"{mode}s mode, {'a used' if dirty else 'a fresh'} core"
                if r.returncode != 0:
                    self.bad(f"vectors in {where}:\n{r.stdout}{r.stderr}")
                elif not dirty:
                    last = (r.stdout.strip().splitlines() or ["(no output)"])[-1]
                    self.notes.append(f"{mode}s: {last.split(': ', 1)[-1]}")
        self.notes.append("from a used core too")

        # 2. The displays.
        if fmts:
            r = self.run(f"{self.core}/build/fmt_vectors", fmt_path)
            out = r.stdout.strip().splitlines()
            if r.returncode != 0 or not out:
                self.bad(f"display vectors:\n{r.stdout}{r.stderr}")
            else:
                self.notes.append("displays: " + out[-1].split(": ", 1)[-1])

        # 3. The printed keys against the vectors, in each mode.
        for m in FENCE.finditer(body):
            line = m.group(0).strip()           # a fence may be indented (in a list item)
            if "key" in m.group(2).lower() and not re.match(r"^```keys[ \t]+[^\s=]+(?:[ \t]+after=\S+)?[ \t]*$", line):
                self.bad(f"a fence that looks like keys but is not checked: '{line}'")
        setup = " ".join(meta.get("setup", "").split())
        if not setup:
            self.bad("front matter has no `setup:` keys (the mode and the display setting, as pressed)")
        found = [(m.group(1), " ".join(m.group(3).split()), m.start(), m.end(), m.group(2))
                 for m in KEYS_BLOCK.finditer(body)]
        # blocks carry their FULL keys (from the setup); own_keys what the student presses there.
        blocks, own_keys, full = [], {}, {}
        for i, (bid, keys, s0, e0, after) in enumerate(found):
            own_keys[bid] = keys
            if after:
                prev = found[i - 1][0] if i > 0 else None
                if after != prev or prev == "setup":
                    self.bad(f"keys block {bid} continues {after}, but the block just before it is {prev}")
                    full[bid] = keys
                else:
                    full[bid] = f"{full[prev]} {keys}"
            else:
                full[bid] = keys
            blocks.append((bid, full[bid], s0, e0))
        continued = {after for (_, _, _, _, after) in found if after}
        byid = {v[0]: v for v in vectors}
        shown, screen, screen_y, status = set(), {}, {}, {}

        def line_says(xline, yline, qkind, text):
            # A prompt for a variable (INPUT's or an equation's "X?") takes the Y line (screen.h);
            # STO's "STO _" takes X. Every other kind is the X line.
            if qkind == "prompt":
                return any(k == "prompt" and t.strip() == text for k, t in (xline, yline))
            return xline[0] == qkind and xline[1].strip() == text
        for bid, keys, _, _ in blocks:
            if bid == "setup":                  # the setup as printed for the student
                if keys != setup:
                    self.bad(f"the setup block '{keys}' is not the front matter's setup '{setup}'")
                continue
            if bid not in byid:
                self.bad(f"keys block {bid} names no vector")
                continue
            shown.add(bid)
            for mode in modes:
                press = setup
                if mode == "35":
                    if setup.split().count("33s") != 1:
                        self.bad("the setup must press the 33s soft key once (the 35s run presses 35s)")
                        break
                    press = " ".join("35s" if t == "33s" else t for t in setup.split())
                fd, trace = tempfile.mkstemp(suffix=".trace")
                os.close(fd)
                r = self.run_vectors([variant(byid[bid][1], mode, False)], env={"STU_TRACE": trace})
                if r.returncode != 0:
                    os.unlink(trace)
                    self.bad(f"{bid}: vector fails alone in {mode}s mode:\n{r.stdout}")
                    continue
                # A block the next one continues may stop at a prompt the continuation answers.
                cont = {"KEYRUN_OPEN_PROMPT": "1"} if bid in continued else {}
                k = self.run(f"{self.core}/build/keyrun", f"{press} {keys}", trace, env=cont)
                os.unlink(trace)
                if k.returncode != 0:
                    self.bad(f"{bid}: printed keys and vector disagree in {mode}s mode: "
                             f"{k.stdout.strip()}{k.stderr.strip()}")
                    continue
                xl = [l.split("\t") for l in k.stdout.splitlines() if l.startswith("X\t")]
                sl = [l.split("\t", 1)[1] for l in k.stdout.splitlines() if l.startswith("STATUS\t")]
                yl = [l.split("\t") for l in k.stdout.splitlines() if l.startswith("YL\t")]
                if mode == modes[0] and xl and len(xl[0]) == 3:
                    screen[bid] = (xl[0][1], xl[0][2])
                    screen_y[bid] = (yl[0][1], yl[0][2]) if yl and len(yl[0]) == 3 else ("?", "")
                    status[bid] = sl[0].split() if sl else []
        for vid in ids:
            if vid not in shown:
                self.bad(f"vector {vid} is shown by no keys block")
        self.notes.append(f"keys: {len(blocks)} blocks, {len(shown)} of {len(ids)} vectors shown, "
                          f"in {' and '.join(m + 's' for m in modes)}")

        # 4. Quoted displays: beside their example, on the device's screen, verified by the formatter.
        fmt_by = {f[0]: f[1] for f in fmts}

        def spelled(tok):                       # FIX4 -> "FIX 4", the display vectors' form
            m = SETTING.match(tok)
            return f"{m.group(1)} {m.group(2)}" if m.group(1) else "ALL"

        # Every vector starts at the setup's setting; a lesson may change it within an example
        # (rpn-03 does), and a quoted display is judged at the setting its own example ends in.
        if len(settings) > 1:
            self.bad(f"the vectors start at {len(settings)} display settings; the setup sets one")
        want = spelled(sorted(settings)[0]) if settings else ""
        if meta.get("display") and meta["display"] != want:
            self.bad(f"front matter `display: {meta['display']}`, but the vectors set {want}")
        def final_setting(toks):
            # FDISP toggles Fraction display on and off; choosing FIX, SCI, ENG or ALL turns it off
            # (unit 007). The maximum denominator and the format are left at their defaults, so a
            # vector that changes them cannot have its display judged here.
            setting, frac = None, False
            for t in toks:
                if SETTING.match(t):
                    setting, frac = spelled(t), False
                elif t == "FDISP":
                    frac = not frac
                elif t in FRAC_SETTINGS:
                    return None
            return "FRAC 4095 P" if frac else setting

        ends_at = {v[0]: final_setting(v[1][2].split()) for v in vectors}
        quotes = list(DISP.finditer(body))
        if body.count("<disp") != len(quotes):
            self.bad(f"{body.count('<disp')} <disp tags, {len(quotes)} of the checked form <disp v=\"ID\">text</disp>")
        for q in quotes:
            vid, qkind, shown_text = q.group(1), q.group(2) or "value", q.group(3)
            before = [b for b in blocks if b[3] <= q.start() and b[0] != "setup"]
            if not before or before[-1][0] != vid:
                self.bad(f'<disp v="{vid}"> is not under its own example '
                         f'(it follows {before[-1][0] if before else "no example"})')
            if qkind == "status":
                # An annunciator (the fraction indicator, RAD, ...): a token of the status band.
                if shown_text not in status.get(vid, []):
                    self.bad(f"{vid}: the status band shows {status.get(vid, [])}, without '{shown_text}'")
                continue
            if qkind != "value":
                # A VIEW's "B=49.75" is no value the formatter's vectors cover: the device's own
                # screen line is the check, kind and text both.
                kind, stext = screen.get(vid, ("?", ""))
                if not line_says((kind, stext), screen_y.get(vid, ("?", "")), qkind, shown_text):
                    self.bad(f"{vid}: the device's X line shows '{stext}' ({kind}), the prose '{shown_text}' ({qkind})")
                continue
            f = fmt_by.get("D-" + vid)
            if not f:
                self.bad(f'<disp v="{vid}"> has no display vector D-{vid}')
                continue
            # A fraction's text may end in its accuracy indicator (" v" below, " ^" above), which the
            # device draws in the status band, not on the X line: the prose quotes the X line, and
            # the status band must carry the matching arrow, or none when the fraction is exact.
            ftext, ind = f[5], ""
            if f[3].startswith("FRAC") and ftext.endswith((" v", " ^")):
                ftext, ind = ftext[:-2], ftext[-1]
            if ftext != shown_text:
                self.bad(f"D-{vid}: the prose shows '{shown_text}', the display vector '{f[5]}'")
            if f[3].startswith("FRAC"):
                arrows = [a for a in ("▼", "▲") if a in status.get(vid, [])]
                need = {"v": ["▼"], "^": ["▲"], "": []}[ind]
                if arrows != need:
                    self.bad(f"D-{vid}: the display vector's indicator is '{ind or 'none'}', the status band has {arrows or 'none'}")
            if f[3] != ends_at.get(vid, want):
                self.bad(f"D-{vid}: display vector at '{f[3]}', vector {vid} ends at '{ends_at.get(vid, want)}'")
            # The device formats X at 21 cells (firmware/screen.c FMT_WIDTH, "ours, v0"); the display
            # runner's default is 22, which agrees for short values only. The screen-line comparison
            # below is the backstop if FMT_WIDTH changes.
            if f[4] not in ("", DEVICE_WIDTH):
                self.bad(f"D-{vid}: display options '{f[4]}'; a quoted display uses the device's ('{DEVICE_WIDTH}' or none)")
            v = byid.get(vid)
            xs = re.findall(r"(?:^|\s)X=(\S+)", v[1][3]) if v else []
            if not xs or xs[-1] != f[2]:
                self.bad(f"D-{vid}: value {f[2]} is not vector {vid}'s exact X result ({xs[-1] if xs else 'none'})")
            kind, stext = screen.get(vid, ("?", ""))
            if kind != "value" or stext.strip() != shown_text:
                self.bad(f"D-{vid}: the device's X line shows '{stext}' ({kind}), the prose '{shown_text}'")
        self.notes.append(f"displays quoted: {len(quotes)}")
        # A sentence that says what the screen shows, with a number in the display's own form
        # (FIX n places) outside a tag, is a display claim nothing checked. A number given as an
        # input ("a 7.25 item") is not a claim about the screen, so only such sentences count.
        m = SETTING.match(sorted(settings)[0]) if settings else None
        if m and m.group(1) == "FIX" and int(m.group(2)) > 0:
            prose = DISP.sub("", KEYS_BLOCK.sub("", body))
            fixed = re.compile(r"(?<![\d.])-?\d+\.\d{%d}(?!\d|\.\d)" % int(m.group(2)))
            for sentence in re.split(r"(?<=[.!?:])\s+", prose):
                if SHOWS.search(sentence):
                    for n in fixed.findall(sentence):
                        self.bad(f"'{n}' looks like a display at {want} but is not in a <disp> tag")

        # 6. A student working through: the setup once, then every block in lesson order on ONE
        # device, nothing reset between them. Each example above is judged from the setup; a student
        # carries whatever the last example left (a display setting, Fraction display, a number still
        # being typed), so every quoted display must also be what that student sees.
        if setup:
            with tempfile.NamedTemporaryFile("w", suffix=".seq", delete=False, encoding="utf-8") as t:
                t.write(f"setup\t{setup}\n")
                for bid, _, _, _ in blocks:
                    if bid != "setup":
                        t.write(f"{bid}\t{own_keys[bid]}\n")
            r = self.run(f"{self.core}/build/keyrun", "--sequence", t.name)
            os.unlink(t.name)
            seq_x, seq_y, seq_st, seq_val = {}, {}, {}, {}
            for l in r.stdout.splitlines():
                p = l.split("\t")
                if p[0] == "X" and len(p) == 4:
                    seq_x[p[1]] = (p[2], p[3])
                elif p[0] == "YL" and len(p) == 4:
                    seq_y[p[1]] = (p[2], p[3])
                elif p[0] == "STATUS" and len(p) == 3:
                    seq_st[p[1]] = p[2].split()
                elif p[0] == "VAL" and len(p) == 6:
                    seq_val[p[1]] = dict(zip("XYZT", p[2:6]))
            if r.returncode != 0:
                self.bad(f"a student working through cannot press the keys in order: {r.stdout.strip()}")
            # Every example's exact X, Y, Z and T expectations, not only the quoted displays: the
            # prose says "X holds 23" and "Y holds 2" too.
            for bid, _, _, _ in blocks:
                if bid not in byid or bid not in seq_val:
                    continue
                for level, want_v in re.findall(r"(?:^|\s)([XYZT])=(\S+)", byid[bid][1][3]):
                    got = seq_val[bid].get(level, "")
                    try:
                        same = Decimal(got) == Decimal(want_v)
                    except InvalidOperation:
                        same = False
                    if not same:
                        self.bad(f"{bid}: working through in order, {level} holds {got or '(not a real)'}, "
                                 f"the vector says {want_v}")
            for q in quotes:
                vid, qkind, shown_text = q.group(1), q.group(2) or "value", q.group(3)
                if qkind == "status":
                    if shown_text not in seq_st.get(vid, []):
                        self.bad(f"{vid}: working through in order, the status band shows {seq_st.get(vid, [])}, "
                                 f"without '{shown_text}'")
                    continue
                kind, stext = seq_x.get(vid, ("?", ""))
                if not line_says((kind, stext), seq_y.get(vid, ("?", "")), qkind, shown_text):
                    self.bad(f"{vid}: working through in order, X shows '{stext}' ({kind}), the prose '{shown_text}'")
            self.notes.append("worked through in order")

        # 5. Voice, the front matter included.
        dashes = sum(text.count(d) for d in EM_DASH)
        if dashes:
            self.bad(f"{dashes} em-dash(es) in lesson.md")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--core", required=True)
    ap.add_argument("lessons", nargs="*")
    a = ap.parse_args()
    if not a.lessons:
        print("check: no lessons")
        return 1
    failed = 0
    for d in a.lessons:
        L = Lesson(d, a.core)
        try:
            L.check()
        except (ValueError, OSError) as e:
            L.bad(f"{type(e).__name__}: {e}")
        status = "FAIL" if L.fail else "ok"
        print(f"{status:4} {L.name}: " + "; ".join(L.notes))
        for f in L.fail:
            print("     " + f.replace("\n", "\n     "))
        failed += bool(L.fail)
    print(f"{len(a.lessons) - failed}/{len(a.lessons)} lessons pass")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
