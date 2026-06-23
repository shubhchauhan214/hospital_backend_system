from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud, schemas

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


@router.post(
    "/",
    response_model=schemas.DocumentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_document(
    document: schemas.DocumentCreate,
    db: Session = Depends(get_db)
):
    return crud.create_document(db=db, document=document)


@router.get("/", response_model=List[schemas.DocumentResponse])
def get_documents(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return crud.get_documents(db=db, skip=skip, limit=limit)


@router.get("/patient/{patient_id}", response_model=List[schemas.DocumentResponse])
def get_documents_by_patient(
    patient_id: int,
    db: Session = Depends(get_db)
):
    return crud.get_documents_by_patient_id(db=db, patient_id=patient_id)


@router.get("/{document_id}", response_model=schemas.DocumentResponse)
def get_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    return crud.get_document_by_id(db=db, document_id=document_id)


@router.put("/{document_id}", response_model=schemas.DocumentResponse)
def update_document(
    document_id: int,
    document: schemas.DocumentUpdate,
    db: Session = Depends(get_db)
):
    return crud.update_document(
        db=db,
        document_id=document_id,
        document_data=document
    )


@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    db: Session = Depends(get_db)
):
    return crud.delete_document(db=db, document_id=document_id)