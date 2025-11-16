import sqlalchemy
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.api import deps
from app.api.v1.api import api_router
from app.core.config import settings

app = FastAPI(title="Harness Design SaaS")

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix="/api/v1")


# --- Debug Endpoint ---
# This endpoint is for debugging purposes to inspect the database state
# from within the running application's context.
@app.get("/debug/db-status")
def debug_db_status(db: Session = Depends(deps.get_db)):
    """
    Debug endpoint to check the database status from within the app context.
    """
    db_url = settings.DATABASE_URL

    try:
        # Check tables
        inspector = sqlalchemy.inspect(db.get_bind())
        tables = inspector.get_table_names()

        # Check harness data
        harness_data = []
        if "harnesses" in tables:
            # Use raw SQL to be safe
            result = db.execute(sqlalchemy.text("SELECT * FROM harnesses"))
            harness_data = [dict(row) for row in result.mappings()]

        return {
            "message": "Database status from within the running FastAPI application.",
            "database_url_in_use": db_url,
            "tables_found": tables,
            "harnesses_table_content": harness_data,
        }
    except Exception as e:
        return {
            "error": "An error occurred while inspecting the database.",
            "details": str(e),
            "database_url_in_use": db_url,
        }
