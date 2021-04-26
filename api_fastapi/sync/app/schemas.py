from typing import List, Optional

from pydantic import BaseModel


class PriceBase(BaseModel):
    ticker: str
    date: str
    open: str
    high: str
    low: str
    close: str
    close_adj: str
    volume: str


class PriceCreate(PriceBase):
    pass


class Price(PriceBase):
    id: int

    class Config:
        orm_mode = True


class TickerBase(BaseModel):
    tickers: str


class Ticker(TickerBase):
    pass
