"""Run from project root: python portfolio/benchmarks/benchmark_d1a.py.

Measures the same operation on the same puzzle collection; no cached network data.
"""
import platform
import sys
from pathlib import Path
from timeit import repeat
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from helpers.file_helpers import load_puzzles
from services.performance_service import filter_unsolved_list, filter_unsolved_set

puzzles = load_puzzles() * 50  # deterministic larger input for a comparison
ids = [f"older-{i:05d}" for i in range(1000)] + [p.id for p in load_puzzles()[:3]]
ids_set = frozenset(ids)
assert filter_unsolved_list(puzzles, ids) == filter_unsolved_set(puzzles, ids_set)
print(f"Python: {platform.python_version()} | Puzzles: {len(puzzles)} | gespeicherte IDs: {len(ids)}")
for name, func in [("Liste", lambda: filter_unsolved_list(puzzles, ids)),
                   ("Frozenset", lambda: filter_unsolved_set(puzzles, ids_set))]:
    samples = repeat(func, number=20, repeat=5)
    print(f"{name}: beste Zeit für 20 Durchläufe = {min(samples):.6f} s | Messungen: {samples}")
