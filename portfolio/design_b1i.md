# B1I – Design-Blatt (Planung)

**Wichtig:** Diese Datei dokumentiert die geplante Architektur. Wird sie erst nach dem Code übernommen, sollte das Erstellungsdatum nicht als Beweis für eine frühere Planung ausgegeben werden.

## Deklarative Anforderungen
- Ein Board besteht aus genau 9 × 9 Zellen mit Werten 0–9; 0 steht für leer.
- Vorgegebene Zahlen bleiben unverändert.
- Nichtleere Werte sind in jeder Zeile, Spalte und jedem 3×3-Block eindeutig.
- Eine gültige unvollständige Eingabe darf nicht als gelöst gelten.
- Die Validierung verändert ihre Eingabewerte nicht.

## Datenfluss
Browser → Flask-Route (JSON) → create_board → validate_board → CheckResult → JSON → Browser.
Dateisystem und HTTP gehören zur I/O-Schicht, nicht zur Pure Function.

## Geplante Operatoren und Daten
Tuple of Tuples für Immutable Board; tuple() zum Erstellen, filter() zum Ausblenden leerer Felder, set() zur Duplikaterkennung, all() zur Kombination der Prüfungen. Funktion `validate_board` ruft die kleinen Prüffunktionen auf.

## Signaturen
- `create_board(rows: object) -> Board`
- `check_row(board: Board, index: int) -> bool`
- `check_column(board: Board, index: int) -> bool`
- `check_box(board: Board, box_row: int, box_col: int) -> bool`
- `check_fixed_cells(original: Board, current: Board) -> bool`
- `validate_board(original: Board, current: Board) -> CheckResult`
