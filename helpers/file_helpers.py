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
    if len(content) > 300_000:
        raise ValueError("Datei ist zu gross (maximal 300 KB).")
    try:
        records = json.loads(content.decode("utf-8"))
        if not isinstance(records, list) or len(records) > 100:
            raise ValueError("Erwartet wird eine Liste mit maximal 100 Rätseln.")
        result = []
        for item in records:
            board = create_board(item["board"])
            solution = create_board(item["solution"])
            result.append(Puzzle(str(item["id"]), str(item["difficulty"]), str(item["title"]), board, solution))
        return tuple(result)
    except (UnicodeDecodeError, json.JSONDecodeError, KeyError, TypeError) as exc:
        raise ValueError("Ungültige JSON-Rätseldatei.") from exc
