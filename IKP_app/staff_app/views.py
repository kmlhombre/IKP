from django.shortcuts import render

from general_app.models import *

# Create your views here.
def index(request):
    return render(request, 'staff-index.html', {'role': navbar_staff(request)})


# Helper functions
def navbar_staff(request):
    role = None
    if request.user.is_authenticated:
        logged_staff = HospitalStaff.objects.get(user=request.user.id)
        if logged_staff is not None:
            role = logged_staff.role.role_name
    return role
