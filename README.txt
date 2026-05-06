Aircraft Maintenance Capstone Project
USAF Inventory & Maintenance Tracking System

---

PROJECT OVERVIEW

This project is a prototype Aircraft Maintenance Tracking System designed to simulate a real-world military logistics environment. The system allows users to import maintenance logs from Excel, view and manage data in a desktop interface, and export reports in CSV and PDF formats.

The purpose of this system is to demonstrate the development of an information system that improves visibility, organization, and reporting of aircraft maintenance activities.

---

SYSTEM REQUIREMENTS

Before running the application, ensure the following are installed:

* Python 3.10 or newer
* pip (Python package manager)
* Windows OS (recommended)

---

PROJECT SETUP INSTRUCTIONS

1. Extract the ZIP file

* Right-click the ZIP folder
* Select "Extract All"
* Open the extracted folder

2. Open PowerShell in the project folder

* Navigate to the "aircraft_maintenance_capstone" folder
* Right-click inside the folder
* Select "Open in Terminal" or "Open PowerShell here"

3. Create a virtual environment

Run the following command:

python -m venv .venv

4. Activate the virtual environment

Run:

..venv\Scripts\activate

If you receive a script error, run:

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

Then activate again.

5. Install required packages

Run:

pip install PySide6 pandas openpyxl reportlab

---

RUNNING THE APPLICATION

1. Navigate to the desktop folder:

cd desktop

2. Run the application:

python app.py

3. The application window should open.

---

USING THE APPLICATION

1. Click "Import Maintenance Logs"
2. Select the sample Excel file located in:

data\maintenance_logs.xlsx

3. The table will populate with maintenance data.

4. Use the following features:

* View maintenance logs in table format
* Export CSV report
* Export PDF report

Exported files will be saved in the "exports" folder.

---


NOTES

* This is a prototype system developed and is still a work in progress.
* Some features may be simplified but demonstrate core functionality.
* If the application does not run, ensure all dependencies are installed correctly.

---

AUTHOR

Michael Eilbracht
Liberty University
CSIS 484 Capstone Project
Dr. Eric Straw

---
