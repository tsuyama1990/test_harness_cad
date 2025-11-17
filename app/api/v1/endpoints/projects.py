# app/api/v1/endpoints/projects.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.api import deps

router = APIRouter()


@router.post("/", response_model=schemas.Project)
def create_project(
    *,
    db: Session = Depends(deps.get_db),
    project_in: schemas.ProjectCreate,
):
    """
    Create new project.
    """
    project = models.Project(name=project_in.name)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@router.post("/{project_id}/save", response_model=schemas.HarnessDesignSaveResponse)
def save_design(
    *,
    db: Session = Depends(deps.get_db),
    project_id: int,
    design_in: schemas.DesignSave,
):
    """
    Save a harness design.
    """
    # In a real app, you'd have a more robust way of handling designs
    # For now, we'll just create a new harness design every time
    harness = models.Harness(name="New Harness")
    db.add(harness)
    db.commit()
    db.refresh(harness)

    harness_design = models.HarnessDesign(
        project_id=project_id,
        harness_id=harness.id,
        design_data=design_in.design_data.model_dump(),
    )
    db.add(harness_design)
    db.commit()
    db.refresh(harness_design)
    return {"status": "success", "harness_design_id": harness_design.id}


@router.post("/{project_id}/settings", response_model=schemas.ProjectSettings)
def update_project_settings(
    *,
    db: Session = Depends(deps.get_db),
    project_id: int,
    settings_in: schemas.ProjectSettingsCreate,
):
    """
    Create or update project settings.
    """
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if project.settings:
        # Update existing settings
        project.settings.system_voltage = settings_in.system_voltage
        project.settings.require_rohs = settings_in.require_rohs
        project.settings.require_ul = settings_in.require_ul
    else:
        # Create new settings
        project.settings = models.ProjectSettings(**settings_in.model_dump())

    db.add(project.settings)
    db.commit()
    db.refresh(project.settings)
    return project.settings
