from typing import List, Optional

from pydantic import BaseModel


class PriceBase(BaseModel):
    ticker: str
    date: str
    open: float
    high: float
    low: float
    close: float
    adj_close: float
    volume: int


class PriceCreate(PriceBase):
    pass


class Price(PriceBase):
    id: int
    ticker: str
    date: str
    open: float
    high: float
    low: float
    close: float
    adj_close: float
    volume: int

    class Config:
        orm_mode = True


class TickerBase(BaseModel):
    tickers: str


class Ticker(TickerBase):
    pass
