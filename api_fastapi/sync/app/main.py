from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/tickers/", response_model=List[schemas.Tickers])
def read_tickers(db: Session = Depends(get_db)):
    tickers = crud.get_tickers(db)
    return tickers


@app.get("/prices/{ticker}", response_model=List[schemas.Price])
def read_prices(ticker: str, start_date: str, end_date: str, limit: int = 1000, db: Session = Depends(get_db)):
    db_ticker_prices = crud.get_ticker_prices(db, ticker=ticker, limit=limit,
                                              start_date=start_date, end_date=end_date)
    if db_ticker_prices is None:
        raise HTTPException(status_code=404, detail="Prices not found")
    return db_ticker_prices
