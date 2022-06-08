from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index),
    path('physician/appointments/', views.appointments_physician),
    path('registration/appointments/', views.appointments_registration),
    path('registration/examinations/', views.examinations_registration),
    path('registration/examinations/examination', views.examination_single_registration)

] + static(settings.STATIC_URL, document_root=settings.STATIC_URL)
