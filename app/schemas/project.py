from typing import Optional

from pydantic import BaseModel


class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(ProjectBase):
    pass


class ProjectInDBBase(ProjectBase):
    id: int

    class Config:
        orm_mode = True


class Project(ProjectInDBBase):
    pass
