# Navatar Remote Consultation Booking App

A modern booking app for remote consultations, featuring a FastAPI backend and a React frontend (Vite).

---

## 🚀 Quick Start

**1. Install Dependencies**

Backend (FastAPI):  
Go to the backend folder and install dependencies:  
```
cd backend
pip install -r requirements.txt
```

Frontend (React/Vite):  
Go to the frontend folder and install dependencies:  
```
cd frontend
npm install
```

---

**2. Run the Backend**

From the backend directory:  
```
uvicorn app.main:app --reload
```
The backend will be available at [http://localhost:8000](http://localhost:8000).

---

**3. Run the Frontend**

From the frontend directory:  
```
npm run dev
```
The frontend will be available at [http://localhost:5713](http://localhost:3000).

---

## 📁 Project Structure

- **backend/**: FastAPI backend (API, database, models)
- **frontend/**: React/Vite frontend (UI, booking logic, notifications)

---

## 🔗 API Documentation

Visit [http://localhost:8000/docs](http://localhost:8000/docs) for interactive API documentation (Swagger UI).

---

## 🔒 Authentication

**Demo users:**  
- **Email:** doctor@example.com  
  **Password:** password  
- **Email:** doctor2@example.com  
  **Password:** password

---

## 📝 Features

- **User login/logout**
- **Booking management (create, view, cancel)**
- **Reminder notifications**
- **Responsive UI**

---

## 📚 Technologies

- **Backend:** FastAPI, SQLite, Python
- **Frontend:** React, Vite, date-fns

---

## 🛠️ Troubleshooting

- **CORS errors:** Ensure your backend allows requests from http://localhost:5713
- **Invalid time value:** Check that all date fields are valid before passing to components
