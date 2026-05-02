from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app import models, schemas

# PATIENTS

# CREATE PATIENT

def create_patient(db: Session, patient: schemas.PatientCreate):
    db_patient = models.Patient(**patient.model_dump())

    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)

    return db_patient

# GET ALL PATIENTS

def get_patients(db:Session, skip: int = 0, limit: int =100):
    patients = (
        db.query(models.Patient)
        .filter(models.Patient.is_active == True)
        .offset(skip)
        .limit(limit)
        .all()
    )

    return patients

# GET SINGLE PATIENT
def get_patient_by_id(db: Session, patient_id: int):
    patient = (
        db.query(models.Patient)
        .filter(
            models.Patient.id == patient_id,
            models.Patient.is_active == True
        )
        .first()
    )

    if not patient:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Patient not found")
    
    return patient

# UPDATE PATIENT
def update_patient(db: Session, patient_id: int, patient_data: schemas.PatientUpdate):
    patient = get_patient_by_id(db, patient_id)

    update_data = patient_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(patient, key, value)

    db.commit()
    db.refresh(patient)

    return patient

# DELETE (SOFT DELETE)
def delete_patient(db: Session, patient_id: int):
    patient = get_patient_by_id(db, patient_id)

    patient.is_active = False
    db.commit()

    return{
        "message": "Patient deleted successfully"
    }
