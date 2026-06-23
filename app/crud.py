from datetime import datetime

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


# APPOINTMENT CRUD
# CREATE APPOINTMENT
def create_appointment(db: Session, appointment: schemas.AppointmentCreate):
    # Check patient exists
    patient = (db.query(models.Patient).filter(models.Patient.id == appointment.patient_id, models.Patient.is_active == True).first())

    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")


    # Check doctor exists
    doctor = (db.query(models.Doctor).filter(models.Doctor.id == appointment.doctor_id, models.Doctor.is_active == True).first())

    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found.")
    
    db_appointment = models.Appointment(**appointment.model_dump())

    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)

    return db_appointment

# GET ALL APPOINTMENTS
def get_appointments(db: Session, skip:int = 0, limit:int = 100):
    return (db.query(models.Appointment).offset(skip).limit(limit).all())

# GET APPOINTMENT
def get_appointment_by_id(db: Session, appointment_id: int):
    appointment = (db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first())

    if not appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found.")
    
    return appointment

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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
    
    db_availability = models.DoctorAvailability(**availability.model_dump())

    db.add(db_availability)
    db.commit()
    db.refresh(db_availability)

    return db_availability

# GET DOCTOR AVAILABILITIES
def get_doctor_availibilities(db: Session, skip:int=0, limit:int=100):
    return(db.query(models.DoctorAvailability).filter(models.DoctorAvailability.is_active == True).offset(skip).limit(limit).all())

# GET DOCTOR AVAILABILITY
def get_doctor_availability_by_id(db:Session, availability_id: int):
    availability = (db.query(models.DoctorAvailability).filter(models.DoctorAvailability.id == availability_id, models.DoctorAvailability.is_active == True).first())

    if not availability:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor availability not found")
    
    return availability

# GET AVAILABILITY BY DOCTOR
def get_availability_by_doctor_id(db:Session, doctor_id: int):
    return (db.query(models.DoctorAvailability).filter(models.DoctorAvailability.doctor_id == doctor_id, models.DoctorAvailability.is_active == True).all())


# UPDATE DOCTOR AVAILABILITY
def update_doctor_availability(db: Session, availability_id: int, availability_data: schemas.DoctorAvailabilityUpdate):
    availability = get_doctor_availability_by_id(db, availability_id)

    update_data = availability_data.model_dump(exclude_unset=True)

    for key, value in update_data.itmes():
        setattr(availability, key, value)

    db.commit()
    db.refresh(availability)

    return availability

# DELETE DOCTOR AVAILABILITY
def delete_doctor_availability(db: Session, availability_id: int):
    availability = get_doctor_availability_by_id(db, availability_id)

    availability.is_active == False

    db.commit()

    return{"message": "Doctor availability deleted successfully"}


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

def create_lab_request(db: Session, lab_request: schemas.LabRequestCreate):
    patient = db.query(models.Patient).filter(models.Patient.id == lab_request.patient_id, models.Patient.is_active == True).first()

    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
    
    doctor = db.query(models.Doctor).filter(models.Doctor.id == lab_request.doctor_id, models.Doctor.is_active == True).first()

    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
    
    lab_service = db.query(models.LabService).filter(models.LabService.id == lab_request.lab_service_id, models.LabService.is_active == True).first()

    if not lab_service:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lab service not found")
    
    db_lab_request = models.LabRequest(**lab_request.model_dump())

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