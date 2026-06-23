from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud, schemas

router = APIRouter(
  prefix="/admissions",
  tags=["Admissions"]
)

@router.post("/", response_model=schemas.AdmissionResponse)
def create_admission(admission:schemas.AdmissionCreate, db: Session=Depends(get_db)):
  return crud.create_admission(db=db, admission=admission)

@router.get("/", response_model=List[schemas.AdmissionResponse])
def get_admissions(skip:int = 0, limit: int = 100, db: Session = Depends(get_db)):
  return crud.get_admissions(db=db, skip=skip, limit=limit)

@router.get("/{admission_id}", response_model=schemas.AdmissionResponse)
def get_admission_by_id(admission_id: int, db: Session =Depends(get_db)):
  return crud.get_admission_by_id(db=db, admission_id=admission_id)

@router.put("/{admission_id}", response_model=schemas.AdmissionResponse)
def update_admission(admission_id: int, admission: schemas.AdmissionUpdate, db: Session=Depends(get_db)):
  return crud.update_admission(db=db, admission_id=admission_id, admission_data=admission)

@router.patch("/{admissoin_id}/discharge", response_model=schemas.AdmissionResponse)
def discharge_patient(admission_id: int, db:Session = Depends(get_db)):
  return crud.discharge_patient(db=db, admission_id=admission_id)

@router.delete("/{admission_id}")
def delete_admission(admission_id: int, db: Session=Depends(get_db)):
  return crud.delete_admission(db=db, admission_id=admission_id)