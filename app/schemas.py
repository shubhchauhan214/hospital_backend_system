from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from app.models import Gender

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