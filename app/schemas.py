from datetime import date, datetime, time 
from typing import Optional
from pydantic import BaseModel, EmailStr
from app.models import Gender
from app.models import AppointmentStatus

# USER SCHEMAS
class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    role: str

class UserCreate(UserBase):
    password: str

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
    day_of_week = Optional[str] = None
    start_time =  Optional[time] = None
    end_time = Optional[time] = None
    max_patients: Optional[int] = None
    is_active: Optional[bool] = None

class DoctorAvailabilityResponse(DoctorAvailabilityBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        