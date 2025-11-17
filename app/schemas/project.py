# app/schemas/project.py
from pydantic import BaseModel, ConfigDict


class ProjectBase(BaseModel):
    name: str


class ProjectCreate(ProjectBase):
    pass


class Project(ProjectBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ProjectSettingsBase(BaseModel):
    system_voltage: float | None = None
    require_rohs: bool = False
    require_ul: bool = False


class ProjectSettingsCreate(ProjectSettingsBase):
    pass


class ProjectSettings(ProjectSettingsBase):
    id: int
    project_id: int

    model_config = ConfigDict(from_attributes=True)
