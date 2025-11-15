import logging
import os
from typing import Optional

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.responses import FileResponse

from app.core.config import settings
from app.schemas.harness_design import DesignData, Edge, Node
from app.services.kicad_engine_service import KiCadEngineService

logger = logging.getLogger(__name__)

router = APIRouter()


def get_kicad_engine_service() -> KiCadEngineService:
    """Get an instance of the KiCadEngineService.

    This function serves as a dependency injector for the KiCadEngineService,
    allowing FastAPI to manage the service's lifecycle.

    Returns
    -------
    KiCadEngineService
        An instance of the KiCadEngineService.
    """
    return KiCadEngineService()


def create_spike_test_data() -> DesignData:
    """Create a fixed DesignData object for spike testing.

    This is used as a default input for the API endpoints when no request
    body is provided, facilitating simple, repeatable tests.

    Returns
    -------
    DesignData
        A pre-populated DesignData object with a simple two-connector harness.
    """
    return DesignData(
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
        edges=[
            Edge(id="E1", source="J1", target="J2"),
        ],
    )


@router.post("/export/spike_test_dxf", response_class=FileResponse)
async def export_spike_test_dxf(
    design_data: Optional[DesignData] = Body(None),
    service: KiCadEngineService = Depends(get_kicad_engine_service),
):
    """Generate and return a DXF file from harness design data.

    This endpoint serves as a spike test to validate the end-to-end workflow
    of generating a `.kicad_sch` file from JSON data and then exporting it
    to DXF format using `kicad-cli`. If no request body is provided, it
    uses a fixed, internal test object.

    Parameters
    ----------
    design_data : Optional[DesignData], optional
        A Pydantic model representing the harness design, received as the
        request body. Defaults to None, in which case a test object is used.
    service : KiCadEngineService, optional
        The KiCad engine service, injected by FastAPI's dependency system.

    Returns
    -------
    FileResponse
        A streaming file response containing the generated DXF file.

    Raises
    ------
    HTTPException
        An exception with status code 500 if any part of the file generation
        or export process fails.
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
            filename=settings.api.default_filenames["dxf"],
            media_type="application/dxf",
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
            # The FileResponse will delete the file after sending on modern
            # versions of Starlette but we'll leave this here as a fallback.
            # os.remove(output_file_path)
            logger.info(f"Cleaned up temporary DXF file: {output_file_path}")


@router.post("/export/spike_test_bom", response_class=FileResponse)
async def export_spike_test_bom(
    design_data: Optional[DesignData] = Body(None),
    service: KiCadEngineService = Depends(get_kicad_engine_service),
):
    """Generate and return a BOM (CSV) file from harness design data.

    Similar to the DXF endpoint, this validates the workflow for BOM
    generation. It takes harness design data, creates a schematic, and then
    exports a Bill of Materials in CSV format. If no request body is
    provided, it uses a fixed, internal test object.

    Parameters
    ----------
    design_data : Optional[DesignData], optional
        A Pydantic model representing the harness design. Defaults to None.
    service : KiCadEngineService, optional
        The KiCad engine service, injected by FastAPI.

    Returns
    -------
    FileResponse
        A streaming file response containing the generated CSV BOM file.

    Raises
    ------
    HTTPException
        An exception with status code 500 if the process fails.
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
            filename=settings.api.default_filenames["bom"],
            media_type="text/csv",
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
