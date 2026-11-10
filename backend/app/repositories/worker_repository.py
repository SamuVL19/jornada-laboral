from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.worker import Worker


class WorkerRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_identification(self, code: str) -> Optional[Worker]:
        stmt = select(Worker).where(Worker.identification_code == code)
        return self.db.scalars(stmt).first()

    def get_by_id(self, worker_id: int) -> Optional[Worker]:
        return self.db.get(Worker, worker_id)