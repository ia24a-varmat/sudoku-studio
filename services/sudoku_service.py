from helpers.models import Board, CheckResult
from helpers.validators import (create_board, check_row, check_column,
                                check_box, check_fixed_cells)


def validate_board(original: Board, current: Board) -> CheckResult:
    """Pure Sudoku validation; a valid incomplete board is not solved."""
    try:
        original, current = create_board(original), create_board(current)
    except ValueError as exc:
        return CheckResult(False, False, str(exc))
    if not check_fixed_cells(original, current):
        return CheckResult(False, False, "Eine vorgegebene Zahl wurde verändert.")
    if not all(check_row(current, i) for i in range(9)):
        return CheckResult(False, False, "Doppelte Zahl in einer Zeile.")
    if not all(check_column(current, i) for i in range(9)):
        return CheckResult(False, False, "Doppelte Zahl in einer Spalte.")
    if not all(check_box(current, r, c) for r in range(3) for c in range(3)):
        return CheckResult(False, False, "Doppelte Zahl in einem 3x3-Block.")
    complete = all(cell != 0 for row in current for cell in row)
    return CheckResult(True, complete, "Sudoku gelöst!" if complete else "Bisher gültig, aber noch nicht fertig.")


def analyse_entries(board: Board) -> dict[str, int]:
    """C2B: function variable, and map/filter/reduce separately on board data."""
    from functools import reduce
    cells = tuple(value for row in create_board(board) for value in row)
    transform = lambda value: int(value != 0)  # Function stored in a variable
    filled_flags = tuple(map(transform, cells))
    nonempty = tuple(filter(lambda value: value != 0, cells))
    total = reduce(lambda acc, value: acc + value, nonempty, 0)
    return {"filled": sum(filled_flags), "empty": 81 - len(nonempty), "sum": total}
