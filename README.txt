# ✈️ Aircraft Maintenance Tracker

A desktop-based aircraft maintenance tracking and operational readiness system built with Python, FastAPI, and PySide6.

---

## 📌 Overview

This project is designed to support aircraft maintenance operations by tracking discrepancies, maintenance actions, technician assignments, and operational status in real time. The system provides a desktop interface for maintenance workflow management along with reporting and analytics capabilities.

---

## 🚀 Features

- Aircraft discrepancy tracking  
- Maintenance log management  
- Technician assignment and workflow tracking  
- Search and filtering functionality  
- Real-time maintenance status updates  
- CSV and PDF report generation  
- Role-based access control  
- Excel-based maintenance data import  

---

## 🧰 Technologies Used

- Python  
- FastAPI  
- PySide6 (Qt for Python)  
- SQLAlchemy  
- pandas  
- ReportLab  

---

## 📊 Key Highlights

- Built RESTful APIs for maintenance data and workflow management  
- Designed a desktop interface for maintenance operations and tracking  
- Implemented maintenance reporting and discrepancy logging  
- Processed structured maintenance datasets using pandas  
- Developed role-based functionality for operational workflows  

---

## ⚡ Quick Start

### Backend

```bash
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Desktop Application

```bash
cd desktop
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

---

## 📁 Project Structure

```text
backend/     → FastAPI backend services
desktop/     → PySide6 desktop application
data/        → Demo maintenance datasets
```

---

## ⚠️ Demo Data Notice

This project uses synthetic demo data for demonstration purposes only.  
No real or sensitive operational data is included in this repository.

---

## 🔮 Future Improvements

- Cloud deployment support  
- Real-time dashboard analytics  
- Multi-aircraft fleet support  
- Authentication with JWT  
- Web-based maintenance portal  

---

## 👤 Author

Michael Eilbracht
