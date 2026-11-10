from datetime import datetime
from typing import TYPE_CHECKING, List
from sqlalchemy import BigInteger, Boolean, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

try:
    from ..core.database import Base
except (ImportError, ValueError):
    try:
        from app.core.database import Base
    except ImportError:
        from backend.app.core.database import Base

if TYPE_CHECKING:
    from .shift import Shift


class Worker(Base):
    __tablename__ = "workers"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    identification_code: Mapped[str] = mapped_column(
        String(10),
        unique=True,
        index=True,
        nullable=False,
    )
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    position: Mapped[str] = mapped_column(String(60), nullable=False)
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        server_default="true",
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # Relación 1 a N con shifts
    shifts: Mapped[List["Shift"]] = relationship(
        "Shift",
        back_populates="worker",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
