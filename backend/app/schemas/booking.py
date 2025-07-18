from pydantic import BaseModel
from typing import Optional
from datetime import date, time, datetime
from ..models import BookingStatus


class BookingBase(BaseModel):
    doctor_id: int
    navatar_id: int
    nurse_id: Optional[int] = None
    date: date
    start_time: time
    end_time: time
    location: str
    status: BookingStatus


class BookingCreate(BookingBase):
    pass


class BookingUpdateStatus(BaseModel):
    status: BookingStatus


class BookingOut(BookingBase):
    booking_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
