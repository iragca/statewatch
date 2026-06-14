from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class Root(BaseModel):
    price: float = Field(..., description="Price of the asset", ge=0)
    date: datetime = Field(..., description="Date of the price in ISO format")

    model_config = ConfigDict(from_attributes=True)


class PriceInsert(BaseModel):
    ticker: str = Field(..., description="Asset ticker symbol (e.g. BTC, XMR)")
    price: float = Field(..., description="Price value", ge=0)
    date: datetime = Field(..., description="Date of the price in ISO format")
