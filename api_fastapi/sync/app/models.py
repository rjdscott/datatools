from sqlalchemy import Column, Integer, String, DECIMAL, Date, Float

from .database import Base


class Price(Base):
    __tablename__ = "prices"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, index=True, nullable=False)
    ticker = Column(String, index=True, nullable=False)
    open = Column(Float, null=False)
    high = Column(Float, null=False)
    low = Column(Float, null=False)
    close = Column(Float, null=False)
    adj_close = Column(Float, null=False)
    volume = Column(DECIMAL, null=False)

