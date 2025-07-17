from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import navatar as schema
from ..crud import navatar as crud
from typing import Optional

router = APIRouter(prefix="/superadmin/navatars", tags=["Navatars"])


@router.post("/", response_model=schema.NavatarOut)
def create_navatar(navatar: schema.NavatarCreate, db: Session = Depends(get_db)):
    return crud.create_navatar(db, navatar)


@router.get("/", response_model=list[schema.NavatarOut])
def get_all_navatars(db: Session = Depends(get_db)):
    return crud.get_all_navatars(db)


@router.get("/search", response_model=list[schema.NavatarOut])
def search_navatars(
    hospital_id: Optional[int] = None,
    search_query: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return crud.search_navatars(db, hospital_id=hospital_id, search=search_query)


@router.get("/{navatar_id}", response_model=schema.NavatarOut)
def get_navatar(navatar_id: int, db: Session = Depends(get_db)):
    return crud.get_navatar_by_id(navatar_id, db)


@router.put("/{navatar_id}", response_model=schema.NavatarOut)
def update_navatar(navatar_id: int, navatar: schema.NavatarCreate, db: Session = Depends(get_db)):
    return crud.update_navatar(navatar_id, navatar, db)


@router.delete("/{navatar_id}")
def delete_navatar(navatar_id: int, db: Session = Depends(get_db)):
    return crud.delete_navatar(navatar_id, db)


@router.get("/{hospital_id}/navatars", response_model=list[schema.NavatarOut])
def get_navatars_by_hospital(
    hospital_id: int,
    db: Session = Depends(get_db)
):
    return crud.get_navatars_by_hospital(db, hospital_id=hospital_id)
