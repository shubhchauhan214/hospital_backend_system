from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud, schemas

router = APIRouter(
  prefix="/lab_services",
  tags=["Lab Services"]
)

@router.post("/", response_model = schemas.LabServiceResponse, status_code = status.HTTP_201_CREATED)
def create_lab_service(lab_service:schemas.LabServiceCreate, db: Session = Depends(get_db)):
    return crud.create_lab_service(db=db, lab_service=lab_service)

@router.get("/", response_model=List[schemas.LabServiceResponse])
def get_lab_services(skip:int = 0, limit:int = 100, db: Session = Depends(get_db)):
    return crud.get_lab_services(db=db, skip=skip, limit=limit)

@router.get("/{lab_service_id}", response_model=schemas.LabServiceResponse)
def get_lab_service_by_id(lab_service_id: int, db: Session = Depends(get_db)):
    return crud.get_lab_service_by_id(db=db, lab_service_id=lab_service_id)

@router.put("/{lab_service_id}", response_model=schemas.LabServiceResponse)
def update_lab_service(lab_service_id:int, lab_service:schemas.LabServiceUpdate, db:Session=Depends(get_db)):
    return crud.update_lab_service(db=db, lab_service_id=lab_service_id, lab_service_data=lab_service)

@router.delete("/{lab_service_id}")
def delete_lab_service(lab_service_id: int, db: Session = Depends(get_db)):
    return crud.delete_lab_service(db=db, lab_service_id=lab_service_id)