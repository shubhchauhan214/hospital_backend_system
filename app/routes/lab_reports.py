from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud, schemas
from app.dependencies.roles import (admin_required, doctor_required, lab_manager_required)

router = APIRouter(
  prefix="/lab-reports",
  tags=["Lab Reports"]
)

# LAB STAFF AND ADMIN CAN CREATE LAB REPORTS
@router.post("/", response_model=schemas.LabReportResponse, status_code=status.HTTP_201_CREATED)
def create_lab_report(lab_report: schemas.LabReportCreate, db: Session = Depends(get_db), current_user=Depends(lab_manager_required)):
  return crud.create_lab_report(db=db, lab_report=lab_report)

# LAB STAFF AND ADMIN CAN GET ALL LAB REPORTS
@router.get("/", response_model=List[schemas.LabReportResponse])
def get_lab_reports(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user=Depends(lab_manager_required)):
  return crud.get_lab_reports(db=db, skip=skip, limit=limit)

# DOCTOR CAN GET HIS/HER OWN LAB REPORTS
@router.get("/my", response_model= List[schemas.LabReportResponse])
def get_my_lab_reports(skip: int= 0, limit: int = 100, db: Session = Depends(get_db), current_user=Depends(doctor_required)):
  return crud.get_my_doctor_lab_reports(db=db, current_user=current_user, skip=skip, limit=limit)

# LAB STAFF AND ADMIN CAN GET LAB REPORT BY ID
@router.get("/{lab_report_id}", response_model=schemas.LabReportResponse)
def get_lab_report(lab_report_id: int, db: Session = Depends(get_db), current_user=Depends(lab_manager_required)):
  return crud.get_lab_report_id(db=db, lab_report_id=lab_report_id)

# LAB STAFF AND ADMIN CAN UPDATE LAB REPORT BY ID
@router.put("/{lab_report_id}", response_model=schemas.LabReportResponse)
def update_lab_report(lab_report_id: int, lab_report: schemas.LabReportUpdate, db: Session = Depends(get_db), current_user=Depends(lab_manager_required)):
  return crud.update_lab_report(db=db, lab_report_id = lab_report_id, lab_report_data=lab_report)

# LAB STAFF AND ADMIN CAN DELETE LAB REPORT BY ID
@router.delete("/{lab_report_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_lab_report(lab_report_id: int, db: Session = Depends(get_db), current_user=Depends(lab_manager_required)):
  return crud.delete_lab_report(db=db, lab_report_id=lab_report_id)
