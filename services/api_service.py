"""Fetch Sudoku puzzles from Dosuku; keep external I/O outside pure functions."""
import hashlib
import json
from urllib.error import URLError
from urllib.request import Request, urlopen

from helpers.models import Puzzle
from helpers.validators import create_board
from services.sudoku_service import validate_board

API_URL = "https://sudoku-api.vercel.app/api/dosuku"


def parse_api_puzzle(payload: object) -> Puzzle:
    """Pure function: convert an API response into a validated immutable Puzzle."""
    try:
        grid = payload["newboard"]["grids"][0]
        board = create_board(grid["value"])
        solution = create_board(grid["solution"])
        difficulty = grid["difficulty"].strip().lower()
    except (KeyError, IndexError, TypeError, AttributeError, ValueError) as exc:
        raise ValueError("Die API hat ungültige Rätseldaten geliefert.") from exc

    if difficulty not in {"easy", "medium", "hard"}:
        raise ValueError("Unbekannter Schwierigkeitsgrad der API.")
    if not validate_board(board, board).valid:
        raise ValueError("Das API-Rätsel ist ungültig.")
    result = validate_board(board, solution)
    if not (result.valid and result.complete):
        raise ValueError("Die API-Lösung ist nicht gültig oder passt nicht zum Rätsel.")

    # A stable ID means an identical puzzle won't be saved twice.
    puzzle_id = "api-" + hashlib.sha256(str(board).encode("utf-8")).hexdigest()[:12]
    return Puzzle(puzzle_id, difficulty, f"Online Sudoku ({difficulty.capitalize()})", board, solution)


def fetch_dosuku_puzzle() -> Puzzle:
    """I/O boundary: fetch one remote puzzle with a timeout and size limit."""
    request = Request(API_URL, headers={"User-Agent": "SudokuStudio-M323/1.0", "Accept": "application/json"})
    try:
        with urlopen(request, timeout=8) as response:
            raw = response.read(50_001)
        if len(raw) > 50_000:
            raise ValueError("Die API-Antwort ist zu gross.")
        payload = json.loads(raw.decode("utf-8"))
    except (URLError, TimeoutError, OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RuntimeError("Online-Rätsel konnten nicht geladen werden. Bitte später erneut versuchen.") from exc
    return parse_api_puzzle(payload)
