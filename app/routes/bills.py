from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud, schemas

router = APIRouter(
    prefix="/bills",
    tags=["Bills"]
)


@router.post("/",response_model=schemas.BillResponse,status_code=status.HTTP_201_CREATED)
def create_bill(bill: schemas.BillCreate, db: Session = Depends(get_db)):
    return crud.create_bill(db=db, bill=bill)


@router.get("/", response_model=List[schemas.BillResponse])
def get_bills(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_bills(db=db, skip=skip, limit=limit)


@router.get("/{bill_id}", response_model=schemas.BillResponse)
def get_bill(bill_id: int, db: Session = Depends(get_db)):
    return crud.get_bill_by_id(db=db, bill_id=bill_id)


@router.put("/{bill_id}", response_model=schemas.BillResponse)
def update_bill(bill_id: int,bill: schemas.BillUpdate,db: Session = Depends(get_db)):
    return crud.update_bill(db=db, bill_id=bill_id, bill_data=bill)


@router.delete("/{bill_id}")
def delete_bill(bill_id: int, db: Session = Depends(get_db)):
    return crud.delete_bill(db=db, bill_id=bill_id)