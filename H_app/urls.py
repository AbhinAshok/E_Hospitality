

from django.urls import path
from . import views
from .views import (
    PatientProfileView, DoctorProfileView, AppointmentCreateView, AppointmentListView,
    BillingListView,
    FacilityListView, FacilityCreateView, HealthEducationResourceListView,
    HealthEducationResourceCreateView, dashboard_redirect, check_appointment_status,
    Services, admin_add_doctor, admin_remove_doctor, manage_specializations, delete_specialization,
    Contact, About, logout, AppointmentDeleteView, payment_success, patient_medical_history, patient_prescriptions
)
from django.contrib.auth import views as auth_views
urlpatterns = [
    #home
    path('', views.home, name='base'),
    path('services/', Services, name='services'),
    path('contact/', Contact, name='contact'),
    path('about/', About, name='about'),
    path('logout/', logout, name='logout'),

    # signup and login
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='user_login'),
    path('patient_dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('doctor_dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # password reset
    
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),


    # Dashboard Redirect
    path('dashboard/', dashboard_redirect, name='dashboard'),

    # Profiles
    path('patient/profile/', PatientProfileView.as_view(), name='patient_profile'),
    path('doctor/profile/', DoctorProfileView.as_view(), name='doctor_profile'),
    path('register-doctor/', views.register_doctor, name='register_doctor'),

    path('user_list/', views.user_list, name='user_list'),
    path('doctors/', views.list_doctors, name='doctors_list'),
    path('doctors/delete/<int:doctor_id>/', views.delete_doctor, name='delete_doctor'),


    # Appointments


    path('appointments/', views.DoctorAppointmentListView.as_view(), name='appointment_list'),
    path('appointments/new/', views.AppointmentCreateView.as_view(), name='appointment_create'),
    path('appointments/confirm/<int:appointment_id>/', views.confirm_appointment, name='confirm_booking'),
    path('appointments/<int:pk>/delete/', AppointmentDeleteView.as_view(), name='appointment_delete'),
    path('appointmentlist/',views.AdminAppointmentListView.as_view(), name='admin_appointment_list'),


    # Doctor Views
    path('appointments/doctor/', views.DoctorAppointmentListView.as_view(), name='doctor_appointment_list'),

    path('patients/<int:patient_id>/medical-history/', views.add_medical_history, name='add_medical_history'),


    # Medical Records

    path('medical-history/<int:patient_id>/', patient_medical_history, name='patient_medical_history'),
    path('prescriptions/<int:patient_id>/', patient_prescriptions, name='patient_prescriptions'),

    # Billing
    path('billing/', BillingListView.as_view(), name='billing_list'),

    # E-Prescriptions

    path('prescribe/<int:appointment_id>/', views.prescribe_medicine, name='prescribe_medicine'),

    # Facilities
    path('facilities/', FacilityListView.as_view(), name='facility_list'),
    path('facilities/new/', FacilityCreateView.as_view(), name='facility_create'),


    # Health Education Resources
    path('resources/', HealthEducationResourceListView.as_view(), name='resource_list'),
    path('resources/new/', HealthEducationResourceCreateView.as_view(), name='resource_create'),

    # register profile

    path('register/patient/', views.register_patient, name='register_patient'),

    path('register/doctor/', DoctorProfileView.as_view(), name='register_doctor'),

    path('success/', views.success_page, name='success_page'),
    path('doctoradd/', views.admin_add_doctor, name='add_doctor'),

    # admin

    path('admin/add-doctor/', admin_add_doctor, name='admin_add_doctor'),
    path('admin/remove-doctor/<int:doctor_id>/', admin_remove_doctor, name='admin_remove_doctor'),
    path('admin/manage-specializations/', manage_specializations, name='manage_specializations'),
    path('admin/delete-specialization/<int:specialization_id>/', delete_specialization, name='delete_specialization'),
    path('admin/patients/<int:patient_id>/', views.admin_patient_detail, name='patient_detail'),
    path('admin/patients/', views.admin_patient_list, name='patient_list'),

    # payment

    # path('make_payment/<int:appointment_id>/', views.make_payment, name='make_payment'),
    # path('paymentprocess/<int:appointment_id>/',views.process_payment, name='process_payment'),
    # path("payment/success/", views.payment_success, name="payment_success"),

   
]


