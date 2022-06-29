from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index),
    path('physician/appointments/', views.appointments_physician),
    path('registration/appointments/', views.appointments_registration),
    path('registration/appointments/appointment-accept/', views.appointment_accept),
    path('registration/examinations/', views.examinations_registration),
    path('registration/examinations/examination', views.examination_single_registration),
    path('registration/examinations/unaccepted-examination', views.examination_single_registration),
    path('registration/examinations/examination/file', views.examination_file),
    path('registration/examinations/unaccepted-examination/file', views.unaccepted_examination_file),
    path('registration/examinations/examination-accept', views.examination_accept),
    path('registration/examinations/examination-reject', views.examination_reject),
    path('analyze_examinations', views.analyze_single_examination)
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_URL)
