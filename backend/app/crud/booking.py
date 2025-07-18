from sqlalchemy.orm import Session
from ..models import Booking, Doctor, Navatar
from ..schemas import booking as booking_schema
from fastapi import HTTPException
from datetime import datetime
from sqlalchemy import select


def check_booking_overlap(
    db: Session,
    hospital_id: int,
    date: str,
    start_time: datetime,
    end_time: datetime,
    doctor_id: int,
    navatar_id: int = None
):
    start_time_naive = start_time.replace(tzinfo=None)
    end_time_naive = end_time.replace(tzinfo=None)

    # ✅ Check 1: Navatar already booked at any doctor of the hospital at the same time
    if navatar_id:
        doctor_ids = select(Doctor.id).where(Doctor.hospital_id == hospital_id)

        navatar_bookings = db.query(Booking).filter(
            Booking.doctor_id.in_(doctor_ids),
            Booking.date == date,
            Booking.navatar_id == navatar_id,
            Booking.start_time < end_time,
            Booking.end_time > start_time
        ).first()

        if navatar_bookings:
            return "Navatar already booked in this time slot."

    # ✅ Check 2: Doctor already booked at this time (no matter the navatar)
    doctor_booking = db.query(Booking).filter(
        Booking.doctor_id == doctor_id,
        Booking.date == date,
        Booking.start_time < end_time,
        Booking.end_time > start_time
    ).first()

    if doctor_booking:
        return "Doctor already has a booking in this time slot."

    return None  


def create_booking(db: Session, booking: booking_schema.BookingCreate):
    doctor = db.query(Doctor).filter(Doctor.id == booking.doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    if booking.navatar_id is not None:
        navatar = db.query(Navatar).filter(
            Navatar.navatar_id == booking.navatar_id).first()
        if not navatar:
            raise HTTPException(status_code=404, detail="Navatar not found")

    if check_booking_overlap(db, doctor.hospital_id, booking.date, booking.start_time, booking.end_time, booking.doctor_id, booking.navatar_id):
        raise HTTPException(
            status_code=400, detail="Booking overlaps with an existing booking.")

    db_booking = Booking(**booking.dict())
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking


def get_booking(db: Session, booking_id: int):
    booking = db.query(Booking).filter(
        Booking.booking_id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking


def get_all_bookings(db: Session):
    return db.query(Booking).all()


def update_booking_status(db: Session, booking_id: int, updated: booking_schema.BookingUpdateStatus):
    db_booking = db.query(Booking).filter(
        Booking.booking_id == booking_id).first()

    if not db_booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    db_booking.status = updated.status
    db.commit()
    db.refresh(db_booking)
    return db_booking


def delete_booking(db: Session, booking_id: int):
    booking = db.query(Booking).filter(
        Booking.booking_id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    db.delete(booking)
    db.commit()
    return {"detail": "Booking deleted"}
