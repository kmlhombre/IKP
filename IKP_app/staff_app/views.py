import datetime
import http
import shutil

from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseForbidden, FileResponse, Http404, HttpResponseNotAllowed
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
    authenticated, role_object, logged_staff = authenticate_staff(request, 'Lekarz')
    examination_id = request.POST.get("examination_id")
    if not authenticated:
        return HttpResponseForbidden()
    else:
        logged_staff = logged_staff[0]
    appointments = Appointments.objects.filter(doctor=logged_staff)
    return render(request, 'appointments.html', {'appointments': appointments, 'role': navbar_staff(request)})


def appointments_registration(request):
    appointments = None
    authenticated, role_object, logged_staff = authenticate_staff(request, 'Rejestrator')
    if not authenticated:
        return HttpResponseForbidden()
    else:
        logged_staff = logged_staff[0]
    appointments = Appointments.objects.all()
    return render(request, 'appointments-registration.html', {'appointments': appointments, 'role': navbar_staff(request)})


def appointment_accept(request):
    authenticated, role_object, logged_staff = authenticate_staff(request, 'Rejestrator')
    if not authenticated:
        return HttpResponseForbidden()
    else:
        logged_staff = logged_staff[0]
    appointment_id = request.POST.get('appointment_id')
    appointment = Appointments.objects.get(id=appointment_id)

    return render(request, 'appointment-accept.html', {'appointment': appointment, 'role': navbar_staff(request)})


def examinations_registration(request):
    examinations = None
    unaccepted_examinations = None
    authenticated, role_object, logged_staff = authenticate_staff(request, 'Rejestrator')
    if not authenticated:
        return HttpResponseForbidden()
    else:
        logged_staff = logged_staff[0]
    examinations = Examinations.objects.all()
    unaccepted_examinations = UnacceptedExaminations.objects.all()

    all_examinations = []
    for x in unaccepted_examinations:
        all_examinations.append(general_examination(x))
    for x in examinations:
        all_examinations.append(general_examination(x))

    return render(request, 'examinations-registration.html', {'exams': all_examinations, 'role': navbar_staff(request)})


def examination_single_registration(request):
    examination = None
    request_uri = request.build_absolute_uri()
    authenticated, role_object, logged_staff = authenticate_staff(request, 'Rejestrator')
    examination_id = request.POST.get("examination_id")
    if not authenticated:
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
        return render(request, 'unaccepted-examination-registration.html', {'exam': examination, 'file_path': file_path})
    else:
        file_path = request_uri + "/file?hash=" + examination.document_content.replace('examinations/', '')
        return render(request, 'examination-registration.html',
                      {'exam': examination, 'file_path': file_path, 'role': navbar_staff(request)})


def examination_file(request):
    examination, examination_type = examination_helper(request, 'normal')
    document_path = (settings.MEDIA_ROOT + "/" + examination.document_content).replace('\\', '/')
    try:
        if examination_type is None:
            return FileResponse(open(document_path, 'rb'))
        return FileResponse(open(document_path, 'rb'), content_type=examination_type)
    except FileNotFoundError:
        raise Http404()


def unaccepted_examination_file(request):
    examination, examination_type = examination_helper(request, 'unaccepted')
    document_path = (settings.MEDIA_ROOT + "/" + examination.document_content.name).replace('\\', '/')
    print(document_path)
    try:
        if examination_type is None:
            return FileResponse(open(document_path, 'rb'))
        return FileResponse(open(document_path, 'rb'), content_type=examination_type)
    except FileNotFoundError:
        raise Http404()


def examination_accept(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed()
    authenticated, _, logged_staff = authenticate_staff(request, 'Rejestrator')
    if not authenticated:
        return HttpResponseForbidden()

    logged_staff_user = logged_staff[0].user.id
    examination_id = request.POST.get('examination_id')
    accept_examination_helper(examination_id, logged_staff_user)

    return examinations_registration(request)


def examination_reject(request):
    return render(request, 'examination-reject.html', {'role': navbar_staff(request)})


# Helper functions
def next_id(model):
    try:
        return int(model.objects.all().order_by("-id")[0].id) + 1
    except IndexError:
        return 0


def examination_helper(request, examination_type):
    examination = None
    examination_document = request.GET.get('hash', '')
    authenticated, role_object, _ = authenticate_staff(request, 'Rejestrator')
    if not authenticated:
        return HttpResponseForbidden()
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


def authenticate_staff(request, staff_role):
    if not request.user.is_authenticated:
        return False, None, None
    role_object = DStaffRole.objects.get(role_name=staff_role)
    logged_staff = HospitalStaff.objects.filter(user=request.user.id, role=role_object)
    if logged_staff is None:
        return False, None, None
    else:
        return True, role_object, logged_staff


def accept_examination_helper(examination_id, accepted_by_id):
    unaccepted_exam = UnacceptedExaminations.objects.get(id=examination_id)
    accepted_by = HospitalStaff.objects.get(id=accepted_by_id)
    uploaded_by = AuthUser.objects.get(id=unaccepted_exam.patient_pesel.user_id)
    new_name = str(unaccepted_exam.document_content).replace('unaccepted_', '', 1)
    # Tworzenie obiektu w tabeli examinations
    Examinations.objects.create(id=next_id(Examinations), patient_pesel=unaccepted_exam.patient_pesel,
                                document_content=new_name, document_type=unaccepted_exam.document_type,
                                uploaded_at=unaccepted_exam.uploaded_at, uploaded_by=uploaded_by,
                                accepted_at=datetime.datetime.now(), accepted_by=accepted_by)
    # Przenoszenie pliku
    old_path = (settings.MEDIA_ROOT + "/" + str(unaccepted_exam.document_content)).replace('\\', '/')
    new_path = (settings.MEDIA_ROOT + "/" + new_name).replace('\\', '/')
    shutil.move(old_path, new_path)
    # Usuwanie z tabeli unaccepted_examinations
    unaccepted_exam.delete()
