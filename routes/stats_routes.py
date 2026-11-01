from flask import Blueprint, render_template, current_app, Response
from helpers.file_helpers import load_results, export_results_csv
from services.statistics_service import calculate_statistics
from services.leaderboard_service import rank_players

stats_bp = Blueprint("stats", __name__)


@stats_bp.get("/statistics")
def statistics():
    data = calculate_statistics(load_results(current_app.config["RESULTS_PATH"]))
    return render_template("statistics.html", stats=data)


@stats_bp.get("/leaderboard")
def leaderboard():
    players = rank_players(load_results(current_app.config["RESULTS_PATH"]))
    return render_template("leaderboard.html", players=players)


@stats_bp.get("/export/results.csv")
def export_results():
    content = export_results_csv(load_results(current_app.config["RESULTS_PATH"]))
    return Response(content, mimetype="text/csv; charset=utf-8",
                    headers={"Content-Disposition": "attachment; filename=results.csv"})
