"""Gleiches Verhalten vor und nach dem Refactoring als prüfbarer Vergleich.

D1I benötigt darüber hinaus echte Vorher/Nachher-Commits aus deinem Repository.
"""
from helpers.validators import check_row, check_column, check_box


def rules_before(board):
    """Eher imperative Version mit mehreren Schleifen."""
    for i in range(9):
        if not check_row(board, i):
            return False
    for i in range(9):
        if not check_column(board, i):
            return False
    for r in range(3):
        for c in range(3):
            if not check_box(board, r, c):
                return False
    return True


def rules_after(board):
    """Aufgeteilte/zusammengesetzte Version mit all()."""
    return (all(check_row(board, i) for i in range(9))
            and all(check_column(board, i) for i in range(9))
            and all(check_box(board, r, c) for r in range(3) for c in range(3)))
