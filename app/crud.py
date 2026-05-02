from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app import models, schemas

#USERS
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(full_name = user.full_name, email=user.email, phone=user.phone, role=user.role, password_hash=user.password)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def get_users(db: Session):
    return db.query(models.User).filter(models.User.is_active == True).all()

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


# DOCTOR CRUD

# CREATE DOCTOR
def create_doctor(db: Session, doctor:schemas.DoctorCreate):
    db_doctor = models.Doctor(**doctor.model_dump())

    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)

    return db_doctor

# GET ALL DOCTORS
def get_doctors(db: Session, skip: int = 0, limit: int = 100):
    db_doctor = db.query(models.Doctor).filter(models.Doctor.is_active == True).offset(skip).limit(limit).all()

# GET DOCTOR BY ID
def get_doctor_by_id(db: Session, doctor_id: int):
    doctor = (db.query(models.Doctor).filter(models.Doctor.id == doctor_id, models.Doctor.is_active == True).first())

    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
    
    return doctor

# UPDATE DOCTOR
def update_doctor(db:Session, doctor_id: int, doctor_data: schemas.DoctorUpdate):
    doctor = get_doctor_by_id(db,doctor_id)

    update_data = doctor_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(doctor, key, value)

    db.commit()
    db.refresh(doctor)

    return doctor

# DELETE DOCTOR
def delete_doctor(db:Session, doctor_id: int):
    doctor = get_doctor_by_id(db, doctor_id)
    doctor.is_active == False
    
    db.commit()

    return {"message": "Doctor deleted successfully"}