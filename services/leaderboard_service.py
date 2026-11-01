from collections import defaultdict
from helpers.models import GameResult


def rank_players(results: tuple[GameResult, ...]) -> tuple[dict, ...]:
    """C2A: aggregate a separate feature, then use a custom sorting key."""
    groups: dict[str, list[GameResult]] = defaultdict(list)
    for result in results:
        groups[result.player].append(result)
    aggregated = ({"player": name, "solved": len(items),
                   "mistakes": sum(item.mistakes for item in items),
                   "average_seconds": round(sum(item.seconds for item in items) / len(items), 1)}
                  for name, items in groups.items())
    return tuple(sorted(aggregated, key=lambda p: (-p["solved"], p["mistakes"], p["average_seconds"], p["player"].lower())))
