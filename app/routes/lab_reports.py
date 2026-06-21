from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud, schemas

router = APIRouter(
  prefix="/lab-reports",
  tags=["Lab Reports"]
)

@router.post("/", response_model=schemas.LabReportResponse, status_code=status.HTTP_201_CREATED)
def create_lab_report(lab_report: schemas.LabReportCreate, db: Session = Depends(get_db)):
  return crud.create_lab_report(db=db, lab_report=lab_report)

@router.get("/", response_model=List[schemas.LabReportResponse])
def get_lab_reports(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
  return crud.get_lab_reports(db=db, skip=skip, limit=limit)

@router.get("/{lab_report_id}", response_model=schemas.LabReportResponse)
def get_lab_report(lab_report_id: int, db: Session = Depends(get_db)):
  return crud.get_lab_report_id(db=db, lab_report_id=lab_report_id)

@router.put("/{lab_report_id}", response_model=schemas.LabReportResponse)
def update_lab_report(lab_report_id: int, lab_report: schemas.LabReportUpdate, db: Session = Depends(get_db)):
  return crud.update_lab_report(db=db, lab_report_id = lab_report_id, lab_report=lab_report)

@router.delete("/{lab_report_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_lab_report(lab_report_id: int, db: Session = Depends(get_db)):
  return crud.delete_lab_report(db=db, lab_report_id=lab_report_id)
