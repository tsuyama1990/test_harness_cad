import os
import tempfile
from collections.abc import Generator
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

import app.models  # Ensure all models are loaded for metadata
from app.api.deps import get_db
from app.db.base import Base
from app.main import app
from app.services.kicad_engine_service import KiCadEngineService

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session() -> Generator:
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session: Session) -> Generator:
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def mock_kicad_engine() -> Generator[MagicMock, None, None]:
    """Fixture to mock the KiCadEngineService and handle temporary files."""
    sch_file = tempfile.NamedTemporaryFile(delete=False, suffix=".kicad_sch")
    dxf_file = tempfile.NamedTemporaryFile(delete=False, suffix=".dxf")

    mock_engine = MagicMock(spec=KiCadEngineService)
    mock_engine.generate_sch_from_json.return_value = sch_file.name
    mock_engine.export_dxf.return_value = dxf_file.name

    yield mock_engine

    # Cleanup: a robust way to remove files that might already be deleted
    for f in [sch_file, dxf_file]:
        try:
            os.remove(f.name)
        except FileNotFoundError:
            pass
