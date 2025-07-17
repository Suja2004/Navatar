from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class HospitalBase(BaseModel):
    hospital_name: str
    country: str
    pincode: str


class HospitalCreate(HospitalBase):
    pass


class HospitalOut(HospitalBase):
    hospital_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
