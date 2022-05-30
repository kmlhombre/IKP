from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index),
    path('logout', views.logout_page),
    path('examinations/examination', views.examination_single),
    path('examinations/', views.examinations),
    path('departments/', views.departments),
    path('appointments/', views.appointments),
    path('appointments/add-appointment', views.add_appointment),
    path('appointments/add-appointment-2', views.add_appointment_2),
    path('appointments/add-appointment-3', views.add_appointment_process),
    path('examinations/add-examination', views.add_examination),
    path('examinations/add-examination-process', views.add_examination_process),
    path('examinations/examination/file', views.examination_file)

] + static(settings.STATIC_URL, document_root=settings.STATIC_URL)
