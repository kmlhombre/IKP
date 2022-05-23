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
    #path('examination/<examination_id>', views.examination_single),
    path('examination/file/<examination_id>', views.examination_file),
    path('examinations/add-examination', views.add_examination),
    path('examinations/add-examination/add-examination-process', views.add_examination_process),
    path('examinations/examination/file', views.examination_file)

] + static(settings.STATIC_URL, document_root=settings.STATIC_URL)
