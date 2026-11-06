import pytest
from shutil import copyfile
from helpers.file_helpers import DATA_DIR
from app import create_app


@pytest.fixture
def client(tmp_path):
    puzzles_path = tmp_path / "puzzles.json"
    copyfile(DATA_DIR / "puzzles.json", puzzles_path)
    app = create_app({"TESTING": True, "RESULTS_PATH": tmp_path / "results.json",
                      "PUZZLES_PATH": puzzles_path})
    return app.test_client()
