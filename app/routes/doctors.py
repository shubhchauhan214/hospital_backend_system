from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud, schemas

router = APIRouter(prefix="/doctors", tags=["Doctors"])


@router.post("/", response_model=schemas.DoctorResponse, status_code=status.HTTP_201_CREATED)
def create_doctor(doctor: schemas.DoctorCreate, db: Session = Depends(get_db)):
    return crud.create_doctor(db=db, doctor=doctor)

@router.get("/", response_model=List[schemas.DoctorResponse])
def get_doctors(skip: int = 0, limit:int = 100, db:Session = Depends(get_db)):
    return crud.get_doctors(db=db, skip=skip, limit=limit)

@router.get("/{doctor_id}", response_model=schemas.DoctorResponse)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    return crud.get_doctor_by_id(db=db, doctor_id=doctor_id)

@router.put("/{doctor_id}", response_model=schemas.DoctorResponse)
def update_doctor(doctor_id: int, doctor: schemas.DoctorUpdate, db: Session = Depends(get_db)):
    return crud.update_doctor(db=db, doctor_id = doctor_id, doctor_data=doctor)

@router.delete("/{doctor_id}")
def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    return crud.delete_doctor(db=db, doctor_id=doctor_id)

