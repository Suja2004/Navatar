from sqlalchemy.orm import Session
from ..models import Booking
from ..schemas import booking as schemas

def get_booking(db: Session, booking_id: int):
    return db.query(Booking).filter(Booking.id == booking_id).first()

def get_bookings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Booking).offset(skip).limit(limit).all()

def create_booking(db: Session, booking: schemas.BookingCreate):
    db_booking = Booking(**booking.dict())
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

def delete_booking(db: Session, booking_id: int):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if booking:
        db.delete(booking)
        db.commit()
        return True
    return False

def check_booking_overlap(db: Session, date: str, start_time: str, end_time: str):
    # Check if any booking overlaps with the given time slot
    bookings = db.query(Booking).filter(Booking.date == date).all()
    for b in bookings:
        b_start = b.start_time
        b_end = b.end_time
        if (start_time < b_end) and (end_time > b_start):
            return True
    return False
