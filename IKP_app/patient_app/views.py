from django.db.models.base import ObjectDoesNotExist
from django.http import Http404, FileResponse
from django.shortcuts import render

from general_app.models import *


# Create your views here.
# Wyświetlanie informacji o wynikach dla obecnie zalogowanego pacjenta


def examinations(request):
    examinations = None
    if request.user.is_authenticated:
        logged_patient_id = Patient.objects.get(user=request.user.id)
        if logged_patient_id != None:
            # Pobranie z BD wyników, w których pesel odnosi się do zalogowanego pacjenta
            examinations = Examinations.objects.filter(patient_pesel=logged_patient_id)
    return render(request, 'examinations.html', {'exams': examinations})


def examination(request):
    '''if request.POST:
        examination_id = int(request.POST['examination_id'])
        if examination_id is None:
            return HttpResponseRedirect('/examinations/')

    examination = None
    if request.user.is_authenticated:
        logged_patient_id = Patient.objects.get(user=request.user.id).pesel
        if logged_patient_id is not None:
            # Pobranie z BD wyników, w których pesel odnosi się do zalogowanego pacjenta
            examinations = Examinations.objects.filter(patient_pesel=logged_patient_id, id=examination_id)'''
    # Czy zalogowany
    try:
        if request.user.is_authenticated:
            # Obecnie zalogowany użytkownik, jeśli jest w tabeli 'patient'
            logged_patient = Patient.objects.get(user=request.user.id)
            if logged_patient != None:
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
            logged_patient = Patient.objects.get(user=request.user)
            if logged_patient != None:
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
            logged_patient = Patient.objects.get(user=request.user.id)
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
            logged_patient = Patient.objects.get(user=request.user.id)
            examination = Examinations.objects.filter(document_scan=examination_document)\
                .filter(patient_pesel=logged_patient)
            examination = examination[0] if examination is not None else None
    except ObjectDoesNotExist:
        # TODO handle error
        print("Logged user not in 'Patient' table")
    try:
        if examination.document_type == 'pdf':
            examination_type = 'application/pdf'
        elif examination.document_type == 'jpg':
            examination_type = 'image/jpg'
        else:
            return FileResponse(open(examination.document_scan, 'rb'))
        return FileResponse(open(examination.document_scan, 'rb'), content_type=examination_type)
    except FileNotFoundError:
        raise Http404()
