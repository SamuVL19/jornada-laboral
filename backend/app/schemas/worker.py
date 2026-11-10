from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class WorkerBase(BaseModel):
    identification_code: str = Field(..., min_length=5, max_length=10)
    full_name: str = Field(..., min_length=3, max_length=120)
    email: EmailStr
    position: str = Field(..., min_length=2, max_length=60)


class WorkerResponse(WorkerBase):
    id: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
