from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, func, UniqueConstraint, Date, Time, Text
from sqlalchemy.orm import relationship
from .database import Base
import enum


# Enums for gender
class Gender(str, enum.Enum):
    Male = "Male"
    Female = "Female"
    Other = "Other"


# Enum for doctor departments
class DoctorDepartment(str, enum.Enum):
    Cardiology = "Cardiology"
    Surgery = "Surgery"
    Pediatrics = "Pediatrics"
    Neurology = "Neurology"


# Enum for nurse departments
class NurseDepartment(str, enum.Enum):
    ICU = "ICU"
    Pediatrics = "Pediatrics"
    Emergency = "Emergency"
    Ward = "Ward"


# Enum for booking status
class BookingStatus(str, enum.Enum):
    Booked = "Booked"
    InSession = "InSession"
    Completed = "Completed"
    Cancelled = "Cancelled"


# Enum for session ended by
class EndedBy(str, enum.Enum):
    Doctor = "Doctor"
    SystemTimeout = "System Timeout"
    Admin = "Admin"


# Enum for video call status
class VideoCallStatus(str, enum.Enum):
    Active = "Active"
    Ended = "Ended"
    Error = "Error"


# Enum for navatar status
class NavatarStatus(str, enum.Enum):
    Available = "Available"
    Booked = "Booked"
    InSession = "InSession"
    Offline = "Offline"


class Session(Base):
    __tablename__ = "sessions"

    session_id = Column(Integer, primary_key=True,
                        index=True, autoincrement=True)
    booking_id = Column(Integer, ForeignKey(
        "bookings.booking_id"), nullable=False)

    start_timestamp = Column(DateTime, nullable=False)
    end_timestamp = Column(DateTime, nullable=True)
    ended_by = Column(Enum(EndedBy), nullable=True)
    video_call_status = Column(
        Enum(VideoCallStatus), nullable=False, default=VideoCallStatus.Active)

    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(),
                        onupdate=func.now(), nullable=False)

    booking = relationship("Booking", back_populates="session")


class Booking(Base):
    __tablename__ = "bookings"

    booking_id = Column(Integer, primary_key=True,
                        index=True, autoincrement=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    navatar_id = Column(Integer, ForeignKey(
        "navatar.navatar_id"), nullable=False)
    nurse_id = Column(Integer, ForeignKey("nurses.id"), nullable=True)

    date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    location = Column(String, nullable=False)
    status = Column(Enum(BookingStatus),
                    default=BookingStatus.Booked, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(),
                        onupdate=func.now(), nullable=False)

    doctor = relationship("Doctor", back_populates="bookings")
    nurse = relationship("Nurse", back_populates="bookings",
                         foreign_keys=[nurse_id])
    navatar = relationship("Navatar", back_populates="bookings")
    session = relationship("Session", uselist=False, back_populates="booking")
    nurse = relationship("Nurse", back_populates="bookings")


class Hospital(Base):
    __tablename__ = "hospital"

    hospital_id = Column(Integer, primary_key=True, index=True)
    hospital_name = Column(String, unique=False, index=True, nullable=False)
    country = Column(String, index=True, nullable=False)
    pincode = Column(String, index=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False,
                        default=func.now(), onupdate=func.now())
    __table_args__ = (
        UniqueConstraint("hospital_name", "pincode",
                         name="unique_hospital_name_pincode"),
    )
    navatars = relationship("Navatar", back_populates="hospital")
    doctors = relationship("Doctor", back_populates="hospital")


class Navatar(Base):
    __tablename__ = "navatar"

    navatar_id = Column(Integer, primary_key=True, index=True)
    navatar_name = Column(String, nullable=False)
    location = Column(String, nullable=True)
    hospital_id = Column(Integer, ForeignKey(
        "hospital.hospital_id"), nullable=True)
    status = Column(Enum(NavatarStatus),
                    default=NavatarStatus.Offline, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False,
                        default=func.now(), onupdate=func.now())
    bookings = relationship("Booking", back_populates="navatar")
    hospital = relationship("Hospital", back_populates="navatars")


class Admin(Base):
    __tablename__ = "admin"

    admin_id = Column(Integer, primary_key=True, index=True)
    admin_name = Column(String, nullable=False)
    hospital_id = Column(Integer, ForeignKey(
        "hospital.hospital_id"), nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False,
                        default=func.now(), onupdate=func.now())


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    department = Column(Enum(DoctorDepartment), nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    hospital_id = Column(Integer, ForeignKey(
        "hospital.hospital_id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False,
                        default=func.now(), onupdate=func.now())

    hospital = relationship("Hospital", back_populates="doctors")
    nurses = relationship("Nurse", back_populates="doctor")
    bookings = relationship("Booking", back_populates="doctor")


class Nurse(Base):
    __tablename__ = "nurses"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    department = Column(Enum(NurseDepartment), nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    assigned_doctor_id = Column(Integer, ForeignKey("doctors.id"))
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False,
                        default=func.now(), onupdate=func.now())

    doctor = relationship("Doctor", back_populates="nurses")
    bookings = relationship("Booking", back_populates="nurse")
