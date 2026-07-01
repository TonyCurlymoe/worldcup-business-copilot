from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_dashboard_contains_teams_and_matches():
    response = client.get("/dashboard")
    assert response.status_code == 200
    payload = response.json()
    assert payload["teams"]
    assert payload["matches"]


def test_match_analysis_demo_mode():
    response = client.post("/analysis/match", json={"home_team": "Brazil", "away_team": "France"})
    assert response.status_code == 200
    assert response.json()["confidence"] > 0
