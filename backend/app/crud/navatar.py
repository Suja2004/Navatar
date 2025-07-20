from sqlalchemy.orm import Session
from ..models import Navatar, Hospital
from ..schemas.navatar import NavatarCreate
from fastapi import HTTPException
from typing import Optional


def create_navatar(db: Session, navatar: NavatarCreate):
    # hospital = db.query(Hospital).filter(
    #     Hospital.hospital_id == navatar.hospital_id).first()
    # if not hospital:
    #     raise HTTPException(status_code=404, detail="Hospital not found")

    existing = db.query(Navatar).filter(
        Navatar.navatar_name == navatar.navatar_name,
        Navatar.hospital_id == navatar.hospital_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="A Navatar with the same name already exists in this hospital."
        )

    db_navatar = Navatar(**navatar.dict())
    db.add(db_navatar)
    db.commit()
    db.refresh(db_navatar)
    return db_navatar


def get_all_navatars(db: Session):
    return db.query(Navatar).all()


def get_navatar_by_id(navatar_id: int, db: Session):
    nav = db.query(Navatar).filter(Navatar.navatar_id == navatar_id).first()
    if not nav:
        raise HTTPException(status_code=404, detail="Navatar not found")
    return nav


def update_navatar(navatar_id: int, navatar: NavatarCreate, db: Session):
    db_navatar = db.query(Navatar).filter(
        Navatar.navatar_id == navatar_id).first()
    if not db_navatar:
        raise HTTPException(status_code=404, detail="Navatar not found")

    # Check if hospital exists
    hospital = db.query(Hospital).filter(
        Hospital.hospital_id == navatar.hospital_id).first()
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")

    # Check for duplicate name in the same hospital (excluding current navatar)
    existing = db.query(Navatar).filter(
        Navatar.navatar_name == navatar.navatar_name,
        Navatar.hospital_id == navatar.hospital_id,
        Navatar.navatar_id != navatar_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Another Navatar with the same name already exists in this hospital."
        )

    for key, value in navatar.dict().items():
        setattr(db_navatar, key, value)
    db.commit()
    db.refresh(db_navatar)
    return db_navatar


def delete_navatar(navatar_id: int, db: Session):
    db_navatar = db.query(Navatar).filter(
        Navatar.navatar_id == navatar_id).first()
    if not db_navatar:
        raise HTTPException(status_code=404, detail="Navatar not found")
    db.delete(db_navatar)
    db.commit()
    return {"detail": "Navatar deleted"}


def search_navatars(db: Session, hospital_id: Optional[int] = None, search: Optional[str] = None):
    query = db.query(Navatar)
    if hospital_id:
        query = query.filter(Navatar.hospital_id == hospital_id)
    if search:
        query = query.filter(Navatar.navatar_name.ilike(f"%{search}%"))

    return query.all()


def get_navatars_by_hospital(db: Session, hospital_id: Optional[int]):
    query = db.query(Navatar)
    if hospital_id:
        query = query.filter(Navatar.hospital_id == hospital_id)
    return query.all()
