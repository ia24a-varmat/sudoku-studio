from helpers.models import Puzzle


def filter_unsolved_list(puzzles: tuple[Puzzle, ...], completed_ids: list[str]) -> tuple[Puzzle, ...]:
    return tuple(p for p in puzzles if p.id not in completed_ids)


def filter_unsolved_set(puzzles: tuple[Puzzle, ...], completed_ids: frozenset[str]) -> tuple[Puzzle, ...]:
    return tuple(p for p in puzzles if p.id not in completed_ids)
