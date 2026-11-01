from helpers.models import GameResult


def calculate_statistics(results: tuple[GameResult, ...]) -> dict:
    if not results:
        return {"solved": 0, "average_seconds": 0, "total_mistakes": 0, "by_difficulty": {}}
    by_difficulty = {level: sum(r.difficulty == level for r in results)
                     for level in ("easy", "medium", "hard")}
    return {"solved": len(results),
            "average_seconds": round(sum(r.seconds for r in results) / len(results), 1),
            "total_mistakes": sum(r.mistakes for r in results),
            "by_difficulty": by_difficulty}
