from sqlalchemy.orm import Session
from datetime import date
from . import models, schemas


def get_tickers(db: Session):
    data = db.query(models.Price.ticker).distinct(models.Price.ticker).all()
    return [{"ticker": x[0]} for x in data]


def get_ticker_prices(db: Session, ticker: str, start_date: date, end_date: date, limit: int = 1000, offset: int = 0):
    return db.query(models.Price)\
            .filter(models.Price.ticker == ticker)\
            .filter(models.Price.date >= start_date)\
            .filter(models.Price.date <= end_date).limit(limit).all()


def create_price(db: Session, price: schemas.PriceCreate):
    db_price = models.Price(**price.dict())
    db.add(db_price)
    db.commit()
    db.refresh(db_price)
    return db_price
