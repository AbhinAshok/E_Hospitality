from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import (
    PatientProfile, DoctorProfile, Specialization, Appointment, MedicalRecord,
    Prescription, Billing, HealthEducationResource, Facility, AdminProfile, Payment
)

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'full_name', 'user_type']

    def get_full_name(self, obj):
        return obj.get_full_name() or obj.username


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True)
    user_type = serializers.ChoiceField(choices=[('patient', 'Patient'), ('doctor', 'Doctor')], default='patient')

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name', 'user_type']

    def validate(self, attrs):
        if attrs['password'] != attrs.pop('password2'):
            raise serializers.ValidationError({'password2': 'Passwords do not match.'})
        return attrs

    def create(self, validated_data):
        user_type = validated_data.pop('user_type', 'patient')
        password = validated_data.pop('password')
        user = User.objects.create_user(password=password, user_type=user_type, **validated_data)
        if user_type == 'patient':
            PatientProfile.objects.get_or_create(user=user)
        return user


class PatientProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = PatientProfile
        fields = ['id', 'user', 'name', 'age', 'phone', 'address', 'medications', 'medical_history', 'treatment_plans']


class DoctorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    specialization_name = serializers.CharField(source='specialization', read_only=True)

    class Meta:
        model = DoctorProfile
        fields = ['id', 'user', 'name', 'email', 'phone_no', 'phone', 'specialization', 'specialization_name', 'availability']


class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = ['id', 'name']


class DoctorCreateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, min_length=8)
    email = serializers.EmailField()
    name = serializers.CharField(max_length=100)
    phone = serializers.CharField(max_length=15, required=False, allow_blank=True)
    specialization = serializers.CharField(max_length=100, required=False, allow_blank=True)
    availability = serializers.CharField(max_length=100, required=False, allow_blank=True)

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(
            username=validated_data.pop('username'),
            email=validated_data.pop('email'),
            password=password,
            user_type='doctor',
        )
        return DoctorProfile.objects.create(user=user, **validated_data)


class AppointmentSerializer(serializers.ModelSerializer):
    patient = UserSerializer(read_only=True)
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    doctor_username = serializers.CharField(source='doctor.user.username', read_only=True)
    specialization = serializers.CharField(source='doctor.specialization', read_only=True)

    class Meta:
        model = Appointment
        fields = [
            'id', 'patient', 'doctor', 'doctor_name', 'doctor_username', 'specialization',
            'date', 'time', 'status', 'appointment_notes', 'duration_minutes',
            'is_virtual', 'location', 'fee', 'payment_status'
        ]
        read_only_fields = ['patient', 'fee', 'payment_status']

    def validate(self, attrs):
        doctor = attrs.get('doctor')
        date = attrs.get('date')
        if doctor and date and Appointment.objects.filter(doctor=doctor, date=date).exclude(
            status='Canceled'
        ).exists():
            raise serializers.ValidationError({'date': 'This doctor already has an appointment on this date.'})
        return attrs


class MedicalRecordSerializer(serializers.ModelSerializer):
    patient = UserSerializer(read_only=True)
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)

    class Meta:
        model = MedicalRecord
        fields = ['id', 'patient', 'doctor', 'doctor_name', 'diagnosis', 'treatment_plan', 'medications', 'allergies', 'created_at']
        read_only_fields = ['patient', 'doctor', 'created_at']


class PrescriptionSerializer(serializers.ModelSerializer):
    patient = UserSerializer(read_only=True)
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)

    class Meta:
        model = Prescription
        fields = ['id', 'patient', 'doctor', 'doctor_name', 'medication_name', 'dosage_instructions', 'medicines', 'created_at']
        read_only_fields = ['patient', 'doctor', 'created_at']


class BillingSerializer(serializers.ModelSerializer):
    patient = UserSerializer(read_only=True)

    class Meta:
        model = Billing
        fields = ['id', 'patient', 'total_amount', 'payment_status', 'date_issued', 'payment_date']
        read_only_fields = ['patient', 'date_issued']


class HealthEducationResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthEducationResource
        fields = ['id', 'title', 'description', 'link']


class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = ['id', 'name', 'location', 'department', 'resources', 'resource_quantity', 'resource_available']


class AdminProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = AdminProfile
        fields = ['id', 'user', 'department', 'name', 'position', 'employee_id', 'profile_picture', 'address', 'state', 'postal_code', 'country', 'is_approved']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'appointment', 'amount', 'stripe_charge_id', 'timestamp']
        read_only_fields = ['stripe_charge_id', 'timestamp']
