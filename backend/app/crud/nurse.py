from sqlalchemy.orm import Session
from ..models import Nurse, Doctor
from ..schemas.nurse import NurseCreate, NurseUpdate
from fastapi import HTTPException


from sqlalchemy.exc import IntegrityError


def create_nurse(db: Session, doctor_id: int, nurse: NurseCreate):
    if not db.query(Doctor).get(doctor_id):
        raise HTTPException(status_code=404, detail="Doctor not found")

    existing_nurse = db.query(Nurse).filter(Nurse.email == nurse.email).first()
    if existing_nurse:
        raise HTTPException(
            status_code=400, detail="Nurse with this email already exists")

    data = nurse.dict()
    data["assigned_doctor_id"] = doctor_id

    db_nurse = Nurse(**data)
    db.add(db_nurse)
    db.commit()
    db.refresh(db_nurse)
    return db_nurse


def get_nurse(db: Session, nurse_id: int):
    nurse = db.query(Nurse).get(nurse_id)
    if not nurse:
        raise HTTPException(status_code=404, detail="Nurse not found")
    return nurse


def list_nurses_for_doctor(db: Session, doctor_id: int):
    return db.query(Nurse).filter(Nurse.assigned_doctor_id == doctor_id).all()


def update_nurse(db: Session, nurse_id: int, updates: NurseUpdate):
    nurse = db.query(Nurse).get(nurse_id)
    if not nurse:
        raise HTTPException(status_code=404, detail="Nurse not found")

    if updates.email:
        existing_nurse = db.query(Nurse).filter(
            Nurse.email == updates.email, Nurse.id != nurse_id).first()
        if existing_nurse:
            raise HTTPException(
                status_code=400, detail="Email already in use by another nurse")

    for field, value in updates.dict(exclude_unset=True).items():
        setattr(nurse, field, value)

    db.commit()
    db.refresh(nurse)
    return nurse


def delete_nurse(db: Session, nurse_id: int):
    nurse = db.query(Nurse).get(nurse_id)
    if not nurse:
        raise HTTPException(status_code=404, detail="Nurse not found")
    db.delete(nurse)
    db.commit()
    return {"message": "Nurse deleted"}


def list_nurses_for_hospital(db: Session, hospital_id: int):
    nurses = (
        db.query(Nurse)
        .filter(Nurse.hospital_id == hospital_id)
        .all()
    )
    return nurses
