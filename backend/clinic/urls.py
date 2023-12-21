from django.contrib import admin
from django.urls import path, include
from .views import (
    Register,
    Login,
    DoctorAppointmentView,
    AppointmentDetailView,
    DoctorListView,
    AvailableAppointments,
    ApplyAppointments
)

urlpatterns = [
    path('register/', Register.as_view()),
    path('login/', Login.as_view()),
    path('doctor/appointment/', DoctorAppointmentView.as_view()),
    path('doctor/appointment/<int:pk>', AppointmentDetailView.as_view()),
    path('patient/doctor/',DoctorListView.as_view()),
    path('patient/appointments/<int:pk>/available', AvailableAppointments.as_view()),
    path('patient/appointments/<int:pk>', ApplyAppointments.as_view()),
]
