from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud, schemas

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


@router.post(
    "/",
    response_model=schemas.PaymentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_payment(payment: schemas.PaymentCreate, db: Session = Depends(get_db)):
    return crud.create_payment(db=db, payment=payment)


@router.get("/", response_model=List[schemas.PaymentResponse])
def get_payments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_payments(db=db, skip=skip, limit=limit)


@router.get("/{payment_id}", response_model=schemas.PaymentResponse)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    return crud.get_payment_by_id(db=db, payment_id=payment_id)


@router.get("/bill/{bill_id}", response_model=List[schemas.PaymentResponse])
def get_payments_by_bill(bill_id: int, db: Session = Depends(get_db)):
    return crud.get_payments_by_bill_id(db=db, bill_id=bill_id)


@router.put("/{payment_id}", response_model=schemas.PaymentResponse)
def update_payment(
    payment_id: int,
    payment: schemas.PaymentUpdate,
    db: Session = Depends(get_db)
):
    return crud.update_payment(db=db, payment_id=payment_id, payment_data=payment)


@router.delete("/{payment_id}")
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    return crud.delete_payment(db=db, payment_id=payment_id)