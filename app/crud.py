from datetime import datetime, date

from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status

from app import models, schemas
from app.auth import hash_password, verify_password

#USERS
def create_user(db: Session, user: schemas.UserCreate):
    print("PASSWORD:", user.password)
    print("PASSWORD LENGTH:", len(user.password))
    db_user = models.User(full_name = user.full_name, email=user.email, phone=user.phone, role=user.role, password_hash=hash_password(user.password))

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def get_users(db: Session):
    return db.query(models.User).filter(models.User.is_active == True).all()

def get_user_by_id(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id, models.User.is_active == True).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

def update_user(db: Session, user_id: int, user_data: schemas.UserUpdate):
    user = get_user_by_id(db, user_id)

    update_data = user_data.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return user

def delete_user(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)

    user.is_active = False

    db.commit()

    return {"message": "User deactivated successfully"}

def change_password(db: Session, current_user: models.User, password_data: schemas.ChangePasswordRequest):
    if not verify_password(password_data.old_password, current_user.password_hash):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Old password is incorrect")
    
    current_user.password_hash = hash_password(password_data.new_password)

    db.commit()

    return {"message": "Password changed successfully"}

# DEPARTMENTS
# DEPARTMENT CREATE
def create_department(db: Session , department:schemas.DepartmentCreate):
    db_department = models.Department(**department.model_dump())

    db.add(db_department)
    db.commit()
    db.refresh(db_department)

    return db_department

# GET DEPARTMENTS
def get_departments(db:Session, skip:int = 0, limit:int = 100):
    return(db.query(models.Department).filter(models.Department.is_active == True).offset(skip).limit(limit).all())


# GET DEPARTMENT
def get_department_by_id(db: Session, department_id: int):
    department =(db.query(models.Department).filter(models.Department.id == department.id, models.Department.is_active ==True).first())

    if not department:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Department Not Found")
    
    return department

#UPDATE DEPARTMENT
def update_department(db: Session, department_id: int, department_data: schemas. DepartmentUpdate):
    department = get_department_by_id(db, department)

    update_data = department_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(department, key, value)

    db.commit()
    db.refresh(department)

    return department

#DELETE DEPARTMENT
def delete_department(db: Session, department_id: int):
    department = get_department_by_id(db, department_id)

    department.is_active = False
    db.commit()

    return{"message": "Department deleted successfully"}


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
    db_doctors = db.query(models.Doctor).filter(models.Doctor.is_active == True).offset(skip).limit(limit).all()

    return db_doctors

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
    doctor.is_active = False
    
    db.commit()

    return {"message": "Doctor deleted successfully"}


# APPOINTMENT CRUD
# CREATE APPOINTMENT
def create_appointment(db: Session, appointment: schemas.AppointmentCreate):
    # Check patient exists
    patient = (db.query(models.Patient).filter(models.Patient.id == appointment.patient_id, models.Patient.is_active == True).first())

    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Active Patient not found")


    # Check doctor exists
    doctor = (db.query(models.Doctor).filter(models.Doctor.id == appointment.doctor_id, models.Doctor.is_active == True).first())

    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Active Doctor not found.")
    
    # Check doctor is generally accepting appointments
    if not doctor.is_available:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Doctor is currently not accepting appointments.")
    
    # Check Appointment date is not in the past
    if appointment.appointment_date < date.today():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Appointment date cannot be in the past.")
    
    # Convert appointment date into weekday
    appointment_day = (appointment.appointment_date.strftime("%A").upper())

    # Check doctor has availability on requested day
    day_availability = (
        db.query(models.DoctorAvailability)
        .filter(
            models.DoctorAvailability.doctor_id == appointment.doctor_id,

            models.DoctorAvailability.day_of_week == appointment_day,

            models.DoctorAvailability.is_active == True
            )
            .first()
    )

    if not day_availability:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=(f"Doctor not available on {appointment_day}."))
    
    # Check Appointment time lies inside any active working slot
    matching_availability = (
        db.query(models.DoctorAvailability)
        .filter(
            models.DoctorAvailability.doctor_id == appointment.doctor_id,

            models.DoctorAvailability.day_of_week == appointment_day,

            models.DoctorAvailability.is_active == True,

            models.DoctorAvailability.start_time <= appointment.appointment_time,

            models.DoctorAvailability.end_time > appointment.appointment_time
        )
        .first()
    )

    if not matching_availability:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Doctor is not available at the selected time.")
    
    # Duplicate appointment check
    existing_appointment = (
        db.query(models.Appointment)
        .filter(
            models.Appointment.doctor_id == appointment.doctor_id,
            models.Appointment.appointment_date == appointment.appointment_date,
            models.Appointment.appointment_time == appointment.appointment_time,
            models.Appointment.status != models.AppointmentStatus.CANCELLED
        )
        .first()
    )

    if existing_appointment:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Doctor already has an appointment at this date and time.")
    
    # Create Appointment
    appointment_data = appointment.model_dump()

    appointment_data["consultation_fee"] = doctor.consultation_fee
    appointment_data["status"] = models.AppointmentStatus.PENDING

    db_appointment = models.Appointment(**appointment_data)

    db.add(db_appointment)

    try:
        db.commit()
        db.refresh(db_appointment)

    except Exception:
        db.rollback()
        raise

    return db_appointment

def update_appointment_status(db: Session, appointment_id: int, status_data: schemas.AppointmentStatusUpdate):
    appointment = get_appointment_by_id(db, appointment_id)

    appointment.status = status_data.status
    
    db.commit()
    db.refresh(appointment)

    return appointment

# GET ALL APPOINTMENTS
def get_appointments(db: Session, skip:int = 0, limit:int = 100):
    return (db.query(models.Appointment).offset(skip).limit(limit).all())

# GET APPOINTMENT
def get_appointment_by_id(db: Session, appointment_id: int):
    appointment = (db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first())

    if not appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found.")
    
    return appointment

# GET DOCTORS' APPOINTMENTS

def get_my_doctor_appointments(db: Session, current_user: models.User, skip:int = 0, limit: int = 100):
    doctor = db.query(models.Doctor).filter(models.Doctor.user_id == current_user.id, models.Doctor.is_active == True).first()

    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor Profile not found")
    
    return(db.query(models.Appointment).filter(models.Appointment.doctor_id == doctor.id).offset(skip).limit(limit).all())

# UPDATE APPOINTMENT
def update_appointment(db: Session, appointment_id: int, appointment_data: schemas.AppointmentUpdate):
    appointment = get_appointment_by_id(db, appointment_id)

    update_data = appointment_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(appointment, key, value)

    db.commit()
    db.refresh(appointment)

    return appointment

# DELETE APPOINTMENT
def delete_appointment(db: Session, appointment_id: int):
    appointment = get_appointment_by_id(db, appointment_id)

    appointment.status = models.AppointmentStatus.CANCELLED

    db.commit()
    db.refresh(appointment)

    return{"message": "Appointment cancelled sucessfully"}


#DOCTOR AVAILIBILITY CRUD
def create_doctor_availability(db: Session, availability: schemas.DoctorAvailabilityCreate):
    doctor = (db.query(models.Doctor).filter(models.Doctor.id == availability.doctor_id, models.Doctor.is_active == True).first())

    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Active Doctor not found")
    
    if availability.start_time >= availability.end_time:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Start time must be earlier than end time.")
    
    overlapping_slot = (db.query(models.DoctorAvailability).filter(
        models.DoctorAvailability.doctor_id == availability.doctor_id,

        models.DoctorAvailability.day_of_week == availability.day_of_week.value,

        models.DoctorAvailability.is_active == True,

        models.DoctorAvailability.start_time < availability.end_time,

        models.DoctorAvailability.end_time > availability.start_time
    ).first())

    if overlapping_slot:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Doctor already has an overlapping" "availability slot.")
    
    availability_data = availability.model_dump()

    if hasattr(availability_data["day_of_week"], "value"):
        availability_data["day_of_week"] = (availability_data["day_of_week"].value)

    availability_data["is_active"] = True

    
    db_availability = models.DoctorAvailability(**availability_data)

    db.add(db_availability)

    try:
        db.commit()
        db.refresh(db_availability)
    except Exception:
        db.rollback()
        raise

    return db_availability



# GET DOCTOR AVAILABILITIES
def get_doctor_availabilities(db: Session, skip:int=0, limit:int=100):
    return(db.query(models.DoctorAvailability).filter(models.DoctorAvailability.is_active == True)
           .order_by(
               models.DoctorAvailability.doctor_id,
               models.DoctorAvailability.day_of_week,
               models.DoctorAvailability.start_time
           )
           .offset(skip).limit(limit).all())

# GET DOCTOR AVAILABILITY
def get_doctor_availability_by_id(db:Session, availability_id: int):
    availability = (db.query(models.DoctorAvailability).filter(models.DoctorAvailability.id == availability_id, models.DoctorAvailability.is_active == True).first())

    if not availability:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor availability not found")
    
    return availability

# GET AVAILABILITY BY DOCTOR ID
def get_availability_by_doctor_id(
    db: Session,
    doctor_id: int
):
    doctor = (
        db.query(models.Doctor)
        .filter(
            models.Doctor.id == doctor_id,
            models.Doctor.is_active.is_(True)
        )
        .first()
    )

    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Active doctor not found."
        )

    return (
        db.query(models.DoctorAvailability)
        .filter(
            models.DoctorAvailability.doctor_id == doctor_id,
            models.DoctorAvailability.is_active.is_(True)
        )
        .order_by(
            models.DoctorAvailability.day_of_week,
            models.DoctorAvailability.start_time
        )
        .all()
    )

# UPDATE DOCTOR AVAILABILITY
def update_doctor_availability(db: Session, availability_id: int, availability_data: schemas.DoctorAvailabilityUpdate):
    availability = get_doctor_availability_by_id(db=db, availability_id=availability_id)

    update_data = availability_data.model_dump(exclude_unset=True)

    new_day = update_data.get("day_of_week", availability.day_of_week)

    if hasattr(new_day, "value"):
        new_day = new_day.value

    new_start_time = update_data.get("start_time", availability.start_time)

    new_end_time = update_data.get("end_time", availability.end_time)

    if new_start_time >= new_end_time:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Start time must be earlier than end time.")
    
    # Check overlap with another availability
    overlapping_slot = (db.query(models.DoctorAvailability)
                        .filter(
                            models.DoctorAvailability.doctor_id == availability.doctor_id,

                            models.DoctorAvailability.day_of_week == new_day,

                            models.DoctorAvailability.id != availability.id,

                            models.DoctorAvailability.is_active == True,

                            models.DoctorAvailability.end_time > new_start_time,

                            models.DoctorAvailability.end_time > new_start_time
                        ).first()
    )

    if overlapping_slot:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=("Updated slot overlaps with another" "doctor availability slot."))

    for key, value in update_data.items():
        if key == "day_of_week" and hasattr(value, "value"):
            value = value.value

        setattr(availability, key, value)

    try:
        db.commit()
        db.refresh(availability)
    
    except Exception:
        db.rollback()
        raise

    return availability

# DELETE DOCTOR AVAILABILITY
def delete_doctor_availability(db: Session, availability_id: int):
    availability = get_doctor_availability_by_id(db=db, availability_id = availability_id)

    availability.is_active = False

    try:
        db.commit()
        db.refresh(availability)
    except Exception:
        db.rollback()
        raise

    return{"message": "Doctor availability deleted successfully."}

# AVAILABILITY CRUD

def update_appointment_status(db: Session, appointment_id: int, status_data: schemas.AppointmentStatusUpdate):
    appointment = get_appointment_by_id(db=db, appointment_id=appointment_id)

    appointment.status = status_data.status

    try:
        db.commit()
        db.refresh(appointment)
    
    except Exception:
        db.rollback()
        raise

    return appointment


# LAB SERVICE CRUD

def create_lab_service(db: Session, lab_service: schemas.LabServiceCreate):
    db_lab_service = models.LabService(**lab_service.model_dump())

    db.add(db_lab_service)
    db.commit()
    db.refresh(db_lab_service)

    return db_lab_service

def get_lab_services(db: Session, skip:int = 0, limit:int = 100):
    return(db.query(models.LabService).filter(models.LabService.is_active == True).offset(skip).limit(limit).all())

def get_lab_service_by_id(db: Session, lab_service_id: int):
    lab_service = (db.query(models.LabService).filter(models.LabService.id == lab_service_id, models.LabService.is_active == True).first())

    if not lab_service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lab service not found")
    
    return lab_service

def update_lab_service(db: Session, lab_service_id: int, lab_service_data: schemas.LabServiceUpdate):
    lab_service = get_lab_service_by_id(db, lab_service_id)

    update_data = lab_service_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(lab_service, key, value)

    db.commit()
    db.refresh(lab_service)

def delete_lab_service(db: Session, lab_service_id: int):
    lab_service = get_lab_service_by_id(db, lab_service_id)

    lab_service.is_active = False

    db.commit()

    return{"message": "Lab service deleted successfully"}


# LAB REQUEST CRUD

def create_lab_request(db: Session, lab_request: schemas.LabRequestCreate, current_user: models.User):
    patient = db.query(models.Patient).filter(models.Patient.id == lab_request.patient_id, models.Patient.is_active == True).first()

    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    
    doctor = db.query(models.Doctor).filter(models.Doctor.user_id == current_user.id, models.Doctor.is_active == True).first()

    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor Profile not found")
    
    lab_service = db.query(models.LabService).filter(models.LabService.id == lab_request.lab_service_id, models.LabService.is_active == True).first()

    if not lab_service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lab service not found")
    
    if lab_request.appointment_id is None:
        appointment = db.query(models.Appointment).filter(models.Appointment.id == lab_request.appointment_id, models.Apppointment.doctor_id == doctor.id, models.Appointment.patient_id == lab_request.patient_id).first()

        if not appointment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found for this patient and doctor")
    
    db_lab_request = models.LabRequest(patient_id=lab_request.patient_id, doctor_id=doctor.id, appointment_id=lab_request.appointment_id, lab_service_id=lab_request.lab_service_id, remarks=lab_request.remarks)
    

    db.add(db_lab_request)
    db.commit()
    db.refresh(db_lab_request)

    return db_lab_request

def get_lab_requests(db: Session, skip:int=0, limit:int=100):
    return(db.query(models.LabRequest).offset(skip).limit(limit).all())

def get_lab_request_by_id(db: Session, lab_request_id: int):
    lab_request = (db.query(models.LabRequest).filter(models.LabRequest.id == lab_request_id).first())

    if not lab_request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lab request not found")
    
    return lab_request

def update_lab_request(db:Session, lab_request_id: int, lab_request_data: schemas.LabRequestUpdate):
    lab_request = get_lab_request_by_id(db, lab_request_id)

    update_data = lab_request_data.model_dum(exclude_unset=True)

    for key, value in update_data.items():
        setattr(lab_request, key, value)

    db.commit()
    db.refresh(lab_request)

    return lab_request

def delete_lab_request(db: Session, lab_request_id: int):
    lab_request = get_lab_request_by_id(db, lab_request_id)

    lab_request.status = models.LabRequestStatus.CANCELLED

    db.commit()
    db.refresh(lab_request)

    return {"message": "Lab request cancelled successfully"}


# LAB REPORT CRUD

def create_lab_report(db: Session, lab_report: schemas.LabReportCreate):
    lab_request = db.query(models.LabRequest).filter(models.LabRequest.id == lab_report.lab_request_id).first()

    if not lab_request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lab request not found")
    
    existing_report = db.query(models.LabReport).filter(models.LabReport.lab_request_id == lab_report.lab_request_id).first()

    if existing_report:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Lab report already exists for this lab request")
    
    db_lab_report = models.LabReport(**lab_report.model_dump())

    lab_request.status = models.LabRequestStatus.COMPLETED

    db.add(db_lab_report)
    db.commit()
    db.refresh(db_lab_report)

    return db_lab_report

# DOCTOR CAN  GET HIS/HER OWN LAB REPORTS
def get_my_doctor_lab_reports(db: Session, current_user: models.User, skip: int=0, limit:int=100):
    doctor = db.query(models.Doctor).filter(models.Doctor.user_id == current_user.id, models.Doctor.is_active == True).first()

    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor profile not found")
    
    return (db.query(models.LabReport).join(models.LabRequest, models.LabReport.lab_request_id == models.LabRequest.id).filter(models.LabRequest.doctor_id == doctor.id).offset(skip).limit(limit).all())


def get_lab_reports(db: Session, skip:int=0, limit:int=100):
    return db.query(models.LabReport).offset(skip).limit(limit).all()

def get_lab_report_by_id(db: Session, lab_report_id: int):
    lab_report = db.query(models.LabReport).filter(models.LabReport.id == lab_report_id).first()

    if not lab_report:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lab report not found")
    
    return lab_report

def update_lab_report(db: Session, lab_report_id: int, lab_report_data: schemas.LabReportUpdate):
    lab_report = get_lab_report_by_id(db, lab_report_id)

    update_data = lab_report_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(lab_report, key, value)

    db.commit()
    db.refresh(lab_report)

    return lab_report

def delete_lab_report(db: Session, lab_report_id: int):
    lab_report = get_lab_report_by_id(db, lab_report_id)

    db.delete(lab_report)
    db.commit()

    return {"message": "Lab report deleted successfully"}


# ward CRUD

def create_ward(db: Session, ward: schemas.WardCreate):
    db_ward = models.Ward(**ward.model_dump())

    db.add(db_ward)
    db.commit()
    db.refresh(db_ward)

    return db_ward

def get_wards(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Ward).filter(models.Ward.is_active == True).offset(skip).limit(limit).all()


def get_ward_by_id(db: Session, ward_id: int):
    ward = db.query(models.Ward).filter(models.Ward.id == ward_id, models.Ward.is_active == True).first()

    if not ward:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ward not found")
    
def update_ward(db: Session, ward_id: int, ward_data: schemas.WardUpdate):
    ward = get_ward_by_id(db, ward_id)

    update_data = ward_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(ward, key, value)

    db.commit()
    db.refresh(ward)

    return ward


def delete_ward(db: Session, ward_id: int):
    ward = get_ward_by_id(db, ward_id)

    ward.is_active = False
    db.commit()

    return {"message": "Ward deleted successfully"}


# BED CRUD

def create_bed(db: Session, bed: Session.BedCreate):
    ward = db.query(models.Ward).filter(models.Ward.id == bed.ward_id, models.Ward.is_active == True).first()

    if not ward:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ward not found")
    
    db_bed = models.Bed(**bed.model_dump())

    db.add(db_bed)
    db.commit()
    db.refresh(db_bed)

    return db_bed

def get_beds(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Bed).offset(skip).limit(limit).all()

def get_bed_by_id(db: Session, bed_id: int):
    bed = db.query(models.Bed).filter(models.Bed.id == bed_id).first()

    if not bed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bed not found")
    
    return bed

def get_available_beds(db: Session):
    return db.query(models.Bed).filter(models.Bed.status == models.BedStatus.AVAILABLE).all()

def update_bed(db: Session, bed_id: int, bed_data: schemas.BedUpdate):
    bed = get_bed_by_id(db, bed_id)

    update_data = bed_data.model_dump(exclude_unset= True)

    for key,value in update_data.items():
        setattr(bed, key, value)

    db.commit()
    db.refresh(bed)

    return bed

def delete_bed(db: Session, bed_id: int):
    bed = get_bed_by_id(db, bed_id)

    bed.status = models.BedStatus.MAINTENANCE

    db.commit()
    db.refresh(bed)

    return {"message": "Bed moved to maintenance successfully"}


# ADMISSION CRUD

def create_admission(db: Session, admission: schemas.AdmissionCreate):
    patient = db.query(models.Patient).filter(models.Patient.id == admission.patient_id, models.Patient.is_active == True).first()

    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    
    doctor = db.query(models.Doctor).filter(models.Doctor.id == admission.doctor_id, models.Doctor.is_active == True).first()

    if not doctor:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Doctor not found")
    
    bed = db.query(models.Bed).filter(models.Bed.id == admission.bed_id).first()

    if not bed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bed not found")
    
    if bed.status != models.BedStatus.AVAILABLE:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bed is not available")
    
    db_admission = models.Admission(**admission.model_dump())

    bed.status = models.BedStatus.OCCUPIED

    db.add(db_admission)
    db.commit()
    db.refresh(db_admission)

    return db_admission

def get_admissions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Admission).offset(skip).limit(limit).all()

def get_admission_by_id(db: Session, admission_id: int):
    admission = db.query(models.Admission).filter(models.Admission.id == admission_id).first()

    if not admission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admission not found")
    
    return admission

def update_admission(db: Session, admission_id: int, admission_data: schemas.AdmissionUpdate):
    admission = get_admission_by_id(db, admission_id)

    update_data = admission_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(admission, key, value)

    if admission.status == models.AdmissionStatus.DISCHARGED:
        admission.bed.status = models.BedStatus.AVAILABLE

    db.commit()
    db.refresh(admission)

    return admission

def discharge_patient(db: Session, admission_id: int):
    admission = get_admission_by_id(db, admission_id)

    admission.status = models.AdmissionStatus.DISCHARGED
    admission.discharge_date = datetime.utcnow()

    admission.bed.status = models.BedStatus.AVAILABLE

    db.commit()
    db.refresh(admission)

    return admission

def delete_admission(db: Session, admission_id: int):
    admission = get_admission_by_id(db, admission_id)

    admission.status = models.AdmissionStatus.DISCHARGED
    admission.discharge_date = datetime.utcnow()

    admission.bed.status = models.BedStatus.AVAILABLE

    db.commit()

    return {"message": "Admission closed successfully."}

# BILL CRUD

def create_bill(db: Session, bill: schemas.BillCreate):
    patient = db.query(models.Patient).filter(models.Patient.id == bill.patient_id, models.Patient.is_active == True).first()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    if bill.admission_id:
        admission = db.query(models.Admission).filter(models.Admission.id == bill.admission_id).first()

        if not admission:
            raise HTTPException(status_code=404, detail="Admission not found")

    existing_bill = db.query(models.Bill).filter(models.Bill.bill_number == bill.bill_number).first()

    if existing_bill:
        raise HTTPException(status_code=400,detail="Bill number already exists")

    db_bill = models.Bill(**bill.model_dump())

    db.add(db_bill)
    db.commit()
    db.refresh(db_bill)

    return db_bill


def get_bills(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Bill).offset(skip).limit(limit).all()


def get_bill_by_id(db: Session, bill_id: int):
    bill = db.query(models.Bill).filter(models.Bill.id == bill_id).first()

    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")

    return bill


def update_bill(db: Session, bill_id: int, bill_data: schemas.BillUpdate):
    bill = get_bill_by_id(db, bill_id)

    update_data = bill_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(bill, key, value)

    db.commit()
    db.refresh(bill)

    return bill


def delete_bill(db: Session, bill_id: int):
    bill = get_bill_by_id(db, bill_id)

    bill.status = models.BillStatus.CANCELLED

    db.commit()
    db.refresh(bill)

    return {"message": "Bill cancelled successfully"}

# PAYMENT CRUD

def create_payment(db: Session, payment: schemas.PaymentCreate):
    bill = db.query(models.Bill).filter(models.Bill.id == payment.bill_id).first()

    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")

    db_payment = models.Payment(**payment.model_dump())

    if payment.payment_status == models.PaymentStatus.SUCCESS:
        bill.paid_amount = bill.paid_amount + payment.amount

        if bill.paid_amount >= bill.total_amount:
            bill.status = models.BillStatus.PAID
        elif bill.paid_amount > 0:
            bill.status = models.BillStatus.PARTIALLY_PAID

    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)

    return db_payment


def get_payments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Payment).offset(skip).limit(limit).all()


def get_payment_by_id(db: Session, payment_id: int):
    payment = db.query(models.Payment).filter(models.Payment.id == payment_id).first()

    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    return payment


def get_payments_by_bill_id(db: Session, bill_id: int):
    return db.query(models.Payment).filter(models.Payment.bill_id == bill_id).all()


def update_payment(db: Session, payment_id: int, payment_data: schemas.PaymentUpdate):
    payment = get_payment_by_id(db, payment_id)

    update_data = payment_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(payment, key, value)

    db.commit()
    db.refresh(payment)

    return payment


def delete_payment(db: Session, payment_id: int):
    payment = get_payment_by_id(db, payment_id)

    payment.payment_status = models.PaymentStatus.REFUNDED

    db.commit()
    db.refresh(payment)

    return {"message": "Payment marked as refunded successfully"}

# DOCUMENTS CRUD

def create_document(db: Session, document: schemas.DocumentCreate):
    patient = db.query(models.Patient).filter(models.Patient.id == document.patient_id,models.Patient.is_active == True).first()

    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    if document.appointment_id:
        appointment = db.query(models.Appointment).filter(models.Appointment.id == document.appointment_id).first()

        if not appointment:
            raise HTTPException(status_code=404, detail="Appointment not found")

    if document.uploaded_by:
        user = db.query(models.User).filter(models.User.id == document.uploaded_by,models.User.is_active == True).first()

        if not user:
            raise HTTPException(status_code=404, detail="Uploaded user not found")

    db_document = models.Document(**document.model_dump())

    db.add(db_document)
    db.commit()
    db.refresh(db_document)

    return db_document


def get_documents(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Document).offset(skip).limit(limit).all()


def get_document_by_id(db: Session, document_id: int):
    document = db.query(models.Document).filter(models.Document.id == document_id).first()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    return document


def get_documents_by_patient_id(db: Session, patient_id: int):
    return db.query(models.Document).filter(models.Document.patient_id == patient_id).all()


def update_document(
    db: Session,
    document_id: int,
    document_data: schemas.DocumentUpdate
):
    document = get_document_by_id(db, document_id)

    update_data = document_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(document, key, value)

    db.commit()
    db.refresh(document)

    return document


def delete_document(db: Session, document_id: int):
    document = get_document_by_id(db, document_id)

    db.delete(document)
    db.commit()

    return {"message": "Document deleted successfully"}


# AUTH CRUD

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(models.User).filter(models.User.email == email, models.User.is_active == True).first()

    if not user:
        return None
    
    if not verify_password(password, user.password_hash):
        return None
    
    return user


# ADMIN DASHBOARD

def get_admin_dashboard(db: Session):
    today = date.today()

    total_users = db.query(models.User).filter(models.User.is_active == True).count()

    total_departments = db.query(models.Department).filter(models.Department.is_active == True).count()

    total_doctors = db.query(models.Doctor).filter(models.Doctor.is_active ==True).count()

    total_patients = db.query(models.Patient).filter(models.Patient.is_active== True).count()

    today_appointments = db.query(models.Appointment).filter(models.Appointment.appointment_date == today).count()

    total_admissions = db.query(models.Admission).count()

    available_beds = db.query(models.Bed).filter(models.Bed.status == models.BedStatus.AVAILABLE).count()

    occupied_beds = db.query(models.Bed).filter(models.Bed.status == models.BedStatus.OCCUPIED).count()

    pending_bills = db.query(models.Bill).filter(models.Bill.status == models.BillStatus.PAID).count()

    paid_bills = db.query(models.Bill).filter(models.Bill.status == models.BillStatus.PAID).count()

    total_revenue = db.query(func.coalesce(func.sum(models.Payment.amount), 0).filter(models.Payment.payment_status == models.PaymentStatus.SUCCESS).scalar())

    return{
        "total_users": total_users,
        "total_departments": total_departments,
        "total_doctors": total_doctors,
        "total_patients": total_patients,
        "today_appointments": today_appointments,
        "total_admissions": total_admissions,
        "available_beds": available_beds,
        "occupied_beds": occupied_beds,
        "pending_bills": pending_bills,
        "paid_bills": paid_bills,
        "total_revenue":total_revenue or 0
    }

# DOCTOR DASHBOARD

def get_doctor_dashboard(db: Session, current_user: models.User):
    today = date.today()

    doctor = db.query(models.Doctor).filter(models.Doctor.user_id == current_user.id, models.Doctor.is_active == True).first()

    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor Profile not found")
    
    today_appointments = db.query(models.Appointment).filter(models.Appointment.doctor_id == doctor.id, models.Appointment.appointment_date == today).count()

    total_appointments = db.query(models.Appointment).filter(models.Appointment.doctor_id == doctor.id).count()

    pending_appointments = db.query(models.Appointment).filter(models.Appointment.doctor_id == doctor.id, models.Appointment.status == models.AppointmentStatus.PENDING).count()

    completed_appointments = db.query(models.Appointment).filter(models.Appointment.doctor_id == doctor.id, models.Appointment.status == models.AppointmentStatus.COMPLETED).count()

    availability_count = db.query(models.DoctorAvailability).filter(models.DoctorAvailability.doctor_id == doctor.id, models.DoctorAvailability.is_active == True).count()

    lab_requests = db.query(models.LabRequest).filter(models.LabRequest.doctor_id == doctor.id).count()

    return{
        "today_appointments": today_appointments,
        "total_appointments": total_appointments,
        "pending_appointments": pending_appointments,
        "completed_appointments": completed_appointments,
        "availability_count": availability_count,
        "lab_requests": lab_requests
    }

# DOCTOR CONSULTATION WORKFLOW

def complete_doctor_consultation(db: Session, appointment_id: int, consultation_data: schemas.AppointmentConsultationUpdate, current_user: models.User):
    doctor = db.query(models.Doctor).filter(models.Doctor.user_id == current_user.id, models.Doctor.is_active == True).first()

    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor Profile not found")
    
    appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id, models.Appointment.doctor_id == doctor.id).first()

    if not appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found for this doctor")
    
    if appointment.status == models.AppointmentStatus.CANCELLED:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cancelled appointment cannot be completed")
    
    appointment.notes = consultation_data.notes
    appointment.status = models.Appointment_data.status 

    db.commit()
    db.refresh(appointment)

    return appointment
    

# DOCTOR OWN LAB REQUESTS

def get_my_doctor_lab_requests(db: Session, current_user: models.User, skip: int = 0, limit: int = 100):
    doctor = db.query(models.Doctor).filter(models.Doctor.user_id == current_user.id, models.Doctor.is_active == True).first()

    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor Profile not found")
    
    return db.query(models.LabRequest).filter(models.LabRequest.doctor_id == doctor.id).offset(skip).limit(limit).all()




