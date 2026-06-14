import json
from datetime import date, datetime

from .rest_api import RestAPI


class BPIAPI(RestAPI):
    def __init__(
        self,
        url: str = (
            "https://www.bpi.com.ph/"
            "content/bpi/ph/en/group"
            "/bpiwealth/our-solution"
            "s/personal/investment-s"
            "olutions/funds/"
        ),
    ):
        super().__init__(
            url, default_fields={"_ts": int(datetime.now().timestamp() * 1000)}
        )

    @property
    def info(self) -> str:
        return """M1ALFMMU: ALFM Money Market Fund Units"""

    def get_M1ALFMMU(
        self, start_date: date = date.today(), end_date: date = date.today()
    ) -> dict:
        endpoint = "alfm-money-market-fund-units/jcr:content/root/container/dynamicgraph_copy_co_211059991.model.json"
        data = self.get(
            endpoint=endpoint,
            startDate=start_date.strftime("%d/%m/%Y"),
            endDate=end_date.strftime("%d/%m/%Y"),
            fundCode="M1ALFMMU",
        )
        data["fundData"] = json.loads(data["fundData"])
        return data
