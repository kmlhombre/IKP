import base64
import os
import datetime
import hashlib
import shutil

from django.db.models.base import ObjectDoesNotExist
from django.http import Http404, FileResponse
from django.shortcuts import render
from django.contrib.auth import logout
from django.conf import settings
from django.http import HttpResponseRedirect

from general_app.models import *
from patient_app.forms import UnacceptedExaminationsForm, AppointmentsForm
# Comment this
# from IKP_app.general_app.models import *



# Create your views here.
def add_appointment_process(request):
    form = AppointmentsForm(request.POST, request.FILES)
    if form.is_valid() and request.user.is_authenticated:
        appointment_type = request.POST.get('appointment_type')
        department = request.POST.get('department')
        suggested_date = request.POST.get('appointment_date')
        uploaded_referral = len(request.FILES) > 0
        if uploaded_referral:
            referral = base64.b64encode(request.FILES['file'].read())
        department_object = Departments.objects.get(department=department)
        appointment_type = DAppointmentType.objects.get(appointment_type=appointment_type)
        # Zmiana formatu daty na akceptowalną
        suggested_date = datetime.datetime.strptime(str(suggested_date).replace("a.m.", "AM").replace("p.m.", "PM"),
                                                    '%b %d, %Y, %I %p')

        logged_patient = Patients.objects.get(user=request.user.id)
        if logged_patient is not None:
            # TODO: sprawdzanie czy nfz
            if uploaded_referral:
                Appointments.objects.create(id=next_id(Appointments), patient_pesel=logged_patient,
                                            department=department_object, appointment_type=appointment_type,
                                            suggested_date=suggested_date, referral=referral, nfz=True)
            else:
                Appointments.objects.create(id=next_id(Appointments), patient_pesel=logged_patient,
                                            department=department_object, appointment_type=appointment_type,
                                            suggested_date=suggested_date, nfz=True)
    return HttpResponseRedirect('/patient/appointments')


def add_appointment_2(request):
    appointment_type = request.POST.get('appointment_type')
    department = request.POST.get('departments')

    timetable = Timetable.objects.filter(appointment_type=appointment_type, department=department)

    return render(request, 'add-appointment-2.html',
                  {'department': department, 'appointment_type': appointment_type, 'timetable': timetable})


def add_appointment(request):
    departments = Departments.objects.filter()
    appointment_types = DAppointmentType.objects.filter()
    return render(request, 'add-appointment.html.', {'departments': departments, 'types': appointment_types})


def add_examination_process(request):
    if request.method == 'POST':
        form = UnacceptedExaminationsForm(request.POST, request.FILES)
        if form.is_valid() and request.user.is_authenticated:
            logged_patient = Patients.objects.get(user=request.user.id)
            description = request.POST.get('description')
            document_scan = request.FILES['file']
            document_type = document_scan.name.split('.')[-1].upper()
            document_scan.name = hashlib.sha256(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S").encode()).hexdigest() + '.' + document_type.lower()
            if logged_patient is not None:
                UnacceptedExaminations.objects.create(id=next_id(UnacceptedExaminations), patient_pesel=logged_patient,
                                                      document_content=document_scan, document_type=document_type)
    return examinations(request)


def add_examination(request):
    return render(request, 'add-examination.html')


def logout_page(request):
    logout(request)
    return render(request, 'logout-success.html')


def index(request):
    return render(request, 'patient-index.html')

class general_examination:
    def __init__(self, orig=None):
        if orig is None:
            return
        if  isinstance(orig, Examinations) or isinstance(orig, UnacceptedExaminations):
            self.id = orig.id
            self.patient_pesel = orig.patient_pesel
            self.document_type = orig.document_type
            self.uploaded_at = orig.uploaded_at


            if isinstance(orig, Examinations):
                self.uploaded_by = orig.uploaded_by
                self.document_scan = orig.document_scan
                self.accepted = True
                self.accepted_at = orig.accepted_at
                self.accepted_by = orig.accepted_by
                return
            if isinstance(orig, UnacceptedExaminations):
                self.document_scan = orig.document_content
                self.rejected_at = orig.rejected_at
                self.rejected_by = orig.rejected_by
                self.rejected_for = orig.rejected_for
                return

    id = -1
    patient_pesel = ''
    document_scan = ''
    document_type = ''
    uploaded_at = models.DateTimeField()
    uploaded_by = -1
    accepted_at = models.DateTimeField()
    accepted_by = -1

    accepted = False
    rejected = False

    rejected_at = models.DateTimeField()
    rejected_by = -1
    rejected_for = 'Object instance not set correctly. Contact you administrator.'

def examinations(request):
    examinations = None
    unaccepted_examinations = None
    if request.user.is_authenticated:
        logged_patient = Patients.objects.get(user=request.user.id)
        if logged_patient is not None:
            # Pobranie z BD wyników, w których pesel odnosi się do zalogowanego pacjenta
            examinations = Examinations.objects.filter(patient_pesel=logged_patient)
            unaccepted_examinations = UnacceptedExaminations.objects.filter(patient_pesel=logged_patient)

            all_examinations = []
            for x in examinations:
                all_examinations.append(general_examination(x))

            for x in unaccepted_examinations:
                all_examinations.append(general_examination(x))

    return render(request, 'examinations.html', {'exams': all_examinations})


def examination(request):
    try:
        if request.user.is_authenticated:
            # Obecnie zalogowany użytkownik, jeśli jest w tabeli 'patient'
            logged_patient = Patients.objects.get(user=request.user.id)
            if logged_patient is not None:
                # Pobranie z BD wyników, w których pesel odnosi się do zalogowanego pacjenta
                examinations = Examinations.objects.filter(patient_pesel=logged_patient)
    except ObjectDoesNotExist:
        # TODO handle error
        print("Logged user not in 'Patient' table")
    return render(request, 'examinations.html', {'exams': examinations})


# Wyświetlanie informacji o istniejących oddziałach
def departments(request):
    # Pobranie z BD wszystkich oddziałów
    departments = Departments.objects.all()
    # Zwraca stronę html z oddziałami
    return render(request, 'departments.html', {'departments': departments})


def appointments(request):
    appointments = None
    # Czy zalogowany
    try:
        if request.user.is_authenticated:
            # Obecnie zalogowany użytkownik, jeśli jest w tabeli 'patient'
            logged_patient = Patients.objects.get(user=request.user.id)
            if logged_patient is not None:
                # Pobranie z BD wyników, w których pesel odnosi się do zalogowanego pacjenta
                appointments = Appointments.objects.filter(patient_pesel=logged_patient)
    except ObjectDoesNotExist:
        # TODO handle error
        print("Logged user not in 'Patient' table")
    return render(request, 'appointments.html', {'appointments': appointments})


def examination_single(request):
    examination = None
    request_uri = request.build_absolute_uri()
    # Czy zalogowany
    try:
        if request.user.is_authenticated:
            # Obecnie zalogowany użytkownik, jeśli jest w tabeli 'patient'
            examination_id = request.POST.get("examination_id")
            logged_patient = Patients.objects.get(user=request.user.id)
            if 'unaccepted-examination' in request_uri:
                examination = UnacceptedExaminations.objects.filter(id=examination_id).filter(patient_pesel=logged_patient)
            else:
                examination = Examinations.objects.filter(id=examination_id).filter(patient_pesel=logged_patient)
            examination = examination[0] if len(examination) > 0 else None
    except ObjectDoesNotExist:
        # TODO handle error
        print("Logged user not in 'Patient' table")
    if 'unaccepted-examination' in request_uri:
        file_path = request_uri + "/file?hash=" + examination.document_content.name.replace('unaccepted_examinations/', '')
        return render(request, 'unaccepted-examination.html', {'exam': examination, 'file_path': file_path})
    else:
        file_path = request_uri + "/file?hash=" + examination.document_scan.replace('examinations/', '')
        return render(request, 'examination.html', {'exam': examination, 'file_path': file_path})


def examination_file(request):
    examination, examination_type = examination_helper(request, 'normal')
    document_path = (settings.MEDIA_ROOT + "/" + examination.document_scan).replace('\\', '/')
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


# Helper functions
def next_id(model):
    try:
        return int(model.objects.all().order_by("-id")[0].id) + 1
    except IndexError:
        return 0


def examination_helper(request, type):
    examination = None
    examination_document = request.GET.get('hash', '')
    # Czy zalogowany
    try:
        if request.user.is_authenticated:
            # Obecnie zalogowany użytkownik, jeśli jest w tabeli 'patient'
            logged_patient = Patients.objects.get(user=request.user.id)
            if type == 'normal':
                examination = Examinations.objects.filter(document_scan='examinations/' + examination_document) \
                    .filter(patient_pesel=logged_patient)
                examination = examination[0] if len(examination) > 0 else None
            else:
                examination = UnacceptedExaminations.objects.filter(document_content='unaccepted_examinations/' + examination_document) \
                    .filter(patient_pesel=logged_patient)
                examination = examination[0] if len(examination) > 0 else None
    except ObjectDoesNotExist:
        # TODO handle error
        print("Logged user not in 'Patient' table")
    if examination.document_type == 'pdf':
        examination_type = 'application/pdf'
    elif examination.document_type == 'jpg':
        examination_type = 'image/jpg'
    else:
        examination_type = None
    return examination, examination_type

def accept_examination_123(examination_id, accepted_by_id):
    unaccepted_exam = UnacceptedExaminations.objects.get(id=examination_id)
    accepted_by = HospitalStaff.objects.get(id=accepted_by_id)
    uploaded_by = AuthUser.objects.get(id=unaccepted_exam.patient_pesel.user_id)
    new_name = str(unaccepted_exam.document_content).replace('unaccepted_', '', 1)
    # Tworzenie obiektu w tabeli examinations
    Examinations.objects.create(id=next_id(Examinations), patient_pesel=unaccepted_exam.patient_pesel,
                                document_scan=new_name, document_type=unaccepted_exam.document_type,
                                uploaded_at=unaccepted_exam.uploaded_at, uploaded_by=uploaded_by,
                                accepted_at=datetime.datetime.now(), accepted_by=accepted_by)
    # Przenoszenie pliku
    old_path = (settings.MEDIA_ROOT + "/" + str(unaccepted_exam.document_content)).replace('\\', '/')
    new_path = (settings.MEDIA_ROOT + "/" + new_name).replace('\\', '/')
    shutil.move(old_path, new_path)
    # Usuwanie z tabeli unaccepted_examinations
    unaccepted_exam.delete()