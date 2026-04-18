from coingecko_sdk import AsyncCoingecko
from datetime import datetime


class CryptocurrencyScraper:
    def __init__(self, COINGECKO_DEMO_API_KEY: str):
        self.client = AsyncCoingecko(
            demo_api_key=COINGECKO_DEMO_API_KEY,
            environment="demo",
        )
        self.time_format = "%Y-%m-%d"

    async def get_current_price(self, name: str) -> float:
        """Get the current price of a cryptocurrency in USD.

        Parameters
        ----------

        name : str
            The name of the cryptocurrency (e.g., "monero", "bitcoin").

        Returns
        -------
        float
            The price of the cryptocurrency in USD.

        Raises
        ------
        ValueError
            If the price for the given name is not found.
        """
        price = await self.client.simple.price.get(
            vs_currencies="usd", ids=name.lower()
        )

        if (price is None) or (name not in price):
            raise ValueError(f"Price for {name} not found")

        usd = price[name].usd

        if usd is None:
            raise ValueError(f"Price for {name} not found")

        return float(usd)

    async def get_price_by_date(self, name: str, date: datetime) -> float:
        """Get the price of a cryptocurrency in USD for a specific date.

        Parameters
        ----------

        name : str
            The name of the cryptocurrency (e.g., "monero", "bitcoin").
        date : datetime
            The date for which to retrieve the price.

        Returns
        -------
        float
            The price of the cryptocurrency in USD on the specified date.

        Raises
        ------
        ValueError
            If the price for the given name and date is not found.
        """

        price = await self.client.coins.history.get(
            id=name.lower(), date=date.strftime(self.time_format)
        )

        if (price is None) or hasattr(price, "market_data") is False:
            raise ValueError(f"Price for {name} on {date} not found")

        if price.market_data is None or price.market_data.current_price is None:
            raise ValueError(f"Price for {name} on {date} not found")

        usd = price.market_data.current_price.usd

        if usd is None:
            raise ValueError(f"Price for {name} on {date} not found")

        return usd

    async def get_price_history(
        self, name: str, start: datetime, end: datetime
    ) -> list[tuple[datetime, float]]:
        """Get the price history of a cryptocurrency in USD for the given date range.

        Parameters
        ----------

        name : str
            The name of the cryptocurrency (e.g., "monero", "bitcoin").
        start : datetime
            The start date for the price history.
        end : datetime
            The end date for the price history.

        Returns
        -------
        list[tuple[datetime, float]]
            A list of tuples containing the timestamp and price in USD.

        Raises
        ------
        ValueError
            If the price history for the given name is not found.
        """

        history = await self.client.coins.market_chart.get_range(
            id=name.lower(),
            vs_currency="usd",
            from_=start.strftime(self.time_format),
            to=end.strftime(self.time_format),
            interval="daily",
        )

        if history is None:
            raise ValueError(f"Price history for {name} not found")

        if history.prices is None:
            raise ValueError(f"Price history for {name} not found")

        # The API returns timestamps in milliseconds,
        # so we need to convert them to UNIX seconds by dividing by 1000.
        return [
            (datetime.fromtimestamp(price[0] / 1000), price[1])
            for price in history.prices
        ]
