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

def normalise_selected(
    selected: object
) -> tuple[int, int] | None:
    """
    Prüft eine ausgewählte Sudoku-Position.

    Ungültige Werte werden mit None beantwortet.
    """

    if not isinstance(selected, list):
        return None

    if len(selected) != 2:
        return None

    if not all(
        type(value) is int and 0 <= value <= 8
        for value in selected
    ):
        return None

    return selected[0], selected[1]