from sqlalchemy import Column, Integer, String, Float
from database import Base


class Addresses(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    distance = Column(Integer)
