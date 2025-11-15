import os

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.api import deps
from app.models.harness_design import HarnessDesign
from app.schemas.harness_design import DesignData
from app.services.kicad_engine_service import KiCadEngineService

router = APIRouter()


def cleanup_files(files: list[str]):
    """
    Remove temporary files.
    """
    for file_path in files:
        if os.path.exists(file_path):
            os.remove(file_path)


@router.get("/{project_id}/export/dxf")
def export_dxf(
    *,
    db: Session = Depends(deps.get_db),
    engine: KiCadEngineService = Depends(deps.get_kicad_engine),
    background_tasks: BackgroundTasks,
    project_id: int,
) -> FileResponse:
    """
    Export the latest harness design for a project as a DXF file.
    """
    latest_design = (
        db.query(HarnessDesign)
        .filter(HarnessDesign.project_id == project_id)
        .order_by(HarnessDesign.created_at.desc())
        .first()
    )

    if not latest_design:
        raise HTTPException(
            status_code=404, detail="No design found for this project."
        )

    try:
        design_data = DesignData.model_validate(latest_design.design_data)
        sch_path = engine.generate_sch_from_json(design_data)
        dxf_path = engine.export_dxf(sch_path)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to generate DXF: {e}"
        ) from e

    background_tasks.add_task(cleanup_files, [sch_path, dxf_path])

    return FileResponse(
        dxf_path,
        media_type="application/dxf",
        filename="export.dxf",
        background=background_tasks,
    )
