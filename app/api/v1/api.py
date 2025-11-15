from fastapi import APIRouter

from app.api.v1.endpoints import admin, harness_exports, kicad_library, projects

api_router = APIRouter()
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(harness_exports.router, prefix="/projects", tags=["exports"])
api_router.include_router(admin.router)
api_router.include_router(kicad_library.router)
