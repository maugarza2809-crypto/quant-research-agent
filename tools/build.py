"""build.py — turns the artifact body into a standalone static page.

`src/page.html` is the exact body published as a Claude Artifact, where the
host supplies the document skeleton and serves the data files next to the
page. A static host supplies neither, so this script adds the skeleton and
repoints the four fetches at `data/`. One source, two targets, no drift.
"""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "src", "page.html")
OUT = os.path.join(ROOT, "index.html")

body = open(SRC, encoding="utf-8").read()

# the page asks for its data with bare relative names; on disk they live in data/
body, n = re.subn(r'fetch\("(indice\.json|term\.json|d_|t_)', r'fetch("data/\1', body)
if n != 4:
    sys.exit(f"expected 4 data fetches, rewrote {n} — check src/page.html")

title = re.search(r"<title>(.*?)</title>", body).group(1)

open(OUT, "w", encoding="utf-8").write(
    "<!doctype html>\n<html lang=\"en\">\n<head>\n"
    "<meta charset=\"utf-8\">\n"
    "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1,viewport-fit=cover\">\n"
    f"<meta name=\"description\" content=\"{title}: an autonomous quantitative research "
    "agent that pre-registers every hypothesis, deflates the bar for multiplicity and "
    "reports zero survivors.\">\n"
    "<style>*{box-sizing:border-box}body{margin:0}</style>\n"
    "</head>\n<body>\n" + body + "\n</body>\n</html>\n")

print(f"index.html written — {os.path.getsize(OUT)/1024:.0f} kB, {n} fetches repointed")
