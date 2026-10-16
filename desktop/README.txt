CUPRA TERRAMAR — Dziennik pokładowy (wersja desktopowa Python)
================================================================

URUCHOMIENIE
------------
1. Zainstaluj Pythona 3.9+ (jeśli jeszcze nie masz): https://www.python.org/downloads/
   Windows: podczas instalacji zaznacz "Add python.exe to PATH".

2. Zainstaluj wymagane biblioteki (CustomTkinter — interfejs, matplotlib — wykresy, Pillow — grafika):
       py -m pip install -r requirements.txt

   Uwaga (Linux): tkinter czasem trzeba doinstalować osobno:
       sudo apt install python3-tk

3. Uruchom aplikację:
       py cupra_terramar_gui.py

DANE
----
Dane zapisują się automatycznie w pliku:
   Windows:  C:\Users\<Ty>\.cupra_terramar\data.json
   Mac/Linux: ~/.cupra_terramar/data.json

Kopię zapasową możesz zrobić w zakładce Ustawienia -> "Eksportuj kopię".
Plik kopii ma ten sam format co w aplikacji na telefon (PWA).

SYNCHRONIZACJA Z ARKUSZEM GOOGLE
--------------------------------
Ustawienia -> "Arkusz Google" -> "Połącz z Google". Wspólne dane z aplikacją na telefon są w arkuszu
„Cupra Terramar - dane”. Potrzebne pliki w C:\Users\<Ty>\.cupra_terramar\ (nigdy w repozytorium):
   client_secret.json   klient OAuth typu „Aplikacja komputerowa” z Google Cloud
   google_token.json    zapisywany po pierwszym zalogowaniu
   sync.json            kolejka zmian czekających na wysłanie
Zmiany wysyłają się same chwilę po zapisie, przy starcie programu i co 10 minut; bez internetu czekają w kolejce.

FUNKCJE
-------
- Pulpit: wskaźnik średniego spalania, kafelki KPI, wykresy kosztów i spalania
  (najedź myszą na wykres, żeby zobaczyć wartość z danego miesiąca)
- Tankowania / Serwisy / Koszty: listy pogrupowane miesiącami; dodawanie, edycja
  (ikona ołówka lub podwójne kliknięcie) i usuwanie z potwierdzeniem
- Formularze: data DD.MM.RRRR z przyciskami Dziś / Wczoraj i kalendarzem, błędy pokazywane
  przy polach, podgląd ceny za litr, dystansu i spalania na żywo; Enter zapisuje, Esc zamyka
- Prognoza: szacowane koszty paliwa na 12 miesięcy do przodu
- Ustawienia: nazwa auta, progi spalania, założenia prognozy, kopia zapasowa (eksport/import .json)
- Ctrl+N: nowy wpis na bieżącej liście

GRAFIKA
-------
assets/ powstaje z logo skryptem:  py tools/make_assets.py <logo.png>
Ikony interfejsu pochodzą z systemowej czcionki Segoe Fluent Icons (Windows 10/11).
