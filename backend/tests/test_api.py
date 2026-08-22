import os
os.environ["DATABASE_URL"] = "sqlite:///./test_matchpoint.db"
from fastapi.testclient import TestClient
from app.main import app
client = TestClient(app)

def test_health(): assert client.get("/health").status_code == 200
def test_same_player_rejected():
    p = client.post("/players", json={"name":"Test Player", "city":"Bolzano", "level":3}).json()
    response = client.post("/matches", json={"player_one_id":p["id"], "player_two_id":p["id"], "scheduled_at":"2026-09-01T18:00:00", "venue":"Club"})
    assert response.status_code == 422


