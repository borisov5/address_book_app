from haversine import haversine
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session


app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Address(BaseModel):
    name: str = Field(min_length=1)
    latitude: float = Field()
    longitude: float = Field()
    distance: int = Field(gt=-1, lt=101)


ADDRESSES = []


@app.get("/")
def read_api(db: Session = Depends(get_db)):
    return db.query(models.Addresses).all()


@app.post("/")
def create_address(address: Address, db: Session = Depends(get_db)):

    address_model = models.Addresses()
    address_model.name = address.name
    address_model.latitude = address.latitude
    address_model.longitude = address.longitude
    address_model.distance = address.distance

    db.add(address_model)
    db.commit()

    return address


@app.put("/{address_id}")
def update_address(address_id: int, address: Address, db: Session = Depends(get_db)):

    address_model = db.query(models.Addresses).filter(models.Addresses.id == address_id).first()

    if address_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {address_id} : Does not exist"
        )

    address_model.name = address.name
    address_model.latitude = address.latitude
    address_model.longitude = address.longitude
    address_model.distance = address.distance

    db.add(address_model)
    db.commit()

    return address


@app.delete("/{address_id}")
def delete_address(address_id: int, db: Session = Depends(get_db)):

    address_model = db.query(models.Addresses).filter(models.Addresses.id == address_id).first()

    if address_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {address_id} : Does not exist"
        )

    db.query(models.Addresses).filter(models.Addresses.id == address_id).delete()

    db.commit()


@app.get("/search")
def search_address(latitude: float, longitude: float, distance: int = 10, db: Session = Depends(get_db)):
    addresses = db.query(models.Addresses).all()
    result = []
    for address in addresses:
        if haversine((latitude, longitude), (address.latitude, address.longitude)) <= distance:
            result.append(address)
    return result
