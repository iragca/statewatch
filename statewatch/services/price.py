from sqlalchemy.orm import Session

from statewatch.db.models import Price, Asset


class PriceService:
    def __init__(
        self,
        db_session: Session,
    ):
        """
        Initialize the price service for price inquires and management.

        Parameters
        ----------
        db : Session
            Active SQLAlchemy session.
        """
        self.db = db_session

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

    def get_price_history(self, ticker: str):
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
