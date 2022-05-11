from django.shortcuts import render

from general_app.models import *


# Create your views here.
# Wyświetlanie informacji o wynikach dla obecnie zalogowanego pacjenta
def examinations(request):

    examinations = None
    if request.user.is_authenticated:
        logged_patient = Patient.objects.get(user=request.user.id)
        if logged_patient != None:
            examinations = Examinations.objects.filter(patient_pesel=logged_patient)    # Pobranie z BD wyników, w których pesel odnosi się do zalogowanego pacjenta
    return render(request, 'examinations.html', {'exams': examinations})

# Wyświetlanie informacji o istniejących oddziałach
def departments(request):
    departments = Departments.objects.all()                                             # Pobranie z BD wszystkich oddziałów
    return render(request, 'departments.html', {'departments': departments})            # Zwraca stronę html z oddziałami

def appointments(request):
    appointments = None
    if request.user.is_authenticated:                                                   # Czy zalogowany
        logged_patient = Patient.objects.get(user=request.user)                         # Obecnie zalogowany użytkownik, jeśli jest w tabeli 'patient'
        if logged_patient != None:
            appointments = Appointments.objects.filter(patient_pesel=logged_patient)    # Pobranie z BD wyników, w których pesel odnosi się do zalogowanego pacjenta
    return render(request, 'appointments.html', {'appointments': appointments})
