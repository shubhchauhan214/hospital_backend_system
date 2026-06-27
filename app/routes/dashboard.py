from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud, schemas
from app.dependencies.roles import admin_required, doctor_required

router =APIRouter(
  prefix="/dashboard",
  tags=["Dashboard"]
)

@router.get("/admin", response_model=schemas.AdminDashboardResponse)
def admin_dashboard(db: Session = Depends(get_db), current_user=Depends(admin_required)):
  return crud.get_admin_dashboard(db=db)

@router.get("/doctor", response_model=schemas.DoctorDashboardResponse)
def doctor_dashboard(db: Session = Depends(get_db), current_user=Depends(doctor_required)):
  return crud.get_doctor_dashboard(db=db, current_user=current_user)