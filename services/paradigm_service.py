"""Vergleichsvarianten für A1B, A1I und A1A: gleiche Zeilenregel."""
from helpers.validators import update_board, has_no_duplicates


class RowChecker:
    """OO: die Zeile gehört zum Zustand eines Objekts."""
    def __init__(self, row):
        self.row = list(row)

    def is_valid(self):
        values = [value for value in self.row if value != 0]
        return len(values) == len(set(values))


def check_row_procedure(row, log):
    """A1B: Prozedur mit Seiteneffekt auf einer übergebenen Liste."""
    log.append("gültig" if check_row_procedural(row) else "ungültig")


def check_row_procedural(row):
    """Prozedural: die lokale Liste `seen` wird Schritt für Schritt erweitert."""
    seen = []
    for value in row:
        if value == 0:
            continue
        if value in seen:
            return False
        seen.append(value)
    return True


def check_row_functional(row):
    """Funktional: unveränderliche Zwischendaten, keine Seiteneffekte."""
    return has_no_duplicates(tuple(row))


def change_cell_mutable(board, row, col, number):
    """A1I: bewusst veränderbare Kopie eines Boards."""
    changed = [list(line) for line in board]
    changed[row][col] = number
    return changed


def change_cell_immutable(board, row, col, number):
    """A1I: unverändertes Original; neues Tuple-Board als Ergebnis."""
    return update_board(board, row, col, number)
