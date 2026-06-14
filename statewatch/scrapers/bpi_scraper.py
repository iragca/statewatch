from datetime import date

from statewatch.wrappers.bpi import BPIAPI


class BPIScraper:
    def __init__(self):
        self.api = BPIAPI()

    def get_price_by_date(self, ticker: str, target_date: date) -> float:
        if ticker.upper() != "M1ALFMMU":
            raise NotImplementedError(f"BPI scraper does not support ticker: {ticker}")

        data = self.api.get_M1ALFMMU(
            start_date=target_date, end_date=target_date
        )
        fund_data = data.get("fundData", {})
        history = fund_data.get("fundDataHistory", [])

        if not history:
            raise ValueError(
                f"Price for {ticker} on {target_date} not found"
            )

        return float(history[0]["navpuValue"])
