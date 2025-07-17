from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, func, UniqueConstraint
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


class Hospital(Base):
    __tablename__ = "hospital"

    hospital_id = Column(Integer, primary_key=True, index=True)
    hospital_name = Column(String, unique=True, index=True, nullable=False)
    country = Column(String, index=True, nullable=False)
    pincode = Column(String, index=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False,
                        default=func.now(), onupdate=func.now())
    __table_args__ = (
        UniqueConstraint("hospital_name", "pincode",
                         name="unique_hospital_name_pincode"),
    )


class NavatarStatus(str, enum.Enum):
    Available = "Available"
    Booked = "Booked"
    InSession = "InSession"
    Offline = "Offline"


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
    __tablename__ = "doctor"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    department = Column(Enum(DoctorDepartment), nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=True)
    hospital_id = Column(Integer, ForeignKey(
        "hospital.hospital_id"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False,
                        default=func.now(), onupdate=func.now())

    hospital = relationship("Hospital", backref="doctors")
    nurses = relationship("Nurse", back_populates="doctor")


class Nurse(Base):
    __tablename__ = "nurse"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    department = Column(Enum(NurseDepartment), nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=True)
    assigned_doctor_id = Column(Integer, ForeignKey("doctor.id"))
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False,
                        default=func.now(), onupdate=func.now())

    doctor = relationship("Doctor", back_populates="nurses")


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String)
    start_time = Column(String)
    end_time = Column(String)
    user_id = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
