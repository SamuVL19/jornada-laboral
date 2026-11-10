from typing import Generator
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.main import app
from app.models.worker import Worker

# Base de datos SQLite en memoria compartida para pruebas
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine_test = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine_test,
)


@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    Base.metadata.create_all(bind=engine_test)
    session = TestingSessionLocal()

    # Datos semilla de prueba
    seed_workers = [
        Worker(
            identification_code="100011",
            full_name="Director General Gomez",
            email="ceo@empresa.com",
            position="CEO",
            is_active=True,
        ),
        Worker(
            identification_code="100012",
            full_name="Asistente Ejecutivo Estrada",
            email="asistente@empresa.com",
            position="Asistente",
            is_active=True,
        ),
        Worker(
            identification_code="100099",
            full_name="Inactivo Test",
            email="inactivo@empresa.com",
            position="Operario",
            is_active=False,
        ),
    ]
    session.add_all(seed_workers)
    session.commit()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine_test)


@pytest.fixture(scope="function")
def client(db_session: Session) -> Generator[TestClient, None, None]:
    def override_get_db() -> Generator[Session, None, None]:
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
