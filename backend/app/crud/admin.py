from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models import Admin as AdminModel, Hospital
from ..schemas.admin import AdminCreate
from typing import Optional


def create_admin(db: Session, admin: AdminCreate):
    if not admin.email or not admin.admin_name:
        raise HTTPException(
            status_code=400, detail="Name and Email are required.")

    existing = db.query(AdminModel).filter(
        AdminModel.email == admin.email).first()
    if existing:
        raise HTTPException(
            status_code=409, detail="Admin with this email already exists.")

    if not db.query(Hospital).filter(Hospital.hospital_id == admin.hospital_id).first():
        raise HTTPException(status_code=404, detail="Hospital not found")

    db_admin = AdminModel(**admin.dict())
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin


def get_all_admins(db: Session):
    return db.query(AdminModel).all()


def get_admin_by_id(admin_id: int, db: Session):
    admin = db.query(AdminModel).filter(
        AdminModel.admin_id == admin_id).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    return admin


def update_admin(admin_id: int, admin_data: AdminCreate, db: Session):
    db_admin = db.query(AdminModel).filter(
        AdminModel.admin_id == admin_id).first()
    if not db_admin:
        raise HTTPException(status_code=404, detail="Admin not found")

    if admin_data.email and admin_data.email != db_admin.email:
        if db.query(AdminModel).filter(AdminModel.email == admin_data.email).first():
            raise HTTPException(
                status_code=409, detail="Email already in use by another admin.")

    for key, value in admin_data.dict().items():
        setattr(db_admin, key, value)

    db.commit()
    db.refresh(db_admin)
    return db_admin


def delete_admin(admin_id: int, db: Session):
    db_admin = db.query(AdminModel).filter(
        AdminModel.admin_id == admin_id).first()
    if not db_admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    db.delete(db_admin)
    db.commit()
    return {"detail": "Admin deleted successfully"}


def get_admins_by_hospital(db: Session, hospital_id: Optional[int]):
    if hospital_id:
        hospital_exists = db.query(Hospital).filter(
            Hospital.hospital_id == hospital_id).first()
        if not hospital_exists:
            raise HTTPException(status_code=404, detail="Hospital not found")

        return db.query(AdminModel).filter(AdminModel.hospital_id == hospital_id).all()

    return db.query(AdminModel).all()


def search_admins(db: Session, hospital_id: Optional[int] = None, search: Optional[str] = None, skip: int = 0, limit: int = 10):
    query = db.query(AdminModel)
    if hospital_id:
        query = query.filter(AdminModel.hospital_id == hospital_id)
    if search:
        query = query.filter(AdminModel.name.ilike(f"%{search}%"))
    return query.offset(skip).limit(limit).all()
