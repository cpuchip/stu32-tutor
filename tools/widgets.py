#!/usr/bin/env python3
"""widgets.py [--selftest]: a lesson's widget blocks and the prose quotes from them (docs/lesson-format.md, Widgets;
docs/courses/astronomy-shape.md; the format agreed with primer, #12390 and #12391).

A widget block is drawn by the page, not run on the calculator:

    ```widget W01 sky-sphere
    lat: 40.7
    epoch: J2000
    shows: ra | 18h 37m
    ```

Its ID is the lesson's own (no keys block shares it); its name, parameters, epochs and shows keys are those
tools/WIDGETS lists; a star parameter names a star in data/stars.tsv. A quote `<disp v="W01" kind="widget" k="ra">`
must give the shows text for that key exactly. A widget block adds no vectors, is not in the student run, has no mode
or entry variants, and is neither tried nor an item. check.py calls problems(); --selftest plants each fault."""
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
WIDGET = re.compile(r"^[ \t]*```widget[ \t]+(\S+)[ \t]+(\S+)[ \t]*\n(.*?)^[ \t]*```[ \t]*$", re.M | re.S)
WIDGET_FENCE = re.compile(r"^[ \t]*```widget\b.*$", re.M)
QUOTE = re.compile(r'<disp((?:\s+[a-z]+="[^"]*")*)\s*>(.*?)</disp>', re.S)
ATTR = re.compile(r'([a-z]+)="([^"]*)"')
DATE = re.compile(r"\d{4}-\d{2}-\d{2}$")


def load_widgets(path):
    """{name: {"params": {key: (type, args)}, "shows": set, "epochs": set}} from tools/WIDGETS:
    `name | param | key | number LO HI` or `one-of A B C` or `star`; `name | shows | key`; `name | epoch | J2000` or
    `date`. Text after a further | is a note for people."""
    out = {}
    for n, line in enumerate(open(path, encoding="utf-8").read().splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        f = [x.strip() for x in line.split("|")]
        name, kind = f[0], f[1] if len(f) > 1 else ""
        w = out.setdefault(name, {"params": {}, "shows": set(), "epochs": set()})
        if kind == "param" and len(f) >= 4:
            spec = f[3].split()
            w["params"][f[2]] = (spec[0], spec[1:])
        elif kind == "shows" and len(f) >= 3:
            w["shows"].add(f[2])
        elif kind == "epoch" and len(f) >= 3:
            w["epochs"].add(f[2])
        else:
            raise ValueError(f"{path}:{n}: expected name | param | key | spec, name | shows | key, or name | epoch | e")
    return out


def load_stars(path):
    """{HR: (name, ra_deg, dec_deg)} from data/stars.tsv (HR | name | RA J2000 deg | Dec J2000 deg | Vmag | source)."""
    out = {}
    for line in open(path, encoding="utf-8").read().splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        f = [x.strip() for x in line.split("|")]
        out[f[0]] = (f[1], float(f[2]), float(f[3]))
    return out


def problems(text, widgets, stars, other_ids=()):
    """The problems with a lesson's widget blocks and its widget quotes. other_ids: the keys blocks' IDs."""
    bad, blocks = [], {}
    found = list(WIDGET.finditer(text))
    if len(found) != len(WIDGET_FENCE.findall(text)):
        bad.append("a widget fence not in the form ```widget ID name ... ```")
    for m in found:
        wid, name, body = m.group(1), m.group(2), m.group(3)
        if wid in blocks or wid in other_ids:
            bad.append(f"widget {wid}: its ID is used twice in the lesson")
        if name not in widgets:
            bad.append(f"widget {wid}: '{name}' is not a widget in tools/WIDGETS")
            continue
        spec = widgets[name]
        params, shows = {}, {}
        for line in body.splitlines():
            if not line.strip():
                continue
            key, sep, val = line.strip().partition(":")
            key, val = key.strip(), val.strip()
            if not sep or not val:
                bad.append(f"widget {wid}: '{line.strip()}' is not a key: value line")
            elif key == "shows":
                sk, bar, stext = val.partition("|")
                sk, stext = sk.strip(), stext.strip()
                if not bar or not stext:
                    bad.append(f"widget {wid}: shows: needs a key, a |, and the text ('{val}')")
                elif sk not in spec["shows"]:
                    bad.append(f"widget {wid}: {name} shows no '{sk}'")
                elif sk in shows:
                    bad.append(f"widget {wid}: shows '{sk}' twice")
                else:
                    shows[sk] = stext
            elif key == "epoch" or key in spec["params"]:
                if key in params:
                    bad.append(f"widget {wid}: '{key}' given twice")
                params[key] = val
            else:
                bad.append(f"widget {wid}: {name} takes no parameter '{key}'")
        if "epoch" not in params:
            bad.append(f"widget {wid}: no epoch: line (J2000, or a date for a widget that precesses)")
        elif not (params["epoch"] in spec["epochs"] or ("date" in spec["epochs"] and DATE.match(params["epoch"]))):
            bad.append(f"widget {wid}: {name} takes epoch {' or '.join(sorted(spec['epochs']))}, not '{params['epoch']}'")
        for key, (typ, args) in spec["params"].items():
            if key not in params:
                bad.append(f"widget {wid}: no {key}: line")
                continue
            val = params[key]
            if typ == "number":
                try:
                    x = float(val)
                    ok = float(args[0]) <= x <= float(args[1])
                except ValueError:
                    ok = False
                if not ok:
                    bad.append(f"widget {wid}: {key} is '{val}', not a number from {args[0]} to {args[1]}")
            elif typ == "one-of" and val not in args:
                bad.append(f"widget {wid}: {key} is '{val}', not one of {' '.join(args)}")
            elif typ == "star" and val not in stars:
                bad.append(f"widget {wid}: star {val} is not in data/stars.tsv")
        blocks[wid] = shows
    for q in QUOTE.finditer(text):
        a = dict(ATTR.findall(q.group(1)))
        if a.get("kind") != "widget":
            continue
        wid, k = a.get("v", ""), a.get("k")
        if wid not in blocks:
            bad.append(f'<disp v="{wid}" kind="widget">: no widget block {wid} in the lesson')
        elif k is None:
            bad.append(f'<disp v="{wid}" kind="widget">: no k= naming the shows key it quotes')
        elif k not in blocks[wid]:
            bad.append(f'<disp v="{wid}" kind="widget" k="{k}">: the widget has no shows: line for {k}')
        elif q.group(2) != blocks[wid][k]:
            bad.append(f'<disp v="{wid}" kind="widget" k="{k}">: the prose quotes \'{q.group(2)}\', '
                       f"the widget shows '{blocks[wid][k]}'")
    return bad


def selftest():
    widgets = load_widgets(os.path.join(ROOT, "tools", "WIDGETS"))
    stars = load_stars(os.path.join(ROOT, "data", "stars.tsv"))
    good = ("```widget W01 sky-sphere\nlat: 40.7\nlst: 18.6\nstar: 7001\ngrids: radec\nepoch: J2000\n"
            "shows: ra | 18h 37m\nshows: dec | +39°\n```\n\nVega is at <disp v=\"W01\" kind=\"widget\" k=\"ra\">18h 37m</disp>.\n")
    plants = [
        ("an unknown widget name", good.replace("W01 sky-sphere", "W01 sky-globe"), "'sky-globe' is not a widget"),
        ("a parameter the widget does not take", good.replace("lat: 40.7\n", "lat: 40.7\nzoom: 2\n"), "takes no parameter 'zoom'"),
        ("no epoch line", good.replace("epoch: J2000\n", ""), "no epoch: line"),
        ("an epoch the widget does not take", good.replace("epoch: J2000", "epoch: B1950"), "takes epoch"),
        ("a quote that differs from shows", good.replace('k="ra">18h 37m<', 'k="ra">18h 36m<'), "the prose quotes '18h 36m'"),
        ("a quote of a key with no shows line", good.replace('k="ra">', 'k="alt">'), "no shows: line for alt"),
        ("a quote of no widget", good.replace('<disp v="W01" kind', '<disp v="W09" kind'), "no widget block W09"),
        ("a shows key the widget does not print", good.replace("shows: dec |", "shows: mag |"), "shows no 'mag'"),
        ("a star not in data/stars.tsv", good.replace("star: 7001", "star: 9999"), "star 9999 is not in data/stars.tsv"),
        ("a latitude out of range", good.replace("lat: 40.7", "lat: 140"), "not a number from -90 to 90"),
        ("a grids value not offered", good.replace("grids: radec", "grids: polar"), "not one of"),
        ("a missing parameter", good.replace("lst: 18.6\n", ""), "no lst: line"),
        ("a widget ID shared with a keys block", good, "used twice"),
    ]
    clean = problems(good, widgets, stars)
    ok = not clean
    print(f"{'ok  ' if ok else 'FAIL'} the clean widget passes" + ("" if ok else f": {clean}"))
    red = 0
    for name, text, why in plants:
        got = problems(text, widgets, stars, other_ids=("W01",) if "keys block" in name else ())
        hit = [p for p in got if why in p]
        print(f"{'ok  ' if hit else 'FAIL'} {name}" + (f"\n       -> {hit[0]}" if hit else f": {got[:2]}"))
        red += bool(hit)
    print(f"{red}/{len(plants)} widget controls red as planted")
    return ok and red == len(plants)


if __name__ == "__main__":
    sys.exit(0 if "--selftest" in sys.argv and selftest() else 1 if "--selftest" in sys.argv else 0)
