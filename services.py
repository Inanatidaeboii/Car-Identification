from sqlalchemy.orm import Session
from database import schemas, models
from uuid import UUID
from typing import List
import random


# CREATE
## Register a new car
def create_car(car: schemas.RegisteredCarCreate, db: Session):
    db_car = db.query(models.RegisteredCar).filter(
        models.RegisteredCar.car_id == car.car_id,
        # models.RegisteredCar.is_active == True
    ).first()

    if db_car:
        return None
    
    new_car = models.RegisteredCar(**car.model_dump())
    db.add(new_car)
    db.commit()
    db.refresh(new_car)
    return new_car

## Add image to a car
def add_car_image(car_id: UUID, images: List[schemas.CarImageCreate], db: Session):
    db_car = db.query(models.RegisteredCar).filter(
        models.RegisteredCar.car_id == car_id,
        # models.RegisteredCar.is_active == True
    ).first()

    if db_car is None:
        return None

    created_images = []

    for image in images:
        mock_vector = [random.uniform(-1.0, 1.0) for _ in range(512)]
        new_image = models.CarImage(
            image_url=image.image_path,
            vector=mock_vector,
            car_id=car_id)
        db.add(new_image)
        created_images.append(new_image)
    
    db.commit()
    for new_image in created_images:
        db.refresh(new_image)

    return created_images

# READ
## Read all active cars
def read_cars(db: Session):
    # return db.query(models.RegisteredCar).filter(models.RegisteredCar.is_active == True).all()
    db_cars = db.query(models.RegisteredCar).all()
    if not db_cars:
        return []
    return db_cars

## Read car details by car_id
def read_car_details(car_id: UUID, db: Session):
    db_car = db.query(models.RegisteredCar).filter(
        models.RegisteredCar.car_id == car_id,
        # models.RegisteredCar.is_active == True
    ).first()

    if db_car is None:
        return None
    
    return db_car

# UPDATE
## Update car details
def update_car(car_id: UUID, car: schemas.RegisteredCarUpdate, db: Session):
    db_car = db.query(models.RegisteredCar).filter(
        models.RegisteredCar.car_id == car_id,
        # models.RegisteredCar.is_active == True
    ).first()

    if db_car is None:
        return None
    
    for key, value in car.model_dump().items():
        setattr(db_car, key, value)

    db.commit()
    db.refresh(db_car)

    return db_car

## Update car image
def update_car_image(car_id: UUID, images: List[schemas.CarImageCreate], db: Session):
    db_images = db.query(models.CarImage).filter(
        models.CarImage.car_id == car_id
    ).first()

    if db_images is None:
        return None

    updated_images = []
    for image in images:
        mock_vector = [random.uniform(-1.0, 1.0) for _ in range(512)]
        db_images.image_path = image.image_path
        db_images.embedding_vector = mock_vector
        db.commit()
        updated_images.append(db_images)

    for updated_image in updated_images:
        db.refresh(updated_image)
    return updated_images

# DELETE
def delete_car(car_id: UUID, db: Session):
    db_car = db.query(models.RegisteredCar).filter(
        models.RegisteredCar.car_id == car_id,
        # models.RegisteredCar.is_active == True
    ).first()

    if db_car is None:
        return None
    
    db_car.is_active = False
    db.commit()
    
    return {"message": f"Car {car_id} deleted successfully"}
