"""Tests für das Refactoring der Sudoku-Hinweisfunktion."""

from helpers.file_helpers import load_puzzles


def get_test_puzzle():
    """Lädt ein Sudoku aus der Bibliothek."""
    return load_puzzles()[0]


def test_hint_without_selection(client):
    """Ohne Auswahl wird das erste geeignete Feld verwendet."""

    puzzle = get_test_puzzle()

    expected = next(
        (row, col)
        for row in range(9)
        for col in range(9)
        if puzzle.board[row][col] == 0
    )

    response = client.post(
        f"/api/hint/{puzzle.id}",
        json={"board": puzzle.board}
    )

    assert response.status_code == 200

    row, col = expected

    assert response.get_json() == {
        "row": row,
        "col": col,
        "value": puzzle.solution[row][col]
    }


def test_hint_selected_cell(client):
    """Ein ausgewähltes Feld wird bevorzugt."""

    puzzle = get_test_puzzle()

    selected = next(
        (row, col)
        for row in reversed(range(9))
        for col in reversed(range(9))
        if puzzle.board[row][col] == 0
    )

    response = client.post(
        f"/api/hint/{puzzle.id}",
        json={
            "board": puzzle.board,
            "selected": list(selected)
        }
    )

    assert response.status_code == 200

    row, col = selected

    assert response.get_json() == {
        "row": row,
        "col": col,
        "value": puzzle.solution[row][col]
    }


def test_invalid_board(client):
    """Ungültige Sudoku-Daten werden abgelehnt."""

    puzzle = get_test_puzzle()

    response = client.post(
        f"/api/hint/{puzzle.id}",
        json={"board": []}
    )

    assert response.status_code == 400
    assert "error" in response.get_json()


def test_completed_sudoku(client):
    """Ein vollständig gelöstes Sudoku braucht keinen Hinweis."""

    puzzle = get_test_puzzle()

    response = client.post(
        f"/api/hint/{puzzle.id}",
        json={"board": puzzle.solution}
    )

    assert response.status_code == 400
    assert "error" in response.get_json()


def test_unknown_puzzle(client):
    """Eine unbekannte Sudoku-ID gibt 404 zurück."""

    response = client.post(
        "/api/hint/does-not-exist",
        json={"board": []}
    )

    assert response.status_code == 404


def test_invalid_selection(client):
    """Eine ungültige Feldauswahl wird ignoriert."""

    puzzle = get_test_puzzle()

    expected = next(
        (row, col)
        for row in range(9)
        for col in range(9)
        if puzzle.board[row][col] == 0
    )

    response = client.post(
        f"/api/hint/{puzzle.id}",
        json={
            "board": puzzle.board,
            "selected": [99, 99]
        }
    )

    assert response.status_code == 200

    row, col = expected

    assert response.get_json() == {
        "row": row,
        "col": col,
        "value": puzzle.solution[row][col]
    }