# Sudoku Studio – LB02 Abgabe-Check

Stand: Überarbeitung des zuvor bereitgestellten Projektarchivs, 6. November 2026.

## Prüfung nach Pflicht-Artefakt

| Feld | Beleg im Projekt | Stand |
|---|---|---|
| A1B | `services/paradigm_service.py`: Prozedur mit Log und Pure Function | Beispiel vorhanden; Selbsttest in PyCharm offen |
| A1I | `services/paradigm_service.py`, `helpers/validators.py`: mutable und immutable Änderung | Beispiel vorhanden; Selbsttest in PyCharm offen |
| A1A | `RowChecker`, `check_row_procedural`, `check_row_functional` | Vergleichsbeispiele vorhanden |
| B1B | `helpers/models.py`, `helpers/validators.py`, `services/sudoku_service.py` | Fundorte dokumentiert |
| B1I | `portfolio/design_b1i.md` | Design-Blatt vorhanden; **Nachweis, dass Planung VOR einer Implementierungsänderung entstand, fehlt** |
| B1A | `routes/sudoku_routes.py`, `services/response_service.py` | Zwei unterschiedliche Routenvarianten vorhanden |
| C1B | `services/sudoku_service.py:validate_board` | Beispieldurchlauf im PDF |
| C1I | `helpers/validators.py` | Teilfunktionen mit Signaturen |
| C1A | `validate_board`, `tests/test_sudoku.py` | Edge Cases und Testentwurf vorhanden |
| C2B | `services/sudoku_service.py:analyse_entries` | map/filter/reduce einzeln |
| C2I | `services/challenge_service.py:recommend_challenge` | anderes Feature, Verkettung und Lambda |
| C2A | `services/leaderboard_service.py:rank_players` | drittes Feature, Aggregation und Sortierung |
| D1B | Vergleichsversionen und PDF D1B | Techniken und Massnahmen benannt |
| D1I | `services/refactoring_examples.py`, Vergleichstests | **Echte eigene Vorher/Nachher-Commits fehlen im Archiv** |
| D1A | `services/performance_service.py`, `portfolio/benchmarks/d1a_results.txt` | timeit in Python 3.13.5 ausgeführt; **eigene Messung in PyCharm wiederholen** |

## Technische Kontrolle

- Fehler in `helpers/validators.py:update_board` behoben: statt nicht definierter Variable `c` wird der korrekte Spaltenindex benutzt.
- JSON-Rätselimport wurde von einer Vorschau zu einem tatsächlichen Import erweitert und kontrolliert Rätsel und Lösung.
- JSON-Export der Bibliothek und CSV-Export der Spielergebnisse stehen zur Verfügung.
- Eine alternative imperative Route sowie eine deklarativere Route wurden ergänzt.
- Kernfunktionen und JSON-Roundtrip wurden in einer Python-Sitzung direkt geprüft, `compileall` ohne Syntaxfehler.
- **Flask war in der zur Erstellung verwendeten Ausführungsumgebung nicht installiert.** Deshalb ist **nicht belegt**, dass alle Flask-Integrationstests erfolgreich laufen.

## Vor Abgabe zwingend selber erledigen

1. ZIP-Projekt in PyCharm mit deinem Repository vergleichen, Änderungen übernehmen, `.git`, `.venv` sowie vorhandene `data/results.json` sicher behalten.
2. `python -m pip install -r requirements.txt`, `python -m pytest -v`, `python app.py` in PyCharm ausführen und Ergebnisse kontrollieren.
3. B1I: Bei der nächsten Feature-Änderung ein Design-Blatt nachweisbar vor dem Code committen.
4. D1I: Eigene echte Git-Vorher/Nachher-Commits aus dem Entwicklungsprozess dokumentieren und mit Tests belegen. Keine Commits oder Screenshots erfinden.
5. D1A: `python portfolio/benchmarks/benchmark_d1a.py` in PyCharm ausführen und eigene Messwerte im Lernnachweis eintragen.
6. Die Reflexion in jedem der 15 PDFs selbst schreiben. Codebeispiele nach Änderungen aktualisieren.
7. Für das Forschungsprojekt mit Open-Source-Spielerstatistiken ist **noch keine echte externe Statistikdatei eingebunden**. Die App berechnet bisher persönliche Statistiken aus `data/results.json`. Diese beginnen leer. Das ist für das Kompetenzraster nicht zwingend, aber eine zuvor gewünschte Erweiterung.
8. Vor der Abgabe alle 15 PDFs mit dem endgültigen Code und der tatsächlichen Git-Historie abstimmen.

## Belegsammlung

- 15 PDFs in `Sudoku_Studio_LB02_Lernnachweise.zip` (separater Download).
- Zeichenzahl-Kontrolle in `Zeichenkontrolle.json`.
- Die PDFs enthalten keine erfundenen persönlichen Reflexionen. Die Testfälle sind als erwartete Ergebnisse formuliert, solange sie nicht aus PyCharm nachgewiesen sind.
