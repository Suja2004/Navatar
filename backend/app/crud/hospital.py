from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..schemas import hospital as hospital_schema
from fastapi import HTTPException
from typing import Optional
from ..models import Hospital, Doctor, Admin, Navatar


def create_hospital(db: Session, hospital: hospital_schema.HospitalCreate):
    existing_hospital = db.query(Hospital).filter(
        Hospital.hospital_name == hospital.hospital_name,
        Hospital.pincode == hospital.pincode
    ).first()

    if existing_hospital:
        raise HTTPException(
            status_code=400,
            detail="Hospital with this name and pincode already exists."
        )

    db_hospital = Hospital(**hospital.dict())
    db.add(db_hospital)
    db.commit()
    db.refresh(db_hospital)
    return db_hospital


def get_all_hospitals(db: Session):
    return db.query(Hospital).all()


def update_hospital(hospital_id: int, hospital: hospital_schema.HospitalCreate, db: Session):
    db_hospital = db.query(Hospital).filter(
        Hospital.hospital_id == hospital_id).first()

    if db_hospital is None:
        raise HTTPException(status_code=404, detail="Hospital not found")

    existing = db.query(Hospital).filter(
        Hospital.hospital_name == hospital.hospital_name,
        Hospital.pincode == hospital.pincode,
        Hospital.hospital_id != hospital_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Another hospital with the same name and pincode already exists."
        )

    for key, value in hospital.dict().items():
        setattr(db_hospital, key, value)

    db.commit()
    db.refresh(db_hospital)
    return db_hospital


def delete_hospital(hospital_id: int, db: Session):
    db_hospital = db.query(Hospital).filter(
        Hospital.hospital_id == hospital_id).first()

    if db_hospital is None:
        raise HTTPException(status_code=404, detail="Hospital not found")

    has_doctors = db.query(Doctor).filter(
        Doctor.hospital_id == hospital_id).first()
    if has_doctors:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete hospital: doctors are still assigned to this hospital."
        )

    has_admins = db.query(Admin).filter(
        Admin.hospital_id == hospital_id).first()
    if has_admins:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete hospital: admins are still associated with this hospital."
        )

    has_navatars = db.query(Navatar).filter(
        Navatar.hospital_id == hospital_id).first()
    if has_navatars:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete hospital: navatars are still assigned to this hospital."
        )

    db.delete(db_hospital)
    db.commit()
    return {"detail": "Hospital deleted successfully"}


def search_hospitals(db: Session, search_query: Optional[str] = None):
    query = db.query(Hospital)
    if search_query:
        query = query.filter(Hospital.hospital_name.ilike(f"%{search_query}%"))
    return query.all()


def get_hospital_by_id(hospital_id: int, db: Session):
    hospital = db.query(Hospital).filter(Hospital.hospital_id == hospital_id).first()
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")
    return hospital