"""D1A: Performance-Vergleich für Sudoku Studio."""

import platform
import sys

from dataclasses import replace
from pathlib import Path
from timeit import repeat


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))


from helpers.file_helpers import load_puzzles

from services.performance_service import (
    filter_unsolved_list,
    filter_unsolved_set
)


def create_test_data():
    """Erstellt eine grössere Sudoku-Bibliothek."""

    example = load_puzzles()[0]

    # 1500 verschiedene Sudoku-IDs
    puzzles = tuple(
        replace(
            example,
            id=f"sudoku-{index:05d}"
        )
        for index in range(1500)
    )

    # Simulierte ältere Spielergebnisse
    completed = [
        f"historisch-{index:05d}"
        for index in range(3000)
    ]

    # Zusätzlich ist jedes zweite Test-Sudoku abgeschlossen
    completed.extend(
        puzzle.id
        for puzzle in puzzles[::2]
    )

    return puzzles, completed


def main():

    puzzles, completed_list = create_test_data()

    completed_set = frozenset(completed_list)

    # Ergebnisse vergleichen
    result_list = filter_unsolved_list(
        puzzles,
        completed_list
    )

    result_set = filter_unsolved_set(
        puzzles,
        completed_set
    )

    assert result_list == result_set

    assert len(result_list) == 750

    # Messung mit Liste
    list_times = repeat(
        lambda: filter_unsolved_list(
            puzzles,
            completed_list
        ),
        repeat=5,
        number=3
    )

    # Messung mit bereits erstelltem Frozenset
    set_times = repeat(
        lambda: filter_unsolved_set(
            puzzles,
            completed_set
        ),
        repeat=5,
        number=3
    )

    # Frozenset inklusive Erstellung messen
    set_build_times = repeat(
        lambda: filter_unsolved_set(
            puzzles,
            frozenset(completed_list)
        ),
        repeat=5,
        number=3
    )

    list_best = min(list_times)
    set_best = min(set_times)
    set_build_best = min(set_build_times)

    report = f"""
D1A - Sudoku Studio Performance

Python-Version: {platform.python_version()}

Anzahl Sudoku-Rätsel: {len(puzzles)}
Anzahl abgeschlossener IDs: {len(completed_list)}

Messungen: 5
Durchläufe pro Messung: 3

Liste:
{list_best:.6f} Sekunden

Frozenset:
{set_best:.6f} Sekunden

Frozenset inklusive Erstellung:
{set_build_best:.6f} Sekunden

Ergebnisse identisch: Ja
"""

    print(report)

    destination = (
        Path(__file__).resolve().parent
        / "d1a_results_local.txt"
    )

    destination.write_text(
        report,
        encoding="utf-8"
    )


if __name__ == "__main__":
    main()