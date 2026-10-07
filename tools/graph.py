#!/usr/bin/env python3
"""graph.py [--selftest] [--json]: the prerequisite graph's check (lessons/TOPICS, front matter `requires:`).

Refuses: a malformed or repeated topic; a topic whose lesson or ## heading is not there; a lesson
with no `requires:` line; a required slug that is not a topic; a lesson requiring a topic it teaches;
a lesson requiring a topic taught only in a mode section (lesson@modes) unless it offers only those
modes; and a cycle between lessons (A needs B when A requires a topic B teaches). --json prints the
graph for the learning page; --selftest plants each fault and checks it is refused."""
import glob
import json
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
ALL_MODES = ("33s", "35s", "STU")
SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*$")


def front_matter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    meta = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
    return meta


def load(root):
    """(topics text, {id: (meta, lesson text)})."""
    topics = open(os.path.join(root, "lessons", "TOPICS"), encoding="utf-8").read()
    lessons = {}
    for p in sorted(glob.glob(os.path.join(root, "lessons", "*", "lesson.md"))):
        text = open(p, encoding="utf-8").read()
        meta = front_matter(text)
        lessons[meta.get("id", p)] = (meta, text)
    return topics, lessons


def parse_topics(text, bad):
    """slug -> (title, lesson id, modes, heading)."""
    out = {}
    for n, line in enumerate(text.splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) != 4 or not all(parts):
            bad.append(f"TOPICS:{n}: expected 'slug | title | lesson | heading'")
            continue
        slug, title, where, heading = parts
        lid, _, modes = where.partition("@")
        if not SLUG.match(slug):
            bad.append(f"TOPICS:{n}: '{slug}' is not a slug (lower case, digits, hyphens)")
        elif slug in out:
            bad.append(f"TOPICS:{n}: '{slug}' is taught twice ({out[slug][1]} and {lid})")
        else:
            out[slug] = (title, lid, tuple(modes.split(",")) if modes else ALL_MODES, heading)
    return out


def check(topics_text, lessons):
    """(problems, graph): graph is {id: {"requires": [...], "teaches": [...], "needs": [...]}}."""
    bad = []
    topics = parse_topics(topics_text, bad)
    teaches = {lid: [] for lid in lessons}
    for slug, (title, lid, modes, heading) in topics.items():
        if lid not in lessons:
            bad.append(f"topic {slug}: no lesson {lid}")
            continue
        text = lessons[lid][1]
        if heading == "-":                      # the opening: prose after the title, before the first ##
            body = re.sub(r"^---\n.*?\n---\n", "", text, count=1, flags=re.S)
            opening = re.split(r"^## ", body, maxsplit=1, flags=re.M)[0]
            if not [l for l in opening.splitlines() if l.strip() and not l.startswith("# ")]:
                bad.append(f"topic {slug}: {lid} has no opening before its first ## heading")
        elif not re.search(rf"^## {re.escape(heading)}[ \t]*$", text, re.M):
            bad.append(f"topic {slug}: {lid} has no section '## {heading}'")
        teaches[lid].append(slug)
    graph = {}
    for lid, (meta, _) in lessons.items():
        if "requires" not in meta:
            bad.append(f"{lid}: no requires: line in its front matter (empty is allowed)")
            continue
        req = meta["requires"].split()
        offered = tuple(meta.get("modes", " ".join(ALL_MODES)).split())
        needs = set()
        for slug in req:
            if slug not in topics:
                bad.append(f"{lid}: requires '{slug}', which is not a topic")
                continue
            _, src, modes, _ = topics[slug]
            if src == lid:
                bad.append(f"{lid}: requires '{slug}', which it teaches itself")
                continue
            if not set(offered) <= set(modes):
                bad.append(f"{lid}: requires '{slug}', taught only in {','.join(modes)} mode, but offers {' '.join(offered)}")
            needs.add(src)
        if len(set(req)) != len(req):
            bad.append(f"{lid}: requires a topic twice")
        graph[lid] = {"requires": req, "teaches": teaches[lid], "needs": sorted(needs)}
    # A cycle between lessons: depth first, reporting the path.
    state, stack = {}, []

    def visit(lid):
        state[lid] = 1
        stack.append(lid)
        for nxt in graph.get(lid, {}).get("needs", []):
            if state.get(nxt) == 1:
                cyc = stack[stack.index(nxt):] + [nxt]
                bad.append("a cycle: " + " needs ".join(cyc))
            elif nxt not in state:
                visit(nxt)
        stack.pop()
        state[lid] = 2
    for lid in sorted(graph):
        if lid not in state:
            visit(lid)
    for lid in lessons:
        if not teaches.get(lid):
            bad.append(f"{lid}: teaches no topic in TOPICS")
    return bad, {"topics": {s: {"title": t, "lesson": l, "modes": list(m), "heading": h}
                            for s, (t, l, m, h) in topics.items()}, "lessons": graph}


def selftest(topics_text, lessons):
    """Each planted fault must be refused, and for its own reason."""
    def with_req(lid, req):
        meta, text = lessons[lid]
        text = re.sub(r"^requires:.*$", f"requires: {req}", text, count=1, flags=re.M)
        return {**lessons, lid: ({**meta, "requires": req}, text)}
    first = next(iter(lessons))
    own = next(s for s, v in parse_topics(topics_text, []).items() if v[1] == first)
    plants = [
        ("an unknown slug", topics_text, with_req(first, "no-such-topic"), "which is not a topic"),
        ("a lesson requiring its own topic", topics_text, with_req(first, own), "which it teaches itself"),
        ("a heading not in its lesson",
         re.sub(rf"^({re.escape(own)} \|[^|]*\|[^|]*\|).*$", r"\1 No such heading", topics_text, count=1, flags=re.M),
         lessons, "has no section"),
        ("a topic taught twice", topics_text + f"\n{own} | again | {first} | Before you start\n", lessons, "is taught twice"),
        ("a missing requires: line", topics_text,
         {**lessons, first: ({k: v for k, v in lessons[first][0].items() if k != "requires"}, lessons[first][1])},
         "no requires: line"),
    ]
    # A cycle: the first lesson that needs another is made to be needed by it.
    g = check(topics_text, lessons)[1]["lessons"]
    a = next((l for l in g if g[l]["needs"]), None)
    if a:
        b = g[a]["needs"][0]
        a_topic = next(s for s, v in parse_topics(topics_text, []).items() if v[1] == a)
        plants.append(("a cycle between lessons", topics_text,
                       with_req(b, " ".join(lessons[b][0]["requires"].split() + [a_topic])), "a cycle"))
    red = 0
    for name, t, ls, why in plants:
        problems = check(t, ls)[0]
        hit = [p for p in problems if why in p]
        print(f"{'ok  ' if hit else 'FAIL'} {name}" + (f"\n       -> {hit[0]}" if hit else f": {problems[:2]}"))
        red += bool(hit)
    print(f"{red}/{len(plants)} graph controls red as planted")
    return red == len(plants)


def main():
    topics_text, lessons = load(ROOT)
    if "--selftest" in sys.argv:
        return 0 if selftest(topics_text, lessons) else 1
    bad, graph = check(topics_text, lessons)
    if "--json" in sys.argv:
        print(json.dumps(graph, ensure_ascii=False, indent=1))
    for b in bad:
        print(f"GRAPH {b}", file=sys.stderr)
    edges = sum(len(v["needs"]) for v in graph["lessons"].values())
    print(f"graph: {len(graph['topics'])} topics, {len(graph['lessons'])}/{len(lessons)} lessons, "
          f"{edges} lesson links, {len(bad)} problems", file=sys.stderr)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
