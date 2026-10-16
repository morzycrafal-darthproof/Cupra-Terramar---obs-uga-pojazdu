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

## Synchronizacja z Arkuszem Google

Wspólnym źródłem danych jest arkusz „Cupra Terramar - dane” na Dysku Google
(ID i identyfikator klienta OAuth: stała `GOOGLE` w `src/app.jsx`).

- Aplikacja działa na kopii lokalnej; każda zmiana trafia do kolejki. Synchronizacja pobiera arkusz,
  nakłada kolejkę, przelicza dystans / spalanie i zapisuje zakładki, które się zmieniły.
- Pierwsze połączenie dopisuje do arkusza wpisy, które są tylko na urządzeniu; w pozostałych wygrywa arkusz.
- Wiersz, którego nie da się odczytać, blokuje zapis (nic nie zostanie nadpisane) do czasu poprawki.
- Logowanie: przekierowanie OAuth (token na godzinę, odnawiany bez pytania przez `prompt=none`).
  Adresy powrotu muszą być wpisane w kliencie „Cupra PWA” w Google Cloud.
- Testy na kopii arkusza: `localStorage["cupra-terramar-sheet-override"] = "<ID kopii>"`.
