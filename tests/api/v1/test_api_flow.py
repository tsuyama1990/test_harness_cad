from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from app.api.deps import get_kicad_engine


def test_full_save_and_export_flow(client: TestClient, mock_kicad_engine: MagicMock):
    """
    Test the full flow of creating a project, saving a design,
    and exporting a DXF.
    """
    # Override the dependency with the mock
    client.app.dependency_overrides[get_kicad_engine] = lambda: mock_kicad_engine

    # 1. Create a project
    project_name = "Test Project"
    response = client.post("/api/v1/projects/", json={"name": project_name})
    assert response.status_code == 200
    project_data = response.json()
    project_id = project_data["id"]
    assert project_data["name"] == project_name

    # 2. Save a design
    design_data = {
        "design_data": {
            "nodes": [{"id": "1", "type": "connector", "position": {}, "data": {}}],
            "edges": [],
        }
    }
    response = client.post(f"/api/v1/projects/{project_id}/save", json=design_data)
    assert response.status_code == 200

    # 3. Export DXF
    response = client.get(f"/api/v1/projects/{project_id}/export/dxf")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/dxf"

    # 4. Assert that the mock engine was called correctly
    mock_kicad_engine.generate_sch_from_json.assert_called_once()
    mock_kicad_engine.export_dxf.assert_called_once()

    # Clean up the override
    del client.app.dependency_overrides[get_kicad_engine]
