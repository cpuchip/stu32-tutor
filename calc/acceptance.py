#!/usr/bin/env python3
"""calc/acceptance.py IMAGE [--rebuild IMAGE2] [--only NAME ...]: stu32-calc's acceptance (abacus #5737).

Every call goes through calc/run.sh, the way a caller makes it. The tests:
  pins       the image names the Makefile's pin, and Casimir's CLI was built on that same core
  cost       the per-call start cost, 10 calls
  probe      the fixed probe set: every lesson's and placement's vectors in each of its modes and entries,
             its display vectors, the student run of each lesson, and a list of Casimir ops. Every vectors
             call must PASS and every student run be OK, as make check finds at the same pin. The outputs
             (wall times dropped) are hashed: the digest is what a rebuild must reproduce.
  ans        an algebraic result is reported exact as ans (and shown), the stack untouched
  planted    a vector with a wrong expectation FAILs, naming it
  runaway    an endless program stops at the core's own RUN LIMIT; 300 of them in one call stop at the
             entry program's CPU limit (TIMEOUT, cpu 10 s, exit 124); with that off, at its wall clock
             (TIMEOUT, wall 15 s); with the inner layer off (--test-no-inner), at run.sh's deadline
             (TIMEOUT, layer outside); and no container is left in any case
  floods     an output flood (OUTPUT_LIMIT) and an input flood (INPUT_LIMIT), each exit 124
  posture    calc/probe.c run as the entry point under run.sh's flags: no write anywhere, no network, the
             licences readable at /licenses
  nonet      the entry program and runners under strace on a slice of the probe set: no network syscall
  rebuild    with --rebuild, the probe digest of IMAGE2 (built from scratch at the same pins) equals IMAGE's
Prints one line per check and exits 1 if any fails.
"""
import concurrent.futures
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import check  # noqa: E402  (the lesson parsers make check uses)

FAILS = []
BASH = shutil.which("bash") or "bash"


def say(name, ok, detail):
    print(f"{'ok  ' if ok else 'FAIL'} {name}: {detail}", flush=True)
    if not ok:
        FAILS.append(name)


def call(image, args, stdin="", run_flags=()):
    """(exit code, the JSON answer, seconds) for one call through run.sh."""
    t0 = time.monotonic()
    r = subprocess.run([BASH, os.path.join(ROOT, "calc", "run.sh"), "--image", image, *run_flags, *args],
                       input=stdin.encode("utf-8"), capture_output=True, timeout=180, cwd=ROOT)
    secs = time.monotonic() - t0
    lines = [l for l in r.stdout.decode("utf-8", "replace").splitlines() if l.strip()]
    try:
        ans = json.loads(lines[-1])
    except (IndexError, json.JSONDecodeError):
        ans = {"status": "UNPARSED", "stdout": r.stdout.decode("utf-8", "replace")[-400:],
               "stderr": r.stderr.decode("utf-8", "replace")[-400:]}
    return r.returncode, ans, secs


def leftovers(image):
    r = subprocess.run(["docker", "ps", "-a", "-q", "--filter", f"ancestor={image}"], capture_output=True, text=True)
    return r.stdout.split()


# ---- the probe set ----

CASIM_OPS = [
    ["derive", "X^2×SIN(X)", "X", "RAD"],
    ["derive", "X^3-4×X+1", "X", "RAD"],
    ["simplify", "SIN(π÷6)", "RAD"],
    ["simplify", "1÷0", "RAD"],
    ["expand", "(X+1)^3", "RAD"],
    ["solve", "X^2-5×X+6", "X", "RAD"],
    ["solve", "X^2+1", "X", "RAD"],
    ["factor", "X^4-1", "X", "RAD"],
    ["integrate", "3×X^2", "X", "RAD"],
    ["defint", "3×X^2", "X", "0", "2", "RAD"],
    ["defint", "SIN(X)", "X", "0", "π", "RAD"],
    ["defint", "1÷X", "X", "0", "1", "RAD"],
    ["pdiv", "X^3-1", "X", "X-1", "RAD"],
    ["cancel", "(X^2-1)÷(X-1)", "X", "RAD"],
    ["derive", "X^^2", "X", "RAD"],
]


def probe_requests():
    """(key, args, stdin, expected status) for the fixed probe set, in a fixed order."""
    reqs = []
    for top in ("lessons", "placement"):
        for name in sorted(os.listdir(os.path.join(ROOT, top))):
            d = os.path.join(ROOT, top, name)
            if not os.path.isfile(os.path.join(d, "vectors.txt")):
                continue
            meta, _ = check.front_matter(open(os.path.join(d, "lesson.md"), encoding="utf-8").read())
            modes, _ = check.lesson_modes(meta)
            entries, _ = check.lesson_entries(meta, modes)
            vectors = check.read_vectors(os.path.join(d, "vectors.txt"), 4)
            for mode in modes:
                for entry in entries:
                    if entry == "alg" and mode != "STU":
                        continue
                    where = f"{mode}{'/' + entry if entry else ''}"
                    lines = [check.variant(v[1], mode, False, entry)
                             for v in check.vectors_for_mode(vectors, mode, None, entry)]
                    reqs.append((f"{name} vectors {where}", ["vectors"], "\n".join(lines) + "\n", "PASS"))
                    if meta.get("setup"):
                        seq = check.student_sequence(d, mode, entry)
                        reqs.append((f"{name} keys {where}", ["keys"], seq, "OK"))
            fmt = os.path.join(d, "fmt-vectors.txt")
            if os.path.isfile(fmt):
                reqs.append((f"{name} display", ["vectors", "--display"], open(fmt, encoding="utf-8").read(), "PASS"))
    for op in CASIM_OPS:
        reqs.append((f"casim {' '.join(op)}", ["casim", *op], "", None))
    return reqs


def normal(ans):
    a = dict(ans)
    a.pop("wall_ms", None)
    return json.dumps(a, ensure_ascii=False, sort_keys=True)


def probe(image, reqs, workers=4):
    """{key: (exit, normalized answer)} and the digest over them."""
    out = {}
    with concurrent.futures.ThreadPoolExecutor(workers) as ex:
        futs = {ex.submit(call, image, args, stdin): key for key, args, stdin, _ in reqs}
        for f in concurrent.futures.as_completed(futs):
            rc, ans, _ = f.result()
            out[futs[f]] = (rc, ans)
    h = hashlib.sha256()
    for key in sorted(out):
        h.update(f"{key}\t{out[key][0]}\t{normal(out[key][1])}\n".encode("utf-8"))
    return out, h.hexdigest()


# ---- the tests ----

def t_pins(image):
    rc, ans, _ = call(image, ["pins"])
    pin = open(os.path.join(ROOT, "Makefile"), encoding="utf-8").read().split("CORE_PIN := ")[1].split()[0]
    fw = ans.get("pins", {}).get("firmware", "")
    one_core = ans.get("pins", {}).get("casim-core") == fw
    say("pins", rc == 0 and fw.startswith(pin) and one_core, f"one core: {one_core}; "
        f"firmware {fw[:12]}, casim {ans.get('pins', {}).get('casim', '')[:12]}, "
        f"tutor {ans.get('pins', {}).get('stu32-tutor', '')[:12]}")


def t_cost(image):
    secs = sorted(call(image, ["pins"])[2] for _ in range(10))
    say("cost", True, f"10 calls of pins: median {secs[5]:.2f} s, min {secs[0]:.2f} s, max {secs[-1]:.2f} s")


def t_probe(image, keep):
    reqs = probe_requests()
    t0 = time.monotonic()
    out, digest = probe(image, reqs)
    bad = [k for k, _, _, want in reqs if want and out[k][1].get("status") != want]
    counts = {}
    for k, _, _, _ in reqs:
        counts[k.split()[1] if not k.startswith("casim") else "casim"] = counts.get(
            k.split()[1] if not k.startswith("casim") else "casim", 0) + 1
    say("probe", not bad, f"{len(reqs)} calls ({', '.join(f'{n} {k}' for k, n in sorted(counts.items()))}) in "
        f"{time.monotonic() - t0:.0f} s; digest {digest[:16]}" + (f"; NOT as make check: {bad[:5]}" if bad else ""))
    path = os.path.join(ROOT, "build", "calc", f"probe-{image.split(':', 1)[1]}.jsonl")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        for k in sorted(out):
            f.write(json.dumps({"key": k, "exit": out[k][0], "answer": json.loads(normal(out[k][1]))},
                               ensure_ascii=False) + "\n")
    keep["digest"] = digest
    keep["casim"] = {k: out[k][1].get("status") + " " + out[k][1].get("text", "") for k, _, _, _ in reqs
                     if k.startswith("casim")}


def t_ans(image):
    rc, ans, _ = call(image, ["keys", "--mode", "STU", "--entry", "alg"], "A\t3452 + 1879 ENTER\n")
    last = (ans.get("steps") or [{}])[-1]
    say("ans", rc == 0 and last.get("ans") == "+5331E+0" and last.get("shown") == "+5331E+0"
        and last.get("stack", {}).get("X") == "+0E-6176",
        f"alg 3452 + 1879: ans {last.get('ans')}, shown {last.get('shown')}, X {last.get('stack', {}).get('X')} "
        f"(the stack untouched)")


def t_planted(image):
    d = os.path.join(ROOT, "lessons", "whole-01-adding-and-subtracting")
    vectors = check.read_vectors(os.path.join(d, "vectors.txt"), 4)
    lines = [check.variant(v[1], "STU", False, "rpn") for v in check.vectors_for_mode(vectors, "STU", None, "rpn")]
    planted = [l.replace("X=5331", "X=5332") if l.startswith("A01@rpn ") else l for l in lines]
    assert planted != lines
    rc, ans, _ = call(image, ["vectors"], "\n".join(planted) + "\n")
    named = [l for l in ans.get("report", []) if "A01" in l]
    say("planted", rc == 0 and ans.get("status") == "FAIL" and bool(named),
        f"{ans.get('status')}, exit {rc}; the report names it: {named[:1]}")


def runaway_steps(n):
    return "R1\tGOLD PRGM PRGM GOLD LBL A GOLD GTO A GOLD PRGM PRGM\n" + \
        "".join(f"R{i}\tXEQ A\n" for i in range(2, n + 2))


def t_runaway(image):
    rc, ans, secs = call(image, ["keys", "--mode", "33s"], runaway_steps(1))
    last = (ans.get("steps") or [{}])[-1].get("x", {})
    say("runaway core", rc == 0 and last.get("text") == "RUN LIMIT",
        f"one endless program: {last.get('kind')} {last.get('text')!r} after {ans.get('wall_ms')} ms")
    rc, ans, secs = call(image, ["keys", "--mode", "33s"], runaway_steps(300))
    left = leftovers(image)
    say("runaway cpu", rc == 124 and ans.get("status") == "TIMEOUT" and ans.get("limit") == "cpu 10 s" and not left,
        f"300 endless programs: {ans.get('status')} ({ans.get('limit')}), exit {rc}, {secs:.1f} s; "
        f"containers left: {len(left)}")
    rc, ans, secs = call(image, ["keys", "--mode", "33s"], runaway_steps(300), run_flags=("--test-no-cpu-limit",))
    left = leftovers(image)
    say("runaway wall", rc == 124 and ans.get("status") == "TIMEOUT" and ans.get("limit") == "wall 15 s" and not left,
        f"CPU limit off: {ans.get('status')} ({ans.get('limit')}), exit {rc}, {secs:.1f} s; "
        f"containers left: {len(left)}")
    rc, ans, secs = call(image, ["keys", "--mode", "33s"], runaway_steps(300),
                         run_flags=("--test-no-inner", "--deadline", "20"))
    time.sleep(2)
    left = leftovers(image)
    say("runaway outer", rc == 124 and ans.get("status") == "TIMEOUT" and ans.get("layer") == "outside" and not left,
        f"inner layer off: {ans.get('status')} (layer {ans.get('layer')}, {ans.get('limit')}), exit {rc}, "
        f"{secs:.1f} s; containers left: {len(left)}")


def t_floods(image):
    steps = "".join(f"F{i}\t1 ENTER\n" for i in range(1000))
    rc, ans, _ = call(image, ["keys", "--mode", "STU"], steps)
    say("flood out", rc == 124 and ans.get("status") == "OUTPUT_LIMIT",
        f"1000 steps: {ans.get('status')} ({ans.get('limit')}), exit {rc}, {len(ans.get('steps', []))} steps kept")
    rc, ans, _ = call(image, ["keys", "--mode", "STU"], "1 ENTER\n" * 9000)
    say("flood in", rc == 124 and ans.get("status") == "INPUT_LIMIT",
        f"72,000 bytes in: {ans.get('status')} ({ans.get('limit')}), exit {rc}")


def gcc_run(script, network=True, mounts=()):
    w = (lambda p: subprocess.run(["cygpath", "-w", p], capture_output=True, text=True).stdout.strip()) \
        if os.name == "nt" else (lambda p: p)
    cmd = ["docker", "run", "--rm"] + ([] if network else ["--network", "none"])
    cmd += ["-v", f"{w(ROOT)}:/w/stu32-tutor"]
    for m in mounts:
        cmd += ["-v", m]
    cmd += ["-w", "/w/stu32-tutor", "gcc:14", "bash", "-euo", "pipefail", "-c", script]
    env = dict(os.environ, MSYS_NO_PATHCONV="1")
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", env=env, timeout=600)


def t_posture(image):
    r = gcc_run("mkdir -p build/calc && cc -O2 -static -Wall -Wextra -Werror calc/probe.c -o build/calc/probe")
    if r.returncode:
        say("posture", False, f"probe did not build: {r.stderr[-300:]}")
        return
    w = (lambda p: subprocess.run(["cygpath", "-w", p], capture_output=True, text=True).stdout.strip()) \
        if os.name == "nt" else (lambda p: p)
    probe_bin = w(os.path.join(ROOT, "build", "calc", "probe"))
    cmd = ["docker", "run", "--rm", "--init", "--network", "none", "--read-only", "--cap-drop", "ALL",
           "--security-opt", "no-new-privileges", "--user", "65532:65532", "--memory", "256m", "--memory-swap",
           "256m", "--pids-limit", "16", "--cpus", "1", "-v", f"{probe_bin}:/probe:ro", "--entrypoint", "/probe",
           image]
    r = subprocess.run(cmd, capture_output=True, text=True, env=dict(os.environ, MSYS_NO_PATHCONV="1"))
    try:
        p = json.loads(r.stdout.strip().splitlines()[-1])
    except (IndexError, json.JSONDecodeError):
        say("posture", False, f"probe output {r.stdout[-200:]!r} {r.stderr[-200:]!r}")
        return
    writes_ok = all(p[k] != "ok" for k in ("write_root", "write_opt", "write_tmp"))
    net_ok = all(p[k] != "ok" for k in ("tcp_1.1.1.1:53", "udp_1.1.1.1:53"))
    say("posture", writes_ok and net_ok and p["uid"] == 65532 and p.get("licenses") == "ok ok ok", json.dumps(p))


def t_nonet():
    # strace from Debian's archive in a throwaway gcc:14 container; the binaries are the stage's, by STU32_CALC_ROOT.
    stage = [d for d in sorted(os.listdir(os.path.join(ROOT, "build", "calc"))) if d.startswith("stage-")]
    if not stage:
        say("nonet", False, "no stage folder")
        return
    st = f"build/calc/{stage[-1]}/opt/stu32"
    script = f"""
        apt-get -qq update >/dev/null && apt-get -qq install -y strace >/dev/null
        export STU32_CALC_ROOT=/w/stu32-tutor/{st}
        b=$STU32_CALC_ROOT/bin/stu32-calc
        printf 'A01\\t3452 + 1879 ENTER\\n' > /tmp/k
        grep -v '^#' lessons/whole-01-adding-and-subtracting/vectors.txt | grep '|' | grep -v '@alg' \
            | sed 's/@rpn//; s/| MODE33 /| STU RPN /' > /tmp/v
        strace -f -qq -e signal=none -e trace=%network -o /tmp/t1 $b keys --mode STU --entry alg < /tmp/k > /dev/null
        strace -f -qq -e signal=none -e trace=%network -o /tmp/t2 $b vectors < /tmp/v > /tmp/vout
        strace -f -qq -e signal=none -e trace=%network -o /tmp/t3 $b casim defint '3×X^2' X 0 2 RAD > /dev/null
        echo "calls: $(cat /tmp/t1 /tmp/t2 /tmp/t3 | grep -vc '+++ exited' || true)"
        strace -f -qq -e signal=none -e trace=%network -o /tmp/tc bash -c 'exec 3<>/dev/tcp/127.0.0.1/9' 2>/dev/null || true
        echo "control: $(grep -vc '+++ exited' /tmp/tc || true)"
        grep -o '"status":"[A-Z_]*"' /tmp/vout | head -1
        cat /tmp/t1 /tmp/t2 /tmp/t3 | grep -v '+++ exited' | head -5 || true
    """
    r = gcc_run(script)
    lines = r.stdout.strip().splitlines()
    calls = next((l for l in lines if l.startswith("calls: ")), "calls: ?")
    control = next((l for l in lines if l.startswith("control: ")), "control: ?")[9:]
    seen = control.isdigit() and int(control) > 0
    say("nonet", r.returncode == 0 and calls == "calls: 0" and seen,
        f"network syscalls under strace -f (keys, vectors, casim): {calls[7:]}; the control (bash /dev/tcp) "
        f"shows {control}; vectors {[l for l in lines if l.startswith('"status')][:1]}"
        + ("" if r.returncode == 0 else f"; {r.stderr[-300:]}"))


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 2
    image = args.pop(0)
    rebuild = args[args.index("--rebuild") + 1] if "--rebuild" in args else None
    only = [args[i + 1] for i, a in enumerate(args) if a == "--only"]
    want = lambda n: not only or n in only  # noqa: E731
    os.makedirs(os.path.join(ROOT, "build", "calc"), exist_ok=True)
    keep = {}
    if want("pins"): t_pins(image)
    if want("cost"): t_cost(image)
    if want("probe") or rebuild: t_probe(image, keep)
    if want("ans"): t_ans(image)
    if want("planted"): t_planted(image)
    if want("runaway"): t_runaway(image)
    if want("floods"): t_floods(image)
    if want("posture"): t_posture(image)
    if want("nonet"): t_nonet()
    if rebuild:
        keep2 = {}
        t_probe(rebuild, keep2)
        say("rebuild", keep["digest"] == keep2["digest"],
            f"{image} {keep['digest'][:16]} and {rebuild} {keep2['digest'][:16]}")
    if keep.get("casim"):
        for k, v in sorted(keep["casim"].items()):
            print(f"     {k} -> {v}")
    print(f"{'FAILED: ' + ' '.join(FAILS) if FAILS else 'all passed'}")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
