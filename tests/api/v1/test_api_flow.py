import tempfile

from fastapi.testclient import TestClient


def test_create_project(client: TestClient):
    """
    Test creating a project.
    """
    project_name = "Test Project"
    response = client.post("/api/v1/projects/", json={"name": project_name})
    assert response.status_code == 200
    project_data = response.json()
    assert project_data["name"] == project_name


def test_3d_model_upload_and_dxf_export(client: TestClient):
    """
    Test uploading a 3D model and exporting a DXF file.
    """
    # 1. Create a harness
    harness_name = "Test Harness"
    response = client.post(
        "/api/v1/harnesses/",
        json={
            "name": harness_name,
            "connectors": [],
            "wires": [],
            "connections": [],
        },
    )
    assert response.status_code == 200
    harness_data = response.json()
    harness_id = harness_data["id"]

    # 2. Create a project and save a design
    project_name = "Test Project"
    response = client.post("/api/v1/projects/", json={"name": project_name})
    assert response.status_code == 200
    project_data = response.json()
    project_id = project_data["id"]

    design_data: dict = {
        "harness_id": harness_id,
        "design_data": {
            "nodes": [],
            "edges": [],
        },
    }
    response = client.post(f"/api/v1/projects/{project_id}/save", json=design_data)
    assert response.status_code == 200

    # 3. Upload a 3D model
    with tempfile.NamedTemporaryFile(suffix=".glb") as tmp:
        tmp.write(b"test")
        tmp.seek(0)
        response = client.post(
            f"/api/v1/harnesses/{harness_id}/3d-model",
            files={"file": (tmp.name, tmp, "model/gltf-binary")},
        )
    assert response.status_code == 200

    # 4. Export a DXF
    response = client.get(f"/api/v1/harnesses/{harness_id}/jig-dxf")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/vnd.dxf"
