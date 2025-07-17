from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..crud import hospital as hospital_crud
from ..schemas import hospital as hospital_schema
from typing import Optional

router = APIRouter(prefix="/superadmin/hospital", tags=["Hospitals"])


@router.post("/", response_model=hospital_schema.HospitalOut)
def create_hospital(hospital: hospital_schema.HospitalCreate, db: Session = Depends(get_db)):
    return hospital_crud.create_hospital(db, hospital)


@router.get("/", response_model=list[hospital_schema.HospitalOut])
def get_all_hospitals(db: Session = Depends(get_db)):
    return hospital_crud.get_all_hospitals(db)


@router.get("/search", response_model=list[hospital_schema.HospitalOut])
def search_hospitals(
    search_query: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    return hospital_crud.search_hospitals(db=db, search_query=search_query)


@router.put("/{hospital_id}", response_model=hospital_schema.HospitalOut)
def update_hospital(hospital_id: int, hospital: hospital_schema.HospitalCreate, db: Session = Depends(get_db)):
    return hospital_crud.update_hospital(hospital_id, hospital, db)


@router.delete("/{hospital_id}")
def delete_hospital(hospital_id: int, db: Session = Depends(get_db)):
    return hospital_crud.delete_hospital(hospital_id, db)
