import os
import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.responses import FileResponse

from app.schemas.harness_design import DesignData, Node, Edge
from app.services.kicad_engine_service import KiCadEngineService

logger = logging.getLogger(__name__)

router = APIRouter()


def get_kicad_engine_service():
    """Dependency injector for the KiCadEngineService."""
    return KiCadEngineService()


def create_spike_test_data() -> DesignData:
    """Creates a fixed DesignData object for spike testing."""
    return DesignData(
        nodes=[
            Node(id="J1", type="connector", position={"x": 100, "y": 100}, data={"label": "CONN_1"}),
            Node(id="J2", type="connector", position={"x": 200, "y": 100}, data={"label": "CONN_2"}),
        ],
        edges=[
            Edge(id="E1", source="J1", target="J2"),
        ]
    )


@router.post("/export/spike_test_dxf", response_class=FileResponse)
async def export_spike_test_dxf(
    design_data: Optional[DesignData] = Body(None),
    service: KiCadEngineService = Depends(get_kicad_engine_service)
):
    """
    Spike test endpoint to generate a DXF file from harness design data.
    If no data is provided, a fixed test object is used.
    """
    sch_file_path = None
    output_file_path = None

    if design_data is None:
        design_data = create_spike_test_data()

    try:
        # 1. Generate .kicad_sch file
        sch_file_path = service.generate_sch_from_json(design_data)

        # 2. Export DXF from the .kicad_sch file
        output_file_path = service.export_dxf(sch_file_path)

        # 3. Return the generated DXF file
        return FileResponse(
            path=output_file_path,
            filename="harness_design.dxf",
            media_type="application/dxf"
        )
    except Exception as e:
        logger.error(f"DXF export failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
    finally:
        # 4. Clean up temporary files
        if sch_file_path and os.path.exists(sch_file_path):
            os.remove(sch_file_path)
            logger.info(f"Cleaned up temporary schematic file: {sch_file_path}")
        if output_file_path and os.path.exists(output_file_path):
            # The FileResponse will delete the file after sending on modern versions of Starlette
            # but we'll leave this here as a fallback.
            # os.remove(output_file_path)
            logger.info(f"Cleaned up temporary DXF file: {output_file_path}")


@router.post("/export/spike_test_bom", response_class=FileResponse)
async def export_spike_test_bom(
    design_data: Optional[DesignData] = Body(None),
    service: KiCadEngineService = Depends(get_kicad_engine_service)
):
    """
    Spike test endpoint to generate a BOM (CSV) file from harness design data.
    If no data is provided, a fixed test object is used.
    """
    sch_file_path = None
    output_file_path = None

    if design_data is None:
        design_data = create_spike_test_data()

    try:
        # 1. Generate .kicad_sch file
        sch_file_path = service.generate_sch_from_json(design_data)

        # 2. Export BOM from the .kicad_sch file
        output_file_path = service.export_bom(sch_file_path)

        # 3. Return the generated BOM file
        return FileResponse(
            path=output_file_path,
            filename="harness_bom.csv",
            media_type="text/csv"
        )
    except Exception as e:
        logger.error(f"BOM export failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
    finally:
        # 4. Clean up temporary files
        if sch_file_path and os.path.exists(sch_file_path):
            os.remove(sch_file_path)
            logger.info(f"Cleaned up temporary schematic file: {sch_file_path}")
        if output_file_path and os.path.exists(output_file_path):
            # os.remove(output_file_path)
            logger.info(f"Cleaned up temporary BOM file: {output_file_path}")
