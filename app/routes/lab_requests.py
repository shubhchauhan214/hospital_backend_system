from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud, schemas

router = APIRouter(
  prefix="/lab-requests",
  tags=["Lab Requests"]
)

@router.post("/", response_model=schemas.LabRequestResponse, status_code=status.HTTP_201_CREATED)
def create_lab_request(lab_request: schemas.LabRequestCreate, db: Session=Depends(get_db)):
    return crud.create_lab_request(db=db, lab_request=lab_request)

@router.get("/", response_model=List[schemas.LabRequestResponse])
def get_lab_requests(skip:int = 0, limit:int = 100, db: Session=Depends(get_db)):
    return crud.get_lab_requests(db=db, skip=skip, limit=limit)

@router.get("/{lab_request_id}", response_model=schemas.LabRequestResponse)
def get_lab_request_by_id(lab_request_id: int, db: Session=Depends(get_db)):
    return crud.get_lab_request_by_id(db=db, lab_request_id=lab_request_id)

@router.put("/{lab_request_id}", response_model=schemas.LabRequestResponse)
def update_lab_request(lab_request_id:int, lab_request:schemas.LabRequestUpdate, db:Session=Depends(get_db)):
    return crud.update_lab_request(db=db, lab_request_id=lab_request_id, lab_request_data=lab_request)

@router.delete("/{lab_request_id}")
def delete_lab_request(lab_request_id: int, db: Session=Depends(get_db)):
    return crud.delete_lab_request(db=db, lab_request_id=lab_request_id)