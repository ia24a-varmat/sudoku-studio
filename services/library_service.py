from helpers.models import Puzzle


def find_puzzle(puzzles: tuple[Puzzle, ...], puzzle_id: str) -> Puzzle | None:
    return next((p for p in puzzles if p.id == puzzle_id), None)


def search_puzzles(puzzles: tuple[Puzzle, ...], query: str = "", difficulty: str = "", sort: str = "id") -> tuple[Puzzle, ...]:
    matching = filter(lambda p: query.lower() in (p.id + " " + p.title).lower(), puzzles)
    matching = filter(lambda p: not difficulty or p.difficulty == difficulty, matching)
    keys = {"id": lambda p: p.id, "title": lambda p: p.title.lower(),
            "difficulty": lambda p: ({"easy": 0, "medium": 1, "hard": 2}.get(p.difficulty, 3), p.id)}
    return tuple(sorted(matching, key=keys.get(sort, keys["id"])))
