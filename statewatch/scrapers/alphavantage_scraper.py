from datetime import date, datetime

from statewatch.wrappers.alphavantage import CustomCommodities
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
        Fetch the daily historical data for an asset by its ticker.

        Parameters
        ----------
        ticker : str
            The ticker symbol of the asset.

        Returns
        -------
        DataFrame
            A DataFrame containing the daily historical data for the asset.
        """

        data = self._get_daily_data(type, ticker)
        return data

    def _get_daily_data(self, type: AssetClass, ticker: str) -> DataFrame:
        """
        Fetch the daily historical data for an asset by its ticker.

        Parameters
        ----------
        ticker : str
            The ticker symbol of the asset.

        Returns
        -------
        DataFrame
            A DataFrame containing the daily historical data for the asset.
        """

        match type:
            case AssetClass.CRYPTOCURRENCY:
                data = self.get_cryptocurrency_history(ticker)
            case AssetClass.COMMODITY:
                data = self.get_commodities_history(ticker)
            case _:
                raise ValueError(f"Unsupported asset class: {type}")

        return data

    def get_cryptocurrency_history(self, ticker: str) -> DataFrame:
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
        cc = CryptoCurrencies(key=self.api_key, output_format="pandas")
        dataframe, _ = cc.get_digital_currency_daily(
            symbol=ticker.upper(), market="USD"
        )
        return dataframe.reset_index(drop=True)[[COLUMNS.DATE, COLUMNS.CLOSE]]

    def get_commodities_history(self, ticker: str) -> DataFrame:
        """
        Fetch the daily historical data for a commodity by its ticker.

        Parameters
        ----------
        ticker : str
            The ticker symbol of the commodity.

        Returns
        -------
        DataFrame
            A DataFrame containing the daily historical data for the commodity.
        """
        comms = CustomCommodities(key=self.api_key, output_format="pandas")
        match ticker.upper():
            case "GOLD" | "XAU":
                dataframe, _ = comms.get_gold(interval="daily")
            case "SILVER" | "XAG":
                dataframe, _ = comms.get_silver(interval="daily")
            case _:
                raise ValueError(f"Unsupported commodity ticker: {ticker}")

        return dataframe.reset_index(drop=True)[[COLUMNS.DATE, COLUMNS.PRICE]]
