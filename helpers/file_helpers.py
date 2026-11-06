"""I/O boundary: parsing and storage live outside pure services."""
import csv
import io
import json
from pathlib import Path
from helpers.models import GameResult, Puzzle
from helpers.validators import create_board

DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def load_puzzles(path: Path | None = None) -> tuple[Puzzle, ...]:
    source = path or DATA_DIR / "puzzles.json"
    records = json.loads(source.read_text(encoding="utf-8"))
    result = []
    for item in records:
        board, solution = create_board(item["board"]), create_board(item["solution"])
        result.append(Puzzle(str(item["id"]), item["difficulty"], item["title"], board, solution))
    return tuple(result)


def load_results(path: Path | None = None) -> tuple[GameResult, ...]:
    source = path or DATA_DIR / "results.json"
    if not source.exists():
        return ()
    return tuple(GameResult(**record) for record in json.loads(source.read_text(encoding="utf-8")))


def save_results(results: tuple[GameResult, ...], path: Path | None = None) -> None:
    source = path or DATA_DIR / "results.json"
    source.write_text(json.dumps([vars(result) for result in results], indent=2, ensure_ascii=False), encoding="utf-8")


def export_results_csv(results: tuple[GameResult, ...]) -> str:
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["player", "puzzle_id", "difficulty", "seconds", "mistakes"])
    for item in results:
        writer.writerow([item.player, item.puzzle_id, item.difficulty, item.seconds, item.mistakes])
    return output.getvalue()


def parse_puzzles_json(content: bytes) -> tuple[Puzzle, ...]:
    """Validate an import file and every proposed board/solution."""
    from services.sudoku_service import validate_board
    if len(content) > 300_000:
        raise ValueError("Datei ist zu gross (maximal 300 KB).")
    try:
        records = json.loads(content.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("Ungültige JSON-Rätseldatei.") from exc
    if not isinstance(records, list) or len(records) > 100:
        raise ValueError("Erwartet wird eine Liste mit maximal 100 Rätseln.")
    result = []
    seen = set()
    for item in records:
        try:
            puzzle_id = str(item["id"]).strip()
            title = item["title"]
            difficulty = item["difficulty"]
            board = create_board(item["board"])
            solution = create_board(item["solution"])
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError("Ein Rätsel hat ungültige Daten.") from exc
        if (not puzzle_id or len(puzzle_id) > 50 or puzzle_id in seen
                or not isinstance(title, str) or not 1 <= len(title.strip()) <= 80
                or not isinstance(difficulty, str)
                or difficulty not in {"easy", "medium", "hard"}):
            raise ValueError("ID, Titel oder Schwierigkeit ist ungültig oder doppelt.")
        if not validate_board(board, board).valid:
            raise ValueError(f"Rätsel {puzzle_id} verletzt Sudoku-Regeln.")
        check = validate_board(board, solution)
        if not (check.valid and check.complete):
            raise ValueError(f"Lösung zu {puzzle_id} ist nicht gültig.")
        seen.add(puzzle_id)
        result.append(Puzzle(puzzle_id, difficulty, title.strip(), board, solution))
    return tuple(result)


def import_puzzles_to_library(puzzles: tuple[Puzzle, ...], path: Path | None = None) -> int:
    """Save all nonduplicate puzzles after checking their IDs."""
    source = path or DATA_DIR / "puzzles.json"
    existing = load_puzzles(source)
    ids = {p.id: p for p in existing}
    added = []
    for puzzle in puzzles:
        if puzzle.id in ids:
            if ids[puzzle.id] != puzzle:
                raise ValueError(f"Die ID {puzzle.id} existiert bereits mit anderem Inhalt.")
            continue
        ids[puzzle.id] = puzzle
        added.append(puzzle)
    if added:
        all_items = existing + tuple(added)
        source.write_text(json.dumps([{
            "id": p.id, "difficulty": p.difficulty, "title": p.title,
            "board": [list(row) for row in p.board],
            "solution": [list(row) for row in p.solution]
        } for p in all_items], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return len(added)


def export_puzzles_json(puzzles: tuple[Puzzle, ...]) -> str:
    """Export library to portable JSON for round trips."""
    return json.dumps([{
        "id": p.id, "difficulty": p.difficulty, "title": p.title,
        "board": [list(row) for row in p.board],
        "solution": [list(row) for row in p.solution]
    } for p in puzzles], indent=2, ensure_ascii=False)


def add_puzzle_to_library(puzzle: Puzzle, path: Path | None = None) -> bool:
    """Persist an API puzzle; return False if this exact puzzle already exists."""
    source = path or DATA_DIR / "puzzles.json"
    existing = load_puzzles(source)
    if any(item.id == puzzle.id for item in existing):
        return False
    records = json.loads(source.read_text(encoding="utf-8"))
    records.append({
        "id": puzzle.id,
        "title": puzzle.title,
        "difficulty": puzzle.difficulty,
        "board": [list(row) for row in puzzle.board],
        "solution": [list(row) for row in puzzle.solution],
    })
    source.write_text(json.dumps(records, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return True
