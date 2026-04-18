from enum import Enum


class AssetClass(str, Enum):
    STOCKS = "Stocks"
    CRYPTOCURRENCY = "Cryptocurrency"
    PRECIOUS_METALS = "Precious Metals"
    CURRENCY = "Currency"
    BONDS = "Bonds"
    REAL_ESTATE = "Real Estate"


class Mode(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TESTING = "testing"
