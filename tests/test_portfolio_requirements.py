"""Tests der Pflicht-Artefakte; benötigt Flask nur für Test der Routen."""
import json
from helpers.file_helpers import load_puzzles, parse_puzzles_json, import_puzzles_to_library, export_puzzles_json
from helpers.validators import create_board
from services.paradigm_service import (RowChecker, check_row_procedural, check_row_functional, check_row_procedure,
                                       change_cell_mutable, change_cell_immutable)
from services.refactoring_examples import rules_before, rules_after
from services.response_service import make_check_response


def test_paradigms_same_result():
    for row, expected in [((1, 0, 3, 4, 0, 6, 0, 0, 0), True),
                          ((1, 0, 3, 4, 1, 6, 0, 0, 0), False)]:
        assert RowChecker(row).is_valid() == expected
        assert check_row_procedural(row) == expected
        assert check_row_functional(row) == expected


def test_procedure_has_visible_effect():
    messages = []
    check_row_procedure((1, 1, 0, 0, 0, 0, 0, 0, 0), messages)
    assert messages == ["ungültig"]


def test_mutable_and_immutable_changes_keep_original():
    board = create_board([[0] * 9 for _ in range(9)])
    mutable = change_cell_mutable(board, 1, 2, 6)
    immutable = change_cell_immutable(board, 1, 2, 6)
    assert tuple(map(tuple, mutable)) == immutable
    assert board[1][2] == 0


def test_refactor_equivalence_edge_cases():
    good = load_puzzles()[0].solution
    bad = create_board([[1] * 9 for _ in range(9)])
    assert rules_before(good) is True and rules_after(good) is True
    assert rules_before(bad) is False and rules_after(bad) is False


def test_pure_response_success_and_bad_input():
    puzzle = load_puzzles()[0]
    assert make_check_response(puzzle.board, puzzle.solution)[0]["complete"] is True
    assert make_check_response(puzzle.board, [])[1] == 400


def test_json_import_export_roundtrip_and_duplicates(tmp_path):
    source = tmp_path / "puzzles.json"
    original = load_puzzles()
    source.write_text(export_puzzles_json(original), encoding="utf-8")
    assert parse_puzzles_json(export_puzzles_json(original).encode()) == original
    assert import_puzzles_to_library(original[:1], source) == 0
    extra = original[0]
    from dataclasses import replace
    extra = replace(extra, id="new-example")
    assert import_puzzles_to_library((extra,), source) == 1
    assert len(load_puzzles(source)) == len(original) + 1


def test_json_import_rejects_bad_solution():
    records = json.loads(export_puzzles_json(load_puzzles()[:1]))
    records[0]["solution"][0] = [1] * 9
    import pytest
    with pytest.raises(ValueError):
        parse_puzzles_json(json.dumps(records).encode())


def test_routes_decl_and_imp_equal(client):
    puzzle = load_puzzles()[0]
    for board in [puzzle.board, puzzle.solution, []]:
        d = client.post("/api/check/001", json={"board": board})
        i = client.post("/api/check-imperative/001", json={"board": board})
        assert d.status_code == i.status_code
        assert d.json == i.json
    assert client.get("/export/puzzles.json").status_code == 200
