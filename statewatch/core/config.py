import os
from typing import Literal

from pathlib import Path
from dotenv import load_dotenv


PROJ_ROOT = Path(__file__).parent.parent.parent

DATA = PROJ_ROOT / "data"
PROCESSED_DATA = DATA / "processed"


class Environment:
    """Environment configuration loader."""

    def __init__(self) -> None:
        load_dotenv()

    @property
    def DATABASE_URL(self) -> str:
        URL = os.getenv("DATABASE_URL")
        if URL is None:
            raise EnvironmentError("DATABASE_URL environment variable is not set.")
        return URL

    @property
    def DB_USERNAME(self) -> str:
        username = self.DATABASE_URL.split("@")[0].split("//")[1].split(":")[0]
        return username

    @property
    def DB_PASSWORD(self) -> str:
        password = self.DATABASE_URL.split("@")[0].split("//")[1].split(":")[1]
        return password

    @property
    def MODE(self) -> str:
        mode = os.getenv("MODE")
        if mode is None:
            raise EnvironmentError("MODE environment variable is not set.")
        return mode

    @property
    def DEPLOYMENT(self) -> Literal["docker", "vercel"]:
        """Deployment environment (e.g., docker or vercel (serverless))."""
        deployment = os.getenv("DEPLOYMENT", "docker")

        if deployment in ["docker", "vercel"]:
            return deployment  # type: ignore

        raise EnvironmentError(
            "DEPLOYMENT environment variable must be either 'docker' or 'vercel'."
        )

    @property
    def TIMEZONE(self) -> str:
        """
        Get the timezone for the application.

        NOTES
        -----
        - The timezone should be in the format of "Area/Location" (e.g., "Asia/Manila", "UTC").
        - Refer to Wikipedia for valid **timezone identifiers**:
            https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
        """
        timezone = os.getenv("TIMEZONE", "UTC")
        return timezone

    @property
    def COINGECKO_DEMO_API_KEY(self) -> str:
        api_key = os.getenv("COINGECKO_DEMO_API_KEY")
        if api_key is None:
            raise EnvironmentError(
                "COINGECKO_DEMO_API_KEY environment variable is not set."
            )
        return api_key

    @property
    def ALPHAVANTAGE_API_KEY(self) -> str:
        api_key = os.getenv("ALPHAVANTAGE_API_KEY")
        if api_key is None:
            raise EnvironmentError(
                "ALPHAVANTAGE_API_KEY environment variable is not set."
            )
        return api_key


env = Environment()
