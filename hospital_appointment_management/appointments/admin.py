from django.contrib import admin
from .models import Department, Doctor, Patient, Appointment

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "description")

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("name", "specialization", "department", "experience", "is_active")
    list_filter = ("department", "is_active")
    search_fields = ("name", "specialization")

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "gender")
    search_fields = ("name", "email", "phone")

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("patient", "doctor", "appointment_date", "appointment_time", "status")
    list_filter = ("status", "appointment_date")
    search_fields = ("patient__name", "doctor__name")
