from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

SAMPLE_HARNESS = {
    "name": "Test Harness",
    "connectors": [
        {
            "id": "CONN1",
            "manufacturer": "TE",
            "part_number": "1-234567-8",
            "pins": [{"id": "1"}, {"id": "2"}],
        },
        {
            "id": "CONN2",
            "manufacturer": "Molex",
            "part_number": "98765-4321",
            "pins": [{"id": "A"}, {"id": "B"}],
        },
    ],
    "wires": [
        {
            "id": "W1",
            "manufacturer": "Alpha Wire",
            "part_number": "1234/5",
            "color": "Red",
            "gauge": 22.0,
            "length": 100.0,
        },
        {
            "id": "W2",
            "manufacturer": "Alpha Wire",
            "part_number": "1234/5",
            "color": "Black",
            "gauge": 22.0,
            "length": 120.0,
        },
    ],
    "connections": [
        {
            "wire_id": "W1",
            "from_connector_id": "CONN1",
            "from_pin_id": "1",
            "to_connector_id": "CONN2",
            "to_pin_id": "A",
        },
        {
            "wire_id": "W2",
            "from_connector_id": "CONN1",
            "from_pin_id": "2",
            "to_connector_id": "CONN2",
            "to_pin_id": "B",
        },
    ],
}


def test_create_harness(client: TestClient, db_session: Session) -> None:
    response = client.post("/api/v1/harnesses/", json=SAMPLE_HARNESS)
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == SAMPLE_HARNESS["name"]
    assert "id" in content

    harness_id = content["id"]

    # Test BOM
    response = client.get(f"/api/v1/harnesses/{harness_id}/bom")
    assert response.status_code == 200
    bom = response.json()
    assert len(bom["connectors"]) == 2
    assert len(bom["wires"]) == 1
    assert bom["connectors"][0]["quantity"] == 1
    assert bom["wires"][0]["quantity"] == 2

    # Test Cutlist
    response = client.get(f"/api/v1/harnesses/{harness_id}/cutlist")
    assert response.status_code == 200
    cutlist = response.json()
    assert len(cutlist["items"]) == 2
    # Sort by wire_id to ensure deterministic order
    cutlist["items"].sort(key=lambda x: x["wire_id"])
    assert cutlist["items"][0]["length"] == 100.0
    assert cutlist["items"][1]["length"] == 120.0

    # Test From-To
    response = client.get(f"/api/v1/harnesses/{harness_id}/fromto")
    assert response.status_code == 200
    fromto = response.json()
    assert len(fromto["items"]) == 2
    # Sort by wire_id to ensure deterministic order
    fromto["items"].sort(key=lambda x: x["wire_id"])
    assert fromto["items"][0]["from_location"] == "CONN1-1"
    assert fromto["items"][0]["to_location"] == "CONN2-A"
    assert fromto["items"][1]["from_location"] == "CONN1-2"
    assert fromto["items"][1]["to_location"] == "CONN2-B"
