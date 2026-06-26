from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies.roles import admin_required

from app.database import get_db
from app import crud, schemas
from app.dependencies.auth import get_current_active_user

router = APIRouter(prefix="/users", tags=["Users"])

# ADMIN APIS

@router.post("/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db), current_user=Depends(admin_required)):
    return crud.create_user(db=db, user=user)

@router.get("/", response_model=List[schemas.UserResponse])
def get_users(db:Session = Depends(get_db)):
    return crud.get_users(db=db)

@router.get("/{user}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db), current_user=Depends(admin_required)):
    return crud.get_user_by_id(db=db, user_id=user_id)

@router.put("/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: int, user_data: schemas.UserUpdate, db: Session = Depends(get_db), current_user=Depends(admin_required)):
    return crud.update_user(db=db, user_id=user_id, user_data=user_data)

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session= Depends(get_db), current_user=Depends(admin_required)):
    return crud.delete_user(db=db, user_id=user_id)

# LOGGED-IN USER APIS

@router.get("/profile", response_model=schemas.CurrentUserResponse)
def get_profile(current_user = Depends(get_current_active_user)):
    return current_user

@router.put("/profile", response_model=schemas.CurrentUserResponse)
def update_profile(user_data: schemas.UserUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    return crud.update_user(db=db, user_id=current_user.id, user_data=user_data)

@router.put("/change-password")
def change_password(password_data: schemas.ChangePasswordRequest, db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    return crud.change_password(db=db, current_user=current_user, password_data=password_data)