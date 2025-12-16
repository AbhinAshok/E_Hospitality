import json
from datetime import datetime
import stripe
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout as auth_logout, get_user_model
from django.contrib.auth import login
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, FormView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponseRedirect
from django.conf import settings

from django.db.models import Q


from .forms import (
    CustomUserLoginForm, CustomUserSignupForm, AppointmentForm,
    FacilityForm, HealthEducationResourceForm, PrescriptionForm,
    SelectDateForm, MedicalRecordForm, DoctorProfileForm, PatientProfileForm, PaymentForm
)
from .models import (
    CustomUser, DoctorProfile, Appointment, MedicalRecord,
    Billing, Facility, HealthEducationResource, Prescription, PatientProfile, Specialization, Payment
)


stripe.api_key = settings.STRIPE_SECRET_KEY

def home(request):
    return render(request, 'base.html')


def signup(request):
    if request.method == 'POST':
        form = CustomUserSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_login')
    else:
        form = CustomUserSignupForm()
    return render(request, 'signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(dashboard_redirect)
    else:
        form = CustomUserLoginForm()
    return render(request, 'login.html', {'form': form})


def dashboard_redirect(request):
    if not request.user.is_authenticated:
        return redirect('user_login')

    user_type_redirects = {
        'patient': 'patient_dashboard',
        'doctor': 'doctor_dashboard',
        'admin': 'admin_dashboard'
    }
    return redirect(user_type_redirects.get(request.user.user_type, 'user_login'))


@login_required
def patient_dashboard(request):
    return render(request, 'patient_dashboard.html')

@login_required
def doctor_dashboard(request):
    return render(request, 'doctor_dashboard.html')

@login_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')


@method_decorator(login_required, name='dispatch')
class PatientProfileView(DetailView):
    """
    Displays and allows updates to the PatientProfile for the logged-in user.
    """
    model = PatientProfile
    template_name = 'patient_profile.html'

    def get_object(self):
       
        profile, created = PatientProfile.objects.get_or_create(user=self.request.user)
        return profile

    def post(self, request, *args, **kwargs):
       
        profile = self.get_object()
        form = PatientProfileForm(request.POST, instance=profile)

        if form.is_valid():
            form.save()
            return redirect('patient_dashboard')  
        else:
           
            return render(request, self.template_name, {'form': form, 'profile': profile})


@login_required
def register_doctor(request):
    """
    Handles doctor registration and profile creation.
    """
    if request.method == 'POST':
        form = DoctorProfileForm(request.POST)
        if form.is_valid():
            form.save()  
            return redirect('doctor_dashboard') 
        else:
            print(form.errors) 
    else:
        form = DoctorProfileForm()

    return render(request, 'register_doctor.html', {'form': form})





class DoctorProfileView(View):
    template_name = 'register_doctor.html'

    def get(self, request, *args, **kwargs):
        
        if request.user.is_authenticated:
            profile, _ = DoctorProfile.objects.get_or_create(user=request.user)
            form = DoctorProfileForm(instance=profile)
        else:
            
            form = DoctorProfileForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            
            profile = get_object_or_404(DoctorProfile, user=request.user)
            form = DoctorProfileForm(request.POST, request.FILES, instance=profile)
        else:
           
            form = DoctorProfileForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('doctor_dashboard')
        else:
           
            print(form.errors)
        return render(request, self.template_name, {'form': form})


class AppointmentBaseView:
    model = Appointment
    context_object_name = 'appointments'


# Patient Appointment Views
@method_decorator(login_required, name='dispatch')
class AppointmentListView(AppointmentBaseView, ListView):
    
    template_name = 'appointments/appointment_list.html'

    def get_queryset(self):
       
        get_object_or_404(PatientProfile, user=self.request.user)
        
        return Appointment.objects.filter(patient=self.request.user)


@method_decorator(login_required, name='dispatch')
class AppointmentCreateView(CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointments/appointment_form.html'

    def form_valid(self, form):
       
        form.instance.patient = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('confirm_booking', kwargs={'appointment_id': self.object.id})
@login_required
def confirm_appointment(request, appointment_id):
    """
    Displays the confirmation page for an appointment and allows the patient to confirm it.
    """
    
    try:
        get_object_or_404(PatientProfile, user=request.user)
    except:
        return JsonResponse({"status": "error", "message": "Patient profile not found."}, status=404)

    
    appointment = get_object_or_404(Appointment, id=appointment_id, patient=request.user)

    
    if appointment.status == 'Confirmed':
        return JsonResponse({"status": "error", "message": "Appointment is already confirmed."}, status=400)

    if request.method == 'POST':
        
        appointment.status = 'Confirmed'
        appointment.save()
        
        return JsonResponse({"status": "success", "message": "Appointment confirmed successfully!"})

    
    return render(request, 'appointments/appointment_confirm.html', {'appointment': appointment})


@method_decorator(login_required, name='dispatch')
class DoctorAppointmentListView(AppointmentBaseView, ListView):
   
    template_name = 'appointments/doctor_appointment_list.html'

    def get_queryset(self):
       
        doctor_profile = get_object_or_404(DoctorProfile, user=self.request.user)
        
        return Appointment.objects.filter(doctor=doctor_profile)



@method_decorator(login_required, name='dispatch')
class AdminAppointmentListView(LoginRequiredMixin, ListView):
    model = Appointment
    template_name = 'appointments/admin_appointment_list.html'
    context_object_name = 'appointments'

    def get_queryset(self):
        return Appointment.objects.all() 
@method_decorator(login_required, name='dispatch')


@method_decorator(login_required, name='dispatch')
class AppointmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Appointment
    template_name = 'appointments/appointment_confirm_delete.html'
    context_object_name = 'appointment'

    def get_success_url(self):
        return reverse_lazy('admin_appointment_list')  


@login_required
def add_medical_history(request, patient_id):
    patient = get_object_or_404(CustomUser, id=patient_id, user_type='patient')

    
    if not hasattr(request.user, 'doctor_profile'):
        return redirect('error_page') 

    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            medical_record = form.save(commit=False)
            medical_record.patient = patient
            medical_record.doctor = request.user.doctor_profile  
            medical_record.save()
            return redirect('doctor_appointment_list') 
    else:
        form = MedicalRecordForm()

    return render(request, 'medical_records/add_medical_history.html', {'form': form, 'patient': patient})


@login_required
def patient_medical_history(request, patient_id):
    patient = get_object_or_404(CustomUser, id=patient_id, user_type='patient')

    
    medical_records = MedicalRecord.objects.filter(patient=patient).order_by('-created_at')

    return render(request, 'medical_records/patient_medical_history.html', {
        'patient': patient,
        'medical_records': medical_records
    })

@method_decorator(login_required, name='dispatch')
class BillingListView(ListView):
    model = Billing
    template_name = 'billing/billing_list.html'
    context_object_name = 'billings'

    def get_queryset(self):
        return Billing.objects.filter(patient=self.request.user)


class HealthEducationResourceListView(ListView):
    model = HealthEducationResource
    template_name = 'education_resources/resource_list.html'
    context_object_name = 'resources'

class HealthEducationResourceCreateView(CreateView):
    model = HealthEducationResource
    form_class = HealthEducationResourceForm
    template_name = 'education_resources/add_health_resource.html'
    success_url = reverse_lazy('resource_list')


class FacilityListView(ListView):
    model = Facility
    template_name = 'facilities/facility_list.html'
    context_object_name = 'facilities'

class FacilityCreateView(CreateView):
    model = Facility
    form_class = FacilityForm
    template_name = 'facilities/facility_form.html'
    success_url = reverse_lazy('facility_list')


@method_decorator(login_required, name='dispatch')
class PrescriptionListView(ListView):
    model = Prescription
    template_name = 'prescriptions/prescription_list.html'
    context_object_name = 'prescriptions'

    def get_queryset(self):
        return Prescription.objects.filter(patient=self.request.user)


def check_appointment_status(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    return JsonResponse({"status": appointment.status})



@login_required
def prescribe_medicine(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

   
    if not hasattr(request.user, 'doctor_profile'):
        return redirect('error_page') 

    if request.method == "POST":
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.patient = appointment.patient 
            prescription.doctor = request.user.doctor_profile  
            prescription.save()
            return redirect("doctor_appointment_list")  
    else:
        form = PrescriptionForm()

    return render(request, "medical_records/prescribe_medicine.html", {"form": form, "appointment": appointment})




@login_required
def patient_prescriptions(request, patient_id):
    patient = get_object_or_404(CustomUser, id=patient_id, user_type='patient')

 
    prescriptions = Prescription.objects.filter(patient=patient).order_by('-created_at')

    return render(request, 'medical_records/patient_prescriptions.html', {
        'patient': patient,
        'prescriptions': prescriptions
    })

def Services(request):
    return render(request, 'services.html')

def Contact(request):
    return render(request, 'contact.html')

def About(request):
    return render(request, 'about.html')

# Logout View
def logout(request):
    auth_logout(request)
    return redirect('base')

@login_required
def register_patient(request):
    
    profile, created = PatientProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = PatientProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('patient_dashboard')  
    else:
        form = PatientProfileForm(instance=profile)

    return render(request, 'patient_register.html', {'form': form})


def admin_add_doctor(request):
    if request.method == 'POST':
        form = CustomUserSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'doctor'
            user.save()
            specialization = get_object_or_404(Specialization, id=request.POST.get('specialization'))
            DoctorProfile.objects.create(user=user, specialization=specialization)
            return redirect('admin_dashboard')
    else:
        form = CustomUserSignupForm()
    specializations = Specialization.objects.all()
    return render(request, 'add_doctor.html', {'form': form, 'specializations': specializations})

def admin_remove_doctor(request, doctor_id):
    doctor = get_object_or_404(DoctorProfile, id=doctor_id)
    if request.method == 'POST':
        doctor.user.delete()
        return redirect('admin_dashboard')
    return render(request, 'confirm_remove_doctor.html', {'doctor': doctor})

def manage_specializations(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Specialization.objects.create(name=name)
    specializations = Specialization.objects.all()
    return render(request, 'manage_specializations.html', {'specializations': specializations})

def delete_specialization(request, specialization_id):
    specialization = get_object_or_404(Specialization, id=specialization_id)
    if request.method == 'POST':
        specialization.delete()
        return redirect('manage_specializations')
    return render(request, 'confirm_delete_specialization.html', {'specialization': specialization})

def get_available_doctors(request):
    selected_date = request.GET.get('date')
    specialization_id = request.GET.get('specialization')

    if not selected_date:
        return JsonResponse({"error": "Date is required"}, status=400)

    try:
        selected_date_obj = datetime.strptime(selected_date, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({"error": "Invalid date format"}, status=400)

    day_of_week = selected_date_obj.strftime('%A')

    doctors = DoctorProfile.objects.all()
    if specialization_id:
        doctors = doctors.filter(specialization_id=specialization_id)

    available_doctors = []
    for doctor in doctors:
        if day_of_week in doctor.availability:
            has_conflicts = Appointment.objects.filter(
                doctor=doctor,
                date=selected_date_obj
            ).exists()
            if not has_conflicts:
                available_doctors.append({
                    "id": doctor.id,
                    "name": doctor.user.get_full_name(),
                    "specialization": doctor.specialization.name,
                    "availability": doctor.availability.get(day_of_week, "Not Available")
                })

    return JsonResponse({"available_doctors": available_doctors})


def success_page(request):
    return render(request, 'success.html')



def user_list(request):
    User = get_user_model() 
    users = User.objects.all() 
    return render(request, 'user_list.html', {'users': users})


class FacilityListView(ListView):
    model = Facility
    template_name = 'facilities/facility_list.html'
    context_object_name = 'facility_list'




def make_payment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            try:
               
                charge = stripe.Charge.create(
                    amount=int(amount * 100),  
                    currency="usd",
                    description=f"Payment for Appointment ID {appointment_id}",
                    source=request.POST['stripeToken']  
                )
                
                Payment.objects.create(
                    appointment=appointment,
                    amount=amount,
                    stripe_charge_id=charge['id'],
                )
                messages.success(request, "Payment successful!")
                return redirect('payment_success') 
            except stripe.error.StripeError as e:
                messages.error(request, f"Payment error: {str(e)}")
    else:
        form = PaymentForm()
    return render(request, 'payment.html', {
        'form': form,
        'appointment': appointment,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    })



def process_payment(request, appointment_id):
    if request.method == "POST":
        appointment = get_object_or_404(Appointment, id=appointment_id)
        data = json.loads(request.body)
        try:
            
            intent = stripe.PaymentIntent.create(
                amount=int(appointment.fee * 100),
                currency="usd",
                payment_method=data["payment_method_id"],
                confirm=True
            )
            return JsonResponse({"success": True})
        except stripe.error.StripeError as e:
            return JsonResponse({"success": False, "error": str(e)})



@login_required
def list_doctors(request):
    doctors = DoctorProfile.objects.all()
    return render(request, 'doctor_list.html', {'doctors': doctors})



def delete_doctor(request, doctor_id):
    if request.method == "POST":
        doctor = get_object_or_404(DoctorProfile, id=doctor_id)
        user = doctor.user
        doctor.delete() 
        user.delete() 
        messages.success(request, "Doctor profile deleted successfully.")
        return redirect('doctors')


def add_health_resource(request):
    if request.method == 'POST':
        form = HealthEducationResourceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Health education resource added successfully!')
            return redirect('add_health_resource')  
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = HealthEducationResourceForm()

    return render(request, 'add_health_resource.html', {'form': form})



@login_required
def facility_create(request):
    if request.method == 'POST':
        form = FacilityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('facilities/facility_form') 
    else:
        form = FacilityForm()
    facilities = Facility.objects.all()  
    return render(request, 'facilities/facility_list.html', { 'form': form, 'facilities': facilities})


def payment_success(request):
    return render(request, "payment_success.html")


def admin_patient_detail(request, patient_id): 
    patient = get_object_or_404(CustomUser, id=patient_id, user_type='patient')
    return render(request, "patient_detail.html", {"patient": patient})


def admin_patient_list(request):
    patients = CustomUser.objects.filter(user_type='patient')  # Fetch all patients
    return render(request, "patient_list.html", {"patients": patients})
