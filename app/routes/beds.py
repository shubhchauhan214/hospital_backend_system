from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud, schemas

router = APIRouter(
  prefix="/beds",
  tags = ["Beds"]
)


@router.post("/", response_model=schemas.BedResposne, status_code=status.HTTP_201_CREATED)
def create_bed(bed: schemas.BedCreate, db: Session = Depends(get_db)):
  return crud.create_bed(db=db, bed=bed)


@router.get("/", response_model=List[schemas.BedResponse])
def get_beds(skip: int = 0, limit: int= 100, db: Session = Depends(get_db)):
  return crud.get_beds(db=db, skip=skip, limit=limit)

@router.get("/available", response_model=List[schemas.BedResponse])
def get_available_beds(db: Session= Depends(get_db))
  return crud.get_available_beds(db=db)

@router.get("/{bed_id}", response_model = schemas.BedResponse)
def get_bed(bed_id: int, db: Session = Depends(get_db)):
  return crud.get_bed_by_id(db=db, bed_id = bed_id)

@router.put("/{bed_id}", response_model=schemas.BedResponse)
def update_bed(bed_id: int, bed: schemas.BedUpdate, db: Session= Depends(get_db)):
  return crud.update_bed(db=db, bed_id=bed_id, bed_data=bed)

@router.delete("/{bed_id}")
def delete_bed(bed_id: int, db: Session = Depends(get_db)):
  return crud.delete_bed(db=db, bed_id=bed_id)