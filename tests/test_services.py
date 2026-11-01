from helpers.file_helpers import load_puzzles, export_results_csv
from helpers.models import GameResult
from services.library_service import search_puzzles
from services.challenge_service import recommend_challenge
from services.statistics_service import calculate_statistics
from services.leaderboard_service import rank_players
from services.performance_service import filter_unsolved_list, filter_unsolved_set


def test_filter_library():
    result = search_puzzles(load_puzzles(), difficulty="hard")
    assert len(result) == 2 and all(p.difficulty == "hard" for p in result)


def test_challenge_excludes_completed():
    result = recommend_challenge(load_puzzles(), "easy", frozenset({"001"}))
    assert result is not None and result.id == "002"


def test_challenge_no_matches():
    assert recommend_challenge(load_puzzles(), "unknown", frozenset()) is None


def test_statistics_empty():
    assert calculate_statistics(())["solved"] == 0


def test_leaderboard_sort():
    results = (GameResult("B", "1", "easy", 120, 0), GameResult("A", "2", "hard", 200, 1),
               GameResult("A", "3", "easy", 100, 0))
    assert rank_players(results)[0]["player"] == "A"
    assert calculate_statistics(results)["solved"] == 3
    assert "player,puzzle_id" in export_results_csv(results)


def test_optimisation_preserves_output():
    puzzles = load_puzzles()
    assert filter_unsolved_list(puzzles, ["001", "004"]) == filter_unsolved_set(puzzles, frozenset({"001", "004"}))
