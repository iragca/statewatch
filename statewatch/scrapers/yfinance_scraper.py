import yfinance as yf
from datetime import datetime, date


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
        yf_ticker = yf.Ticker(f"{ticker.upper()}-USD")
        price = yf_ticker.history(start=date, period="1d")["Close"].iloc[0]

        if price.empty:
            raise ValueError(f"Price for {ticker} on {date} not found")

        return price

    def get_price_history(
        self, ticker: str, start_date: datetime, end_date: datetime
    ) -> list[tuple[datetime, float]]:
        """
        Fetch the price history of a cryptocurrency by its ticker and date range.

        Parameters
        ----------
        ticker : str
            The ticker symbol of the cryptocurrency.
        start_date : datetime
            The start date for the price history.
        end_date : datetime
            The end date for the price history.

        Returns
        -------
        list[tuple[datetime, float]]
            A list of tuples containing dates and prices for the specified date range.
        """
        yf_ticker = yf.Ticker(f"{ticker.upper()}-USD")
        prices = yf_ticker.history(start=start_date, end=end_date)["Close"]

        if prices.empty:
            raise ValueError(
                f"Price history for {ticker} from {start_date} to {end_date} not found"
            )

        return sorted(
            [(date.to_pydatetime(), price) for date, price in prices.to_dict().items()]
        )
