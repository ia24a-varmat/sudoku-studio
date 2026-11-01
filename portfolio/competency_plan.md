# Kompetenzplan M323 – Sudoku Studio

| Feld | Feature / Fundort | Pflicht-Artefakt |
|---|---|---|
| A1B | `services/sudoku_service.py` | Prozedur und Pure Function nebeneinander: prozedurale Vergleichsvariante selbst erstellen |
| A1I | `helpers/validators.py:update_board` | Mutation und immutable Variante vergleichen |
| A1A | `validate_board` | OO, prozedural und funktional für exakt dieselbe Aufgabe vergleichen |
| B1B | `helpers/models.py`, `helpers/validators.py` | Immutable Types, Constructors, Composable Operators und Fundorte |
| B1I | `portfolio/design_b1i.md` | Design-Blatt vor Implementierung |
| B1A | `routes/sudoku_routes.py:check` | Imperative und deklarative Route vergleichen |
| C1B | `services/sudoku_service.py:validate_board` | Algorithmus mit Input-/Output-Durchlauf |
| C1I | `helpers/validators.py` | Teilfunktionen mit Signaturen |
| C1A | `validate_board` | Komposition, Tests und Edge Cases |
| C2B | `analyse_entries` | Funktion als Variable, map/filter/reduce separat |
| C2I | `recommend_challenge` | Lambda sowie verkettete map/filter/reduce |
| C2A | `rank_players` | Aggregation und benutzerdefinierte Sortierung |
| D1B | `helpers/validators.py` | 3 Refactoring-Techniken und 2 Performance-Massnahmen begründen |
| D1I | `validate_board` | Echte eigene Vorher-/Nachher-Commits und gleicher Testoutput |
| D1A | `services/performance_service.py` | Eigene Vorher-/Nachher-Messung und Datenstrukturwahl |

**Achtung:** Die fertige App allein erfüllt nicht alle Portfolio-Nachweise. Die Vergleichsvarianten, die echten Git-Commits und die selbst geschriebene Reflexion sind noch eigenständig zu erarbeiten.
