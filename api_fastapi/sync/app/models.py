from sqlalchemy import Column, Integer, String, DECIMAL, Date, Float

from .database import Base


class Price(Base):
    __tablename__ = "prices"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, nullable=False)
    ticker = Column(String, nullable=False)
    open = Column(String)
    high = Column(String)
    low = Column(String)
    close = Column(String)
    close_adj = Column(String)
    volume = Column(String)

