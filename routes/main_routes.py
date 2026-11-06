from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, Response
from helpers.file_helpers import (load_puzzles, parse_puzzles_json, add_puzzle_to_library,
                                  import_puzzles_to_library, export_puzzles_json)
from services.library_service import search_puzzles
from services.api_service import fetch_dosuku_puzzle

main_bp = Blueprint("main", __name__)


@main_bp.get("/")
def index():
    return render_template("index.html")


@main_bp.get("/library")
def library():
    puzzles = search_puzzles(load_puzzles(current_app.config["PUZZLES_PATH"]), request.args.get("q", ""),
                             request.args.get("difficulty", ""), request.args.get("sort", "id"))
    return render_template("library.html", puzzles=puzzles)


@main_bp.post("/import")
def import_puzzles():
    """Validate uploaded JSON and store nonduplicate puzzles."""
    upload = request.files.get("file")
    if not upload or not upload.filename.lower().endswith(".json"):
        flash("Bitte eine JSON-Datei wählen.")
        return redirect(url_for("main.library"))
    try:
        puzzles = parse_puzzles_json(upload.read())
        count = import_puzzles_to_library(puzzles, current_app.config["PUZZLES_PATH"])
        flash(f"{count} neue Rätsel importiert. ({len(puzzles) - count} bereits vorhanden.)")
    except (ValueError, OSError) as exc:
        flash(str(exc))
    return redirect(url_for("main.library"))


@main_bp.post("/library/online")
def import_online_puzzle():
    """Fetch a real public Sudoku puzzle and add it to the local library."""
    try:
        puzzle = fetch_dosuku_puzzle()
        added = add_puzzle_to_library(puzzle, current_app.config["PUZZLES_PATH"])
    except (ValueError, RuntimeError, OSError) as exc:
        flash(str(exc))
    else:
        flash("Online-Sudoku gespeichert!" if added else "Dieses Sudoku ist bereits in deiner Bibliothek.")
    return redirect(url_for("main.library"))


@main_bp.get("/export/puzzles.json")
def export_puzzles():
    content = export_puzzles_json(load_puzzles(current_app.config["PUZZLES_PATH"]))
    return Response(content, mimetype="application/json; charset=utf-8",
                    headers={"Content-Disposition": "attachment; filename=puzzles.json"})
