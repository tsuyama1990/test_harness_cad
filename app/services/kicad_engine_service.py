import subprocess
import tempfile
import os
import logging
from typing import Dict

import kicad_sch_api as ksa
from app.schemas.harness_design import DesignData, Node

logger = logging.getLogger(__name__)


class KiCadEngineService:
    """
    Service to handle KiCad schematic generation and file exports.
    """

    def generate_sch_from_json(self, design_data: DesignData) -> str:
        """
        Generates a .kicad_sch file from JSON design data.

        Args:
            design_data: The Pydantic model containing nodes and edges.

        Returns:
            The file path of the generated .kicad_sch file.
        """
        logger.info("Generating KiCad schematic from JSON data.")
        try:
            sch = ksa.create_schematic("HarnessDesign")

            # Create a lookup table for node positions
            node_positions: Dict[str, tuple[float, float]] = {
                node.id: (node.position['x'], node.position['y'])
                for node in design_data.nodes
            }

            # Add components for each node
            for node in design_data.nodes:
                if node.type == 'connector':
                    # For this spike, add a fixed connector symbol
                    sch.components.add(
                        lib_id="Connector:Conn_01x02",
                        reference=node.id,
                        value=node.data.get('label', 'J?'),
                        position=node_positions[node.id],
                        footprint="Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical"
                    )
                # Add other component types here in the future

            # Add wires for each edge
            for edge in design_data.edges:
                start_pos = node_positions.get(edge.source)
                end_pos = node_positions.get(edge.target)
                if start_pos and end_pos:
                    sch.add_wire(start=start_pos, end=end_pos)

            # Save to a temporary file
            with tempfile.NamedTemporaryFile(
                mode='w+', suffix=".kicad_sch", delete=False, encoding='utf-8'
            ) as tmp_sch_file:
                sch_file_path = tmp_sch_file.name
                sch.save(sch_file_path)

            logger.info(f"Successfully generated schematic file at {sch_file_path}")
            return sch_file_path
        except Exception as e:
            logger.error(f"Failed to generate KiCad schematic: {e}")
            raise

    def _run_kicad_cli_command(self, command: list[str]):
        """Helper to run a kicad-cli command."""
        logger.info(f"Running command: {' '.join(command)}")
        try:
            result = subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            logger.info(f"Command successful. STDOUT: {result.stdout}")
            if result.stderr:
                logger.warning(f"Command produced STDERR: {result.stderr}")
        except FileNotFoundError:
            logger.error("`kicad-cli` not found. Is KiCad installed and in the system's PATH?")
            raise
        except subprocess.CalledProcessError as e:
            logger.error(f"kicad-cli command failed with exit code {e.returncode}.")
            logger.error(f"STDOUT: {e.stdout}")
            logger.error(f"STDERR: {e.stderr}")
            raise

    def export_dxf(self, sch_file_path: str) -> str:
        """
        Exports a DXF file from a .kicad_sch file.

        Args:
            sch_file_path: The path to the source .kicad_sch file.

        Returns:
            The file path of the generated .dxf file.
        """
        with tempfile.NamedTemporaryFile(
            suffix=".dxf", delete=False
        ) as tmp_dxf_file:
            dxf_file_path = tmp_dxf_file.name

        command = [
            "kicad-cli", "sch", "export", "dxf",
            "--output", dxf_file_path,
            sch_file_path
        ]
        self._run_kicad_cli_command(command)
        logger.info(f"Successfully exported DXF file to {dxf_file_path}")
        return dxf_file_path

    def export_bom(self, sch_file_path: str) -> str:
        """
        Exports a BOM (CSV) file from a .kicad_sch file.

        Args:
            sch_file_path: The path to the source .kicad_sch file.

        Returns:
            The file path of the generated .csv BOM file.
        """
        with tempfile.NamedTemporaryFile(
            suffix=".csv", delete=False
        ) as tmp_bom_file:
            bom_file_path = tmp_bom_file.name

        command = [
            "kicad-cli", "sch", "export", "bom",
            "--output", bom_file_path,
            sch_file_path
        ]
        self._run_kicad_cli_command(command)
        logger.info(f"Successfully exported BOM file to {bom_file_path}")
        return bom_file_path
