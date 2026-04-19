from datetime import datetime

import questionary
import yfinance as yf
from pytz import timezone

from statewatch.core.config import env
from statewatch.dependencies.db import get_db_session
from statewatch.dependencies.services import get_task_service
from statewatch.schemas.enums import AssetClass
from statewatch.utils.datetime import convert_datetime_timezone

from .menu import Menu


class AssetManagerMenu(Menu):
    menu_name = "Manage Assets"

    def __init__(self, parent: str | None = None) -> None:
        self.parent_name = parent
        self.task_service = get_task_service(next(get_db_session()))

    def menu(self) -> None:
        previous_choice = None
        while True:
            char_nav = questionary.select(
                self.breadcrumbs,
                choices=[
                    f"🔙 Back to {self.parent_name}",
                    "Add Asset",
                ],
                default=previous_choice,
            ).ask()
            if char_nav is None or char_nav.startswith("🔙"):
                break

            previous_choice = char_nav

            match char_nav:
                case "Add Asset":
                    self.add_asset()
                case _:
                    break

    def add_asset(self) -> None:
        ticker = questionary.text("Enter the asset ticker (Yahoo Finance):").ask()

        if ticker:
            ticker = ticker.upper()
            yfTicker = yf.Ticker(ticker)

            name = str(
                yfTicker.info.get("shortName")
                or questionary.text("Enter the asset name:").ask()
            ).title()

            asset_class: str = questionary.select(
                "Select the asset class:",
                choices=[
                    AssetClass.CRYPTOCURRENCY.name,
                    AssetClass.BONDS.name,
                    AssetClass.STOCKS.name,
                    AssetClass.CURRENCY.name,
                    AssetClass.PRECIOUS_METALS.name,
                    AssetClass.REAL_ESTATE.name,
                ],
            ).ask()

            questionary.print("Fetching price history...")
            start_date = questionary.text(
                "Enter the start date for price history (YYYY-MM-DD):"
            ).ask()
            if start_date:
                history = yfTicker.history(
                    start=start_date, end=datetime.now(timezone(env.TIMEZONE))
                )
                prices = [
                    (
                        convert_datetime_timezone(
                            row["Date"].to_pydatetime(), env.TIMEZONE
                        ),
                        float(row["Close"]),
                    )
                    for _, row in history.reset_index().iterrows()
                ]
                self.task_service.add_asset_and_prices(
                    ticker=ticker, asset_class=asset_class, name=name, prices=prices
                )
                questionary.print(
                    "Price history added successfully!", style="bold green"
                )

        else:
            print("Asset ticker cannot be empty.")
