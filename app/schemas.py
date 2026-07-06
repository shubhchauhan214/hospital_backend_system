from datetime import date, datetime, time 
from typing import Optional
from pydantic import BaseModel, EmailStr
from app.models import Gender
from app.models import AppointmentStatus, LabRequestStatus, BedStatus, AdmissionStatus, BillStatus, PaymentMode, PaymentStatus, UserRole, AppointmentStatus 

# USER SCHEMAS
class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    role: UserRole


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

#DEPARTMENT SCHEMAS

class DepartmentBase(BaseModel):
    name: str
    description: Optional[str] = None

class DepartmentCreate(DepartmentBase):
    pass 

class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class DepartmentResponse(DepartmentBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


#PATIENT SCHEMAS

class PatientBase(BaseModel):
    full_name: str
    phone: str
    email: Optional[EmailStr] = None
    gender: Optional[Gender] = None
    date_of_birth: Optional[date] = None
    blood_group: Optional[str] = None
    address: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None

class PatientCreate(PatientBase):
    pass 

class PatientUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    gender: Optional[Gender] = None
    date_of_birth: Optional[date] = None
    address: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None

class PatientResponse(PatientBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


#DOCTOR SCHEMAS
class DoctorBase(BaseModel):
    user_id: int
    department_id: int
    specialization: str
    qualification: Optional[str] = None
    experience_years: int = 0
    consultation_fee: float = 0
    is_available: bool = True

class DoctorCreate(DoctorBase):
    pass 

class DoctorUpdate(BaseModel):
    department_id: Optional[int] = None
    specialization: Optional[str] = None
    qualification: Optional[str] = None
    experience_years: Optional[int] = None
    consultation_fee: Optional[float] = None
    is_available: Optional[bool] = None

class DoctorResponse(DoctorBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


#APPOINTMENT SCHEMA

class AppointmentBase(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_date: date
    appointment_time: time
    reason: Optional[str] = None
    consultation_fee: float = 0
    notes: Optional[str] = None

class AppointmentCreate(AppointmentBase):
    pass 

class AppointmentUpdate(BaseModel):
    appointment_date: Optional[date] = None
    appointment_time: Optional[time] = None
    reason: Optional[str] = None
    status: Optional[AppointmentStatus] = None
    consultation_fee: Optional[float] = None
    notes: Optional[str] = None

class AppointmentResponse(AppointmentBase):
    id: int
    status: AppointmentStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# APPOINTMENT STATUS SCHEMA (We have added it later)

class AppointmentStatusUpdate(BaseModel):
    status: AppointmentStatus

# APPOINTMENT CONSULTATION UPDATE (We have added it later)

class AppointmentConsultationUpdate(BaseModel):
    notes: str
    status: AppointmentStatus = AppointmentStatus.COMPLETED


# DOCTOR AVAILABILITY SCHEMA

class DoctorAvailabilityBase(BaseModel):
    doctor_id: int
    day_of_week: str
    start_time: time
    end_time: time
    max_patients: Optional[int] = None
    is_active: bool = True

class DoctorAvailabilityCreate(DoctorAvailabilityBase):
    pass 

class DoctorAvailabilityUpdate(BaseModel):
    day_of_week: Optional[str] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    max_patients: Optional[int] = None
    is_active: Optional[bool] = None

class DoctorAvailabilityResponse(DoctorAvailabilityBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# LAB SERVICE SCHEMAS

class LabServiceBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

class LabServiceCreate(LabServiceBase):
    pass

class LabServiceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class LabServiceResponse(LabServiceBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        

# LAB REQUEST SCHEMAS

class LabRequestBase(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_id: Optional[int] = None
    lab_service_id: int
    remarks: Optional[str] = None

class LabRequestCreate(LabRequestBase):
    pass

class LabRequestUpdate(BaseModel):
    status: Optional[LabRequestStatus] = None
    remarks: Optional[str] = None

class LabRequestResponse(LabRequestBase):
    id: int
    request_date: datetime
    status: LabRequestStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# LAB REPORT SCHEMAS

class LabReportBase(BaseModel):
    lab_request_id: int
    report_title: str
    report_summary: Optional[str] = None
    report_file_url: Optional[str] = None

class LabReportCreate(LabReportBase):
    pass

class LabReportUpdate(BaseModel):
    report_title: Optional[str] = None
    report_summary: Optional[str] = None
    report_file_url: Optional[str] = None

class LabReportResponse(LabReportBase):
    id: int
    result_date: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# WARD SCHEMAS

class WardBase(BaseModel):
    name: str
    ward_type: Optional[str] = None
    floor_number: Optional[int] = None

class WardCreate(WardBase):
    pass

class WardUpdate(BaseModel):
    name: Optional[str] = None
    ward_type: Optional[str] = None
    floor_number: Optional[int] = None

class WardResponse(WardBase):
    id: int
    is_active: bool
    create_at: datetime
    update_at: datetime

    class Config:
        from_attributes = True

# BED SCHEMAS

class BedBase(BaseModel):
    ward_id: int
    bed_number: str
    status: BedStatus = BedStatus.AVAILABLE
    price_per_day: float = 0

class BedCreate(BedBase):
    pass 

class BedUpdate(BedBase):
    ward_id: Optional[int] = None
    bed_number: Optional[str] = None
    status: Optional[BedStatus] = None
    price_per_day: Optional[float] = None

class BedResponse(BedBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# ADMISSION SCHEMAS

class AdmissionBase(BaseModel):
    patient_id: int
    doctor_id: int
    bed_id: int
    reason: Optional[str] = None
    status: AdmissionStatus = AdmissionStatus.ADMITTED

class AdmissionCreate(AdmissionBase):
    pass 

class AdmissionUpdate(AdmissionBase):
    doctor_id: Optional[int] = None
    bed_id: Optional[int] = None
    discharge_date: Optional[datetime] = None
    reason: Optional[str] = None
    status: Optional[AdmissionStatus]=None

class AdmissionResponse(AdmissionBase):
    id: int
    admission_date: datetime
    discharge_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# BILL SCHEMAS 

class BillBase(BaseModel):
    patient_id: int
    admission_id: Optional[int] = None

    bill_number: str

    consultation_charges: float = 0
    lab_charges: float = 0
    bed_charges: float = 0
    medicine_charges: float = 0
    other_charges: float = 0

    discount: float = 0
    total_amount: float
    paid_amount: float = 0

    status: BillStatus = BillStatus.PENDING

class BillCreate(BillBase):
    pass


class BillUpdate(BaseModel):
    consultation_charges: Optional[float] = None
    lab_charges: Optional[float] = None
    bed_charges: Optional[float] = None
    medicine_charges: Optional[float] = None
    other_charges: Optional[float] = None
    discount: Optional[float] = None
    total_amount: Optional[float] = None
    paid_amount: Optional[float] = None
    status: Optional[BillStatus] = None


class BillResponse(BillBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


#PAYMENT SCHEMAS
class PaymentBase(BaseModel):
    bill_id: int
    amount: float
    payment_mode: PaymentMode
    payment_status: PaymentStatus = PaymentStatus.SUCCESS
    transaction_id: Optional[str] = None


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    amount: Optional[float] = None
    payment_mode: Optional[PaymentMode] = None
    payment_status: Optional[PaymentStatus] = None
    transaction_id: Optional[str] = None


class PaymentResponse(PaymentBase):
    id: int
    payment_date: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# DOCUMENT SCHEMAS

class DocumentBase(BaseModel):
    patient_id: int
    appointment_id: Optional[int] = None
    document_type: str
    file_name: str
    file_url: str
    description: Optional[str] = None
    uploaded_by: Optional[int] = None


class DocumentCreate(DocumentBase):
    pass


class DocumentUpdate(BaseModel):
    document_type: Optional[str] = None
    file_name: Optional[str] = None
    file_url: Optional[str] = None
    description: Optional[str] = None


class DocumentResponse(DocumentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# AUTH SCHEMAS

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class CurrentUserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    phone: str
    role: str
    is_active: bool

    class Config:
        from_attributes = True


# DASHBOARD SCHEMAS

class AdminDashboardResponse(BaseModel):
    total_users: int
    total_departments: int
    total_doctors: int
    total_patients: int
    today_appointments: int
    total_admissions: int
    available_beds: int
    occupied_beds: int
    pending_bills: int
    paid_bills: int
    total_revenue: float


class DoctorDashboardResponse(BaseModel):
    today_appointments: int
    total_appointments: int
    pending_appointments: int
    completed_appointments: int
    availability_count: int
    lab_requests: int
