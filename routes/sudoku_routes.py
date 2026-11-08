from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    abort,
    current_app
)

from helpers.file_helpers import (
    load_puzzles,
    load_results,
    save_results
)

from helpers.models import GameResult

from helpers.validators import (
    create_board,
    check_fixed_cells
)

from services.library_service import find_puzzle

from services.sudoku_service import (
    validate_board,
    analyse_entries
)

from services.challenge_service import recommend_challenge
from services.response_service import make_check_response


# Flask Blueprint
sudoku_bp = Blueprint("sudoku", __name__)


# =====================================================
# SUDOKU LADEN
# =====================================================

def get_puzzle(puzzle_id):
    """Lädt ein Sudoku anhand seiner ID."""

    puzzles = load_puzzles(
        current_app.config["PUZZLES_PATH"]
    )

    puzzle = find_puzzle(puzzles, puzzle_id)

    if puzzle is None:
        abort(404)

    return puzzle


# =====================================================
# SUDOKU SPIELEN
# =====================================================

@sudoku_bp.get("/play/<puzzle_id>")
def play(puzzle_id):
    """Zeigt das ausgewählte Sudoku an."""

    puzzle = get_puzzle(puzzle_id)

    return render_template(
        "sudoku.html",
        puzzle=puzzle
    )


# =====================================================
# TAGES-CHALLENGE
# =====================================================

@sudoku_bp.get("/challenge")
def challenge():
    """Wählt ein passendes Sudoku aus."""

    difficulty = request.args.get(
        "difficulty",
        "easy"
    )

    results = load_results(
        current_app.config["RESULTS_PATH"]
    )

    completed = frozenset(
        result.puzzle_id
        for result in results
    )

    puzzles = load_puzzles(
        current_app.config["PUZZLES_PATH"]
    )

    puzzle = recommend_challenge(
        puzzles,
        difficulty,
        completed
    )

    if puzzle is None:
        return render_template(
            "challenge_empty.html",
            difficulty=difficulty
        )

    return render_template(
        "sudoku.html",
        puzzle=puzzle
    )


# =====================================================
# SUDOKU PRÜFEN - DEKLARATIV
# =====================================================

@sudoku_bp.post("/api/check/<puzzle_id>")
def check(puzzle_id):
    """Prüft das Sudoku mit funktionaler Logik."""

    puzzle = get_puzzle(puzzle_id)

    payload = request.get_json(silent=True)

    raw = (
        payload.get("board")
        if isinstance(payload, dict)
        else None
    )

    data, status = make_check_response(
        puzzle.board,
        raw
    )

    return jsonify(data), status


# =====================================================
# SUDOKU PRÜFEN - IMPERATIV
# Für Kompetenz B1A
# =====================================================

@sudoku_bp.post("/api/check-imperative/<puzzle_id>")
def check_imperative(puzzle_id):
    """Imperative Vergleichsvariante."""

    puzzle = get_puzzle(puzzle_id)

    try:
        payload = request.get_json(silent=True)

        if not isinstance(payload, dict):
            raise ValueError(
                "Das Sudoku braucht genau 9 Zeilen."
            )

        board = create_board(
            payload.get("board")
        )

    except ValueError as exc:

        return jsonify({
            "valid": False,
            "complete": False,
            "message": str(exc)
        }), 400

    outcome = validate_board(
        puzzle.board,
        board
    )

    data = {
        "valid": outcome.valid,
        "complete": outcome.complete,
        "message": outcome.message,
        "analysis": analyse_entries(board)
    }

    return jsonify(data), 200


# =====================================================
# ERGEBNIS SPEICHERN
# =====================================================

@sudoku_bp.post("/api/submit/<puzzle_id>")
def submit(puzzle_id):
    """Speichert ein erfolgreich gelöstes Sudoku."""

    puzzle = get_puzzle(puzzle_id)

    payload = request.get_json(silent=True)

    if not isinstance(payload, dict):
        return jsonify({
            "error": "Ungültige Eingabe."
        }), 400

    try:
        board = create_board(
            payload.get("board")
        )

        seconds = payload.get("seconds")
        mistakes = payload.get("mistakes")
        player = payload.get("player", "Gast")

        if (
            type(seconds) is not int
            or not 0 <= seconds <= 86_400
            or type(mistakes) is not int
            or not 0 <= mistakes <= 999
            or not isinstance(player, str)
            or not 1 <= len(player.strip()) <= 30
        ):
            raise ValueError(
                "Name, Zeit oder Fehlerzahl ungültig."
            )

    except ValueError as exc:

        return jsonify({
            "error": str(exc)
        }), 400

    # Sudoku validieren
    state = validate_board(
        puzzle.board,
        board
    )

    if not state.complete:

        return jsonify({
            "error": "Sudoku ist nicht vollständig korrekt gelöst."
        }), 400

    # Spielergebnis erstellen
    entry = GameResult(
        player.strip(),
        puzzle.id,
        puzzle.difficulty,
        seconds,
        mistakes
    )

    # Ergebnis speichern
    path = current_app.config["RESULTS_PATH"]

    results = load_results(path)

    save_results(
        results + (entry,),
        path
    )

    return jsonify({
        "saved": True,
        "message": "Ergebnis gespeichert!"
    })


# =====================================================
# HINWEIS-FUNKTION
# =====================================================

@sudoku_bp.post("/api/hint/<puzzle_id>")
def hint(puzzle_id):
    """Gibt eine richtige Zahl als Hinweis zurück."""

    puzzle = get_puzzle(puzzle_id)

    payload = request.get_json(silent=True)

    if not isinstance(payload, dict):
        return jsonify({
            "error": "Ungültige Eingabe."
        }), 400

    try:
        board = create_board(
            payload.get("board")
        )

    except ValueError as exc:

        return jsonify({
            "error": str(exc)
        }), 400

    fixed_values_unchanged = check_fixed_cells(
        puzzle.board,
        board
    )

    if not fixed_values_unchanged:
        return jsonify({
            "error": "Eine vorgegebene Zahl wurde verändert."
        }), 400

    # Felder suchen, die einen Hinweis benötigen.
    candidates = [
        (row, col)

        for row in range(9)
        for col in range(9)

        if (
            puzzle.board[row][col] == 0
            and board[row][col] != puzzle.solution[row][col]
        )
    ]

    if not candidates:

        return jsonify({
            "error": "Kein Hinweis mehr verfügbar."
        }), 400

    # Ausgewähltes Feld bevorzugen.
    selected = payload.get("selected")

    if (
        isinstance(selected, list)
        and len(selected) == 2
        and all(
            type(value) is int and 0 <= value <= 8
            for value in selected
        )
        and tuple(selected) in candidates
    ):
        row, col = selected

    else:
        row, col = candidates[0]

    # Nur eine korrekte Zahl zurückgeben.
    return jsonify({
        "row": row,
        "col": col,
        "value": puzzle.solution[row][col]
    })