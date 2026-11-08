"""Tests für den Performance-Vergleich in D1A."""

from helpers.file_helpers import load_puzzles

from services.performance_service import (
    filter_unsolved_list,
    filter_unsolved_set
)


def test_same_results():
    """Liste und Frozenset liefern dieselben Rätsel."""

    puzzles = load_puzzles()

    completed = ["001", "004"]

    result_list = filter_unsolved_list(
        puzzles,
        completed
    )

    result_set = filter_unsolved_set(
        puzzles,
        frozenset(completed)
    )

    assert result_list == result_set


def test_no_completed_puzzles():
    """Ohne abgeschlossene IDs bleiben alle Rätsel übrig."""

    puzzles = load_puzzles()

    result_list = filter_unsolved_list(
        puzzles,
        []
    )

    result_set = filter_unsolved_set(
        puzzles,
        frozenset()
    )

    assert result_list == puzzles
    assert result_set == puzzles


def test_all_completed():
    """Wenn alle Rätsel gelöst sind, bleibt keines übrig."""

    puzzles = load_puzzles()

    completed = [puzzle.id for puzzle in puzzles]

    result_list = filter_unsolved_list(
        puzzles,
        completed
    )

    result_set = filter_unsolved_set(
        puzzles,
        frozenset(completed)
    )

    assert result_list == ()
    assert result_set == ()


def test_original_data_unchanged():
    """Die Funktionen verändern ihre Eingabedaten nicht."""

    puzzles = load_puzzles()

    completed = ["001", "002"]
    original_completed = completed.copy()

    filter_unsolved_list(
        puzzles,
        completed
    )

    filter_unsolved_set(
        puzzles,
        frozenset(completed)
    )

    assert completed == original_completed