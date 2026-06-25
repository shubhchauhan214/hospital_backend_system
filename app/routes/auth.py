from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import crud, schemas
from app.auth import create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=schemas.Token)
def login(login_data: schemas.LoginRequest, db: Session = Depends(get_db)):
  user = crud.authenticate_user(db=db, email=login_data.email, password=login_data.password)

  if not user:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
  
  access_token = create_access_token(data={"sub": str(user.id), "email": user.email, "role": user.role.value})

  return {
    "access_token": access_token,
    "token_type": "bearer"
  }

@router.get("/me", response_model=schemas.CurrentUserResponse)
def get_me(current_user=Depends(get_current_user)):
  return current_user