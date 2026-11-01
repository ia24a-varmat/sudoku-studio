# 🧩 Sudoku Studio – M323 LB02

Flask-Webapp mit Sudoku-Prüfung, Rätselbibliothek, Challenge, Statistiken, CSV-Export und Bestenliste.

## Start in PyCharm (Windows)
1. Projektordner `sudoku-studio` in PyCharm öffnen.
2. Unter **Settings → Project → Python Interpreter** eine virtuelle Umgebung (`.venv`) mit Python 3.12 oder neuer wählen/erstellen.
3. Im PyCharm-Terminal ausführen:
   ```powershell
   python -m pip install -r requirements.txt
   python app.py
   ```
4. Im Browser `http://127.0.0.1:5000` öffnen.

## Tests
```powershell
python -m pytest -v
```

## Performance
```powershell
python portfolio/benchmarks/benchmark_d1a.py
```

## Struktur
- `routes/` HTTP und HTML
- `services/` Anwendungslogik
- `helpers/` Immutable Datenmodelle, Validierung und Datei-I/O
- `templates/`, `static/` Frontend
- `data/` lokale Demo-Daten
- `tests/` Pytest
- `portfolio/` Planung und Nachweis-Hilfen

## Hinweise für LB02
- Dies ist ein **funktionierender Ausgangscode**, nicht die fertige LB02-Dokumentation.
- C2B: Eingabeanalyse; C2I: Challenge; C2A: Bestenliste – drei getrennte Features.
- Import validiert derzeit nur JSON als **Vorschau** und speichert nichts; CSV-Export ist implementiert.
- D1I verlangt **echte** selbst erstellte Git-Vorher/Nachher-Commits, die hier nicht enthalten sind. Auch A1A verlangt noch eigene OO/prozedurale Vergleichsversionen.
- Vorhandene Demo-Rätsel beruhen auf einer festen gültigen Lösung, sind also für Logik-/UI-Demos gedacht und keine garantierten eindeutig lösbaren Rätsel.
- Ergebnisse werden lokal in `data/results.json` gespeichert; keine Anmeldung, keine Mehrbenutzer-Sicherheit. Nur lokal zu Lernzwecken verwenden.
