from pydantic import BaseModel
from typing import Optional
from enum import Enum
from datetime import datetime


class NavatarStatus(str, Enum):
    Available = "Available"
    Booked = "Booked"
    InSession = "InSession"
    Offline = "Offline"


class NavatarBase(BaseModel):
    navatar_name: str
    location: Optional[str] = None
    hospital_id: Optional[int] = None
    status: Optional[NavatarStatus] = NavatarStatus.Offline


class NavatarCreate(NavatarBase):
    pass


class NavatarOut(NavatarBase):
    navatar_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # For Pydantic v2
