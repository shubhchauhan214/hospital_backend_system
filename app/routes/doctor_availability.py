from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud, schemas
from app.dependencies.roles import appointment_manager_required

router = APIRouter(
  prefix="/doctor_availability",
  tags=["Doctor Availability"]
)

@router.post("/", response_model = schemas.DoctorAvailabilityResponse, status_code=status.HTTP_201_CREATED)
def create_doctor_availability(availability: schemas.DoctorAvailabilityCreate, db: Session = Depends(get_db), current_user=Depends(appointment_manager_required)):
    return crud.create_doctor_availability(db, availability = availability)

@router.get("/", response_model=List[schemas.DoctorAvailabilityResponse])
def get_doctor_availabilities(skip:int = 0, limit:int = 100, db: Session = Depends(get_db)):
    return crud.get_doctor_availabilities(db=db, skip=skip, limit=limit)

@router.get("/doctor/{doctor_id}", response_model=List[schemas.DoctorAvailabilityResponse])
def get_availability_by_doctor(doctor_id:int, db:Session = Depends(get_db)):
    return crud.get_availability_by_doctor_id(db=db, doctor_id=doctor_id)

@router.get("/{availability_id}", response_model=schemas.DoctorAvailabilityResponse)
def get_doctor_availability_by_id(availability_id: int, db: Session = Depends(get_db)):
    return crud.get_doctor_availability_by_id(db=db, availability_id=availability_id)

@router.put("/{availability_id}", response_model=schemas.DoctorAvailabilityResponse)
def update_doctor_availability(availability_id:int, availability:schemas.DoctorAvailabilityUpdate, db:Session=Depends(get_db), current_user=Depends(appointment_manager_required)):
    return crud.update_doctor_availability(db=db, availability_id=availability_id, availability_data=availability)

@router.delete("/{availability_id}")
def delete_doctor_availability(availability_id:int, db:Session=Depends(get_db), current_user=Depends(appointment_manager_required)):
    return crud.delete_doctor_availability(db=db, availability_id=availability_id)
                               
    
