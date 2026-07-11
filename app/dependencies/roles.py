from fastapi import Depends, HTTPException, status

from app.models import UserRole
from app.dependencies.auth import get_current_active_user

def role_required(allowed_roles: list[UserRole]):
  def checker(current_user=Depends(get_current_active_user)):
    if current_user.role not in allowed_roles:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to perform this actiion")
    
    return current_user
  
  return checker

admin_required=role_required([
  UserRole.ADMIN,
  UserRole.SUPER_ADMIN
])

doctor_required=role_required([
  UserRole.DOCTOR
])

receptionist_required = role_required([
  UserRole.RECEPTIONIST
])

lab_staff_required=role_required([
  UserRole.LAB_STAFF
])

patient_required = role_required([
  UserRole.PATIENT
])

# FEATURE BASED ROLE GROUPS

user_manager_required = role_required([
  UserRole.ADMIN,
  UserRole.SUPER_ADMIN
])

department_manager_required = role_required([
  UserRole.ADMIN,
  UserRole.SUPER_ADMIN
])

doctor_manager_required = role_required([
  UserRole.ADMIN,
  UserRole.SUPER_ADMIN
])

appointment_manager_required = role_required([
  UserRole.ADMIN,
  UserRole.SUPER_ADMIN,
  UserRole.RECEPTIONIST
])

billing_manager_required = role_required([
  UserRole.ADMIN,
  UserRole.SUPER_ADMIN,
  UserRole.RECEPTIONIST
])

lab_manager_required = role_required([
  UserRole.ADMIN,
  UserRole.SUPER_ADMIN,
  UserRole.LAB_STAFF
])

admission_manager_required = role_required([
  UserRole.ADMIN,
  UserRole.SUPER_ADMIN,
  UserRole.RECEPTIONIST
])

lab_request_creator_required = role_required([
  UserRole.ADMIN,
  UserRole.SUPER_ADMIN,
  UserRole.DOCTOR
])

