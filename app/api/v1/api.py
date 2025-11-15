from fastapi import APIRouter

from app.api.v1.endpoints import harness_exports

api_router = APIRouter()
api_router.include_router(harness_exports.router, prefix="/harness", tags=["harness"])
