from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud, schemas
from app.dependencies.roles import (doctor_required, lab_manager_required, lab_request_creator_required)

router = APIRouter(
  prefix="/lab-requests",
  tags=["Lab Requests"]
)

# DOCTOR, ADMIN AND SUPER ADMIN CAN CREATE LAB REQUESTS
@router.post("/", response_model=schemas.LabRequestResponse, status_code=status.HTTP_201_CREATED)
def create_lab_request(lab_request: schemas.LabRequestCreate, db: Session=Depends(get_db), current_user=Depends(lab_request_creator_required)):
    return crud.create_lab_request(db=db, lab_request=lab_request)

# LAB STAFF AND ADMIN CAN GET ALL LAB REQUESTS
@router.get("/", response_model=List[schemas.LabRequestResponse])
def get_lab_requests(skip:int = 0, limit:int = 100, db: Session=Depends(get_db), current_user=Depends(lab_manager_required)):
    return crud.get_lab_requests(db=db, skip=skip, limit=limit)

# DOCTOR CAN GET HIS/HER OWN LAB REQUESTS
@router.get("/my", response_model=List[schemas.LabRequestResponse])
def get_my_lab_requests(skip: int = 0, limit: int = 100, db: Session=Depends(get_db), current_user=Depends(doctor_required)):
    return crud.get_my_doctor_lab_requests(db=db, current_user=current_user, skip=skip, limit=limit)

#LAB STAFF AND ADMIN CAN GET LAB REQUEST BY ID
@router.get("/{lab_request_id}", response_model=schemas.LabRequestResponse)
def get_lab_request_by_id(lab_request_id: int, db: Session=Depends(get_db), current_user=Depends(lab_manager_required)):
    return crud.get_lab_request_by_id(db=db, lab_request_id=lab_request_id)

#LAB STAFF AND ADMIN CAN UPDATE LAB REQUEST BY ID
@router.put("/{lab_request_id}", response_model=schemas.LabRequestResponse)
def update_lab_request(lab_request_id:int, lab_request:schemas.LabRequestUpdate, db:Session=Depends(get_db), current_user=Depends(lab_manager_required)):
    return crud.update_lab_request(db=db, lab_request_id=lab_request_id, lab_request_data=lab_request)

#LAB STAFF AND ADMIN CAN DELETE LAB REQUEST BY ID
@router.delete("/{lab_request_id}")
def delete_lab_request(lab_request_id: int, db: Session=Depends(get_db), current_user=Depends(lab_manager_required)):
    return crud.delete_lab_request(db=db, lab_request_id=lab_request_id)