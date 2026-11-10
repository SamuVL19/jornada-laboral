from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.shift import (
    ShiftActionRequest,
    ShiftCurrentStatusResponse,
    ShiftResponse,
)
from app.services.shift_service import ShiftService

router = APIRouter(prefix="/shifts", tags=["Shifts"])

@router.post(
    "/start",
    response_model=ShiftResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Iniciar jornada laboral",
)
def start_shift(
    payload: ShiftActionRequest,
    db: Session = Depends(get_db),
) -> ShiftResponse:
    service = ShiftService(db)
    return service.start_shift(payload.identification_code)

@router.post(
    "/end",
    response_model=ShiftResponse,
    status_code=status.HTTP_200_OK,
    summary="Finalizar jornada laboral activa",
)
def end_shift(
    payload: ShiftActionRequest,
    db: Session = Depends(get_db),
) -> ShiftResponse:
    service = ShiftService(db)
    return service.end_shift(payload.identification_code)

@router.get(
    "/current/{identification_code}",
    response_model=ShiftCurrentStatusResponse,
    status_code=status.HTTP_200_OK,
    summary="Consultar estado actual de jornada por cédula",
)
def get_current_shift_status(
    identification_code: str,
    db: Session = Depends(get_db),
) -> ShiftCurrentStatusResponse:
    service = ShiftService(db)
    return service.get_current_status(identification_code)