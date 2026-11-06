"""API parser and route tests without calling an external service."""
import json

import pytest
from helpers.file_helpers import load_puzzles
from services.api_service import parse_api_puzzle


def api_payload():
    puzzle = load_puzzles()[0]
    return {"newboard": {"grids": [{
        "value": [list(row) for row in puzzle.board],
        "solution": [list(row) for row in puzzle.solution],
        "difficulty": "Easy",
    }]}}


def test_parse_api_puzzle_returns_immutable_board():
    puzzle = parse_api_puzzle(api_payload())
    assert puzzle.id.startswith("api-")
    assert puzzle.difficulty == "easy"
    assert isinstance(puzzle.board, tuple)
    assert isinstance(puzzle.board[0], tuple)


def test_reject_invalid_solution():
    payload = api_payload()
    payload["newboard"]["grids"][0]["solution"][0] = [1] * 9
    with pytest.raises(ValueError):
        parse_api_puzzle(payload)


def test_online_import_route_saves_once(client, monkeypatch):
    # No internet during tests: simulate an external API response.
    puzzle = parse_api_puzzle(api_payload())
    monkeypatch.setattr("routes.main_routes.fetch_dosuku_puzzle", lambda: puzzle)
    response = client.post("/library/online", follow_redirects=True)
    assert response.status_code == 200
    assert "Online-Sudoku gespeichert!" in response.get_data(as_text=True)
    assert puzzle.id in response.get_data(as_text=True)
    response = client.post("/library/online", follow_redirects=True)
    assert "bereits in deiner Bibliothek" in response.get_data(as_text=True)
