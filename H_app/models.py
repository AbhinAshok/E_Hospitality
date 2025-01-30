from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from E_Hospitality import settings

# Custom User Model
class CustomUser(AbstractUser):
    USER_TYPES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('admin', 'Admin'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='patient')




# Patient Profile

class PatientProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='patient_profile'
    )
    name = models.CharField(max_length=100, null=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    medications = models.TextField(blank=True)
    medical_history = models.TextField(blank=True)
    treatment_plans = models.TextField(blank=True)

    def __str__(self):
        return self.user.username
# Doctor Profile

User = get_user_model()
class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    name = models.CharField(max_length=100, null=True)
    email = models.EmailField(null=True)
    phone_no = models.IntegerField(null=True)
    specialization = models.CharField(max_length=100, null=True)
    availability = models.CharField(max_length=100, null=True)  # Example: 'Mon-Fri, 9 AM - 5 PM'
    phone = models.CharField(max_length=15, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.specialization}"


class Specialization(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
# Appointment Model

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
    ]

    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='patient_appointments'
    )
    doctor = models.ForeignKey(
        'DoctorProfile',
        on_delete=models.CASCADE,
        related_name='doctor_appointments'
    )
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Scheduled')
    appointment_notes = models.TextField(blank=True)
    duration_minutes = models.PositiveIntegerField(default=30)
    is_virtual = models.BooleanField(default=False)
    location = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Appointment with Dr. {self.doctor.user.username} on {self.date} at {self.time}"

# Medical Record Model
class MedicalRecord(models.Model):
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="medical_records"
    )
    doctor = models.ForeignKey(
        DoctorProfile,
        on_delete=models.CASCADE,
        related_name='doctor_medical_records'
    )
    diagnosis = models.TextField()
    treatment_plan = models.TextField()
    medications = models.CharField(max_length=255, blank=True)
    allergies = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Medical Record for {self.patient.username} by Dr. {self.doctor.user.username}"

# Prescription Model
class Prescription(models.Model):
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='prescriptions'
    )
    doctor = models.ForeignKey(
        DoctorProfile,
        on_delete=models.CASCADE,
        related_name='doctor_prescriptions'
    )
    medication_name = models.CharField(max_length=200)
    dosage_instructions = models.TextField()
    medicines = models.TextField(null = True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prescription for {self.patient.username} by Dr. {self.doctor.user.username}"

# Billing Model
class Billing(models.Model):
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="billings"
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(
        max_length=10,
        choices=[('Paid', 'Paid'), ('Pending', 'Pending')],
        default='Pending'
    )
    date_issued = models.DateTimeField(auto_now_add=True)
    payment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Billing for {self.patient.username}: {self.total_amount} - {self.payment_status}"

# Health Education Resource Model
class HealthEducationResource(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

# Facility Model
class Facility(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    department = models.CharField(max_length=100)
    resources = models.TextField(blank=True, null=True)
    resource_quantity = models.PositiveIntegerField(default=1)
    resource_available = models.BooleanField(default=True)


    def __str__(self):
        return self.name

# Admin Profile Model
class AdminProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="admin_profile"
    )
    department = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100, null=True)
    employee_id = models.CharField(max_length=100, unique=True, default=1)

    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    address = models.TextField(blank=True, null=True)

    state = models.CharField(max_length=100, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, null=True)
    is_approved = models.BooleanField(default=False)


    def __str__(self):
        return self.user.username


class Payment(models.Model):
    appointment = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payment')
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    stripe_charge_id = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)



