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
# el <title> pasa al <head>; dejarlo tambien en el cuerpo duplicaria la etiqueta
body = body.replace(f"<title>{title}</title>\n", "", 1).replace(f"<title>{title}</title>", "", 1)

URL = "https://maugarza2809-crypto.github.io/quant-research-agent/"
DESC = ("An autonomous research agent that pre-registered 11,514 hypotheses, measured 50,794 "
        "configurations against a deflated bar of t >= 4.24, and found zero survivors. "
        "Interactive: a backtest engine over 547,569 real H1 bars and a trading terminal.")

# Sin estas etiquetas el <head> no tenia ni titulo: ningun rastreador podia construir una
# vista previa, y LinkedIn rechazaba el enlace por eso. El <title> del cuerpo es el que ve
# la pestana; este es el que ven los rastreadores.
open(OUT, "w", encoding="utf-8").write(
    "<!doctype html>\n<html lang=\"en\">\n<head>\n"
    "<meta charset=\"utf-8\">\n"
    "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1,viewport-fit=cover\">\n"
    f"<title>{title}</title>\n"
    f"<meta name=\"description\" content=\"{DESC}\">\n"
    "<meta name=\"author\" content=\"Mauricio Alan Garza Oyanguren\">\n"
    "<link rel=\"canonical\" href=\"" + URL + "\">\n"
    "<meta property=\"og:type\" content=\"website\">\n"
    f"<meta property=\"og:title\" content=\"{title} - zero survivors out of 11,514 hypotheses\">\n"
    f"<meta property=\"og:description\" content=\"{DESC}\">\n"
    "<meta property=\"og:url\" content=\"" + URL + "\">\n"
    "<meta property=\"og:image\" content=\"" + URL + "og.png\">\n"
    "<meta property=\"og:image:width\" content=\"1200\">\n"
    "<meta property=\"og:image:height\" content=\"630\">\n"
    f"<meta property=\"og:image:alt\" content=\"{title}: 11,514 pre-registered hypotheses, zero survivors\">\n"
    "<meta property=\"og:site_name\" content=\"Hypothesis Ledger\">\n"
    "<meta name=\"twitter:card\" content=\"summary_large_image\">\n"
    f"<meta name=\"twitter:title\" content=\"{title} - zero survivors out of 11,514 hypotheses\">\n"
    f"<meta name=\"twitter:description\" content=\"{DESC}\">\n"
    "<meta name=\"twitter:image\" content=\"" + URL + "og.png\">\n"
    "<style>*{box-sizing:border-box}body{margin:0}</style>\n"
    "</head>\n<body>\n" + body + "\n</body>\n</html>\n")

print(f"index.html written — {os.path.getsize(OUT)/1024:.0f} kB, {n} fetches repointed")
