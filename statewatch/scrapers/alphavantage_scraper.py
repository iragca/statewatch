from datetime import date, datetime

from alpha_vantage.cryptocurrencies import CryptoCurrencies
from pandas import DataFrame

from statewatch.schemas.enums import ALPHAVANTAGE_DAILY_FUNCTION_COLUMNS as COLUMNS
from statewatch.schemas.enums import AssetClass


class ALPHAVANTAGEScraper:
    def __init__(self, ALPHAVANTAGE_API_KEY: str):
        self.api_key = ALPHAVANTAGE_API_KEY

    def get_price_by_date(
        self, type: AssetClass, ticker: str, date: datetime | date
    ) -> float:
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
        data = self._get_daily_data(type, ticker)
        price = data[data[COLUMNS.DATE] == date][COLUMNS.CLOSE]

        if not price:
            raise ValueError(f"Price for {ticker} on {date} not found")

        return float(price)

    def get_price_history(self, type: AssetClass, ticker: str) -> DataFrame:
        """
        Fetch the daily historical data for a cryptocurrency by its ticker.

        Parameters
        ----------
        ticker : str
            The ticker symbol of the cryptocurrency.

        Returns
        -------
        DataFrame
            A DataFrame containing the daily historical data for the cryptocurrency.
        """

        data = self._get_daily_data(type, ticker)
        return data[COLUMNS.DATE, COLUMNS.CLOSE]

    def _get_daily_data(self, type: AssetClass, ticker: str) -> DataFrame:
        """
        Fetch the daily historical data for a cryptocurrency by its ticker.

        Parameters
        ----------
        ticker : str
            The ticker symbol of the cryptocurrency.

        Returns
        -------
        DataFrame
            A DataFrame containing the daily historical data for the cryptocurrency.
        """

        match type:
            case AssetClass.CRYPTOCURRENCY:
                cc = CryptoCurrencies(key=self.api_key, output_format="pandas")
                result = cc.get_digital_currency_daily(
                    symbol=ticker.upper(), market="USD"
                ).reset_index()
                data: DataFrame = result[0]
            case _:
                raise ValueError(f"Unsupported asset class: {type}")

        return data
