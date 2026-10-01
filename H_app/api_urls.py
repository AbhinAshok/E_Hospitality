from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .api_views import (
    health_check, RegisterView, login_view, logout_view, me_view, dashboard_view,
    PatientProfileView, DoctorProfileView, AdminProfileView, DoctorViewSet,
    SpecializationViewSet, AppointmentViewSet, MedicalRecordViewSet, PrescriptionViewSet,
    BillingViewSet, HealthEducationResourceViewSet, FacilityViewSet, UserViewSet,
    PatientViewSet, DoctorAdminViewSet, AdminDashboardView
)

router = DefaultRouter()
router.register('doctors', DoctorViewSet, basename='doctors')
router.register('specializations', SpecializationViewSet, basename='specializations')
router.register('appointments', AppointmentViewSet, basename='appointments')
router.register('medical-records', MedicalRecordViewSet, basename='medical-records')
router.register('prescriptions', PrescriptionViewSet, basename='prescriptions')
router.register('billing', BillingViewSet, basename='billing')
router.register('resources', HealthEducationResourceViewSet, basename='resources')
router.register('facilities', FacilityViewSet, basename='facilities')
router.register('users', UserViewSet, basename='users')
router.register('patients', PatientViewSet, basename='patients')
router.register('admin/doctors', DoctorAdminViewSet, basename='admin-doctors')

urlpatterns = [
    path('health/', health_check),
    path('auth/register/', RegisterView.as_view()),
    path('auth/login/', login_view),
    path('auth/logout/', logout_view),
    path('auth/refresh/', TokenRefreshView.as_view()),
    path('auth/me/', me_view),
    path('dashboard/', dashboard_view),
    path('profile/patient/', PatientProfileView.as_view()),
    path('profile/doctor/', DoctorProfileView.as_view()),
    path('profile/admin/', AdminProfileView.as_view()),
    path('admin/dashboard/', AdminDashboardView.as_view()),
    path('', include(router.urls)),
]
