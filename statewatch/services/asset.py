from typing import Optional

from sqlalchemy.orm import Session

from statewatch.db.models import Asset
from statewatch.schemas.enums import AssetClass


class AssetService:
    def __init__(
        self,
        db_session: Session,
    ):
        """
        Initialize the asset service for asset management.

        Parameters
        ----------
        db : Session
            Active SQLAlchemy session.
        """
        self.db = db_session

    def create_asset(
        self, ticker: str, asset_class: Optional[AssetClass], name: Optional[str]
    ) -> Asset:
        """
        Create a new asset record in the database.

        Parameters
        ----------
        ticker : str
            The ticker symbol of the asset to create.
        asset_class : AssetClass
            The class or category to which the asset belongs.
        name : str
            The name of the asset to create.

        Returns
        -------
        Asset
            The newly created asset record.
        """
        asset = Asset(ticker=ticker.upper(), name=name, asset_class=asset_class)
        self.db.add(asset)
        self.db.commit()
        self.db.refresh(asset)
        return asset

    def get_asset_by_ticker(self, ticker: str) -> Asset:
        """
        Retrieve an asset record by its ticker symbol.

        Parameters
        ----------
        ticker : str
            The ticker symbol to search for.

        Returns
        -------
        Asset
            The asset record matching the given ticker, or None if not found.
        """
        result = self.db.query(Asset).filter(Asset.ticker == ticker.upper()).first()

        if not result:
            raise ValueError("Asset not found for the given ticker")

        return result
