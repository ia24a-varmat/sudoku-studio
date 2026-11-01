from functools import reduce
from helpers.models import Puzzle


def recommend_challenge(puzzles: tuple[Puzzle, ...], difficulty: str,
                        completed_ids: frozenset[str]) -> Puzzle | None:
    """C2I: map/filter/reduce in a separate recommendation feature."""
    candidates = filter(lambda puzzle: puzzle.difficulty == difficulty and puzzle.id not in completed_ids, puzzles)
    scored = map(lambda puzzle: (sum(cell == 0 for row in puzzle.board for cell in row), puzzle), candidates)

    def choose_fewer_blanks(best, candidate):
        if best is None or candidate[0] < best[0]:
            return candidate
        return best

    selected = reduce(choose_fewer_blanks, scored, None)
    return selected[1] if selected is not None else None
