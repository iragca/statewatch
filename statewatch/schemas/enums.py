from enum import Enum


class AssetClass(str, Enum):
    STOCKS = "Stocks"
    INDEX = "Index"
    CRYPTOCURRENCY = "Cryptocurrency"
    COMMODITY = "Commodity"
    CURRENCY = "Currency"
    BONDS = "Bonds"
    REAL_ESTATE = "Real Estate"
    FUTURES = "Futures"
    FUNDS = "Funds"


class Currency(str, Enum):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    JPY = "JPY"
    PHP = "PHP"
    CAD = "CAD"
    AUD = "AUD"
    CHF = "CHF"
    CNY = "CNY"

    def __str__(self) -> str:
        return self.value


class Mode(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TESTING = "testing"


class ALPHAVANTAGE_DAILY_FUNCTION_COLUMNS(str, Enum):
    """
    Column names for the Alpha Vantage daily function output.
    Not all columns are used for each function, but are commonly found.
    """

    DATE = "date"
    OPEN = "1. open"
    HIGH = "2. high"
    LOW = "3. low"
    CLOSE = "4. close"
    VOLUME = "5. volume"
    PRICE = "price"
    VALUE = "value"
