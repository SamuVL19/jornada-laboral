# Directrices de Desarrollo - Registro de Jornada Laboral

## Contexto del Proyecto
Aplicación full-stack de registro de entrada y salida laboral para trabajadores.
- Identificador del empleado: Cédula única (`identification_code`).
- Roles semilla: CEO (`100011`) y Asistente (`100012`).

## Stack Tecnológico
- Backend: Python 3.14, FastAPI, SQLAlchemy 2.0 (sintaxis `select()`, `Mapped`), Pydantic v2.
- Base de Datos: PostgreSQL en Supabase, claves primarias `BigInteger` autoincrementables.
- Frontend: React + Vite (SPA).

## Reglas Estrictas de Código y Arquitectura
- **Importaciones Limpias:** NUNCA uses bloques `try...except` anidados para importar módulos. Usa siempre imports absolutos directos con el prefijo `app.` (ejemplo: `from app.core.database import get_db`).
- **Arquitectura en Capas:**
  - `models/`: Entidades de SQLAlchemy puras.
  - `schemas/`: DTOs de Pydantic v2 (`ConfigDict(from_attributes=True)`).
  - `repositories/`: Consultas y operaciones de base de datos sin lógica de negocio ni HTTP exceptions.
  - `services/`: Reglas de negocio y lanzamiento de excepciones de dominio (`DomainException`).
  - `api/v1/endpoints/`: Controladores FastAPI delgados que delegan al servicio e inyectan dependencias.
  - `main.py`: Manejo global de excepciones (`exception_handler`) y middlewares.

## Escenarios de Error Controlados
1. `WorkerNotFoundException` (HTTP 404): Cédula no registrada o empleado inactivo (`WORKER_NOT_FOUND`).
2. `ShiftAlreadyActiveException` (HTTP 400): Intento de iniciar turno teniendo una jornada activa (`SHIFT_ALREADY_ACTIVE`).
3. `ShiftNotActiveException` (HTTP 400): Intento de finalizar turno sin haber iniciado previamente (`SHIFT_NOT_ACTIVE`).