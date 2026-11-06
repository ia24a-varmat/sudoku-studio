"""Deklarativere Datenaufbereitung für das HTTP-Prüfergebnis (B1A)."""
from helpers.validators import create_board
from services.sudoku_service import validate_board, analyse_entries


def make_check_response(original, raw_board):
    """Pure Function: erstellt Daten und Status ohne Flask-Abhängigkeit."""
    try:
        board = create_board(raw_board)
    except ValueError as exc:
        return {"valid": False, "complete": False, "message": str(exc)}, 400
    result = validate_board(original, board)
    return {
        "valid": result.valid,
        "complete": result.complete,
        "message": result.message,
        "analysis": analyse_entries(board),
    }, 200
