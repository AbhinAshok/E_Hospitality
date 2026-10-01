from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(PatientProfile)
admin.site.register(DoctorProfile)
admin.site.register(AdminProfile)
admin.site.register(Appointment)
admin.site.register(Specialization)
admin.site.register(Payment)
admin.site.register(Billing)
admin.site.register(MedicalRecord)
admin.site.register(Facility)
admin.site.register(Prescription)
admin.site.register(HealthEducationResource)