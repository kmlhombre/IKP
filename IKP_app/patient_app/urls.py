from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('examinations/examination', views.examination),
    path('examinations/', views.examinations),
    path('departments/', views.departments),
    path('appointments/', views.appointments),
    path('examination/<examination_id>', views.examination_single),
    path('examination/file/<examination_id>', views.examination_file)

] + static(settings.STATIC_URL, document_root=settings.STATIC_URL)
