from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..schemas import session as session_schema
from ..crud import session as session_crud
from ..database import get_db
from typing import List

router = APIRouter(prefix="/sessions", tags=["Sessions"])

@router.post("/", response_model=session_schema.SessionOut)
def create(session: session_schema.SessionCreate, db: Session = Depends(get_db)):
    return session_crud.create_session(db, session)

@router.get("/{session_id}", response_model=session_schema.SessionOut)
def read(session_id: int, db: Session = Depends(get_db)):
    return session_crud.get_session(db, session_id)

@router.get("/", response_model=List[session_schema.SessionOut])
def read_all(db: Session = Depends(get_db)):
    return session_crud.get_all_sessions(db)

@router.put("/{session_id}", response_model=session_schema.SessionOut)
def update(session_id: int, session: session_schema.SessionUpdate, db: Session = Depends(get_db)):
    return session_crud.update_session(db, session_id, session)

@router.delete("/{session_id}")
def delete(session_id: int, db: Session = Depends(get_db)):
    return session_crud.delete_session(db, session_id)
