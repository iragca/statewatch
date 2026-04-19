from typing import Union

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
        self, ticker: str, asset_class: Union[AssetClass, str], name: str
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
        if isinstance(asset_class, str):
            asset_class = AssetClass[asset_class.title()]

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

    def get_current_key_index(self) -> int:
        """
        Retrieve the current maximum index of assets in the database.

        Returns
        -------
        int
            The current maximum index of assets, or 0 if no assets exist.
        """
        max_index = self.db.query(Asset).order_by(Asset.id.desc()).first()
        return max_index.id if max_index else 0
