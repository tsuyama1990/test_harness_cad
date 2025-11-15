import os
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from app.schemas.harness_design import DesignData, Edge, Node


def test_export_spike_test_dxf_endpoint(client: TestClient):
    """Test the /export/spike_test_dxf endpoint.

    This test verifies the behavior of the DXF export endpoint. It uses
    `unittest.mock.patch` to replace the `KiCadEngineService` with a mock,
    thereby isolating the endpoint from the actual service logic involving
    file system operations and subprocess calls.

    Parameters
    ----------
    client : TestClient
        The FastAPI TestClient fixture for making requests to the application.
    """
    # Mock the service methods
    with patch(
        "app.api.v1.endpoints.harness_exports.KiCadEngineService"
    ) as MockKiCadEngineService:
        # Create an instance of the mock
        mock_service_instance = MockKiCadEngineService.return_value
        mock_service_instance.generate_sch_from_json.return_value = (
            "/tmp/fake_schematic.kicad_sch"
        )
        mock_service_instance.export_dxf.return_value = "/tmp/fake_harness.dxf"

        # Create a dummy DXF file for FileResponse to return
        with open("/tmp/fake_harness.dxf", "w") as f:
            f.write("FAKE DXF CONTENT")

        # Define some test data
        test_design_data = {
            "nodes": [
                {
                    "id": "J1",
                    "type": "connector",
                    "position": {"x": 100, "y": 100},
                    "data": {"label": "CONN_1"},
                }
            ],
            "edges": [],
        }

        # Make the request
        response = client.post(
            "/api/v1/harness/export/spike_test_dxf", json=test_design_data
        )

        # Assertions
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/dxf"
        assert (
            'attachment; filename="harness_design.dxf"'
            in response.headers["content-disposition"]
        )
        assert response.text == "FAKE DXF CONTENT"

        # Verify that the service methods were called correctly
        mock_service_instance.generate_sch_from_json.assert_called_once()
        mock_service_instance.export_dxf.assert_called_once_with(
            "/tmp/fake_schematic.kicad_sch"
        )

        # Clean up the dummy file
        os.remove("/tmp/fake_harness.dxf")


def test_export_spike_test_bom_endpoint(client: TestClient):
    """Test the /export/spike_test_bom endpoint.

    This test verifies the BOM export endpoint, mocking the `KiCadEngineService`
    to ensure the test is fast and independent of the service's implementation
    details.

    Parameters
    ----------
    client : TestClient
        The FastAPI TestClient fixture.
    """
    with patch(
        "app.api.v1.endpoints.harness_exports.KiCadEngineService"
    ) as MockKiCadEngineService:
        mock_service_instance = MockKiCadEngineService.return_value
        mock_service_instance.generate_sch_from_json.return_value = (
            "/tmp/fake_schematic.kicad_sch"
        )
        mock_service_instance.export_bom.return_value = "/tmp/fake_bom.csv"

        with open("/tmp/fake_bom.csv", "w") as f:
            f.write("Id,Reference,Value")

        response = client.post(
            "/api/v1/harness/export/spike_test_bom", json={"nodes": [], "edges": []}
        )

        assert response.status_code == 200
        assert response.headers["content-type"] == "text/csv; charset=utf-8"
        assert (
            'attachment; filename="harness_bom.csv"'
            in response.headers["content-disposition"]
        )
        assert response.text == "Id,Reference,Value"

        mock_service_instance.generate_sch_from_json.assert_called_once()
        mock_service_instance.export_bom.assert_called_once_with(
            "/tmp/fake_schematic.kicad_sch"
        )

        os.remove("/tmp/fake_bom.csv")


@patch("kicad_sch_api.create_schematic")
def test_kicad_engine_generate_sch_from_json(mock_create_schematic):
    """Unit test for the KiCadEngineService.generate_sch_from_json method.

    This test validates the schematic generation logic within the service.
    It mocks the `kicad-sch-api` library to ensure that the service calls
    the library's functions with the expected arguments, without creating
    an actual schematic file.

    Parameters
    ----------
    mock_create_schematic : MagicMock
        A mock of the `kicad_sch_api.create_schematic` function.
    """
    from app.services.kicad_engine_service import KiCadEngineService

    # Mock the schematic object and its methods
    mock_sch = MagicMock()
    mock_create_schematic.return_value = mock_sch

    service = KiCadEngineService()
    design_data = DesignData(
        nodes=[
            Node(
                id="J1",
                type="connector",
                position={"x": 100, "y": 100},
                data={"label": "CONN_1"},
            ),
            Node(
                id="J2",
                type="connector",
                position={"x": 200, "y": 100},
                data={"label": "CONN_2"},
            ),
        ],
        edges=[Edge(id="E1", source="J1", target="J2")],
    )

    # Call the method
    sch_file_path = service.generate_sch_from_json(design_data)

    # Assertions
    mock_create_schematic.assert_called_once_with("HarnessDesign")
    assert mock_sch.components.add.call_count == 2
    mock_sch.add_wire.assert_called_once()
    mock_sch.save.assert_called_once_with(sch_file_path)

    # Clean up the created temporary file
    if os.path.exists(sch_file_path):
        os.remove(sch_file_path)


@patch("subprocess.run")
def test_kicad_engine_export_dxf(mock_subprocess_run):
    """Unit test for the KiCadEngineService.export_dxf method.

    This test ensures that the `export_dxf` method correctly constructs and
    executes the `kicad-cli` command via `subprocess.run`. The `subprocess.run`
    function is mocked to prevent actual execution of external commands.

    Parameters
    ----------
    mock_subprocess_run : MagicMock
        A mock of the `subprocess.run` function.
    """
    from app.services.kicad_engine_service import KiCadEngineService

    # Configure the mock to simulate a successful command execution
    mock_subprocess_run.return_value = MagicMock(
        returncode=0, stdout="", stderr="", check_returncode=lambda: None
    )

    service = KiCadEngineService()
    fake_sch_path = "/tmp/test.kicad_sch"
    dxf_file_path = service.export_dxf(fake_sch_path)

    # Assertions
    assert dxf_file_path.endswith(".dxf")
    mock_subprocess_run.assert_called_once()

    # Check the command arguments passed to subprocess.run
    args, kwargs = mock_subprocess_run.call_args
    command_list = args[0]
    assert "kicad-cli" in command_list
    assert "sch" in command_list
    assert "export" in command_list
    assert "dxf" in command_list
    assert "--output" in command_list
    assert dxf_file_path in command_list
    assert fake_sch_path in command_list

    # Clean up the created temporary file
    if os.path.exists(dxf_file_path):
        os.remove(dxf_file_path)
