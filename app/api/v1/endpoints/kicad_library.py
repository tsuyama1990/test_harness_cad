from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.models.component import Component
from app.models.component_category import ComponentCategory
from app.schemas.kicad_http import (
    KiCadHttpCategory,
    KiCadHttpPart,
    KiCadHttpValidation,
)

router = APIRouter(prefix="/kicad_library", tags=["kicad_http"])


@router.get("/", response_model=KiCadHttpValidation)
def validate_kicad_http_library() -> KiCadHttpValidation:
    """
    KiCad HTTP library validation endpoint.
    """
    return KiCadHttpValidation(categories="categories", parts="parts")


@router.get("/categories", response_model=List[KiCadHttpCategory])
def get_categories(*, db: Session = Depends(deps.get_db)) -> List[KiCadHttpCategory]:
    """
    Get all component categories.
    """
    categories = db.query(ComponentCategory).all()
    return [KiCadHttpCategory(id=str(cat.id), name=cat.name) for cat in categories]


@router.get("/parts/category/{category_id}", response_model=List[KiCadHttpPart])
def get_parts_by_category(
    *,
    db: Session = Depends(deps.get_db),
    category_id: str,
) -> List[KiCadHttpPart]:
    """
    Get all components in a category.
    """
    try:
        cat_id = int(category_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Category not found")

    category = db.get(ComponentCategory, cat_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    parts = db.query(Component).filter(Component.category_id == cat_id).all()
    return [
        KiCadHttpPart(
            id=str(part.id),
            name=part.name,
            description=part.description or "",
            symbol=part.symbol_reference,
            footprint=part.footprint_reference,
            mpn=part.manufacturer_part_number or "",
        )
        for part in parts
    ]
