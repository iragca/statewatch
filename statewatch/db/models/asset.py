from datetime import datetime
from typing import TYPE_CHECKING, List

import pytz
from sqlalchemy import Enum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from statewatch.core.config import env
from statewatch.schemas.enums import AssetClass

from .base import Base

if TYPE_CHECKING:
    from .price import Price


class Asset(Base):
    """
    Asset model representing an asset in the system.

    Attributes
    ----------
    id : int
        Primary key identifier for the asset.
    name : str
        Unique name of the asset (e.g., ``Bitcoin``, ``Apple Inc.``).
    ticker : str
        Unique ticker symbol for the asset. (e.g., ``BTC``, ``AAPL``).
    asset_class : str
        The class or category to which the asset belongs (e.g., ``stock``, ``bond``, ``commodity``).
    """

    __tablename__ = "asset"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    ticker: Mapped[str] = mapped_column(unique=True, nullable=False)
    asset_class: Mapped[AssetClass] = mapped_column(Enum(AssetClass), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.now(tz=pytz.timezone(env.TIMEZONE)),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now(tz=pytz.timezone(env.TIMEZONE)),
        onupdate=datetime.now(tz=pytz.timezone(env.TIMEZONE)),
        server_default=func.now(),
    )

    prices: Mapped[List["Price"]] = relationship(back_populates="asset")
