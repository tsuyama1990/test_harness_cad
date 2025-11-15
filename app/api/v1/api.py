from fastapi import APIRouter

from app.api.v1.endpoints import harness_exports, harnesses, projects

api_router = APIRouter()
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(harness_exports.router, prefix="/projects", tags=["exports"])
api_router.include_router(harnesses.router, prefix="/harnesses", tags=["harnesses"])
