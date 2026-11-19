#!/usr/bin/env python3
"""fetch-sources.py: fetch the texts that the lessons quote into sources/cache/, as plain text.

    python3 scripts/fetch-sources.py            # fetch what is missing, then report each text's sha256
    python3 scripts/fetch-sources.py --force    # fetch everything again

sources/SOURCES.tsv lists each source: its id, what it is, where it was read, and the sha256 of the text
this script writes. tools/check.py finds every ```quote``` block's words in that text (T65: every history
claim from a text opened and cached). The cache is never committed, because one of the texts is still in
copyright and is quoted only briefly. Run this on a machine with network access and `pdftotext`
(poppler); the check needs only the files it writes. A text whose sha256 differs from the table's is
reported: the source changed upstream, and the quotes must be read against it again before the table is
updated.
"""
import argparse
import hashlib
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CACHE = os.path.join(ROOT, "sources", "cache")
UA = {"User-Agent": "stu32-tutor-sources/0.1"}


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r:
        return r.read()


def html_text(h):
    """A rendered page's text: tags dropped, paragraphs kept."""
    h = re.sub(r"<style.*?</style>", "", h, flags=re.S)
    h = re.sub(r"<br\s*/?>", "\n", h)
    h = re.sub(r"</p>|</div>|</tr>", "\n", h)
    h = re.sub(r"</td>", " ", h)
    t = html.unescape(re.sub(r"<[^>]+>", "", h))
    return re.sub(r"\n\s*\n+", "\n\n", t).strip() + "\n"


def wikisource_pages(index, first, last, first_page):
    """The Page: namespace pages first..last of a Wikisource index, rendered, each headed by its printed page."""
    out = []
    for n in range(first, last + 1):
        q = urllib.parse.urlencode({"action": "parse", "page": f"Page:{index}/{n}", "prop": "text", "format": "json",
                                    "formatversion": "2"})
        h = json.loads(get(f"https://fr.wikisource.org/w/api.php?{q}"))["parse"]["text"]
        out.append(f"[p. {first_page + n - first}]\n" + html_text(h))
    return "\n".join(out)


def gutenberg_tex(url):
    """A Project Gutenberg TeX source, its licence header and footer cut (what is left is the public-domain
    work)."""
    raw = get(url)
    try:
        t = raw.decode("utf-8")
    except UnicodeDecodeError:
        t = raw.decode("latin-1")           # ebook 15114's TeX is Latin-1
    a = t.find("*** START OF THIS PROJECT GUTENBERG EBOOK")
    a = t.find("\n", a) + 1 if a >= 0 else 0      # from the line after it: the title page on
    b = t.find("\\chapter{PROJECT GUTENBERG")
    return t[a:b if b > 0 else len(t)]


def pdf_text(url):
    if not shutil.which("pdftotext"):
        raise SystemExit("pdftotext (poppler) is needed for a PDF source")
    with tempfile.TemporaryDirectory() as d:
        pdf = os.path.join(d, "s.pdf")
        open(pdf, "wb").write(get(url))
        subprocess.run(["pdftotext", "-layout", pdf, os.path.join(d, "s.txt")], check=True)
        return open(os.path.join(d, "s.txt"), encoding="utf-8").read()


FETCH = {
    "leibniz-1703": lambda: wikisource_pages("Leibniz-en.francais-Gerhardt.Math.1a7.djvu", 528, 532, 223),
    "boole-1854": lambda: gutenberg_tex("https://archive.org/download/aninvestigationo15114gut/15114-t.tex"),
    "shannon-1937": lambda: pdf_text("https://dspace.mit.edu/server/api/core/bitstreams/"
                                     "0428777a-799c-45b7-a2ed-5207da683e53/content"),
}


def table():
    rows = {}
    for line in open(os.path.join(ROOT, "sources", "SOURCES.tsv"), encoding="utf-8"):
        if line.startswith("#") or not line.strip():
            continue
        f = line.rstrip("\n").split("\t")
        rows[f[0]] = f
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    os.makedirs(CACHE, exist_ok=True)
    rows, bad = table(), 0
    for sid, row in rows.items():
        if sid not in FETCH:
            print(f"FAIL {sid}: no fetcher in scripts/fetch-sources.py")
            bad += 1
            continue
        p = os.path.join(CACHE, f"{sid}.txt")
        if a.force or not os.path.exists(p) or not os.path.getsize(p):
            text = FETCH[sid]()                 # fetched whole before anything is written: no half file is left
            open(p + ".part", "w", encoding="utf-8", newline="\n").write(text)
            os.replace(p + ".part", p)
        h = hashlib.sha256(open(p, "rb").read()).hexdigest()
        if h == row[-1]:
            print(f"ok   {sid} {h}")
        else:
            print(f"DIFF {sid} {h} (the table has {row[-1]}): read the quotes against it before updating the table")
            bad += 1
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
