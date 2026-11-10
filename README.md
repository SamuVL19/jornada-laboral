# Sistema de Registro de Jornada Laboral

Aplicación full-stack de control horario corporativo diseñada para quioscos y terminales de presencia. Permite a los empleados iniciar y finalizar su jornada laboral mediante su cédula, manteniendo un cómputo continuo del tiempo de trabajo y sincronización en vivo del cronómetro.

## Tecnologías Utilizadas

- **Backend:** Python 3.14, FastAPI, SQLAlchemy 2.0, Pydantic v2.
- **Base de Datos:** PostgreSQL en Supabase.
- **Frontend:** React 19, Vite, Tailwind CSS v4, Lucide React.
- **Testing:** Pytest, HTTPX.

## Arquitectura del Backend

El backend implementa una arquitectura en capas desacopladas sin dependencias circulares:

- `app/models/`: Entidades de SQLAlchemy puras (`Worker`, `Shift`).
- `app/schemas/`: Modelos de validación y DTOs con Pydantic v2.
- `app/repositories/`: Consultas de persistencia aisladas de la capa HTTP.
- `app/services/`: Lógica de negocio y orquestación de transacciones.
- `app/core/exceptions.py`: Excepciones de dominio personalizadas.
- `app/api/v1/endpoints/`: Controladores delgados para exposición de endpoints REST.
- `app/main.py`: Configuración de CORS y manejadores globales de excepciones.

## Reglas de Negocio y Errores Controlados

| Código HTTP | Error Code | Descripción |
| :--- | :--- | :--- |
| **404 Not Found** | `WORKER_NOT_FOUND` | La cédula ingresada no existe o el trabajador está inactivo. |
| **400 Bad Request** | `SHIFT_ALREADY_ACTIVE` | El trabajador ya posee una jornada en curso (`status == 'ACTIVE'`). |
| **400 Bad Request** | `SHIFT_NOT_ACTIVE` | Intento de cerrar jornada cuando no hay ningún turno activo. |

El tiempo acumulado de la jornada se computa automáticamente en minutos al cerrar el turno, asegurando un redondeo mínimo de 1 minuto.

## Datos Semilla de Prueba

- **Director General Gomez (CEO):** Cédula `100011`
- **Asistente Ejecutivo Estrada:** Cédula `100012`
