from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas

router = APIRouter(prefix="/departments", tags=["Departments"])

@router.post("/", response_model=schemas.DepartmentResponse, status_code=status.HTTP_201_CREATED)
def create_department(department: schemas.DepartmentCreate, db: Session = Depends(get_db)):
    return crud.create_department(db=db, department=department)

@router.get("/", response_model=schemas.DepartmentResponse)
def get_departments(skip:int=0, limit:int = 100, db: Session = Depends(get_db)):
    return crud.get_departments(db=db, skip=skip, limit=limit)


@router.get("/{department_id}", response_model=schemas.DepartmentResponse)
def get_department(department_id: int, db: Session=Depends(get_db)):
    return crud.get_department_by_id(db=db, department_id=department_id)

@router.put("/{departent_id}", response_model=schemas.DepartmentResponse)
def update_department(department_id: int, department: schemas.DepartmentUpdate, db: Session = Depends(get_db)):
    return crud.update_department(db=db, department_id = department_id, department_data =department)


@router.delete("/{department_id}")
def delete_department(department_id: int, db: Session=Depends(get_db)):
    return crud.delete_department(db=db, department_id=department_id)