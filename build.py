"""Buduje index.html z src/ i vendor/ oraz podbija wersję cache w sw.js.

    py build.py                   # kompilacja src/app.jsx Babelem (wymaga Node.js + npm install)
    py build.py --compiled X.js   # pomija Babela, wkleja gotowy, skompilowany JS
    py build.py --no-bump         # nie zmienia sw.js

Kolejność składania:
    src/head.html + vendor/react + vendor/react-dom + skompilowany src/app.jsx + src/foot.html
"""
import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
VENDOR = ROOT / "vendor"
INDEX = ROOT / "index.html"
SW = ROOT / "sw.js"
CACHE_RE = re.compile(r'cupra-terramar-v(\d+)')


def read(p):
    return p.read_text(encoding="utf-8")


def compile_jsx():
    npx = shutil.which("npx")
    if not npx:
        sys.exit("Brak Node.js (npx). Zainstaluj Node LTS z https://nodejs.org, potem `npm install`.")
    if not (ROOT / "node_modules" / "@babel" / "cli").exists():
        sys.exit("Brak zależności Babela. Uruchom najpierw: npm install")
    # konfiguracja (runtime: classic) w babel.config.json
    res = subprocess.run([npx, "--no-install", "babel", "src/app.jsx"], cwd=ROOT,
                         capture_output=True, text=True, encoding="utf-8")
    if res.returncode != 0:
        sys.exit("Babel zwrócił błąd:\n" + res.stderr)
    return res.stdout


def check_compiled(js):
    # runtime: 'automatic' wstawia importy -> "Cannot use import statement outside a module"
    if re.search(r'^\s*import\s', js, re.M) or "jsx-runtime" in js:
        sys.exit("Skompilowany kod zawiera import/jsx-runtime — sprawdź runtime: 'classic' w babel.config.json")
    if "React.createElement" not in js:
        sys.exit("Skompilowany kod nie zawiera React.createElement — czy to na pewno wynik kompilacji JSX?")
    if "</script" in js:
        sys.exit("Skompilowany kod zawiera '</script' — zamknąłby tag <script> w index.html")


def assemble(app_js):
    return (read(SRC / "head.html")
            + "<script>" + read(VENDOR / "react.production.min.js") + "</script>\n"
            + "<script>" + read(VENDOR / "react-dom.production.min.js") + "</script>\n"
            + "<script>\n" + app_js.strip("\n") + "\n"
            + read(SRC / "foot.html"))


def bump_sw():
    sw = read(SW)
    m = CACHE_RE.search(sw)
    if not m:
        sys.exit("Nie znaleziono 'cupra-terramar-vN' w sw.js")
    new = f"cupra-terramar-v{int(m.group(1)) + 1}"
    SW.write_text(sw[:m.start()] + new + sw[m.end():], encoding="utf-8", newline="")
    return m.group(0), new


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--compiled", type=Path, help="gotowy skompilowany JS zamiast uruchamiania Babela")
    ap.add_argument("--no-bump", action="store_true", help="nie podbijaj wersji cache w sw.js")
    args = ap.parse_args()

    app_js = read(args.compiled) if args.compiled else compile_jsx()
    check_compiled(app_js)
    html = assemble(app_js)

    old = read(INDEX) if INDEX.exists() else None
    if html == old:
        print("index.html bez zmian — sw.js nie jest podbijany.")
        return
    INDEX.write_text(html, encoding="utf-8", newline="")
    print(f"index.html zapisany ({len(html.encode('utf-8')) / 1024:.0f} KB)")
    if args.no_bump:
        print("sw.js pominięty (--no-bump) — pamiętaj o podbiciu wersji przed wdrożeniem!")
    else:
        before, after = bump_sw()
        print(f"sw.js: {before} -> {after}")


if __name__ == "__main__":
    main()
