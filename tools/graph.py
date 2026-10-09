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
        # An item's topics (docs/lesson-format.md, Items) are where a miss links back: each must be a topic.
        for im in re.finditer(r"^[ \t]*```item[ \t]+(\S+)[ \t]*\n(.*?)^[ \t]*```", lessons[lid][1], re.M | re.S):
            tl = re.search(r"^[ \t]*topics:(.*)$", im.group(2), re.M)
            for slug in (tl.group(1).split() if tl else []):
                if slug not in topics:
                    bad.append(f"{lid}: item {im.group(1)} names topic '{slug}', which is not a topic")
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
        ("an item naming a topic that is not one", topics_text,
         {**lessons, first: (lessons[first][0], lessons[first][1] + "\n```item Z99\nprompt: p\ntopics: no-such-topic\n"
                             "answer: type\ncalculator: no\n```\n")},
         "item Z99 names topic 'no-such-topic'"),
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


ENTRIES = ("rpn", "alg")


def load_courses(root):
    """{file name: text} for courses/*.course."""
    return {os.path.basename(p): open(p, encoding="utf-8").read()
            for p in sorted(glob.glob(os.path.join(root, "courses", "*.course")))}


def check_courses(course_texts, graph):
    """(problems, courses). A course file: `course | id | title`, `entry | rpn alg` (offered, default first),
    any `prerequisite | course-id` lines (courses a learner is expected to have done first), then `unit | n |
    title` and `lesson | id` lines in order. Refused: a malformed line; an unknown or repeated lesson; an
    unknown prerequisite; a lesson requiring a topic taught later in the same course, by no lesson in any
    course, or by a lesson that is neither earlier in this course nor in one of its prerequisites (taken
    transitively): a learner who starts the course would meet the topic nowhere before it (abacus #5112)."""
    bad, courses, in_some = [], {}, set()
    parsed = []
    for name, text in course_texts.items():
        c = {"file": name, "id": None, "title": None, "entry": ["rpn"], "prerequisites": [], "units": []}
        for n, line in enumerate(text.splitlines(), 1):
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            parts = [p.strip() for p in line.split("|")]
            kind, args = parts[0], parts[1:]
            if kind == "course" and len(args) == 2:
                c["id"], c["title"] = args
            elif kind == "entry" and len(args) == 1 and args[0].split() and all(e in ENTRIES for e in args[0].split()):
                c["entry"] = args[0].split()
            elif kind == "prerequisite" and len(args) == 1 and args[0] and not c["units"]:
                c["prerequisites"].append(args[0])
            elif kind == "unit" and len(args) == 2:
                c["units"].append({"n": args[0], "title": args[1], "lessons": []})
            elif kind == "lesson" and len(args) == 1 and c["units"]:
                c["units"][-1]["lessons"].append(args[0])
            else:
                bad.append(f"{name}:{n}: expected course | id | title, entry | rpn alg, prerequisite | course-id "
                           f"(before the units), unit | n | title, or lesson | id")
        if not c["id"] or f"{c['id']}.course" != name:
            bad.append(f"{name}: its course line must name it ({name[:-7]})")
        parsed.append(c)
        for u in c["units"]:
            in_some.update(u["lessons"])
    topics = graph["topics"]
    by_id = {c["id"]: c for c in parsed if c["id"]}
    for c in parsed:
        for p in c["prerequisites"]:
            if p not in by_id or p == c["id"]:
                bad.append(f"{c['file']}: prerequisite {p} is not another course")
    for c in parsed:
        order = [l for u in c["units"] for l in u["lessons"]]
        # The lessons of its prerequisites, taken transitively.
        before, todo, done = set(), list(c["prerequisites"]), {c["id"]}
        while todo:
            p = todo.pop()
            if p in done or p not in by_id:
                continue
            done.add(p)
            before.update(l for u in by_id[p]["units"] for l in u["lessons"])
            todo.extend(by_id[p]["prerequisites"])
        seen = set()
        for i, lid in enumerate(order):
            if lid not in graph["lessons"]:
                bad.append(f"{c['file']}: lesson {lid} is not a lesson")
                continue
            if lid in seen:
                bad.append(f"{c['file']}: lesson {lid} is listed twice")
            seen.add(lid)
            for slug in graph["lessons"][lid]["requires"]:
                src = topics.get(slug, {}).get("lesson")
                if src in order and order.index(src) > i:
                    bad.append(f"{c['file']}: {lid} requires '{slug}', taught later in the course by {src}")
                elif src is not None and src not in in_some:
                    bad.append(f"{c['file']}: {lid} requires '{slug}', taught by {src}, which is in no course")
                elif src is not None and src not in order and src not in before:
                    bad.append(f"{c['file']}: {lid} requires '{slug}', taught by {src}, which is neither earlier "
                               f"in this course nor in a prerequisite course")
        courses[c["id"]] = {k: c[k] for k in ("title", "entry", "prerequisites", "units")}
    for lid in sorted(set(graph["lessons"]) - in_some):
        bad.append(f"{lid}: in no course")
    return bad, courses


def selftest_courses(course_texts, graph):
    """Each planted course fault must be refused, and for its own reason."""
    name = "algebra-to-calculus.course"
    t = course_texts[name]
    plants = [
        ("an unknown lesson in a course", t + "lesson | no-such-01\n", "is not a lesson"),
        ("a lesson listed twice", t + "lesson | rpn-01\n", "is listed twice"),
        ("a lesson before the one that teaches what it requires",
         t.replace("lesson | rpn-01\n", "").replace("lesson | rpn-02\n", "lesson | rpn-02\nlesson | rpn-01\n"),
         "taught later in the course"),
        ("a malformed line", t + "lessn | rpn-01\n", "expected course"),
        ("a lesson in no course", t.replace("lesson | int-01\n", ""), "int-01: in no course"),
        ("an unknown prerequisite", t.replace("entry | rpn\n", "entry | rpn\nprerequisite | no-such-course\n"),
         "prerequisite no-such-course is not another course"),
    ]
    # A second course listing a lesson whose requires the algebra course teaches: refused without the
    # prerequisite line, accepted with it.
    lone = "course | lone | Lone\nunit | 1 | One\nlesson | int-01\n"
    plants.append(("a lesson requiring what only another course teaches, that course not a prerequisite",
                   lone, "int-01 requires"))
    red = 0
    for pname, text, why in plants:
        texts = {**course_texts, "lone.course": text} if text is lone else {**course_texts, name: text}
        problems = check_courses(texts, graph)[0]
        hit = [p for p in problems if why in p]
        print(f"{'ok  ' if hit else 'FAIL'} {pname}" + (f"\n       -> {hit[0]}" if hit else f": {problems[:2]}"))
        red += bool(hit)
    print(f"{red}/{len(plants)} course controls red as planted")
    with_pre = lone.replace("unit | 1", "prerequisite | algebra-to-calculus\nunit | 1")
    still = [p for p in check_courses({**course_texts, "lone.course": with_pre}, graph)[0] if "lone.course" in p]
    green = not still
    print(f"{'ok  ' if green else 'FAIL'} the same course naming the algebra course as its prerequisite is accepted"
          + ("" if green else f": {still[:2]}"))
    return red == len(plants) and green


def main():
    topics_text, lessons = load(ROOT)
    if "--selftest" in sys.argv:
        ok = selftest(topics_text, lessons)
        ok = selftest_courses(load_courses(ROOT), check(topics_text, lessons)[1]) and ok
        return 0 if ok else 1
    bad, graph = check(topics_text, lessons)
    cbad, graph["courses"] = check_courses(load_courses(ROOT), graph)
    bad += cbad
    if "--json" in sys.argv:
        print(json.dumps(graph, ensure_ascii=False, indent=1))
    for b in bad:
        print(f"GRAPH {b}", file=sys.stderr)
    edges = sum(len(v["needs"]) for v in graph["lessons"].values())
    listed = sum(len(u["lessons"]) for c in graph["courses"].values() for u in c["units"])
    print(f"graph: {len(graph['topics'])} topics, {len(graph['lessons'])}/{len(lessons)} lessons, "
          f"{edges} lesson links, {len(graph['courses'])} courses ({listed} lessons listed), {len(bad)} problems",
          file=sys.stderr)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
