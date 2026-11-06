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

## Echte Open-Source-Rätsel laden (Dosuku)
Auf **Bibliothek** gehen und **Online-Sudoku hinzufügen** klicken. Flask ruft
`https://sudoku-api.vercel.app/api/dosuku` ab und speichert das Rätsel mit
Lösung und Schwierigkeitsgrad in `data/puzzles.json`. Die API benötigt laut
Dokumentation keinen Schlüssel. Unsere App prüft die erhaltenen Daten, bevor
sie gespeichert werden. Bei fehlender Internetverbindung bleiben alle bereits
lokal gespeicherten Rätsel nutzbar.

**Wichtig:** Die API liefert Sudoku-Rätsel, **keine Benutzerstatistiken**.
`data/results.json` beginnt leer und füllt sich erst mit selbst gespeicherten
Spielergebnissen. In der LB02 klar unterscheiden: externe Rätseldaten versus
eigene Ergebnisdaten. API-Quelle im Portfolio dokumentieren.

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
- JSON-Import speichert gültige neue Rätsel; JSON-Export der Bibliothek und CSV-Export der Resultate sind implementiert.
- D1I verlangt **echte** selbst erstellte Git-Vorher/Nachher-Commits, die hier nicht enthalten sind. Auch A1A verlangt noch eigene OO/prozedurale Vergleichsversionen.
- Vorhandene Demo-Rätsel beruhen auf einer festen gültigen Lösung, sind also für Logik-/UI-Demos gedacht und keine garantierten eindeutig lösbaren Rätsel.
- Ergebnisse werden lokal in `data/results.json` gespeichert; keine Anmeldung, keine Mehrbenutzer-Sicherheit. Nur lokal zu Lernzwecken verwenden.

## Zusätzliche Belege
- `services/paradigm_service.py`: echte A1B/A1I/A1A-Vergleichsvarianten.
- `services/response_service.py` und `routes/sudoku_routes.py`: deklarative und imperative B1A-Prüfroute.
- `services/refactoring_examples.py`: Gegenüberstellung gleichen Verhaltens für D1I, **kein Ersatz für Git-Commits**.
- `tests/test_portfolio_requirements.py`: Vergleichstests, Import/Export-Roundtrip, Edge Cases.
- Die persönlichen Statistiken bleiben leer, bis Ergebnisse gespeichert werden. Ein externer Forschungsdatensatz kann separat für offene Sudoku-Statistiken verwendet werden; er ist derzeit **nicht in die Anwendung importiert**.
- Flask-Integrationstests müssen in PyCharm ausgeführt werden; die ZIP enthält keine erfundene Testausgabe.

## Portfolio-PDFs und Abgabe
Die separat bereitgestellten 15 PDFs sind **Arbeitsfassungen** mit echten Code-Auszügen aus dieser Projektversion. Die Zeichenkontrolle steht in `Zeichenkontrolle.json`. Prüfe die noch offenen Punkte in `portfolio/ABGABE_CHECKLISTE.md`.
