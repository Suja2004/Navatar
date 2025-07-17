from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models import Doctor, Hospital
from ..schemas.doctor import DoctorCreate, DoctorUpdate


def create_doctor(db: Session, hospital_id: int, doctor: DoctorCreate):
    if not doctor.name or not doctor.email:
        raise HTTPException(
            status_code=400, detail="Name and Email are required.")

    if db.query(Doctor).filter(Doctor.email == doctor.email).first():
        raise HTTPException(
            status_code=409, detail="Doctor with this email already exists.")

    if not db.query(Hospital).filter(Hospital.hospital_id == hospital_id).first():
        raise HTTPException(status_code=404, detail="Hospital not found.")

    if doctor.phone and len(doctor.phone) < 10:
        raise HTTPException(
            status_code=422, detail="Phone number must be at least 10 digits.")

    db_doctor = Doctor(**doctor.dict(), hospital_id=hospital_id)
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor


def update_doctor(db: Session, doctor_id: int, updates: DoctorUpdate):
    doctor = db.query(Doctor).get(doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    if updates.email and updates.email != doctor.email:
        if db.query(Doctor).filter(Doctor.email == updates.email).first():
            raise HTTPException(
                status_code=409, detail="Another doctor already uses this email.")

    if updates.phone and len(updates.phone) < 10:
        raise HTTPException(
            status_code=422, detail="Phone number must be at least 10 digits.")

    for field, value in updates.dict(exclude_unset=True).items():
        setattr(doctor, field, value)

    db.commit()
    db.refresh(doctor)
    return doctor


def list_doctors_by_hospital(db: Session, hospital_id: int):
    return db.query(Doctor).filter(Doctor.hospital_id == hospital_id).all()


def get_doctor(db: Session, doctor_id: int):
    doctor = db.query(Doctor).get(doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor


def delete_doctor(db: Session, doctor_id: int):
    doctor = db.query(Doctor).get(doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    db.delete(doctor)
    db.commit()
    return {"message": f"Doctor '{doctor.name}' deleted successfully"}
