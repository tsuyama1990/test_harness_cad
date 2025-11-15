from unittest.mock import MagicMock, patch

import pytest

from app.schemas.harness_design import DesignData, Edge, Node
from app.services.kicad_engine_service import KiCadEngineService


@pytest.fixture
def dummy_design_data() -> DesignData:
    """Provides a dummy DesignData object for testing."""
    return DesignData(
        nodes=[
            Node(id="1", type="connector", position={}, data={}),
            Node(id="2", type="resistor", position={}, data={}),
            Node(id="3", type="connector", position={}, data={}),
        ],
        edges=[Edge(id="e1-2", source="1", target="2")],
    )


def test_generate_sch_from_json(dummy_design_data):
    """
    Test that generate_sch_from_json correctly processes nodes
    and interacts with the kicad_sch_api mock.
    """
    with patch("app.services.kicad_engine_service.ksa") as mock_ksa:
        # Arrange
        mock_sch = MagicMock()
        mock_ksa.Schematic.return_value = mock_sch
        service = KiCadEngineService(cli_path="/usr/bin/kicad-cli")

        # Act
        sch_path = service.generate_sch_from_json(dummy_design_data)

        # Assert
        mock_ksa.Schematic.assert_called_once()
        # Only connector nodes should result in a call to add component
        assert mock_sch.components.add.call_count == 2
        mock_sch.components.add.assert_any_call(
            lib="Connector:Conn_01x02", ref="U1", value="Conn", unit=1
        )
        mock_sch.components.add.assert_any_call(
            lib="Connector:Conn_01x02", ref="U3", value="Conn", unit=1
        )
        mock_sch.save.assert_called_once_with(sch_path)


def test_export_dxf():
    """
    Test that export_dxf calls subprocess.run with the correct arguments.
    """
    with patch("app.services.kicad_engine_service.subprocess.run") as mock_subprocess:
        # Arrange
        cli_path = "/usr/bin/kicad-cli"
        service = KiCadEngineService(cli_path=cli_path)
        sch_path = "/tmp/dummy.kicad_sch"

        # Act
        dxf_path = service.export_dxf(sch_path)

        # Assert
        mock_subprocess.assert_called_once()
        call_args = mock_subprocess.call_args[0][0]
        assert call_args[0] == cli_path
        assert "sch" in call_args
        assert "export" in call_args
        assert "dxf" in call_args
        assert "--output" in call_args
        assert dxf_path in call_args
        assert sch_path in call_args


def test_export_bom():
    """
    Test that export_bom calls subprocess.run with the correct arguments.
    """
    with (
        patch("app.services.kicad_engine_service.subprocess.run") as mock_subprocess,
        patch("app.services.kicad_engine_service.Path.rename"),
        patch(
            "app.services.kicad_engine_service.Path.glob", return_value=[MagicMock()]
        ),
    ):
        # Arrange
        cli_path = "/usr/bin/kicad-cli"
        service = KiCadEngineService(cli_path=cli_path)
        sch_path = "/tmp/dummy.kicad_sch"

        # Act
        service.export_bom(sch_path)

        # Assert
        mock_subprocess.assert_called_once()
        call_args = mock_subprocess.call_args[0][0]
        assert call_args[0] == cli_path
        assert "sch" in call_args
        assert "export" in call_args
        assert "bom" in call_args
        assert "--output-dir" in call_args
        assert sch_path in call_args
