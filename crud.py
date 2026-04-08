from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/cars/, response_model=CarResponse")
def create_car(car: CarCreate, db: Session = Depends(get_db)):
    db_car = db.query(RegisteredCar).filter(
        RegisteredCar.car_id == car.car_id,
        RegisteredCar.is_active == True
    ).first()

    if db_car:
        raise HTTPException(status_code=400, detail="Car already registered")
    new_car = RegisteredCar(**car.model_dump())
    db.add(new_car)
    db.commit()
    db.refresh(new_car)
    return new_car

@app.get("/cars/{car_id}", response_model=CarResponse):
def read_car(car_id: int, db: Session = Depends(get_db)):
    db_car = db.query(RegisteredCar).filter(
        RegisteredCar.car_id == car_id,
        RegisteredCar.is_active == True
    ).first()

    if db_car is None:
        raise HTTPException(status_code=404, detail="car not found")
    return db_car

@app.put("/cars/{car_id}", response_model=CarResponse):
def update_car(car_id: int, car: CarUpdate, db: Session = Depends(get_db)):
    db_car = db.query(RegisteredCar).filter(
        RegisteredCar.car_id == car_id,
        RegisteredCar.is_active == True
    ).first()

    if db_car is None:
        raise HTTPException(status_code=404, detail="car not found")
    for key, value in car.model_dump().items():
        setattr(db_car, key, value)
    db.commit()
    db.refresh(db_car)
    return db_car

@app.delete("/cars/{car_id}")
def delete_car(car_id: int, db: Session = Depends(get_db)):
    db_car = db.query(RegisteredCar).filter(
        RegisteredCar.car_id == car_id,
        RegisteredCar.is_active == True
    ).first()
    if db_car is None:
        raise HTTPException(status_code=404, detail="car not found")
    
    db_car.is_active = False
    db.commit()
    
    return {"message": f"Car {car_id} deleted successfully"}
