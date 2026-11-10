from datetime import datetime, timezone
import math
from typing import Any, Dict
from sqlalchemy.orm import Session

from app.core.exceptions import (
    ShiftAlreadyActiveException,
    ShiftNotActiveException,
    WorkerNotFoundException,
)
from app.models.shift import Shift
from app.models.worker import Worker
from app.repositories.shift_repository import ShiftRepository
from app.repositories.worker_repository import WorkerRepository


class ShiftService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.worker_repo = WorkerRepository(db)
        self.shift_repo = ShiftRepository(db)

    def _get_active_worker_or_fail(self, identification_code: str) -> Worker:
        worker = self.worker_repo.get_by_identification(identification_code)
        if not worker or not worker.is_active:
            raise WorkerNotFoundException()
        return worker

    def start_shift(self, identification_code: str) -> Shift:
        worker = self._get_active_worker_or_fail(identification_code)
        active_shift = self.shift_repo.get_active_by_worker_id(worker.id)
        if active_shift is not None:
            raise ShiftAlreadyActiveException()

        new_shift = Shift(
            worker_id=worker.id,
            start_time=datetime.now(timezone.utc),
            status="ACTIVE",
        )
        return self.shift_repo.create(new_shift)

    def end_shift(self, identification_code: str) -> Shift:
        worker = self._get_active_worker_or_fail(identification_code)
        active_shift = self.shift_repo.get_active_by_worker_id(worker.id)
        if active_shift is None:
            raise ShiftNotActiveException()

        now = datetime.now(timezone.utc)
        active_shift.end_time = now

        duration_seconds = (now - active_shift.start_time).total_seconds()
        calculated_minutes = math.ceil(duration_seconds / 60)
        active_shift.total_minutes = max(1, calculated_minutes)
        active_shift.status = "COMPLETED"

        return self.shift_repo.update(active_shift)

    def get_current_status(self, identification_code: str) -> Dict[str, Any]:
        worker = self._get_active_worker_or_fail(identification_code)
        active_shift = self.shift_repo.get_active_by_worker_id(worker.id)

        return {
            "worker_id": worker.id,
            "identification_code": worker.identification_code,
            "full_name": worker.full_name,
            "position": worker.position,
            "active_shift": active_shift,
        }