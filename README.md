# Cupra Terramar — Dziennik pokładowy

Aplikacja do śledzenia tankowań, serwisów, kosztów i prognozy wydatków.

- **PWA** (główna): `index.html` + `sw.js` + `manifest.json` + ikony, hostowane na GitHub Pages
- **Desktop**: `desktop/cupra_terramar_gui.py` (tkinter + matplotlib), opis w `desktop/README.txt`

## Struktura

| Ścieżka | Rola |
|---|---|
| `src/app.jsx` | **źródło aplikacji** — tu wprowadzamy zmiany |
| `src/head.html`, `src/foot.html` | początek i koniec `index.html` (meta, style, ekran startowy, rejestracja SW) |
| `vendor/` | React 18.3.1 i ReactDOM (UMD, wklejane inline) |
| `build.py` | skleja `index.html` i podbija wersję cache w `sw.js` |
| `index.html` | **plik wynikowy** — nie edytować ręcznie |

## Budowanie

Jednorazowo: zainstaluj [Node.js LTS](https://nodejs.org), potem w katalogu repo:

```
npm install
```

Po każdej zmianie w `src/`:

```
py build.py
```

Skrypt kompiluje JSX Babelem (`runtime: 'classic'`, bez modułów ES), składa `index.html`
i — jeśli plik się zmienił — podbija `cupra-terramar-vN` w `sw.js`, żeby telefon pobrał nową wersję.
Opcje: `--no-bump` (bez zmiany `sw.js`), `--compiled plik.js` (pomija Babela).
