from pydantic import BaseModel, Field
from datetime import datetime

class BookingBase(BaseModel):
    date: str
    start_time: str
    end_time: str
    user_id: str | None = None

class BookingCreate(BookingBase):
    pass

class Booking(BookingBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
