from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class ShiftActionRequest(BaseModel):
    identification_code: str = Field(
        ...,
        min_length=5,
        max_length=10,
        description="Cédula del trabajador para registrar evento",
    )


class ShiftResponse(BaseModel):
    id: int
    worker_id: int
    start_time: datetime
    end_time: Optional[datetime] = None
    total_minutes: Optional[int] = None
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ShiftCurrentStatusResponse(BaseModel):
    worker_id: int
    identification_code: str
    full_name: str
    position: str
    active_shift: Optional[ShiftResponse] = None
