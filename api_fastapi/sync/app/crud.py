from sqlalchemy.orm import Session

from . import models, schemas


def get_tickers(db: Session):
    data = db.query(models.Price.ticker).distinct(models.Price.ticker).all()
    return [{"ticker": x[0]} for x in data]


def get_ticker_prices(db: Session, ticker: str, limit: int = 2000, offset: int = 0):
    return db.query(models.Price).filter(models.Price.ticker == ticker).limit(limit).offset(offset).all()


def create_price(db: Session, price: schemas.PriceCreate):
    db_price = models.Price(**price.dict())
    db.add(db_price)
    db.commit()
    db.refresh(db_price)
    return db_price
