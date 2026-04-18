from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy.orm import Session

from statewatch.db.models import Asset, Price
from statewatch.scrapers import CryptocurrencyScraper


class PriceService:
    def __init__(
        self,
        db_session: Session,
        cryptocurrency_scraper: Optional[CryptocurrencyScraper] = None,
    ):
        """
        Initialize the price service for price inquires and management.

        Parameters
        ----------
        db : Session
            Active SQLAlchemy session.
        """
        self.db = db_session
        self.cryptocurrency_scraper = cryptocurrency_scraper

    def get_latest_price(self, ticker: str) -> Price:
        """
        Retrieve the latest price for a given ticker.

        Parameters
        ----------
        ticker : str
            The ticker symbol to retrieve the price for.

        Returns
        -------
        Price
            The latest price record for the specified ticker.
        """
        result = (
            self.db.query(Price)
            .join(Price.asset)
            .filter(Asset.ticker == ticker.upper())
            .order_by(Price.date.desc())
            .first()
        )

        if not result:
            raise ValueError("Price not found for the given ticker")

        return result

    def get_price_history(self, ticker: str) -> list[Price]:
        """
        Retrieve the price history for a given ticker.

        Parameters
        ----------
        ticker : str
            The ticker symbol to retrieve the price history for.

        Returns
        -------
        List[Price]
            A list of price records for the specified ticker.
        """
        results = (
            self.db.query(Price)
            .join(Price.asset)
            .filter(Asset.ticker == ticker.upper())
            .order_by(Price.date.desc())
            .all()
        )

        if not results:
            raise ValueError("Price history not found for the given ticker")

        return results

    def find_missing_prices(
        self, ticker: str, start_date: Optional[datetime] = None
    ) -> list[datetime]:
        """
        Identify missing price records for a given ticker.

        Parameters
        ----------
        ticker : str
            The ticker symbol to check for missing price records.
        start_date : Optional[datetime]
            The date from which to start checking for missing price records. If not provided, it will check from the earliest available record.

        Returns
        -------
        List[datetime]
            A list of dates for which price records are missing.
        """

        if self.cryptocurrency_scraper:
            raise NotImplementedError(
                "Missing price detection is not implemented for cryptocurrencies yet."
            )

        existing_records = self.get_price_history(ticker)

        if not existing_records and not start_date:
            raise ValueError("No price records found for the given ticker")

        existing_dates = {record.date for record in existing_records}

        if start_date:
            date_range = [
                start_date + timedelta(days=i)
                for i in range((datetime.now() - start_date).days)
            ]
        else:
            date_range = [
                existing_records[-1].date + timedelta(days=i)
                for i in range((datetime.now().date() - existing_records[-1].date).days)
            ]

        missing_dates = sorted(d for d in date_range if d not in existing_dates)

        return missing_dates

    def add_price(self, price: float, date: datetime, asset_id: int):
        """
        Add a new price record for a given asset.

        Parameters
        ----------
        price : float
            The price value to be added.
        date : datetime
            The date for which the price is being added.
        asset_id : int
            The ID of the asset for which to add the price.
        price : float
            The price value to be added.
        date : datetime
            The date for which the price is being added.
        """

        new_price = Price(value=price, date=date, asset_id=asset_id)
        self.db.add(new_price)
        self.db.commit()

    def add_prices(self, prices: list[tuple[datetime, float]], asset_id: int):
        """
        Add multiple price records for a given asset.

        Parameters
        ----------
        prices : List[Tuple[float, datetime]]
            A list of tuples containing the price value and date for each record to be added.
        asset_id : int
            The ID of the asset for which to add the prices.
        """

        new_prices = [
            Price(value=price, date=date, asset_id=asset_id) for price, date in prices
        ]
        self.db.add_all(new_prices)
        self.db.commit()
