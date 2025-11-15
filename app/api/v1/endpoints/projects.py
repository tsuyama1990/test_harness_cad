from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.models.harness_design import HarnessDesign
from app.models.project import Project
from app.schemas import project as project_schema
from app.schemas import harness_design as harness_design_schema


router = APIRouter()


@router.post("/", response_model=project_schema.Project)
def create_project(
    *,
    db: Session = Depends(deps.get_db),
    project_in: project_schema.ProjectCreate,
) -> Project:
    """
    Create a new project.
    """
    project = db.query(Project).filter(Project.name == project_in.name).first()
    if project:
        raise HTTPException(
            status_code=400,
            detail="A project with this name already exists.",
        )
    db_project = Project(name=project_in.name)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


@router.get("/{project_id}", response_model=project_schema.Project)
def get_project(
    *,
    db: Session = Depends(deps.get_db),
    project_id: int,
) -> Project:
    """
    Get a project by its ID.
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.post("/{project_id}/save")
def save_harness_design(
    *,
    db: Session = Depends(deps.get_db),
    project_id: int,
    design_in: harness_design_schema.DesignSave,
) -> dict:
    """
    Save a new harness design for a project.
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    harness_design = HarnessDesign(
        project_id=project_id,
        design_data=design_in.design_data.model_dump()
    )
    db.add(harness_design)
    db.commit()
    db.refresh(harness_design)
    return {"status": "success", "harness_design_id": harness_design.id}
