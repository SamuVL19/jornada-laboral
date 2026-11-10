from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.endpoints.shifts import router as shifts_router
from app.core.exceptions import (
    ShiftAlreadyActiveException,
    ShiftNotActiveException,
    WorkerNotFoundException,
)

app = FastAPI(
    title="Sistema de Registro de Jornada Laboral",
    version="1.0.0",
)

# Configuración de CORS para clientes web (React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers globales para excepciones de dominio
@app.exception_handler(WorkerNotFoundException)
async def worker_not_found_handler(request: Request, exc: WorkerNotFoundException) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": {"code": exc.code, "message": exc.message}},
    )

@app.exception_handler(ShiftAlreadyActiveException)
async def shift_already_active_handler(request: Request, exc: ShiftAlreadyActiveException) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": {"code": exc.code, "message": exc.message}},
    )

@app.exception_handler(ShiftNotActiveException)
async def shift_not_active_handler(request: Request, exc: ShiftNotActiveException) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": {"code": exc.code, "message": exc.message}},
    )

# Inclusión de routers
app.include_router(shifts_router, prefix="/api/v1")

# Health check
@app.get("/", tags=["Health Check"])
def health_check() -> dict:
    return {
        "status": "ok",
        "service": "Sistema de Registro de Jornada Laboral",
    }