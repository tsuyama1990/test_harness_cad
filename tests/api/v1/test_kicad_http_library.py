from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app

client = TestClient(app)


def test_validation_endpoint():
    response = client.get("/api/v1/kicad_library/")
    assert response.status_code == 200
    assert response.json() == {"categories": "categories", "parts": "parts"}


def test_full_http_library_flow(client: TestClient, db_session: Session):
    # Create a category
    category_data = {"name": "Test D-Sub", "description": "D-Sub connectors"}
    response = client.post("/api/v1/admin/categories", json=category_data)
    assert response.status_code == 200
    category = response.json()
    assert category["name"] == category_data["name"]
    category_id = category["id"]

    # Create a component
    component_data = {
        "name": "Test DB-9",
        "description": "9-pin D-Sub male connector",
        "manufacturer_part_number": "DB-9-MALE-TEST",
        "symbol_reference": "MyLib:DB9",
        "footprint_reference": "Connector_Dsub:DSUB-9_Male_...",
        "category_id": category_id,
    }
    response = client.post("/api/v1/admin/components", json=component_data)
    assert response.status_code == 200
    component = response.json()
    assert component["name"] == component_data["name"]

    # Get categories
    response = client.get("/api/v1/kicad_library/categories")
    assert response.status_code == 200
    categories = response.json()
    assert len(categories) > 0
    # Find our test category - note the ID is a string in the response
    test_cat_in_response = next(
        (cat for cat in categories if cat["id"] == str(category_id)), None
    )
    assert test_cat_in_response is not None
    assert test_cat_in_response["name"] == "Test D-Sub"

    # Get parts by category
    response = client.get(f"/api/v1/kicad_library/parts/category/{category_id}")
    assert response.status_code == 200
    parts = response.json()
    assert len(parts) == 1
    part = parts[0]
    assert part["name"] == "Test DB-9"
    assert part["symbol"] == "MyLib:DB9"
    assert part["footprint"] == "Connector_Dsub:DSUB-9_Male_..."
    assert part["mpn"] == "DB-9-MALE-TEST"

    # Test getting parts for a non-existent category
    response = client.get("/api/v1/kicad_library/parts/category/999")
    assert response.status_code == 404
