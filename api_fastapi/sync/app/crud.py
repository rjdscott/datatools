from sqlalchemy.orm import Session

from . import models, schemas


def get_tickers(db: Session):
    return db.query(models.Price).distinct(models.Price.ticker).all()


def get_price(db: Session, user_id: int):
    return db.query(models.Price).filter(models.Price.id == user_id).first()


def get_ticker_prices(db: Session, ticker: str, limit: int = 2000):
    return db.query(models.Price).filter(models.Price.ticker == ticker).limit(limit).all()


def create_price(db: Session, price: schemas.PriceCreate):
    db_price = models.Price(**price.dict())
    db.add(db_price)
    db.commit()
    db.refresh(db_price)
    return db_price
