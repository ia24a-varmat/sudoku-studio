"""Run: python portfolio/benchmarks/benchmark_d1a.py (from project root)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from timeit import repeat
from helpers.file_helpers import load_puzzles
from services.performance_service import filter_unsolved_list, filter_unsolved_set

puzzles = load_puzzles() * 100
ids = [str(i).zfill(3) for i in range(1, 3000)]
ids_set = frozenset(ids)
assert filter_unsolved_list(puzzles, ids) == filter_unsolved_set(puzzles, ids_set)
for name, func in [("Liste", lambda: filter_unsolved_list(puzzles, ids)),
                   ("Set", lambda: filter_unsolved_set(puzzles, ids_set))]:
    samples = repeat(func, number=100, repeat=5)
    print(f"{name}: beste Zeit für 100 Durchläufe = {min(samples):.6f} s")
