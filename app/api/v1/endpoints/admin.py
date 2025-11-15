from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.models.component import Component as ComponentModel
from app.models.component_category import ComponentCategory as ComponentCategoryModel
from app.schemas.component import (
    Component,
    ComponentCategory,
    ComponentCategoryCreate,
    ComponentCreate,
)

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/categories", response_model=ComponentCategory)
def create_component_category(
    *,
    db: Session = Depends(deps.get_db),
    category_in: ComponentCategoryCreate,
) -> ComponentCategory:
    """
    Create a new component category.
    """
    db_category = ComponentCategoryModel(**category_in.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@router.post("/components", response_model=Component)
def create_component(
    *,
    db: Session = Depends(deps.get_db),
    component_in: ComponentCreate,
) -> Component:
    """
    Create a new component.
    """
    category = db.get(ComponentCategoryModel, component_in.category_id)
    if not category:
        raise HTTPException(
            status_code=404,
            detail="Component category not found",
        )
    db_component = ComponentModel(**component_in.model_dump())
    db.add(db_component)
    db.commit()
    db.refresh(db_component)
    return db_component
