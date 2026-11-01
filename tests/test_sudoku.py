import pytest
from helpers.file_helpers import load_puzzles
from helpers.validators import create_board, update_board
from services.sudoku_service import validate_board, analyse_entries

puzzle = load_puzzles()[0]


def test_initial_puzzle_is_valid_but_incomplete():
    result = validate_board(puzzle.board, puzzle.board)
    assert result.valid and not result.complete


def test_solution_is_valid_and_complete():
    result = validate_board(puzzle.board, puzzle.solution)
    assert result.valid and result.complete


def test_duplicate_row_rejected():
    board = tuple(tuple([5] * 9) if i == 0 else row for i, row in enumerate(puzzle.board))
    assert not validate_board(puzzle.board, board).valid


def test_fixed_cell_cannot_change():
    assert not validate_board(puzzle.board, update_board(puzzle.board, 0, 0, 1)).valid


@pytest.mark.parametrize("rows", [[], [[0]*9]*8, [[12]*9]*9, [[True]*9]*9])
def test_bad_inputs(rows):
    with pytest.raises(ValueError):
        create_board(rows)


def test_immutable_update():
    empty = create_board([[0]*9 for _ in range(9)])
    updated = update_board(empty, 0, 0, 9)
    assert empty[0][0] == 0 and updated[0][0] == 9


def test_entry_analysis():
    empty = create_board([[0]*9 for _ in range(9)])
    assert analyse_entries(empty) == {"filled": 0, "empty": 81, "sum": 0}
