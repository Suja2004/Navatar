from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import admin as schema
from ..crud import admin as crud
from typing import Optional

router = APIRouter(prefix="/superadmin/admins", tags=["Admins"])


@router.post("/", response_model=schema.AdminOut)
def create_admin(admin: schema.AdminCreate, db: Session = Depends(get_db)):
    return crud.create_admin(db, admin)


@router.get("/", response_model=list[schema.AdminOut])
def get_all_admins(db: Session = Depends(get_db)):
    return crud.get_all_admins(db)


@router.get("/search", response_model=list[schema.AdminOut])
def search_admins(
    hospital_id: Optional[int] = None,
    search_query: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return crud.search_admins(db, hospital_id=hospital_id, search=search_query)


@router.get("/by-hospital", response_model=list[schema.AdminOut])
def get_admins_by_hospital(
    hospital_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    return crud.get_admins_by_hospital(db, hospital_id=hospital_id)


@router.get("/{admin_id}", response_model=schema.AdminOut)
def get_admin(admin_id: int, db: Session = Depends(get_db)):
    return crud.get_admin_by_id(admin_id, db)


@router.put("/{admin_id}", response_model=schema.AdminOut)
def update_admin(admin_id: int, admin: schema.AdminCreate, db: Session = Depends(get_db)):
    return crud.update_admin(admin_id, admin, db)


@router.delete("/{admin_id}")
def delete_admin(admin_id: int, db: Session = Depends(get_db)):
    return crud.delete_admin(admin_id, db)
