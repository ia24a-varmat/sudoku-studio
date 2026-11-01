"""A1A comparison: the *same* no-duplicates check in three paradigms.

Use as a reference; analyse the tradeoffs yourself in your portfolio.
"""


class RowChecker:
    """OO version: stores the row in an object."""

    def __init__(self, row):
        self.row = list(row)

    def is_valid(self):
        numbers = [value for value in self.row if value != 0]
        return len(numbers) == len(set(numbers))


def check_row_procedural(row):
    """Procedural version: step-by-step accumulation with local mutation."""
    seen = []
    for value in row:
        if value == 0:
            continue
        if value in seen:
            return False
        seen.append(value)
    return True


def check_row_functional(row):
    """Functional version: immutable intermediate values, no mutations."""
    numbers = tuple(filter(lambda value: value != 0, row))
    return len(numbers) == len(frozenset(numbers))
