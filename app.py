import os
from pathlib import Path
from flask import Flask
from routes.main_routes import main_bp
from routes.sudoku_routes import sudoku_bp
from routes.stats_routes import stats_bp


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.update(SECRET_KEY=os.environ.get("SECRET_KEY", "dev-only-change-me"),
                      RESULTS_PATH=Path(__file__).resolve().parent / "data" / "results.json",
                      PUZZLES_PATH=Path(__file__).resolve().parent / "data" / "puzzles.json",
                      MAX_CONTENT_LENGTH=300_000)
    if test_config:
        app.config.update(test_config)
    app.register_blueprint(main_bp)
    app.register_blueprint(sudoku_bp)
    app.register_blueprint(stats_bp)
    return app


if __name__ == "__main__":
    create_app().run(debug=True)
