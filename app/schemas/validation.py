# app/schemas/validation.py
from pydantic import BaseModel


class ValidationError(BaseModel):
    component_id: str
    component_type: str
    message: str
    error_type: str
