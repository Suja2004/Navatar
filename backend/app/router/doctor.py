from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas.doctor import DoctorCreate, DoctorUpdate, DoctorOut
from typing import List
from ..crud import doctors as doctor_crud

router = APIRouter(prefix="/admin", tags=["Doctors"])


@router.post("/{hospital_id}/doctors", response_model=DoctorOut)
def create_doctor(hospital_id: int, doctor: DoctorCreate, db: Session = Depends(get_db)):
    return doctor_crud.create_doctor(db, hospital_id, doctor)

@router.get("/doctors/by-email/{email}", response_model=DoctorOut)
def get_doctor_by_email(email: str, db: Session = Depends(get_db)):
    return doctor_crud.get_doctor_by_email(db, email)


@router.get("/{hospital_id}/doctors", response_model=List[DoctorOut])
def list_doctors(hospital_id: int, db: Session = Depends(get_db)):
    return doctor_crud.list_doctors_by_hospital(db, hospital_id)


@router.get("/doctors/{doctor_id}", response_model=DoctorOut)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    return doctor_crud.get_doctor(db, doctor_id)


@router.put("/doctors/{doctor_id}", response_model=DoctorOut)
def update_doctor(doctor_id: int, updates: DoctorUpdate, db: Session = Depends(get_db)):
    return doctor_crud.update_doctor(db, doctor_id, updates)


@router.delete("/doctors/{doctor_id}")
def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    return doctor_crud.delete_doctor(db, doctor_id)
