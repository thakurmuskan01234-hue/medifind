# Hospital Appointment Management System

A beginner-friendly Django + SQLite hospital appointment website for ITL/PBL.

## Features
- Patient registration and login
- Doctor search by department
- Appointment booking
- Duplicate active-slot prevention
- Appointment history
- Appointment cancellation
- Django Admin for doctors, patients, departments and appointments
- Responsive Bootstrap UI

## Run in VS Code

### 1. Open the project folder
Open `hospital_appointment_management` in VS Code.

### 2. Create virtual environment
Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Django
```bash
pip install -r requirements.txt
```

### 4. Create database
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create admin account
```bash
python manage.py createsuperuser
```
Enter username, email and password.

### 6. Start server
```bash
python manage.py runserver
```

Open:
http://127.0.0.1:8000/

Admin:
http://127.0.0.1:8000/admin/

## Add sample data
After opening Admin, create:
1. Departments (Cardiology, General Medicine, Dermatology, etc.)
2. Doctors
3. Patients if needed
4. Appointments

Then use the website to register as a patient and book appointments.

## Important
This is an academic/demo project. For real hospital deployment, add production security, proper role permissions, audit logging, secure hosting, backups, privacy controls, and medical-data compliance.
