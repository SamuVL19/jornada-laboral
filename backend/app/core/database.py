from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

try:
    from .config import settings
except (ImportError, ValueError):
    try:
        from app.core.config import settings
    except ImportError:
        from backend.app.core.config import settings


class Base(DeclarativeBase):
    """Clase base declarativa para todos los modelos SQLAlchemy 2.0."""
    pass


# Engine de SQLAlchemy configurado para conexión con Supabase / PostgreSQL
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
)

# Creador de sesiones de base de datos
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db() -> Generator[Session, None, None]:
    """Generador de sesiones de base de datos para inyección de dependencias."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
