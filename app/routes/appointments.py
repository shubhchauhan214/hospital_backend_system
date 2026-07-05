from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud, schemas
from app.dependencies.roles import appointment_manager_required, admin_required, doctor_required

router = APIRouter(prefix="/appointments", tags=["Appointments"])

@router.post("/", response_model=schemas.AppointmentResponse, status_code=status.HTTP_201_CREATED)
def create_appointment(appointment: schemas.AppointmentCreate, db:Session = Depends(get_db), current_user=Depends(appointment_manager_required)):
    return crud.create_appointment(db=db, appointment=appointment)

@router.get("/", response_model=List[schemas.AppointmentResponse])
def get_appointments(skip:int =0, limit:int=100, db:Session=Depends(get_db), current_user=Depends(appointment_manager_required)):
    return crud.get_appointments(db=db, skip=skip, limit=limit)

@router.get("/my", response_model=List[schemas.AppointmentResponse])
def get_my_appointments(skip:int = 0, limit: int = 100, db: Session = Depends(get_db), current_user=Depends(doctor_required)):
    return crud.get_my_doctor_appointments(db=db, current_user=current_user, skip=skip, limit=limit)

@router.get("/{appointment_id}", response_model=schemas.AppointmentResponse)
def get_appointment(appointment_id: int, db: Session = Depends(get_db), current_user=Depends(appointment_manager_required)):
    return crud.get_appointment_by_id(db=db, appointment_id=appointment_id)

@router.put("/{appointment_id}", response_model=schemas.AppointmentResponse)
def update_appointment(appointment_id: int, appointment: schemas.AppointmentUpdate, db: Session=Depends(get_db), current_user=Depends(appointment_manager_required)):
    return crud.update_appointment(db=db, appointment_id = appointment_id, appointment_data = appointment)

@router.patch("/{appointment_id}/status", response_model=schemas.AppointmentResponse)
def update_appointment_status(appointment_id: int, status_data: schemas.AppointmentStatusUpdate, db: Session=Depends(get_db), current_user=Depends(appointment_manager_required)):
    return crud.update_appointment_status(db=db, appointment_id=appointment_id, status_data=status_data)

@router.delete("/{appointment_id}")
def delete_appointment(appointment_id: int, db:Session=Depends(get_db), current_user=Depends(appointment_manager_required)):
    return crud.delete_appointment(db=db, appointment_id=appointment_id)