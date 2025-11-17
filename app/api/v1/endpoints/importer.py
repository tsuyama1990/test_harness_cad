# app/api/v1/endpoints/import.py
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app import models, schemas
from app.api import deps
from app.services.importer import importer_service

router = APIRouter()


@router.post("/harnesses/import-dxf", response_model=schemas.Harness)
def import_dxf(
    *,
    db: Session = Depends(deps.get_db),
    project_id: int,
    dxf_file: UploadFile = File(...),
):
    """
    Import a DXF file to create a new harness with connectors.
    """
    if not dxf_file.filename.lower().endswith(".dxf"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a .dxf file.")

    try:
        harness = importer_service.import_dxf(
            db=db, dxf_file=dxf_file.file, project_id=project_id
        )
    except Exception as e:
        # Basic error handling for parsing issues
        raise HTTPException(status_code=400, detail=f"Failed to parse DXF file: {e}")

    return harness
