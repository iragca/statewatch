from typing import Literal

from alpha_vantage.alphavantage import AlphaVantage as av
from alpha_vantage.commodities import Commodities


class CustomCommodities(Commodities):
    def __init__(self, key: str, output_format: str = "pandas"):
        super().__init__(key=key, output_format=output_format)

    @av._output_format
    @av._call_api_on_func
    def get_gold(
        self, interval: str = "daily", symbol: Literal["GOLD", "XAU"] = "GOLD"
    ):
        _FUNCTION_KEY = "GOLD_SILVER_HISTORY"
        return _FUNCTION_KEY, "data", None

    @av._output_format
    @av._call_api_on_func
    def get_silver(
        self, interval: str = "daily", symbol: Literal["SILVER", "XAG"] = "SILVER"
    ):
        _FUNCTION_KEY = "GOLD_SILVER_HISTORY"
        return _FUNCTION_KEY, "data", None
