from datetime import datetime
from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
import H_app.permissions as per
from django.conf import settings

from .models import (
    PatientProfile, DoctorProfile, Specialization, Appointment, MedicalRecord,
    Prescription, Billing, HealthEducationResource, Facility, AdminProfile
)
from .serializers import (
    UserSerializer, RegisterSerializer, PatientProfileSerializer, DoctorProfileSerializer,
    DoctorCreateSerializer, SpecializationSerializer, AppointmentSerializer,
    MedicalRecordSerializer, PrescriptionSerializer, BillingSerializer,
    HealthEducationResourceSerializer, FacilitySerializer, AdminProfileSerializer
)
from .permissions import IsAdminRole, IsDoctorRole, IsPatientRole, IsAdminOrReadOnly

User = get_user_model()


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    return Response({'status': 'ok', 'service': 'E-Hospitality API'})


class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    from django.contrib.auth import authenticate
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'detail': 'Invalid username or password.'}, status=status.HTTP_401_UNAUTHORIZED)
    refresh = RefreshToken.for_user(user)
    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'user': UserSerializer(user).data,
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    refresh = request.data.get('refresh')
    if refresh:
        try:
            RefreshToken(refresh).blacklist()
        except Exception:
            pass
    return Response({'detail': 'Logged out successfully.'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me_view(request):
    return Response(UserSerializer(request.user).data)


class PatientProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = PatientProfileSerializer
    permission_classes = [IsPatientRole]

    def get_object(self):
        profile, _ = PatientProfile.objects.get_or_create(user=self.request.user)
        return profile


class DoctorProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = DoctorProfileSerializer
    permission_classes = [IsDoctorRole]

    def get_object(self):
        profile, _ = DoctorProfile.objects.get_or_create(user=self.request.user)
        return profile


class AdminProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = AdminProfileSerializer
    permission_classes = [IsAdminRole]

    def get_object(self):
        profile, _ = AdminProfile.objects.get_or_create(
            user=self.request.user,
            defaults={'department': 'Administration', 'name': self.request.user.get_full_name() or self.request.user.username,
                      'employee_id': f'ADMIN-{self.request.user.id}'}
        )
        return profile


class DoctorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DoctorProfile.objects.select_related('user')
    serializer_class = DoctorProfileSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='available')
    def available(self, request):
        date_str = request.query_params.get('date')
        specialization = request.query_params.get('specialization')
        if not date_str:
            return Response({'detail': 'date is required.'}, status=400)
        try:
            selected = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return Response({'detail': 'Invalid date format. Use YYYY-MM-DD.'}, status=400)

        doctors = self.get_queryset()
        if specialization:
            doctors = doctors.filter(specialization=specialization)
        results = []
        for doctor in doctors:
            if doctor.availability and selected.strftime('%A').lower() in doctor.availability.lower():
                conflict = Appointment.objects.filter(
                    doctor=doctor, date=selected
                ).exclude(status='Canceled').exists()
                if not conflict:
                    results.append(DoctorProfileSerializer(doctor).data)
        return Response(results)


class SpecializationViewSet(viewsets.ModelViewSet):
    queryset = Specialization.objects.all().order_by('name')
    serializer_class = SpecializationSerializer
    permission_classes = [IsAdminOrReadOnly]


class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = Appointment.objects.all().order_by('-date', '-time')
        if user.user_type == 'patient':
            return qs.filter(patient=user)
        if user.user_type == 'doctor':
            doctor_profile = getattr(user, 'doctor_profile', None)
            return qs.filter(doctor=doctor_profile) if doctor_profile else qs.none()
        return qs  

    def perform_create(self, serializer):
        doctor = serializer.validated_data.get('doctor')
        fee = getattr(doctor, 'consultation_fee', 0) if doctor else 0
        serializer.save(patient=self.request.user, fee=fee)

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        appointment = self.get_object()
        if appointment.status == 'Confirmed':
            return Response({'status': 'error', 'message': 'Appointment is already confirmed.'}, status=400)
        if appointment.payment_status != 'Paid':
            return Response({
                'status': 'error',
                'message': 'Please complete payment before confirming this appointment.',
            }, status=400)
        appointment.status = 'Confirmed'
        appointment.save(update_fields=['status'])
        return Response({'status': 'success', 'message': 'Appointment confirmed successfully!'})

    @action(detail=True, methods=['get'], url_path='status')
    def check_status(self, request, pk=None):
        appointment = self.get_object()
        return Response({'status': appointment.status, 'payment_status': appointment.payment_status})

    @action(detail=True, methods=['post'])
    def pay(self, request, pk=None):
        """Charge the patient's card (Stripe token from the frontend) for this
        appointment's fee, record the Payment, and mark it Paid."""
        appointment = self.get_object()

        if appointment.payment_status == 'Paid':
            return Response({'detail': 'This appointment is already paid for.'}, status=400)

        stripe_token = request.data.get('stripe_token')
        if not stripe_token:
            return Response({'detail': 'stripe_token is required.'}, status=400)

        amount = appointment.fee or 0
        try:
            charge = stripe.Charge.create(
                amount=int(amount * 100),
                currency='usd',
                description=f"Payment for Appointment #{appointment.id}",
                source=stripe_token,
            )
        except stripe.error.StripeError as e:
            return Response({'error': str(e)}, status=400)

        Payment.objects.create(
            appointment=appointment,
            amount=amount,
            stripe_charge_id=charge['id'],
        )
        appointment.payment_status = 'Paid'
        appointment.save(update_fields=['payment_status'])

        Billing.objects.create(
            patient=appointment.patient,
            total_amount=amount,
            payment_status='Paid',
            payment_date=timezone.now(),
        )

        return Response(AppointmentSerializer(appointment).data)



class MedicalRecordViewSet(viewsets.ModelViewSet):
    serializer_class = MedicalRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = MedicalRecord.objects.select_related('patient', 'doctor', 'doctor__user').order_by('-created_at')
        if self.request.user.user_type == 'patient':
            return qs.filter(patient=self.request.user)
        if self.request.user.user_type == 'doctor':
            patient_id = self.request.query_params.get('patient')
            qs = qs.filter(doctor__user=self.request.user)
            return qs.filter(patient_id=patient_id) if patient_id else qs
        return qs

    def perform_create(self, serializer):
        if self.request.user.user_type != 'doctor':
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('Only doctors can create medical records.')
        patient_id = self.request.data.get('patient_id')
        patient = get_object_or_404(User, id=patient_id, user_type='patient')
        doctor = get_object_or_404(DoctorProfile, user=self.request.user)
        serializer.save(patient=patient, doctor=doctor)


class PrescriptionViewSet(viewsets.ModelViewSet):
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Prescription.objects.select_related('patient', 'doctor', 'doctor__user').order_by('-created_at')
        if self.request.user.user_type == 'patient':
            return qs.filter(patient=self.request.user)
        if self.request.user.user_type == 'doctor':
            patient_id = self.request.query_params.get('patient')
            qs = qs.filter(doctor__user=self.request.user)
            return qs.filter(patient_id=patient_id) if patient_id else qs
        return qs

    def perform_create(self, serializer):
        if self.request.user.user_type != 'doctor':
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('Only doctors can create prescriptions.')
        patient_id = self.request.data.get('patient_id')
        patient = get_object_or_404(User, id=patient_id, user_type='patient')
        doctor = get_object_or_404(DoctorProfile, user=self.request.user)
        serializer.save(patient=patient, doctor=doctor)


class BillingViewSet(viewsets.ModelViewSet):
    serializer_class = BillingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Billing.objects.select_related('patient').order_by('-date_issued')
        return qs.filter(patient=self.request.user) if self.request.user.user_type == 'patient' else qs

    def perform_create(self, serializer):
        if self.request.user.user_type != 'admin':
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('Only administrators can create billing records.')
        serializer.save(patient_id=self.request.data.get('patient_id'))


class HealthEducationResourceViewSet(viewsets.ModelViewSet):
    queryset = HealthEducationResource.objects.all().order_by('-id')
    serializer_class = HealthEducationResourceSerializer
    permission_classes = [IsAdminOrReadOnly]


class FacilityViewSet(viewsets.ModelViewSet):
    queryset = Facility.objects.all().order_by('name')
    serializer_class = FacilitySerializer
    permission_classes = [IsAdminOrReadOnly]


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAdminRole]

    def get_queryset(self):
        qs = super().get_queryset()
        user_type = self.request.query_params.get('user_type')
        return qs.filter(user_type=user_type) if user_type else qs


class PatientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.filter(user_type='patient').order_by('username')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.user_type == 'patient':
            return self.queryset.filter(id=self.request.user.id)
        return self.queryset


class DoctorAdminViewSet(viewsets.ModelViewSet):
    queryset = DoctorProfile.objects.select_related('user').all()
    permission_classes = [IsAdminRole]

    def get_serializer_class(self):
        return DoctorCreateSerializer if self.action == 'create' else DoctorProfileSerializer

    def destroy(self, request, *args, **kwargs):
        doctor = self.get_object()
        user = doctor.user
        doctor.delete()
        user.delete()
        return Response(status=204)


class AdminDashboardView(generics.GenericAPIView):
    permission_classes = [IsAdminRole]

    def get(self, request):
        return Response({
            'users': User.objects.count(),
            'patients': User.objects.filter(user_type='patient').count(),
            'doctors': User.objects.filter(user_type='doctor').count(),
            'appointments': Appointment.objects.count(),
            'pending_bills': Billing.objects.filter(payment_status='Pending').count(),
            'facilities': Facility.objects.count(),
            'resources': HealthEducationResource.objects.count(),
        })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_view(request):
    user = request.user
    if user.user_type == 'patient':
        return Response({
            'role': 'patient',
            'appointments': Appointment.objects.filter(patient=user).count(),
            'prescriptions': Prescription.objects.filter(patient=user).count(),
            'medical_records': MedicalRecord.objects.filter(patient=user).count(),
            'pending_bills': Billing.objects.filter(patient=user, payment_status='Pending').count(),
        })
    if user.user_type == 'doctor':
        return Response({
            'role': 'doctor',
            'appointments': Appointment.objects.filter(doctor__user=user).count(),
            'patients': Appointment.objects.filter(doctor__user=user).values('patient').distinct().count(),
            'prescriptions': Prescription.objects.filter(doctor__user=user).count(),
            'medical_records': MedicalRecord.objects.filter(doctor__user=user).count(),
        })
    return AdminDashboardView().get(request)
