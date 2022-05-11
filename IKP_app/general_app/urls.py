from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('main/', views.main, name='index'),
    path('login_user/', views.login_user, name='index'),
    path('check_password/', views.check_password, name='index'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_URL)
