from helpers.file_helpers import load_puzzles


def test_pages(client):
    for path in ["/", "/library", "/statistics", "/leaderboard", "/play/001"]:
        assert client.get(path).status_code == 200


def test_check_endpoint(client):
    puzzle = load_puzzles()[0]
    response = client.post("/api/check/001", json={"board": puzzle.board})
    assert response.status_code == 200 and response.json["valid"]


def test_submit_only_correct_solution(client):
    puzzle = load_puzzles()[0]
    payload = {"board": puzzle.board, "player": "Tanu", "seconds": 100, "mistakes": 0}
    assert client.post("/api/submit/001", json=payload).status_code == 400
    payload["board"] = puzzle.solution
    assert client.post("/api/submit/001", json=payload).json["saved"]
    assert "Tanu" in client.get("/leaderboard").get_data(as_text=True)


def test_bad_input(client):
    assert client.post("/api/check/001", json={"board": []}).status_code == 400
    assert client.get("/play/does-not-exist").status_code == 404


def test_csv_export(client):
    response = client.get("/export/results.csv")
    assert response.status_code == 200
    assert "player,puzzle_id" in response.get_data(as_text=True)
