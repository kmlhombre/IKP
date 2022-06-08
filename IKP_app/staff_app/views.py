import http

from django.shortcuts import render
from django.http import HttpResponseForbidden
from general_app.models import *
from patient_app.views import general_examination
# Comment this
# from IKP_app.general_app.models import *
# from IKP_app.patient_app.views import general_examination


# Create your views here.
def index(request):
    return render(request, 'index-staff.html', {'role': navbar_staff(request)})


def appointments_physician(request):
    appointments = None
    # Czy zalogowany
    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    role_object = DStaffRole.objects.get(role_name='Lekarz')
    logged_staff = HospitalStaff.objects.filter(user=request.user.id, role=role_object)
    if logged_staff is None:
        return HttpResponseForbidden()
    else:
        logged_staff = logged_staff[0]
    appointments = Appointments.objects.filter(doctor=logged_staff)
    return render(request, 'appointments.html', {'appointments': appointments, 'role': navbar_staff(request)})


def appointments_registration(request):
    appointments = None
    # Czy zalogowany
    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    role_object = DStaffRole.objects.get(role_name='Rejestrator')
    logged_staff = HospitalStaff.objects.filter(user=request.user.id, role=role_object)
    if logged_staff is None:
        return HttpResponseForbidden()
    else:
        logged_staff = logged_staff[0]
    appointments = Appointments.objects.all()
    return render(request, 'appointments.html', {'appointments': appointments, 'role': navbar_staff(request)})


def examinations_registration(request):
    examinations = None
    unaccepted_examinations = None
    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    role_object = DStaffRole.objects.get(role_name='Rejestrator')
    logged_staff = HospitalStaff.objects.filter(user=request.user.id, role=role_object)
    if logged_staff is None:
        return HttpResponseForbidden()
    else:
        logged_staff = logged_staff[0]
    examinations = Examinations.objects.all()
    unaccepted_examinations = UnacceptedExaminations.objects.all()

    all_examinations = []
    for x in examinations:
        all_examinations.append(general_examination(x))

    for x in unaccepted_examinations:
        all_examinations.append(general_examination(x))

    return render(request, 'examinations.html', {'exams': all_examinations, 'role': navbar_staff(request)})


def examination_single_registration(request):
    examination = None
    request_uri = request.build_absolute_uri()
    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    role_object = DStaffRole.objects.get(role_name='Rejestrator')
    logged_staff = HospitalStaff.objects.filter(user=request.user.id, role=role_object)
    examination_id = request.POST.get("examination_id")
    if logged_staff is None:
        return HttpResponseForbidden()
    else:
        logged_staff = logged_staff[0]
    if 'unaccepted-examination' in request_uri:
        examination = UnacceptedExaminations.objects.filter(id=examination_id)
    else:
        examination = Examinations.objects.filter(id=examination_id)
    examination = examination[0] if len(examination) > 0 else None
    if 'unaccepted-examination' in request_uri:
        file_path = request_uri + "/file?hash=" + examination.document_content.name.replace('unaccepted_examinations/',
                                                                                            '')
        return render(request, 'unaccepted-examination.html', {'exam': examination, 'file_path': file_path})
    else:
        file_path = request_uri + "/file?hash=" + examination.document_content.replace('examinations/', '')
        return render(request, 'examination.html',
                      {'exam': examination, 'file_path': file_path, 'role': navbar_staff(request)})


# Helper functions
def next_id(model):
    try:
        return int(model.objects.all().order_by("-id")[0].id) + 1
    except IndexError:
        return 0


def examination_helper(request, examination_type):
    examination = None
    examination_document = request.GET.get('hash', '')
    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    role_object = DStaffRole.objects.get(role_name='Rejestrator')
    if examination_type == 'normal':
        examination = Examinations.objects.filter(document_content='examinations/' + examination_document)
        examination = examination[0] if len(examination) > 0 else None
    else:
        examination = UnacceptedExaminations.objects.filter(
            document_content='unaccepted_examinations/' + examination_document)
        examination = examination[0] if len(examination) > 0 else None

    if examination.document_type == 'pdf':
        examination_type = 'application/pdf'
    elif examination.document_type == 'jpg':
        examination_type = 'image/jpg'
    else:
        examination_type = None
    return examination, examination_type


def navbar_staff(request):
    role = None
    if request.user.is_authenticated:
        logged_staff = HospitalStaff.objects.get(user=request.user.id)
        if logged_staff is not None:
            role = logged_staff.role.role_name
    return role
