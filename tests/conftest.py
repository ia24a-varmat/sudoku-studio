import pytest
from app import create_app


@pytest.fixture
def client(tmp_path):
    app = create_app({"TESTING": True, "RESULTS_PATH": tmp_path / "results.json"})
    return app.test_client()
