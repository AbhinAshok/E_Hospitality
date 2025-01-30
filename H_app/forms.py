from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserSignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'user_type']

class CustomUserLoginForm(AuthenticationForm):
    pass

#---------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------

from django import forms
from .models import (
    Appointment, MedicalRecord, Billing,
    Facility, HealthEducationResource, Prescription, DoctorProfile, PatientProfile, Payment
)

from django.contrib.auth import get_user_model

# Appointment Form
class AppointmentForm(forms.ModelForm):
    patient_name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter patient name'}),
        label='Patient Name'
    )
    doctor = forms.ModelChoiceField(queryset=DoctorProfile.objects.all(), label="Select Doctor")

    class Meta:
        model = Appointment
        fields = ['patient_name', 'doctor', 'date', 'time', 'status']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        self.logged_in_user = kwargs.pop('logged_in_user', None)  # Accept logged-in user in constructor
        super().__init__(*args, **kwargs)
        if self.logged_in_user:
            self.fields['logged_in_user_name'] = forms.CharField(
                initial=self.logged_in_user.get_full_name(),  # Display logged-in user's name
                widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
                label='Logged-in User'
            )

# Medical Record Form
class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['diagnosis', 'treatment_plan', 'medications', 'allergies']
        widgets = {
            'diagnosis': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'treatment_plan': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'medications': forms.TextInput(attrs={'class': 'form-control'}),
            'allergies': forms.TextInput(attrs={'class': 'form-control'}),
        }

# Billing Form
class BillingForm(forms.ModelForm):
    class Meta:
        model = Billing
        fields = ['total_amount', 'payment_status', 'payment_date']
        widgets = {
            'payment_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


# payment form

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter payment amount'}),
        }


# E-Prescription Form

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['medication_name', 'dosage_instructions', 'medicines']
        widgets = {
            'medication_name': forms.TextInput(attrs={'class': 'form-control'}),
            'dosage_instructions': forms.Textarea(attrs={'class': 'form-control'}),
            'medicines': forms.Textarea(attrs={'class': 'form-control'}),
        }
# Facility Form
class FacilityForm(forms.ModelForm):
    class Meta:
        model = Facility
        fields = ['name', 'location', 'department', 'resources']
        widgets = {
            'resources': forms.Textarea(attrs={'rows': 3}),
        }

# Health Education Resource Form
class HealthEducationResourceForm(forms.ModelForm):
    class Meta:
        model = HealthEducationResource
        fields = ['title', 'description', 'link']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'link': forms.URLInput(attrs={'placeholder': 'https://example.com'}),
        }

class SelectDateForm(forms.Form):
    appointment_date = forms.DateField(widget=forms.SelectDateWidget)



User = get_user_model()

class DoctorProfileForm(forms.ModelForm):
    # Fields for user creation
    username = forms.CharField(
        max_length=150,
        required=True,
        label="Username",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}),
        required=True,
        label="Password"
    )
    name = forms.CharField(
        max_length=50,
        required=True,
        label="Name",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter name'})
    )
    email = forms.EmailField(
        required=True,
        label="Email Address",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'})
    )
    phone_no = forms.CharField(
        max_length=15,
        required=True,
        label="Phone No",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'})
    )

    class Meta:
        model = DoctorProfile
        fields = ['specialization', 'availability', 'phone']
        widgets = {
            'specialization': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter specialization'}),
            'availability': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter availability in JSON format',
                'rows': 5
            }),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
        }

    def __init__(self, *args, **kwargs):
        print(f"Initializing DoctorProfileForm with args: {args}, kwargs: {kwargs}")  # Debug statement
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        """
        Save both the user and doctor profile.
        """
        # Create the user first
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],  # Automatically hashed
            email=self.cleaned_data['email'],
        )

        # Create the doctor profile
        doctor_profile = super().save(commit=False)
        doctor_profile.user = user  # Associate the user with the doctor profile
        if commit:
            doctor_profile.save()
        return doctor_profile


# patient profile


class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = PatientProfile
        fields = ['name','age', 'phone', 'address', 'medications', 'medical_history', 'treatment_plans']
        widgets = {
            'name':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your age'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your address', 'rows': 3}),
            'medications': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'List any medications you are taking', 'rows': 3}),
            'medical_history': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Provide details of your medical history', 'rows': 3}),
            'treatment_plans': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Provide details of any treatment plans', 'rows': 3}),
        }

