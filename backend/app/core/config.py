from pathlib import Path
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Ruta al directorio backend donde se ubica .env
BACKEND_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """Configuración de la aplicación cargada desde variables de entorno y backend/.env."""

    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/postgres"

    @field_validator("DATABASE_URL", mode="after")
    @classmethod
    def assemble_db_connection(cls, v: str) -> str:
        # Supabase suele proporcionar cadenas con prefijo postgres://,
        # pero SQLAlchemy 2.0 requiere postgresql://
        if v.startswith("postgres://"):
            return v.replace("postgres://", "postgresql://", 1)
        return v

    model_config = SettingsConfigDict(
        env_file=(
            BACKEND_DIR / ".env",
            ".env",
        ),
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
