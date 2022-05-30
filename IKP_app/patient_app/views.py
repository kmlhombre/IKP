import base64
import os
import datetime
import hashlib

from django.db.models.base import ObjectDoesNotExist
from django.http import Http404, FileResponse
from django.shortcuts import render
from django.contrib.auth import logout

from general_app.models import *
from patient_app.forms import UnacceptedExaminationsForm


# Create your views here.


def add_appointment_process(request):
    appointment_type = request.POST.get('appointment_type')
    department = request.POST.get('department')
    suggested_date = request.POST.get('appointment_date')
    uploaded_referral = len(request.FILES) > 0
    if uploaded_referral:
        referral = base64.b64encode(request.FILES['file'].read())
    department_object = Departments.objects.get(department=department)
    appointment_type = DAppointmentType.objects.get(appointment_type=appointment_type)
    suggested_date = datetime.datetime.strptime(str(suggested_date).replace("a.m.", "AM").replace("p.m.", "PM"),
                                                '%b %d, %Y, %I %p')

    if request.user.is_authenticated:
        logged_patient = Patients.objects.get(user=request.user.id)
        if logged_patient is not None:
            # TODO: sprawdzanie czy nfz
            if uploaded_referral:
                Appointments.objects.create(id=next_id(Appointments), patient_pesel=logged_patient,
                                            department=department_object, appointment_type=appointment_type,
                                            suggested_date=suggested_date, referral=referral, nfz=True)
            else:
                Appointments.objects.create(id=next_id(Appointments), patient_pesel=logged_patient, department=department_object,
                                            appointment_type=appointment_type, suggested_date=suggested_date, nfz=True)
    return appointments(request)


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


def examinations(request):
    examinations = None
    if request.user.is_authenticated:
        logged_patient = Patients.objects.get(user=request.user.id)
        if logged_patient is not None:
            # Pobranie z BD wyników, w których pesel odnosi się do zalogowanego pacjenta
            examinations = Examinations.objects.filter(patient_pesel=logged_patient)
    return render(request, 'examinations.html', {'exams': examinations})


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
    # Czy zalogowany
    try:
        if request.user.is_authenticated:
            # Obecnie zalogowany użytkownik, jeśli jest w tabeli 'patient'
            examination_id = request.POST.get("examination_id")
            logged_patient = Patients.objects.get(user=request.user.id)
            examination = Examinations.objects.filter(id=examination_id).filter(patient_pesel=logged_patient)
            examination = examination[0] if examination is not None else None
    except ObjectDoesNotExist:
        # TODO handle error
        print("Logged user not in 'Patient' table")
    pdf_path = request.build_absolute_uri() + "/file?hash=" + examination.document_scan
    print(pdf_path, '\n')
    return render(request, 'examination.html', {'exam': examination, 'pdf_path': pdf_path})


def examination_file(request):
    examination = None
    examination_document = request.GET.get('hash', '')
    # Czy zalogowany
    try:
        if request.user.is_authenticated:
            # Obecnie zalogowany użytkownik, jeśli jest w tabeli 'patient'
            logged_patient = Patients.objects.get(user=request.user.id)
            examination = Examinations.objects.filter(document_scan=examination_document) \
                .filter(patient_pesel=logged_patient)
            examination = examination[0] if examination is not None else None
    except ObjectDoesNotExist:
        # TODO handle error
        print("Logged user not in 'Patient' table")
    PROJECT_PATH = os.path.abspath(os.path.dirname(__name__))
    document_path = (PROJECT_PATH + '/media/examinations/' + examination.document_scan).replace('\\', '/')
    print("\n\n", document_path, "\n\n")
    try:
        if examination.document_type == 'pdf':
            examination_type = 'application/pdf'
        elif examination.document_type == 'jpg':
            examination_type = 'image/jpg'
        else:
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
