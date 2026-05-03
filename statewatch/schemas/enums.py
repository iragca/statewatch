from enum import Enum


class AssetClass(str, Enum):
    STOCKS = "Stocks"
    CRYPTOCURRENCY = "Cryptocurrency"
    COMMODITIES = "Commodities"
    CURRENCY = "Currency"
    BONDS = "Bonds"
    REAL_ESTATE = "Real Estate"


class Mode(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TESTING = "testing"


class ALPHAVANTAGE_DAILY_FUNCTION_COLUMNS(str, Enum):
    """
    Column names for the Alpha Vantage daily function output.
    Assumes the `pandas.DataFrame.reset_index()` format.
    """

    DATE = "date"
    OPEN = "1. open"
    HIGH = "2. high"
    LOW = "3. low"
    CLOSE = "4. close"
    VOLUME = "5. volume"
