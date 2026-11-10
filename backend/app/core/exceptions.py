class DomainException(Exception):
    """Excepción base para errores de la lógica de dominio."""

    def __init__(self, message: str, code: str) -> None:
        super().__init__(message)
        self.message = message
        self.code = code


class WorkerNotFoundException(DomainException):
    def __init__(
        self,
        message: str = "Trabajador no encontrado o inactivo",
        code: str = "WORKER_NOT_FOUND",
    ) -> None:
        super().__init__(message, code)


class ShiftAlreadyActiveException(DomainException):
    def __init__(
        self,
        message: str = "El trabajador ya tiene una jornada activa",
        code: str = "SHIFT_ALREADY_ACTIVE",
    ) -> None:
        super().__init__(message, code)


class ShiftNotActiveException(DomainException):
    def __init__(
        self,
        message: str = "No hay una jornada activa registrada para terminar",
        code: str = "SHIFT_NOT_ACTIVE",
    ) -> None:
        super().__init__(message, code)
