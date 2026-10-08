from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AppointmentForm, PatientRegistrationForm
from .models import Appointment, Department, Doctor, Patient

def home(request):
    context = {
        "doctor_count": Doctor.objects.filter(is_active=True).count(),
        "department_count": Department.objects.count(),
        "appointment_count": Appointment.objects.count(),
    }
    return render(request, "home.html", context)

def register(request):
    if request.method == "POST":
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Patient.objects.create(
                user=user,
                name=form.cleaned_data["name"],
                email=form.cleaned_data["email"],
                phone=form.cleaned_data["phone"],
            )
            login(request, user)
            messages.success(request, "Registration successful. Welcome!")
            return redirect("dashboard")
    else:
        form = PatientRegistrationForm()
    return render(request, "register.html", {"form": form})

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("dashboard")
        messages.error(request, "Invalid username or password.")
    return render(request, "login.html")

def user_logout(request):
    logout(request)
    return redirect("home")

@login_required
def dashboard(request):
    patient, _ = Patient.objects.get_or_create(
        user=request.user,
        defaults={"name": request.user.get_full_name() or request.user.username,
                  "email": request.user.email, "phone": ""}
    )
    appointments = Appointment.objects.filter(patient=patient)[:5]
    return render(request, "dashboard.html", {"patient": patient, "appointments": appointments})

def doctors(request):
    selected_department = request.GET.get("department")
    doctor_list = Doctor.objects.filter(is_active=True).select_related("department")
    if selected_department:
        doctor_list = doctor_list.filter(department_id=selected_department)
    return render(request, "doctors.html", {
        "doctors": doctor_list,
        "departments": Department.objects.all(),
        "selected_department": selected_department,
    })

@login_required
def book_appointment(request):
    patient, _ = Patient.objects.get_or_create(
        user=request.user,
        defaults={"name": request.user.username, "email": request.user.email, "phone": ""}
    )
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = patient
            appointment.status = "Pending"
            # Prevent exact duplicate active slot bookings.
            exists = Appointment.objects.filter(
                doctor=appointment.doctor,
                appointment_date=appointment.appointment_date,
                appointment_time=appointment.appointment_time,
                status__in=["Pending", "Confirmed"],
            ).exists()
            if exists:
                messages.error(request, "This time slot is already booked. Please choose another slot.")
            else:
                appointment.save()
                messages.success(request, "Appointment booked successfully.")
                return redirect("my_appointments")
    else:
        form = AppointmentForm()
    return render(request, "book.html", {"form": form})

@login_required
def my_appointments(request):
    patient, _ = Patient.objects.get_or_create(
        user=request.user,
        defaults={"name": request.user.username, "email": request.user.email, "phone": ""}
    )
    appointments = Appointment.objects.filter(patient=patient).select_related("doctor", "doctor__department")
    return render(request, "appointments.html", {"appointments": appointments})

@login_required
def cancel_appointment(request, pk):
    patient = get_object_or_404(Patient, user=request.user)
    appointment = get_object_or_404(Appointment, pk=pk, patient=patient)
    if appointment.status in ["Pending", "Confirmed"]:
        appointment.status = "Cancelled"
        appointment.save()
        messages.success(request, "Appointment cancelled.")
    return redirect("my_appointments")
