from sqlalchemy import Column, Integer, String, Text, Boolean, Date, Time, DateTime, ForeignKey, Numeric, Enum as SqlEnum
from datetime import datetime, date, time
from enum import Enum
from sqlalchemy.orm import relationship
from app.database import Base

#ENUMS
class UserRole(str, Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    ADMIN = "ADMIN"
    DOCTOR = "DOCTOR"
    RECEPTIONIST ="RECEPTIONIST"
    LAB_STAFF = "LAB_STAFF"
    PATIENT = "PATIENT"

class Gender(str, Enum):
    MALE ="MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"

class AppointmentStatus(str, Enum):
    PENDING = "PENDING"
    CONFIRMED  = "CONFIRMED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class LabRequestStatus(str, Enum):
    REQUESTED = "REQUESTED"
    SAMPLE_COLLECTED = "SAMPLE_COLLECTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class BedStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    OCCUPIED = "OCCUPIED"
    MAINTENANCE = "MAINTENANCE"

class AdmissionStatus(str, Enum):
    ADMITTED = "ADMITTED"
    DISCHARGED = "DISCHARGED"

class BillStatus(str, Enum):
    PENDING = "PENDING"
    PARTIALLY_PAID = "PARTIALLY_PAID"
    PAID = "PAID"
    CANCELLED = "CANCELLED"

class PaymentMode(str, Enum):
    CASH = "CASH"
    UPI = "UPI"
    CARD = "CARD"
    NET_BANKING = "NET_BANKING"
    INSURANCE = "INSURANCE"

class PaymentStatus(str, Enum):
    SUCCESS ="SUCCESS"
    FAILED = "FAILED"
    REFUNDED ="REFUNDED"


class TimestampMixin:
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


#USERS
class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    phone = Column(String(20), index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)

    role = Column(SqlEnum(UserRole), nullable=False)
    is_active = Column(Boolean, default=True)

    doctor_profile = relationship("Doctor", back_populates="user", uselist=False)
    patient_profile = relationship("Patient", back_populates="user", uselist=False)


#DEPARTMENTS
class Department(Base, TimestampMixin):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True)

    doctors = relationship("Doctor", back_populates="department")


#DOCTORS
class Doctor(Base, TimestampMixin):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    department_id  = Column(Integer, ForeignKey("departments.id"), nullable=False)

    specialization = Column(String(150), nullable=False)
    qualification = Column(String(150), nullable=False)
    experience_years = Column(Integer, default=0)
    consultation_fee = Column(Numeric(10,2), default=0)

    is_available = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)

    user = relationship("User", back_populates="doctor_profile")
    department = relationship("Department", back_populates="doctors")

    availabilities = relationship("DoctorAvailability", back_populates="doctor")
    appointments = relationship("Appointment", back_populates="doctor")
    admissions = relationship("Admission", back_populates="doctor")
    lab_requests = relationship("LabRequest", back_populates="doctor")


#PATIENTS
class Patient(Base, TimestampMixin):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=True)

    full_name = Column(String(150), nullable=False)
    phone = Column(String(20), index=True, nullable=False)
    email = Column(String(150), nullable=True)

    gender = Column(SqlEnum(Gender), nullable=True)
    date_of_birth = Column(Date, nullable=True)
    blood_group = Column(String(10), nullable=True)

    address = Column(Text, nullable=True)
    emergency_contact_name = Column(String(150), nullable=True)
    emergency_contact_phone = Column(String(20), nullable=True)

    is_active = Column(Boolean, default=True)

    user = relationship("User", back_populates="patient_profile")

    appointments = relationship("Appointment", back_populates="patient")
    lab_requests = relationship("LabRequest", back_populates="patient")
    admission = relationship("Admission", back_populates="patient")
    bills = relationship("Bill", back_populates="patient")
    documents = relationship("Document", back_populates="patient")

#DOCTOR AVAILABILITY
class DoctorAvailability(Base, TimestampMixin):
    __tablename__ = "doctor_availability"

    id = Column(Integer, primary_key=True, index=True)

    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)

    day_of_week = Column(String(20), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    max_patients = Column(Integer,  nullable=True)
    is_active = Column(Boolean, default=True)

    doctor = relationship("Doctor", back_populates="availabilities")


#APPOINTMENTS
class Appointment(Base, TimestampMixin):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)

    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)

    appointment_date = Column(Date, nullable=False, index=True)
    appointment_time = Column(Time, nullable=False)

    reason = Column(Text, nullable=True)
    status = Column(SqlEnum(AppointmentStatus), default=AppointmentStatus.PENDING)

    consulation_fee = Column(Numeric(10,2), default=0)
    notes = Column(Text, nullable=True)

    patient = relationship("Patient", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")

    lab_requests = relationship("LabRequest", back_populates="appointment")
    documents = relationship("Document", back_populates="appointment")


#LAB SERVICES
class LabService(Base, TimestampMixin):
    __tablename__ = "lab_services"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(150), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Numeric(10,2), nullable=False)

    is_active = Column(Boolean, default=True)

    lab_requests = relationship("LabRequest", back_populates="lab_services")


#LAB REQUESTS
class LabRequest(Base, TimestampMixin):
    __tablename__ = "lab_requests"

    id = Column(Integer, primary_key=True, unique=True)

    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    appointment_id = Column(Integer, ForeignKey("appointments.id"), nullable=True)
    lab_service_id = Column(Integer, ForeignKey("lab_services.id"), nullable=False)

    request_date = Column(DateTime, default=datetime.utcnow)
    status = Column(SqlEnum(LabRequestStatus), default=LabRequestStatus.REQUESTED)

    remarks = Column(Text, nullable=True)

    patient = relationship("Patient", back_populates="lab_requests")
    doctor = relationship("Doctor", back_populates="lab_requests")
    appointment = relationship("Appointment", back_populates="lab_requests")
    lab_service = relationship("LabService", back_populates="lab_requests")

    lab_report = relationship("LabReport", back_populates="lab_request", uselist=False)


#LAB REPORTS
class LabReport(Base, TimestampMixin):
    __tablename__ = "lab_reports"

    id = Column(Integer, primary_key=True, index=True)

    lab_request_id = Column(Integer, ForeignKey("lab_requests.id"), unique=True, nullable=False)

    report_title = Column(String(150), nullable=False)
    report_summary = Column(Text, nullable=True)
    report_file_url = Column(String(500), nullable=True)

    result_date = Column(DateTime, default=datetime.utcnow)

    lab_request = relationship("LabRequest", back_populates="lab_report")


#WARD
class Ward(Base, TimestampMixin):
    __tablename__ = "wards"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), unique=True, nullable=False)
    ward_type = Column(String(100), nullable=False)
    floor_number = Column(String(50), nullable=True)

    is_active = Column(Boolean, default=True)

    beds =relationship("Bed", back_populates="ward")

#BEDS
class Bed(Base, TimestampMixin):
    __tablename__ = "beds"

    id = Column(Integer, primary_key=True, index=True)

    ward_id = Column(Integer, ForeignKey("wards.id"), nullable=False)

    bed_number = Column(String(50), nullable=False)
    status = Column(SqlEnum(BedStatus), default=BedStatus.AVAILABLE)

    price_per_day = Column(Numeric(10,2), default=0)

    ward = relationship("Ward", back_populates="beds")
    admissions =relationship("Admission", back_populates="beds")

#ADMISSIONS
class Admission(Base, TimestampMixin):
    __tablename__ = "admissions"

    id = Column(Integer, primary_key=True, index=True)

    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    bed_id = Column(Integer, ForeignKey("beds.id"), nullable=False)

    admission_date = Column(DateTime, default=datetime.utcnow)
    discharge_date = Column(DateTime, default=datetime.utcnow)

    reason = Column(Text, nullable=True)
    status = Column(SqlEnum(AdmissionStatus), default=AdmissionStatus.ADMITTED)

    patient = relationship("Patient", back_populates="admisisons")
    doctor = relationship("Doctor", back_populates="admissions")
    bed = relationship("Bed", back_populates="admissions")

    bills = relationship("Bill", back_populates="admissions")

#BILLS
class Bill(Base, TimestampMixin):
    __tablename__ = "bills"

    id = Column(Integer, primary_key=True, index=True)

    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    admission_id = Column(Integer, ForeignKey("admissions.id"), nullable=False)

    bill_number = Column(String(100), unique=True, nullable=False)

    consultation_charges = Column(Numeric(10,2), default=0)
    lab_charges = Column(Numeric(10,2), default=0)
    bed_charges = Column(Numeric(10,2), default=0)
    medicine_charges = Column(Numeric(10,2), default=0)
    other_charges = Column(Numeric(10,2), default=0)

    discount = Column(Numeric(10,2), default=0)
    total_amount = Column(Numeric(10,2), nullable=False)
    paid_amount = Column(Numeric(10,2), default=0)

    status = Column(SqlEnum(BillStatus), default=BillStatus.PENDING)

    patient = relationship("Patient", back_populates="bills")
    admission = relationship("Admission", back_populates="bills")
    payments = relationship("Payment", back_populates="bills")


#PAYMENTS
class Payment(Base, TimestampMixin):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)

    bill_id = Column(Integer, ForeignKey("bills.id"), nullable=False)

    amount = Column(Numeric(10,2), nullable=False)
    payment_mode = Column(SqlEnum(PaymentMode), nullable=False)
    payment_status = Column(SqlEnum(PaymentStatus), default=PaymentStatus.SUCCESS)

    transaction_id = Column(String(150), nullable=True)
    payment_date = Column(DateTime, default=datetime.utcnow)

    bill = relationship("Bill", back_populates="payments")

#DOCUMENTS
class Document(Base, TimestampMixin):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    appointment_id = Column(Integer, ForeignKey("appointments.id"), nullable=False)

    document_type = Column(String(100), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_url = Column(String(500), nullable=False)

    description = Column(Text, nullable=True)
    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    patient = relationship("Patient", back_populates="documents")
    appointment = relationship("Appointment", back_populates="documents")



    


