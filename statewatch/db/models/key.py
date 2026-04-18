from datetime import datetime

import pytz
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from statewatch.core.config import env

from .base import Base


class Key(Base):
    """Key model representing an API key in the system.

    Attributes
    ----------
    id : int
        Primary key identifier for the API key entry.
    api_key : str
        The API key string used for authentication and authorization.
    created_at : datetime
        The date and time when the API key was created.
    """

    __tablename__ = "key"

    id: Mapped[int] = mapped_column(primary_key=True)
    api_key: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.now(tz=pytz.timezone(env.TIMEZONE)),
        server_default=func.now(),
    )
