from datetime import datetime
from typing import List, TYPE_CHECKING
from sqlalchemy import BigInteger, Boolean, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.shift import Shift


class Worker(Base):
    __tablename__ = "workers"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    identification_code: Mapped[str] = mapped_column(String(10), unique=True, index=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    position: Mapped[str] = mapped_column(String(60), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    shifts: Mapped[List["Shift"]] = relationship(
        "Shift",
        back_populates="worker",
        cascade="all, delete-orphan",
    )