from datetime import date, datetime, timedelta
from typing import Optional

import pytz
import yfinance as yf

from statewatch.core.config import env


class YFinanceScraper:
    def __init__(self):
        pass

    def get_price_by_date(self, ticker: str, date: datetime | date) -> float:
        """
        Fetch the price of a cryptocurrency by its ticker and date.

        Parameters
        ----------
        ticker : str
            The ticker symbol of the cryptocurrency.
        date : datetime | date
            The date for which to fetch the price.

        Returns
        -------
        float
            The price of the cryptocurrency on the specified date.
        """
        yf_ticker = yf.Ticker(f"{ticker.upper()}")
        price = yf_ticker.history(start=date, period="1d")["Close"].iloc[0]

        if not price:
            raise ValueError(f"Price for {ticker} on {date} not found")

        return price

    def get_price_history(
        self, ticker: str, start_date: Optional[datetime], end_date: Optional[datetime]
    ) -> list[tuple[datetime, float]]:
        """
        Fetch the price history of a cryptocurrency by its ticker and date range.

        Parameters
        ----------
        ticker : str
            The ticker symbol of the cryptocurrency.
        start_date : Optional[datetime]
            The start date for the price history.
        end_date : Optional[datetime]
            The end date for the price history.

        Returns
        -------
        list[tuple[datetime, float]]
            A list of tuples containing dates and prices for the specified date range.
        """

        if start_date is None and end_date is None:
            end_date = datetime.now(tz=pytz.timezone(env.TIMEZONE))

        yf_ticker = yf.Ticker(f"{ticker.upper()}")
        prices = yf_ticker.history(start=start_date, end=end_date)["Close"]

        if not prices:
            raise ValueError(
                f"Price history for {ticker} from {start_date} to {end_date} not found"
            )

        return sorted(
            [(date.to_pydatetime(), price) for date, price in prices.to_dict().items()]
        )
