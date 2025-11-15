from collections.abc import Generator

from app.core.config import settings
from app.db.session import SessionLocal
from app.services.kicad_engine_service import KiCadEngineService


def get_db() -> Generator:
    """
    Dependency function that yields a new SQLAlchemy database session.
    """
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        if db:
            db.close()


def get_kicad_engine() -> KiCadEngineService:
    """
    Dependency function that returns an instance of the KiCadEngineService.
    """
    return KiCadEngineService(cli_path=settings.KICAD_CLI_PATH)
