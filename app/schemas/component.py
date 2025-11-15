from typing import Optional

from pydantic import BaseModel, ConfigDict


class ComponentCategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None


class ComponentCategory(ComponentCategoryCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ComponentCreate(BaseModel):
    name: str
    description: Optional[str] = None
    manufacturer_part_number: Optional[str] = None
    symbol_reference: str
    footprint_reference: str
    category_id: int


class Component(ComponentCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
