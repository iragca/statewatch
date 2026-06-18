from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from statewatch.schemas.enums import Currency


class Root(BaseModel):
    price: float = Field(..., description="Price of the asset", ge=0)
    currency: Currency = Field(
        Currency.USD, description="Currency of the price"
    )
    date: datetime = Field(..., description="Date of the price in ISO format")

    model_config = ConfigDict(from_attributes=True)


class PriceInsert(BaseModel):
    ticker: str = Field(..., description="Asset ticker symbol (e.g. BTC, XMR)")
    price: float = Field(..., description="Price value", ge=0)
    currency: Currency = Field(
        Currency.USD, description="Currency of the price"
    )
    date: datetime = Field(..., description="Date of the price in ISO format")
