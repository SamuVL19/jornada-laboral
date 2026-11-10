from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.shift import Shift


class ShiftRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_active_by_worker_id(self, worker_id: int) -> Optional[Shift]:
        return self.db.scalars(
            select(Shift).where(
                Shift.worker_id == worker_id,
                Shift.status == "ACTIVE",
            )
        ).first()

    def create(self, shift: Shift) -> Shift:
        self.db.add(shift)
        self.db.commit()
        self.db.refresh(shift)
        return shift

    def update(self, shift: Shift) -> Shift:
        self.db.commit()
        self.db.refresh(shift)
        return shift