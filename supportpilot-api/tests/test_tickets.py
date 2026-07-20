from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_and_list_tickets():
    response = client.post(
        "/api/tickets",
        json={
            "subject": "VPN not working",
            "description": "The VPN connection keeps failing",
            "severity": "High",
            "priority": "P1",
            "status": "Open",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["subject"] == "VPN not working"
    assert body["category"] in {"Network", "Unknown"}
    assert body["confidence"] >= 0

    list_response = client.get("/api/tickets")
    assert list_response.status_code == 200
    tickets = list_response.json()
    assert any(ticket["ticket_id"] == body["ticket_id"] for ticket in tickets)
