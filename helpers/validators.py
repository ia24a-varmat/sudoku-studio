from helpers.models import Board


def create_board(rows: object) -> Board:
    """Convert submitted values into immutable 9x9 board, or raise ValueError."""
    if not isinstance(rows, (list, tuple)) or len(rows) != 9:
        raise ValueError("Das Sudoku braucht genau 9 Zeilen.")
    output = []
    for row in rows:
        if not isinstance(row, (list, tuple)) or len(row) != 9:
            raise ValueError("Jede Zeile braucht genau 9 Zellen.")
        converted = []
        for value in row:
            if type(value) is int and 0 <= value <= 9:
                converted.append(value)
            elif isinstance(value, str) and (value == "" or value in "0123456789"):
                converted.append(int(value) if value else 0)
            else:
                raise ValueError("Erlaubt sind nur Zahlen von 0 bis 9.")
        output.append(tuple(converted))
    return tuple(output)


def has_no_duplicates(values: tuple[int, ...]) -> bool:
    nonempty = tuple(filter(lambda value: value != 0, values))
    return len(nonempty) == len(set(nonempty))


def check_row(board: Board, index: int) -> bool:
    return has_no_duplicates(board[index])


def check_column(board: Board, index: int) -> bool:
    return has_no_duplicates(tuple(row[index] for row in board))


def check_box(board: Board, box_row: int, box_col: int) -> bool:
    values = tuple(board[r][c]
                   for r in range(box_row * 3, box_row * 3 + 3)
                   for c in range(box_col * 3, box_col * 3 + 3))
    return has_no_duplicates(values)


def check_fixed_cells(original: Board, current: Board) -> bool:
    return all(original[r][c] == 0 or original[r][c] == current[r][c]
               for r in range(9) for c in range(9))


def update_board(board: Board, row: int, col: int, value: int) -> Board:
    if not (0 <= row < 9 and 0 <= col < 9 and type(value) is int and 0 <= value <= 9):
        raise ValueError("Ungültiger Index oder Wert.")
    return tuple(tuple(value if (r, column) == (row, col) else cell
                       for column, cell in enumerate(values))
                 for r, values in enumerate(board))
