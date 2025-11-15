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
