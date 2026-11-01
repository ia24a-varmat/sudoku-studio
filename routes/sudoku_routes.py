from flask import Blueprint, render_template, request, jsonify, abort, current_app
from helpers.file_helpers import load_puzzles, load_results, save_results
from helpers.models import GameResult
from helpers.validators import create_board
from services.library_service import find_puzzle
from services.sudoku_service import validate_board, analyse_entries
from services.challenge_service import recommend_challenge

sudoku_bp = Blueprint("sudoku", __name__)


def get_puzzle(puzzle_id):
    puzzle = find_puzzle(load_puzzles(), puzzle_id)
    if puzzle is None:
        abort(404)
    return puzzle


@sudoku_bp.get("/play/<puzzle_id>")
def play(puzzle_id):
    return render_template("sudoku.html", puzzle=get_puzzle(puzzle_id))


@sudoku_bp.get("/challenge")
def challenge():
    difficulty = request.args.get("difficulty", "easy")
    results = load_results(current_app.config["RESULTS_PATH"])
    completed = frozenset(r.puzzle_id for r in results)
    puzzle = recommend_challenge(load_puzzles(), difficulty, completed)
    if puzzle is None:
        return render_template("challenge_empty.html", difficulty=difficulty)
    return render_template("sudoku.html", puzzle=puzzle)


@sudoku_bp.post("/api/check/<puzzle_id>")
def check(puzzle_id):
    puzzle = get_puzzle(puzzle_id)
    try:
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            raise ValueError("Ungültige JSON-Eingabe.")
        board = create_board(payload.get("board"))
    except ValueError as exc:
        return jsonify({"valid": False, "complete": False, "message": str(exc)}), 400
    outcome = validate_board(puzzle.board, board)
    return jsonify({"valid": outcome.valid, "complete": outcome.complete, "message": outcome.message,
                    "analysis": analyse_entries(board)})


@sudoku_bp.post("/api/submit/<puzzle_id>")
def submit(puzzle_id):
    puzzle = get_puzzle(puzzle_id)
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({"error": "Ungültige Eingabe."}), 400
    try:
        board = create_board(payload.get("board"))
        seconds = payload.get("seconds")
        mistakes = payload.get("mistakes")
        player = payload.get("player", "Gast")
        if (type(seconds) is not int or not 0 <= seconds <= 86_400
                or type(mistakes) is not int or not 0 <= mistakes <= 999
                or not isinstance(player, str) or not 1 <= len(player.strip()) <= 30):
            raise ValueError("Name, Zeit oder Fehlerzahl ungültig.")
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    state = validate_board(puzzle.board, board)
    if not state.complete or board != puzzle.solution:
        return jsonify({"error": "Sudoku ist nicht vollständig korrekt gelöst."}), 400
    entry = GameResult(player.strip(), puzzle.id, puzzle.difficulty, seconds, mistakes)
    path = current_app.config["RESULTS_PATH"]
    save_results(load_results(path) + (entry,), path)
    return jsonify({"saved": True, "message": "Ergebnis gespeichert!"})
