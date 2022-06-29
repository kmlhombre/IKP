from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index),
    path('analyze_examinations', views.analyze_single_examination)

] + static(settings.STATIC_URL, document_root=settings.STATIC_URL)
