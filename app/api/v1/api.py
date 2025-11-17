from fastapi import APIRouter

from app.api.v1.endpoints import components, harness_exports, harnesses, projects, importer

api_router = APIRouter()
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(harness_exports.router, prefix="/harnesses", tags=["exports"])
api_router.include_router(harnesses.router, prefix="/harnesses", tags=["harnesses"])
api_router.include_router(components.router, prefix="/components", tags=["components"])
