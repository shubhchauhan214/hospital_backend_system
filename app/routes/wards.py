from  typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud, schemas

router = APIRouter(
  prefix="/wards",
  tags=["Wards"]
)

@router.post("/", response_model=schemas.WardResponse, status_code=status.HTTP_201_CREATED)
def create_ward(ward: schemas.WardCreate, db: Session = Depends(get_db)):
  return crud.create_ward(db=db, ward=ward)

@router.get("/", response_model=List[schemas.WardResponse])
def get_wards(skip:int = 0, limit: int = 100, db: Session = Depends(get_db)):
  return crud.get_wards(db=db, skip=skip, limit=limit)

@router.get("/{ward_id}", response_model=schemas.WardResponse)
def get_ward(ward_id: int, db: Session = Depends(get_db)):
  return crud.get_ward_by_id(db=db, ward_id=ward_id)

@router.put("/{ward_id}", response_model=schemas.WardResponse)
def update_ward(ward_id: int, ward: schemas.WardUpdate, db: Session = Depends(get_db)):
  return crud.update_ward(db=db, ward_id=ward_id, ward=ward)

@router.delete("/{ward_id}")
def delete_ward(ward_id: int, db: Session = Depends(get_db)):
  return crud.delete_ward(db=db, ward_id=ward_id)