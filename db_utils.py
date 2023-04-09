from haversine import haversine
from fastapi import FastAPI, HTTPException, Depends
from database.db_init import engine, SessionLocal
from models import models
from sqlalchemy.orm import Session
from models.models import Addresses, Address
from logger.logger import log_warning, log_error, log_critical


ADDRESSES = []

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    """
    This is function for getting database.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_api(db: Session = Depends(get_db)):
    """
    This method will return all addresses which are presented in database.
    """
    log_warning('All addresses are readed')
    return db.query(models.Addresses).all()


@app.post("/")
def create_address(address: Address, db: Session = Depends(get_db)):
    """
    This is post method for creating a new address to database.
    It will perform the commit to db.
    """
    address_model = models.Addresses()
    address_model.name = address.name
    address_model.latitude = address.latitude
    address_model.longitude = address.longitude
    address_model.distance = address.distance

    db.add(address_model)
    db.commit()
    log_warning('Address created')
    return address


@app.put("/{address_id}")
def update_address(address_id: int, address: Address, db: Session = Depends(get_db)):
    """
    This is put method for updating address in database.
    """
    address_model = db.query(models.Addresses).filter(Addresses.id == address_id).first()
    if address_model is None:
        log_error('There is no such id')
        raise HTTPException(
            status_code=404,
            detail=f"ID {address_id} : Does not exist",
        )
    address_model.name = address.name
    address_model.latitude = address.latitude
    address_model.longitude = address.longitude
    address_model.distance = address.distance
    db.add(address_model)
    db.commit()
    log_warning('Address updated')
    return address


@app.delete("/{address_id}")
def delete_address(address_id: int, db: Session = Depends(get_db)):
    """
    This will delete the address from database based on primary key.
    """
    address_model = db.query(models.Addresses).filter(models.Addresses.id == address_id).first()
    if address_model is None:
        log_error('There is no such id')
        raise HTTPException(
            status_code=404,
            detail=f"ID {address_id} : Does not exist",
        )
    db.query(models.Addresses).filter(models.Addresses.id == address_id).delete()
    db.commit()
    log_critical('Address deleted')
    return f"Address with {address_id} successfuly deleted"


@app.get("/search")
def search_address(latitude: float, longitude: float, distance: int = 10, db: Session = Depends(get_db)):
    """
    This is get method for searching address.
    """
    addresses = db.query(models.Addresses).all()
    result = []
    for address in addresses:
        if haversine((latitude, longitude), (address.latitude, address.longitude)) <= distance:
            result.append(address)
    log_warning('Searching for address')
    return result


@app.get("/{address_id}")
def read_api_by_id(address_id: int, db: Session = Depends(get_db)):
    """
    This is get method for reading addresses.
    """
    address_model = db.query(models.Addresses).filter(models.Addresses.id == address_id).first()
    if address_model is None:
        log_error('There is no such id')
        raise HTTPException(
            status_code=404,
            detail=f"ID {address_id} : Does not exist",
        )
    log_warning('Address is readed')
    return address_model
