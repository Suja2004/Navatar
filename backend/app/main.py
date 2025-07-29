from .database import SessionLocal, engine, Base
from . import models
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from .router import hospital, navatar, doctor, nurse, session, admin, booking, auth_router

app = FastAPI(
    title="Hospital Management API",
    description="API for managing hospitals",
    version="1.0.0",
    redirect_slashes=False
)

# Create tables
models.Base.metadata.create_all(bind=engine)

# Allow CORS
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:8080",
    "https://navatar-user.vercel.app",
    "https://navatar-ashen.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Welcome to the Hospital Management API"}


# Register routers
app.include_router(hospital.router)
app.include_router(navatar.router)
app.include_router(doctor.router)
app.include_router(nurse.router)
app.include_router(admin.router)
app.include_router(booking.router)
app.include_router(session.router)
app.include_router(auth_router.router)
