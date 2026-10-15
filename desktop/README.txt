CUPRA TERRAMAR — Dziennik pokładowy (wersja desktopowa Python)
================================================================

URUCHOMIENIE
------------
1. Zainstaluj Pythona 3.9+ (jeśli jeszcze nie masz): https://www.python.org/downloads/
   Windows: podczas instalacji zaznacz "Add python.exe to PATH".

2. Zainstaluj wymaganą bibliotekę (tylko jedna — matplotlib do wykresów):
       pip install -r requirements.txt

   Uwaga (Linux): tkinter czasem trzeba doinstalować osobno:
       sudo apt install python3-tk

3. Uruchom aplikację:
       python cupra_terramar_gui.py

DANE
----
Dane zapisują się automatycznie w pliku:
   Windows:  C:\Users\<Ty>\.cupra_terramar\data.json
   Mac/Linux: ~/.cupra_terramar/data.json

Kopię zapasową możesz zrobić w zakładce Ustawienia -> "Eksportuj kopię".

FUNKCJE
-------
- Pulpit: wskaźnik średniego spalania, KPI, wykresy kosztów i spalania
- Tankowania / Serwisy / Koszty: listy z możliwością dodawania i usuwania wpisów
- Prognoza: szacowane koszty paliwa na 12 miesięcy do przodu
- Ustawienia: progi spalania, nazwa auta, kopia zapasowa danych (eksport/import .json)
