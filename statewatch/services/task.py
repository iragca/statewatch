from .asset import AssetService
from .price import PriceService
from sqlalchemy.orm import Session
from datetime import datetime

class TaskService(AssetService, PriceService):
    def __init__(
        self,
        db_session: Session,
    ):
        self.db = db_session

    def add_asset_and_prices(
        self,
        ticker: str,
        asset_class: str,
        name: str,
        prices: list[tuple[datetime, float]],
    ) -> None:
        """
        Add a new asset along with its price history in a single transaction.

        Parameters
        ----------
        ticker : str
            The ticker symbol of the asset to create.
        asset_class : str
            The class or category to which the asset belongs.
        name : str
            The name of the asset to create.
        prices : list[tuple[datetime, float]]
             A list of tuples containing the price value and date for each record to be added.
        """

        try:
            asset = self.create_asset(
                ticker=ticker, asset_class=asset_class, name=name, commit=False
            )
            self.db.flush()
            self.db.refresh(asset)
            self.add_prices(prices=prices, asset_id=asset.id, commit=False)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e