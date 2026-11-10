from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import Session

try:
    from ..models.worker import Worker
except (ImportError, ValueError):
    try:
        from app.models.worker import Worker
    except ImportError:
        from backend.app.models.worker import Worker


class WorkerRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_identification(self, code: str) -> Optional[Worker]:
        return self.db.scalars(
            select(Worker).where(Worker.identification_code == code)
        ).first()

    def get_by_id(self, worker_id: int) -> Optional[Worker]:
        return self.db.get(Worker, worker_id)
