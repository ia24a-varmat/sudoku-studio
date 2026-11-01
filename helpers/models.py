from dataclasses import dataclass
from typing import TypeAlias

Board: TypeAlias = tuple[tuple[int, ...], ...]


@dataclass(frozen=True)
class Puzzle:
    id: str
    difficulty: str
    title: str
    board: Board
    solution: Board


@dataclass(frozen=True)
class CheckResult:
    valid: bool
    complete: bool
    message: str


@dataclass(frozen=True)
class GameResult:
    player: str
    puzzle_id: str
    difficulty: str
    seconds: int
    mistakes: int
