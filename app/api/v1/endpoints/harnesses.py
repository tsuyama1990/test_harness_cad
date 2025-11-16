from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import schemas
from app.api import deps
from app.exceptions import HarnessNotFoundException, InvalidHarnessDataException
from app.services import harness_service

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
            }
            for conn in db_harness.connections
            if conn.wire and conn.from_pin and conn.to_pin and conn.from_pin.connector and conn.to_pin.connector
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
