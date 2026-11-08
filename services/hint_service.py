"""Funktionale Verarbeitung von Sudoku-Hinweisen."""

from helpers.models import Board


def choose_hint_cell(
    original: Board,
    current: Board,
    solution: Board,
    selected: tuple[int, int] | None = None
) -> tuple[int, int] | None:
    """
    Sucht ein geeignetes Feld für einen Hinweis.

    Die Funktion verändert keine vorhandenen Daten.
    """

    candidates = tuple(
        (row, col)

        for row in range(9)
        for col in range(9)

        if (
            original[row][col] == 0
            and current[row][col] != solution[row][col]
        )
    )

    if selected in candidates:
        return selected

    return candidates[0] if candidates else None