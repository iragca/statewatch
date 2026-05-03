from datetime import datetime
from typing import TYPE_CHECKING

import pytz
from sqlalchemy import DateTime, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from statewatch.core.config import env

from .base import Base

if TYPE_CHECKING:
    from .asset import Asset


class Price(Base):
    """Price model representing the price of an asset at a specific timestamp.


    Attributes
    ----------
    id : int
        Primary key identifier for the price entry.
    asset_id : int
        Foreign key referencing the associated asset.
    price : float
        The price of the asset at the given timestamp.
    date : Date
        The date and time when the price was recorded.
    """

    __tablename__ = "price"

    id: Mapped[int] = mapped_column(primary_key=True)
    asset_id: Mapped[int] = mapped_column(ForeignKey("asset.id"), nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    date: Mapped[datetime] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(tz=pytz.timezone(env.TIMEZONE)),
        server_default=func.now(),
    )

    asset: Mapped["Asset"] = relationship(back_populates="prices")

    __table_args__ = (UniqueConstraint("asset_id", "date", name="uq_asset_date"),)
