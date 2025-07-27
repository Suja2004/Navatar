from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from ..models import NurseDepartment, Gender


class NurseBase(BaseModel):
    name: str = Field(..., min_length=1)
    gender: Gender
    department: NurseDepartment
    email: EmailStr
    phone: Optional[str] = Field(None, min_length=10, max_length=15)


class NurseCreate(NurseBase):
    assigned_doctor_id: Optional[int] = None


class NurseUpdate(BaseModel):
    name: Optional[str]
    gender: Optional[Gender]
    department: Optional[NurseDepartment]
    email: Optional[EmailStr]
    phone: Optional[str] = Field(None, min_length=10, max_length=15)
    assigned_doctor_id: Optional[int]


class NurseOut(NurseBase):
    id: int
    hospital_id: int
    assigned_doctor_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
