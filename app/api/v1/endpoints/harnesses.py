import csv
import csv
import io
import os
import shutil
from pathlib import Path
from tempfile import NamedTemporaryFile
from uuid import UUID

from fastapi import APIRouter, Depends, File, HTTPException, Response, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app import models, schemas
from app.api import deps
from app.exceptions import HarnessNotFoundException, InvalidHarnessDataException
from app.services import harness_service, validation_service
from app.services.dxf_exporter import DxfExporter

router = APIRouter()


@router.post("/", response_model=schemas.Harness)
def create_harness(
    *,
    db: Session = Depends(deps.get_db),
    harness_in: schemas.HarnessCreate,
):
    """
    Create new harness.
    """
    try:
        harness = harness_service.create_harness(db=db, harness_in=harness_in)
    except InvalidHarnessDataException as e:
        raise HTTPException(status_code=400, detail=str(e))
    return harness


@router.get("/{harness_id}", response_model=schemas.HarnessFull)
def get_harness(
    *,
    db: Session = Depends(deps.get_db),
    harness_id: UUID,
):
    """
    Get full harness data.
    """
    try:
        db_harness = harness_service.get_harness(db=db, harness_id=harness_id)
    except HarnessNotFoundException:
        raise HTTPException(status_code=404, detail="Harness not found")

    response_data = {
        "id": db_harness.id,
        "name": db_harness.name,
        "connectors": [
            {
                "id": c.logical_id,
                "manufacturer": c.manufacturer,
                "part_number": c.part_number,
                "pins": [{"id": p.logical_id} for p in c.pins],
            }
            for c in db_harness.connectors
        ],
        "wires": [
            {
                "id": w.logical_id,
                "manufacturer": w.manufacturer,
                "part_number": w.part_number,
                "color": w.color,
                "gauge": w.gauge,
                "length": w.length,
            }
            for w in db_harness.wires
        ],
        "connections": [
            {
                "wire_id": conn.wire.logical_id,
                "from_connector_id": conn.from_pin.connector.logical_id,
                "from_pin_id": conn.from_pin.logical_id,
                "to_connector_id": conn.to_pin.connector.logical_id,
                "to_pin_id": conn.to_pin.logical_id,
                "strip_length_a": conn.strip_length_a,
                "strip_length_b": conn.strip_length_b,
                "terminal_part_number_a": conn.terminal_part_number_a,
                "terminal_part_number_b": conn.terminal_part_number_b,
                "marking_text_a": conn.marking_text_a,
                "marking_text_b": conn.marking_text_b,
            }
            for conn in db_harness.connections
            if (
                conn.wire
                and conn.from_pin
                and conn.to_pin
                and conn.from_pin.connector
                and conn.to_pin.connector
            )
        ],
    }

    return response_data


@router.put("/{harness_id}", response_model=schemas.Harness)
def update_harness(
    *,
    db: Session = Depends(deps.get_db),
    harness_id: UUID,
    harness_in: schemas.HarnessCreate,
):
    """
    Update a harness.
    """
    try:
        harness = harness_service.update_harness(
            db=db, harness_id=harness_id, harness_in=harness_in
        )
    except (HarnessNotFoundException, InvalidHarnessDataException) as e:
        raise HTTPException(status_code=404, detail=str(e))
    return harness


@router.get("/{harness_id}/bom", response_model=schemas.BomResponse)
def get_bom(
    *,
    db: Session = Depends(deps.get_db),
    harness_id: UUID,
):
    """
    Get Bill of Materials for a harness.
    """
    try:
        harness = harness_service.get_harness(db=db, harness_id=harness_id)
    except HarnessNotFoundException:
        raise HTTPException(status_code=404, detail="Harness not found")

    return harness_service.generate_bom(db_harness=harness)


@router.get("/{harness_id}/cutlist", response_model=schemas.CutlistResponse)
def get_cutlist(
    *,
    db: Session = Depends(deps.get_db),
    harness_id: UUID,
):
    """
    Get Cutlist for a harness.
    """
    try:
        harness = harness_service.get_harness(db=db, harness_id=harness_id)
    except HarnessNotFoundException:
        raise HTTPException(status_code=404, detail="Harness not found")

    return harness_service.generate_cutlist(db_harness=harness)


@router.get("/{harness_id}/fromto", response_model=schemas.FromToResponse)
def get_fromto(
    *,
    db: Session = Depends(deps.get_db),
    harness_id: UUID,
):
    """
    Get From-To list for a harness.
    """
    try:
        harness = harness_service.get_harness(db=db, harness_id=harness_id)
    except HarnessNotFoundException:
        raise HTTPException(status_code=404, detail="Harness not found")

    return harness_service.generate_fromto(db_harness=harness)


@router.get("/{harness_id}/validate", response_model=list[schemas.ValidationError])
def validate_harness(
    *,
    db: Session = Depends(deps.get_db),
    harness_id: UUID,
):
    """
    Validate the harness against project settings.
    """
    try:
        harness = harness_service.get_harness(db=db, harness_id=harness_id)
    except HarnessNotFoundException:
        raise HTTPException(status_code=404, detail="Harness not found")

    # This assumes the harness is part of a project and settings are available.
    # In a real app, you might need a more robust way to get from harness to
    # project settings.
    harness_design = (
        db.query(models.HarnessDesign)
        .filter(models.HarnessDesign.harness_id == harness_id)
        .first()
    )
    if not harness_design or not harness_design.project.settings:
        raise HTTPException(
            status_code=400, detail="Project settings not found for this harness."
        )

    errors = validation_service.validate_harness(
        db=db, harness=harness, settings=harness_design.project.settings
    )
    return errors


@router.get("/{harness_id}/procurement/export-csv")
def export_procurement_csv(
    *,
    db: Session = Depends(deps.get_db),
    harness_id: UUID,
):
    """
    Export the Bill of Materials (BOM) as a CSV file for procurement.
    The export is blocked if validation fails.
    """
    try:
        harness = harness_service.get_harness(db=db, harness_id=harness_id)
    except HarnessNotFoundException:
        raise HTTPException(status_code=404, detail="Harness not found")

    harness_design = (
        db.query(models.HarnessDesign)
        .filter(models.HarnessDesign.harness_id == harness_id)
        .first()
    )
    if not harness_design or not harness_design.project.settings:
        raise HTTPException(
            status_code=400, detail="Project settings not found for this harness."
        )

    # First, run validation
    errors = validation_service.validate_harness(
        db=db, harness=harness, settings=harness_design.project.settings
    )
    if errors:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Validation failed. Cannot export procurement data.",
                "errors": [e.dict() for e in errors],
            },
        )

    # If validation passes, generate BOM and CSV
    bom = harness_service.generate_bom(db_harness=harness)
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Part Number", "Manufacturer", "Quantity"])
    for item in bom.connectors:
        writer.writerow([item.part_number, item.manufacturer, item.quantity])
    for item in bom.wires:
        writer.writerow([item.part_number, item.manufacturer, item.quantity])

    output.seek(0)
    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=bom_harness_{harness_id}.csv"
        },
    )


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/{harness_id}/3d-model")
def upload_3d_model(
    *,
    db: Session = Depends(deps.get_db),
    harness_id: UUID,
    file: UploadFile = File(...),
):
    """
    Upload a 3D model for the harness.
    """
    # Validate file extension
    allowed_extensions = {".glb", ".gltf", ".obj"}
    file_extension = Path(file.filename).suffix.lower()
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid file type. Allowed extensions are: "
                f"{', '.join(allowed_extensions)}"
            ),
        )

    try:
        harness = harness_service.get_harness(db=db, harness_id=harness_id)
    except HarnessNotFoundException:
        raise HTTPException(status_code=404, detail="Harness not found")

    # Sanitize filename
    filename = f"{harness_id}_{Path(file.filename).name}"
    file_path = UPLOAD_DIR / filename
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Update the harness with the URL
    file_url = f"/api/v1/harnesses/uploads/{filename}"
    harness.three_d_model_path = file_url
    db.commit()

    return {"message": "3D model uploaded successfully", "file_path": file_url}


@router.get("/uploads/{filename}")
def get_uploaded_file(filename: str):
    """
    Serve an uploaded file.
    """
    file_path = UPLOAD_DIR / filename
    if not os.path.abspath(file_path).startswith(os.path.abspath(UPLOAD_DIR)):
        raise HTTPException(status_code=403, detail="Forbidden")

    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path)


@router.put("/{harness_id}/wires/{wire_id}/3d-path", response_model=schemas.Wire)
def update_wire_3d_path(
    *,
    db: Session = Depends(deps.get_db),
    harness_id: UUID,
    wire_id: UUID,
    path_in: schemas.Path3D,
    manufacturing_margin: float = 1.0,
):
    """
    Update the 3D path and calculate the length for a specific wire in a harness.
    """
    try:
        wire = harness_service.get_wire(db=db, harness_id=harness_id, wire_id=wire_id)
    except HarnessNotFoundException:
        raise HTTPException(status_code=404, detail="Wire not found in this harness")

    wire.path_3d = [p.dict() for p in path_in.points]

    # Calculate length
    length = 0.0
    for i in range(len(path_in.points) - 1):
        p1 = path_in.points[i]
        p2 = path_in.points[i + 1]
        length += ((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2 + (p2.z - p1.z) ** 2) ** 0.5
    wire.length = length * manufacturing_margin

    db.commit()
    db.refresh(wire)

    return wire


@router.get("/{harness_id}/jig-dxf")
def get_jig_dxf(
    *,
    db: Session = Depends(deps.get_db),
    harness_id: UUID,
    scale: float = 1.0,
):
    """
    Generate a DXF file for a manufacturing jig.
    """
    try:
        # Assuming the 2D layout is stored in a HarnessDesign model
        design = (
            db.query(models.HarnessDesign)
            .filter(models.HarnessDesign.harness_id == harness_id)
            .first()
        )
        if not design:
            raise HTTPException(status_code=404, detail="Harness design data not found")

        harness_design = schemas.HarnessDesign.model_validate(design.design_data)

    except HarnessNotFoundException:
        raise HTTPException(status_code=404, detail="Harness not found")

    exporter = DxfExporter(scale=scale)
    dxf_doc = exporter.export_harness_design(harness_design)

    # Save to a temporary file and stream the response
    with NamedTemporaryFile(delete=False, suffix=".dxf") as tmpfile:
        dxf_doc.saveas(tmpfile.name)
        tmpfile.seek(0)
        return Response(
            content=tmpfile.read(),
            media_type="application/vnd.dxf",
            headers={
                "Content-Disposition": f"attachment; filename=jig_{harness_id}.dxf"
            },
        )
