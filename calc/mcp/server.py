#!/usr/bin/env python3
"""stu32-calc's MCP server (abacus #5737): stdio, standard library only, one container per tool call.

Each tool call is one calc/run.sh call, so every call gets the container's limits and run.sh's outer deadline;
this server keeps no state between calls and never runs the core itself. Tools:
  calc_keys     printed key names pressed on one device, in order (keys)
  calc_vectors  a vectors file judged by the firmware's runner (vectors)
  calc_casim    one Casimir op by name (casim)
  calc_pins     the pins of the image that answers
The answer is the entry program's JSON, as text. A call is an error (isError) only when it did not run: a bad
request, a limit, or no image. FAIL and Casimir's statuses are answers.

Environment: STU32_CALC_IMAGE (default: the image tagged for the Makefile's pin, as run.sh finds it),
STU32_CALC_DEADLINE (run.sh's outer deadline in seconds, default 30), STU32_CALC_BASH (bash to run run.sh with).

  python calc/mcp/server.py             serve on stdin and stdout
  python calc/mcp/server.py --selftest  start a server, speak to it, and check its answers
"""
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RUN = os.path.join(os.path.dirname(HERE), "run.sh")
NAME, VERSION = "stu32-calc", "1.0.0"
PROTOCOLS = ("2025-06-18", "2025-03-26", "2024-11-05")

TOOLS = [
    {"name": "calc_keys",
     "description": "Press STU-32 keys, by their printed names (e.g. '3452 ENTER 1879 +', 'GOLD EQN 2 × RCL X yˣ 2 "
                    "ENTER CAS D/DX X'), on one fresh calculator, step after step. With mode, the lessons' setup is "
                    "pressed first. Each step answers the X and Y display lines, the status band, and X/Y/Z/T as exact "
                    "34-digit text. For an exact result use entry rpn (an algebraic result is ANS, shown only on the "
                    "display line).",
     "inputSchema": {"type": "object", "required": ["steps"], "additionalProperties": False, "properties": {
         "steps": {"type": "array", "minItems": 1, "maxItems": 1000, "items": {"type": "string"},
                   "description": "one step per item: printed key names separated by spaces, optionally 'ID<TAB>keys'"},
         "mode": {"type": "string", "enum": ["STU", "33s", "35s"]},
         "entry": {"type": "string", "enum": ["alg", "rpn"], "description": "STU mode only"},
         "angle": {"type": "string", "enum": ["DEG", "RAD", "GRAD"]},
         "fix": {"type": "integer", "minimum": 0, "maximum": 11}}}},
    {"name": "calc_vectors",
     "description": "Judge a vectors file with the STU-32 firmware's own runner: lines 'ID | note | STU RPN FIX4 keys | "
                    "X=value ...' in the core's tokens. Answers PASS or FAIL with the runner's report.",
     "inputSchema": {"type": "object", "required": ["text"], "additionalProperties": False, "properties": {
         "text": {"type": "string", "maxLength": 65536},
         "display": {"type": "boolean", "description": "a display-vectors file instead"}}}},
    {"name": "calc_casim",
     "description": "One op of Casimir, the STU-32's computer algebra, exact: derive, simplify, expand, collect, subst, "
                    "solve, integrate, defint, factor, pdiv, pgcd, cancel. args are the CLI's, e.g. op derive, args "
                    "['X^2×SIN(X)', 'X', 'RAD']; op defint, args ['3×X^2', 'X', '0', '2', 'RAD']. The calculator's "
                    "notation: × ÷ ^ π, upper-case names, no implied products.",
     "inputSchema": {"type": "object", "required": ["op", "args"], "additionalProperties": False, "properties": {
         "op": {"type": "string", "enum": ["derive", "simplify", "expand", "collect", "subst", "solve", "integrate",
                                           "defint", "factor", "pdiv", "pgcd", "cancel"]},
         "args": {"type": "array", "maxItems": 7, "items": {"type": "string", "maxLength": 1024}}}}},
    {"name": "calc_pins",
     "description": "The firmware, Casimir and tool commits of the calculator image that answers.",
     "inputSchema": {"type": "object", "additionalProperties": False, "properties": {}}},
]
RAN = {"OK", "PASS", "FAIL", "CASIM_STATUS"}         # answers; anything else (BAD_KEY, a limit) is an error


def run(args, stdin=""):
    bash = os.environ.get("STU32_CALC_BASH") or shutil.which("bash") or "bash"
    flags = ["--deadline", os.environ.get("STU32_CALC_DEADLINE", "30")]
    if os.environ.get("STU32_CALC_IMAGE"):
        flags += ["--image", os.environ["STU32_CALC_IMAGE"]]
    try:
        r = subprocess.run([bash, RUN, *flags, *args], input=stdin.encode("utf-8"), capture_output=True,
                           timeout=int(flags[1]) + 30)
    except subprocess.TimeoutExpired:
        return {"status": "TIMEOUT", "layer": "server"}
    lines = [l for l in r.stdout.decode("utf-8", "replace").splitlines() if l.strip()]
    try:
        return json.loads(lines[-1])
    except (IndexError, json.JSONDecodeError):
        return {"status": "NO_ANSWER", "stderr": r.stderr.decode("utf-8", "replace")[-500:]}


def call_tool(name, a):
    if name == "calc_keys":
        args = ["keys"]
        for k in ("mode", "entry", "angle"):
            if a.get(k):
                args += [f"--{k}", a[k]]
        if a.get("fix") is not None:
            args += ["--fix", str(a["fix"])]
        steps = a.get("steps") or []
        if not all(isinstance(s, str) and "\n" not in s for s in steps):
            return {"status": "BAD_REQUEST", "detail": "each step is one line of text"}
        return run(args, "".join(s + "\n" for s in steps))
    if name == "calc_vectors":
        return run(["vectors"] + (["--display"] if a.get("display") else []), a.get("text", ""))
    if name == "calc_casim":
        if not isinstance(a.get("args"), list) or not all(isinstance(x, str) for x in a["args"]):
            return {"status": "BAD_REQUEST", "detail": "args is a list of strings"}
        return run(["casim", str(a.get("op", "")), *a["args"]])
    if name == "calc_pins":
        return run(["pins"])
    return None


def handle(msg):
    """The reply to one JSON-RPC message, or None for a notification."""
    mid, method, params = msg.get("id"), msg.get("method"), msg.get("params") or {}
    if mid is None:
        return None
    if method == "initialize":
        want = params.get("protocolVersion")
        result = {"protocolVersion": want if want in PROTOCOLS else PROTOCOLS[0],
                  "capabilities": {"tools": {"listChanged": False}},
                  "serverInfo": {"name": NAME, "version": VERSION},
                  "instructions": "The STU-32 calculator's own core, one fresh container per call. Keep mpmath's "
                                  "value beside the core's in every record, so a calculator bug cannot confirm "
                                  "itself (tools/records.py checks the records)."}
    elif method == "ping":
        result = {}
    elif method == "tools/list":
        result = {"tools": TOOLS}
    elif method == "tools/call":
        ans = call_tool(params.get("name"), params.get("arguments") or {})
        if ans is None:
            return {"jsonrpc": "2.0", "id": mid, "error": {"code": -32602, "message": f"no tool {params.get('name')}"}}
        result = {"content": [{"type": "text", "text": json.dumps(ans, ensure_ascii=False)}],
                  "structuredContent": ans, "isError": ans.get("status") not in RAN}
    else:
        return {"jsonrpc": "2.0", "id": mid, "error": {"code": -32601, "message": f"no method {method}"}}
    return {"jsonrpc": "2.0", "id": mid, "result": result}


def serve():
    sys.stdin.reconfigure(encoding="utf-8")
    sys.stdout.reconfigure(encoding="utf-8")
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            reply = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "parse error"}}
        else:
            reply = handle(msg) if isinstance(msg, dict) else \
                {"jsonrpc": "2.0", "id": None, "error": {"code": -32600, "message": "one request per line"}}
        if reply is not None:
            sys.stdout.write(json.dumps(reply, ensure_ascii=False) + "\n")
            sys.stdout.flush()


def selftest():
    sys.stdout.reconfigure(encoding="utf-8")
    p = subprocess.Popen([sys.executable, os.path.abspath(__file__)], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         text=True, encoding="utf-8")
    n = 0

    def ask(method, params=None, notify=False):
        nonlocal n
        n += 1
        msg = {"jsonrpc": "2.0", "method": method, **({} if notify else {"id": n}), **({"params": params} if params else {})}
        p.stdin.write(json.dumps(msg, ensure_ascii=False) + "\n")
        p.stdin.flush()
        return None if notify else json.loads(p.stdout.readline())

    fails = []

    def expect(what, ok, got):
        print(f"{'ok  ' if ok else 'FAIL'} {what}: {got}")
        if not ok:
            fails.append(what)

    r = ask("initialize", {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "selftest"}})
    expect("initialize", r["result"]["serverInfo"]["name"] == NAME, r["result"]["protocolVersion"])
    ask("notifications/initialized", notify=True)
    r = ask("tools/list")
    expect("tools/list", [t["name"] for t in r["result"]["tools"]] == [t["name"] for t in TOOLS],
           [t["name"] for t in r["result"]["tools"]])
    r = ask("tools/call", {"name": "calc_keys", "arguments": {"mode": "STU", "entry": "rpn",
                                                              "steps": ["A\t3452 ENTER 1879 +"]}})
    sc = r["result"]["structuredContent"]
    expect("calc_keys", sc["status"] == "OK" and sc["steps"][-1]["stack"]["X"] == "+5331E+0" and not r["result"]["isError"],
           f"{sc['status']} X={sc['steps'][-1]['stack']['X']}")
    r = ask("tools/call", {"name": "calc_vectors", "arguments": {
        "text": "V1 | 3452 + 1879 | STU RPN FIX4 3452 ENTER 1879 + | X=5332\n"}})
    sc = r["result"]["structuredContent"]
    expect("calc_vectors planted", sc["status"] == "FAIL" and not r["result"]["isError"], f"{sc['status']} {sc['report'][:1]}")
    r = ask("tools/call", {"name": "calc_casim", "arguments": {"op": "defint", "args": ["3×X^2", "X", "0", "2", "RAD"]}})
    sc = r["result"]["structuredContent"]
    expect("calc_casim", sc["status"] == "OK" and sc["text"] == "8", f"{sc['status']} {sc['text']}")
    r = ask("tools/call", {"name": "calc_keys", "arguments": {"mode": "STU", "steps": ["1 ENTER\n2 ENTER"]}})
    sc = r["result"]["structuredContent"]
    expect("a step with a newline refused", sc["status"] == "BAD_REQUEST" and r["result"]["isError"], sc["status"])
    r = ask("tools/call", {"name": "calc_pins", "arguments": {}})
    expect("calc_pins", bool(r["result"]["structuredContent"].get("pins", {}).get("firmware")),
           r["result"]["structuredContent"].get("pins", {}).get("firmware", "")[:12])
    r = ask("no/such")
    expect("unknown method", r.get("error", {}).get("code") == -32601, r.get("error"))
    p.stdin.close()
    p.wait(timeout=30)
    print("all passed" if not fails else "FAILED: " + " ".join(fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(selftest() if sys.argv[1:] == ["--selftest"] else serve())
