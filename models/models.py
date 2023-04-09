from sqlalchemy import Column, Integer, String, Float
from pydantic import BaseModel, Field
from database.db_init import Base


class Addresses(Base):
    """
    This is a model class. It has address table structure.
    """
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    latitude = Column(Float)
    longitude = Column(Float)
    distance = Column(Integer)


class Address(BaseModel):
    """
    Pydantic model for address
    """
    name: str = Field(min_length=1)
    latitude: float = Field()
    longitude: float = Field()
    distance: int = Field(gt=-1, lt=101)