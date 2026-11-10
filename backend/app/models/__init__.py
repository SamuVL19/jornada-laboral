try:
    from ..core.database import Base
except (ImportError, ValueError):
    try:
        from app.core.database import Base
    except ImportError:
        from backend.app.core.database import Base

from .shift import Shift
from .worker import Worker

__all__ = ["Base", "Worker", "Shift"]
