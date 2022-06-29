from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index),
    path('registration/accept_appointments', views.accept_appointments),
    path('physician/appointments/', views.appointments_physician),
    path('physician/appointments/patient', views.patient_physician),
    path('physician/appointments/appointment', views.appointment_physician),
    path('physician/appointments/appointment/file', views.appointment_physician_file),
    path('registration/appointments/', views.appointments_registration),
    path('registration/accept_appointments/accept_single_appointment', views.accept_single_appointment),
    path('registration/appointments/appointment-accept/', views.appointment_accept),
    path('registration/accept_appointments/accept_single_appointment/staff_accept_single_appointment_2', views.staff_accept_single_appointment_2),
    path('registration/accept_appointments/accept_single_appointment/staff_delete_single_appointment_2', views.staff_delete_single_appointment_2),
    path('registration/examinations/', views.examinations_registration),
    path('registration/examinations/examination', views.examination_single_registration),
    path('registration/examinations/unaccepted-examination', views.examination_single_registration),
    path('registration/examinations/examination/file', views.examination_file),
    path('registration/examinations/unaccepted-examination/file', views.unaccepted_examination_file),
    path('registration/examinations/examination-accept', views.examination_accept),
    path('registration/examinations/examination-reject', views.examination_reject),
    path('analyze_examinations', views.analyze_single_examination)
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_URL)
