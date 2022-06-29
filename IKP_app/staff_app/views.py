from django.shortcuts import render

from general_app.models import *

# Create your views here.
def index(request):
    return render(request, 'staff-index.html', {'role': navbar_staff(request)})

def analyze_single_examination(request):
    unaccepted_examinations = UnacceptedExaminations.objects.filter().order_by('id')
    examinations_left = len(unaccepted_examinations)-1
    unaccepted_examination = unaccepted_examinations[0]
    #patient_pesel = unaccepted_examination.patient_pesel

    #next_id = UnacceptedExaminations.objects.order_by('-id').first().id + 1

    request_uri = request.build_absolute_uri()
    file_path = request_uri + "/file?hash=" + unaccepted_examination.document_content.name.replace('unaccepted_examinations/', '')
    return render(request, 'staff-analyze-examinations.html', {'examination': unaccepted_examination, 'file_path' : file_path, 'examinations_left' : examinations_left})


def discard_examination(request):
    pass

def accept_examination():
    pass

# Helper functions
def navbar_staff(request):
    role = None
    if request.user.is_authenticated:
        logged_staff = HospitalStaff.objects.get(user=request.user.id)
        if logged_staff is not None:
            role = logged_staff.role.role_name
    return role
