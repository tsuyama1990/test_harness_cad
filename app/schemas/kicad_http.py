from pydantic import BaseModel


class KiCadHttpValidation(BaseModel):
    categories: str
    parts: str


class KiCadHttpCategory(BaseModel):
    id: str
    name: str


class KiCadHttpPart(BaseModel):
    id: str
    name: str
    description: str
    symbol: str
    footprint: str
    mpn: str
