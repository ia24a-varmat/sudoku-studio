from flask import Blueprint, render_template, request, redirect, url_for, flash
from helpers.file_helpers import load_puzzles, parse_puzzles_json
from services.library_service import search_puzzles

main_bp = Blueprint("main", __name__)


@main_bp.get("/")
def index():
    return render_template("index.html")


@main_bp.get("/library")
def library():
    puzzles = search_puzzles(load_puzzles(), request.args.get("q", ""),
                             request.args.get("difficulty", ""), request.args.get("sort", "id"))
    return render_template("library.html", puzzles=puzzles)


@main_bp.post("/import")
def import_puzzles():
    """Validate uploaded JSON; preview count without writing untrusted data to disk."""
    upload = request.files.get("file")
    if not upload or not upload.filename.lower().endswith(".json"):
        flash("Bitte eine JSON-Datei wählen.")
        return redirect(url_for("main.library"))
    try:
        puzzles = parse_puzzles_json(upload.read())
        flash(f"{len(puzzles)} Rätsel erfolgreich geprüft (Vorschau, nicht gespeichert).")
    except ValueError as exc:
        flash(str(exc))
    return redirect(url_for("main.library"))
