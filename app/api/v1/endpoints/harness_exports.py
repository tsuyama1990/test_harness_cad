import csv
import io
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import StreamingResponse

from app.api import deps
from app.exceptions import HarnessNotFoundException
from app.services import harness_service

router = APIRouter()


@router.get("/{harness_id}/strip-list", response_class=StreamingResponse)
def get_strip_list(
    *,
    db: Session = Depends(deps.get_db),
    harness_id: UUID,
):
    """
    Get Strip List for a harness.
    """
    try:
        harness = harness_service.get_harness(db=db, harness_id=harness_id)
    except HarnessNotFoundException:
        raise HTTPException(status_code=404, detail="Harness not found")

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(
        [
            "wire_id",
            "strip_length_a",
            "terminal_part_number_a",
            "strip_length_b",
            "terminal_part_number_b",
        ]
    )
    for conn in harness.connections:
        writer.writerow(
            [
                conn.wire.logical_id,
                conn.strip_length_a,
                conn.terminal_part_number_a,
                conn.strip_length_b,
                conn.terminal_part_number_b,
            ]
        )
    output.seek(0)
    return StreamingResponse(
        io.BytesIO(output.read().encode()),
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=strip-list-{harness_id}.csv"
        },
    )


@router.get("/{harness_id}/mark-tube-list", response_class=StreamingResponse)
def get_mark_tube_list(
    *,
    db: Session = Depends(deps.get_db),
    harness_id: UUID,
):
    """
    Get Mark Tube List for a harness.
    """
    try:
        harness = harness_service.get_harness(db=db, harness_id=harness_id)
    except HarnessNotFoundException:
        raise HTTPException(status_code=404, detail="Harness not found")

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["text_to_print", "quantity", "diameter_mm", "length_mm"])
    for conn in harness.connections:
        if conn.marking_text_a:
            writer.writerow([conn.marking_text_a, 1, 3.0, 20])
        if conn.marking_text_b:
            writer.writerow([conn.marking_text_b, 1, 3.0, 20])

    output.seek(0)
    return StreamingResponse(
        io.BytesIO(output.read().encode()),
        media_type="text/csv",
        headers={
            "Content-Disposition": (
                f"attachment; filename=mark-tube-list-{harness_id}.csv"
            )
        },
    )


@router.get("/{harness_id}/formboard-pdf", response_class=StreamingResponse)
def get_formboard_pdf(
    *,
    db: Session = Depends(deps.get_db),
    harness_id: UUID,
):
    """
    Get Formboard PDF for a harness.
    """
    try:
        harness = harness_service.get_harness(db=db, harness_id=harness_id)
    except HarnessNotFoundException:
        raise HTTPException(status_code=404, detail="Harness not found")

    pdf_bytes = harness_service.generate_formboard_pdf(db_harness=harness)

    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=formboard-{harness_id}.pdf"
        },
    )
