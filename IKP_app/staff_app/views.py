import datetime
import hashlib
import http
import shutil

from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseForbidden, FileResponse, Http404, HttpResponseNotAllowed
from general_app.models import *
from patient_app.views import general_examination
from django.http import HttpResponseNotFound
from django.shortcuts import HttpResponseRedirect
from staff_app.forms import ExaminationsForm
from django.contrib.auth.models import User
from random import randrange

# Comment this
# from IKP_app.general_app.models import *
# from IKP_app.patient_app.views import general_examination

def create_account_2(request):
    pesel = request.POST.get('pesel','-1')
    name = request.POST.get('first_name','')
    last_name = request.POST.get('last_name','')
    second_name = request.POST.get('second_name','')
    gender = request.POST.get('gender','X')
    phone_number = request.POST.get('phone_number','')
    email = request.POST.get('email','')
    address_prefix = request.POST.get('address_prefix','Ul.')
    address = request.POST.get('address','')
    house_number = request.POST.get('house_number','')
    apartment_number = request.POST.get('apartment_number','')
    city = request.POST.get('city','')
    region = request.POST.get('region','')
    country = request.POST.get('country','')
    birth_date = request.POST.get('birth_date','')

    new_id = AuthUser.objects.order_by('-id').first().id +1
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    new_password = User.objects.make_random_password(length=8)
    new_password_hash = make_password(new_password)

    new_username = name[0:5]+last_name[0:3]+str(randrange(10000,99999))
    print('-----------------------------------'+region)
    u = AuthUser(
        id=new_id,
        password = new_password_hash,
        is_superuser = False,
        username = new_username,
        first_name = name,
        last_name = last_name,
        email = email,
        is_staff = False,
        is_active = True,
        date_joined = now,
        has_to_change_password = True,
        last_password_change = now,
        password_expires = now
    )
    u.save()

    gender_object = DGender.objects.get(gender=gender)
    prefix_object = DAddressPrefix.objects.get(prefix=address_prefix)
    region_object = DRegion.objects.get(region=region)
    country_object = DCountry.objects.get(country=country)
    actual_staff_user = HospitalStaff.objects.get(user=request.user.id)

    p = Patients(
        pesel = pesel,
        user = u,
        second_name = second_name,
        gender = gender_object,
        phone_number = phone_number,
        address_prefix = prefix_object,
        address = address,
        house_number = house_number,
        apartment_number = apartment_number,
        city = city,
        region = region_object,
        country = country_object,
        birthdate = birth_date,
        created_at = now,
        created_by = actual_staff_user
    )

    p.save()
    return render(request,'staff-create-account2.html',
                  {'username' : new_username,
                   'password' : new_password
                   })

def create_account(request):
    genders = DGender.objects.filter()
    address_prefix = DAddressPrefix.objects.filter()
    region = DRegion.objects.filter()
    country = DCountry.objects.filter()

    return render(request, 'staff-create-account.html',
                  {'role': navbar_staff(request),
                   'gender': genders,
                   'prefix' : address_prefix,
                   'region' : region,
                   'country' : country

                   })

def staff_accept_single_appointment_2(request):
    app_id = request.POST.get("appointment_id")

    date = request.POST.get("app_date")
    time = request.POST.get("app_hour")
    doctor = request.POST.get("doctor")
    room = request.POST.get("room")

    date_time_obj = datetime.datetime.strptime((str(date) + ' ' + str(time)), '%Y-%m-%d %H:%M')
    doctor_object = HospitalStaff.objects.get(id=doctor)
    room_object = Rooms.objects.get(room_name=room)

    app_object = Appointments.objects.get(id=app_id)
    app_object.appointment_date = date_time_obj
    app_object.doctor = doctor_object
    app_object.room = room_object

    current_user = AuthUser.objects.get(username=request.user)
    app_object.accepted_by = HospitalStaff.objects.get(user=current_user)
    app_object.accepted_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

    app_object.save(update_fields=['appointment_date', 'doctor', 'room', 'accepted_by', 'accepted_at'])
    return HttpResponseRedirect('/staff/registration/accept_appointments/accept_single_appointment')


def staff_delete_single_appointment_2(request):
    app_id = request.POST.get("appointment_id", "")
    Appointments.objects.get(id=app_id).delete()

    return HttpResponseRedirect('/staff/registration/accept_appointments/accept_single_appointment')


# Create your views here.
def index(request):
    return render(request, 'index-staff.html', {'role': navbar_staff(request)})


def accept_appointments(request):
    appointments = Appointments.objects.filter(accepted_by__isnull=True)
    booked_visits = []
    for x in appointments:
        booked_visits.append(Appointments.objects.filter(department=x.department, appointment_type=x.appointment_type,
                                                         appointment_date=x.suggested_date).count())
    appointments_left = len(appointments)

    return render(request, 'staff-accept-appointments.html', {'role': navbar_staff(request),'appointments': zip(appointments, booked_visits), 'appointments_left' : appointments_left})


def appointments_physician(request):
    appointments = None
    # Czy zalogowany
    authenticated, role_object, logged_staff = authenticate_staff(request, 'Lekarz')
    if not authenticated:
        return HttpResponseForbidden()
    else:
        logged_staff = logged_staff[0]
    date_today = datetime.date.today()
    appointments = Appointments.objects.filter(doctor=logged_staff, appointment_date__year=date_today.year,
                                               appointment_date__month=date_today.month,
                                               appointment_date__day=date_today.day)
    patient_list = [i.patient_pesel for i in appointments]
    patient_names = {}
    for i in patient_list:
        patient_names[i.pesel] = str(AuthUser.objects.get(id=i.user_id).first_name) + " " + str(
            AuthUser.objects.get(id=i.user_id).last_name)
    return render(request, 'appointments-physician.html',
                  {'appointments': appointments, 'role': navbar_staff(request), 'patient_names': patient_names})


def appointment_physician(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed()
    authenticated, _, _ = authenticate_staff(request, 'Lekarz')
    if not authenticated:
        return HttpResponseForbidden()
    appointment_id = request.POST.get('appointment_id')
    appointment = Appointments.objects.get(id=appointment_id)
    patient_name = str(AuthUser.objects.get(id=appointment.patient_pesel.user_id).first_name) + " " + \
                   str(AuthUser.objects.get(id=appointment.patient_pesel.user_id).last_name)

    if 'text' in request.POST:
        appointment_physician_update(appointment, request.POST.get('text'))

    request_uri = request.build_absolute_uri()
    file_path = request_uri + "/file?hash=" + str(appointment.referral).replace('referrals/', '')
    return render(request, 'appointment-physician.html',
                  {'role': navbar_staff(request), 'appointment': appointment, 'file_path': file_path,
                   'patient_name': patient_name})


def appointment_physician_file(request):
    appointment = None
    appointment_referral = request.GET.get('hash', '')
    authenticated, role_object, _ = authenticate_staff(request, 'Lekarz')
    if not authenticated:
        return HttpResponseForbidden()
    appointment = Appointments.objects.filter(
        referral='referrals/' + appointment_referral)
    appointment = appointment[0] if len(appointment) > 0 else None

    document_path = (settings.MEDIA_ROOT + "/" + str(appointment.referral)).replace('\\', '/')
    try:
        return FileResponse(open(document_path, 'rb'))
    except FileNotFoundError:
        raise Http404()


def patient_physician(request):
    authenticated, role_object, _ = authenticate_staff(request, 'Lekarz')
    if not authenticated:
        return HttpResponseForbidden()
    patient_pesel = request.POST.get('patient_pesel')
    patient = Patients.objects.get(pesel=patient_pesel)
    patient_first_name = str(AuthUser.objects.get(id=patient.user_id).first_name)
    patient_last_name = str(AuthUser.objects.get(id=patient.user_id).last_name)
    patient_email = str(AuthUser.objects.get(id=patient.user_id).email)
    examinations = Examinations.objects.filter(patient_pesel=patient)
    return render(request, 'patient-physician.html', {'role': navbar_staff(request), 'patient': patient,
                                                      'exams': examinations, 'first_name': patient_first_name,
                                                      'last_name': patient_last_name, 'email': patient_email})


def add_examination_physician(request):
    authenticated, role_object, _ = authenticate_staff(request, 'Lekarz')
    if not authenticated:
        return HttpResponseForbidden()
    patient_pesel = request.POST.get('patient_pesel')
    return render(request, 'add-examination-physician.html', {'role': navbar_staff(request), 'patient_pesel': patient_pesel})


def add_examination_process_physician(request):
    if request.method == 'POST':
        form = ExaminationsForm(request.POST, request.FILES)
        if form.is_valid() and request.user.is_authenticated:
            logged_staff = HospitalStaff.objects.get(user_id=request.user.id)
            auth_user = AuthUser.objects.get(id=request.user.id)
            description = request.POST.get('description')
            patient_pesel = request.POST.get('patient_pesel')
            patient = Patients.objects.get(pesel=patient_pesel)
            document_content = request.FILES['file']
            document_type = document_content.name.split('.')[-1].upper()
            document_content.name = hashlib.sha256(datetime.datetime.now().strftime(
                "%m/%d/%Y, %H:%M:%S").encode()).hexdigest() + '.' + document_type.lower()
            if logged_staff is not None:
                Examinations.objects.create(id=next_id(Examinations), patient_pesel=patient,
                                            document_content=document_content, document_type=document_type,
                                            description=description, accepted_by=logged_staff, accepted_at=datetime.datetime.now(),
                                            uploaded_at=datetime.datetime.now(), uploaded_by=auth_user)
    return patient_physician(request)


def examination_single_physician(request):
    examination = None
    request_uri = request.build_absolute_uri()
    authenticated, role_object, logged_staff = authenticate_staff(request, 'Lekarz')
    examination_id = request.POST.get("examination_id")
    if not authenticated:
        return HttpResponseForbidden()
    else:
        logged_staff = logged_staff[0]
    examination = Examinations.objects.get(id=examination_id)
    file_path = request_uri + "/file?hash=" + str(examination.document_content).replace('examinations/', '')
    return render(request, 'examination-physician.html',
                  {'exam': examination, 'file_path': file_path, 'role': navbar_staff(request)})


def appointments_registration(request):
    appointments = None
    authenticated, role_object, logged_staff = authenticate_staff(request, 'Rejestrator')
    if not authenticated:
        return HttpResponseForbidden()
    else:
        logged_staff = logged_staff[0]
    appointments = Appointments.objects.all()
    return render(request, 'appointments-registration.html',
                  {'appointments': appointments, 'role': navbar_staff(request)})


def appointment_accept(request):
    authenticated, role_object, logged_staff = authenticate_staff(request, 'Rejestrator')
    if not authenticated:
        return HttpResponseForbidden()
    else:
        logged_staff = logged_staff[0]
    appointment_id = request.POST.get('appointment_id')
    appointment = Appointments.objects.get(id=appointment_id)

    return render(request, 'appointment-accept.html', {'appointment': appointment, 'role': navbar_staff(request)})


def accept_single_appointment(request):
    unaccepted_appointments = Appointments.objects.filter(accepted_by__isnull=True).order_by('id')
    appointments_left = len(unaccepted_appointments)

    if len(unaccepted_appointments) == 0:
        return HttpResponseRedirect('/staff/registration/accept_appointments')

    unaccepted_appointment = None

    if request.POST.get('appointment_id'):
        unaccepted_appointment = Appointments.objects.get(id=request.POST.get('appointment_id'))
    else:
        unaccepted_appointment = unaccepted_appointments[0]

    request_uri = request.build_absolute_uri()
    file_path = ''
    appointments_that_day = Appointments.objects.filter(department=unaccepted_appointment.department,
                                                        appointment_type=unaccepted_appointment.appointment_type,
                                                        appointment_date=unaccepted_appointment.suggested_date).count()

    doctors = HospitalStaff.objects.filter(role='Lekarz')
    rooms = Rooms.objects.filter(department=unaccepted_appointment.department)

    # TODO bartek zrób żeby się wyświetlało skierownie
    # if unaccepted_appointment.referral is not None:
    #    file_path = request_uri + "/file?hash=" + unaccepted_appointment.referral.name.replace(
    #       'unaccepted_examinations/', '')
    return render(request, 'staff-accept-single-appointment.html',
                  {'appointment': unaccepted_appointment, 'file_path': file_path,
                   'appointments_left': appointments_left,
                   'appointments_that_day': appointments_that_day,
                   'doctors': doctors,
                   'rooms': rooms
                   })


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
        if(x.rejected_by is None):
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
        return render(request, 'unaccepted-examination-registration.html',
                      {'exam': examination, 'file_path': file_path})
    else:
        file_path = request_uri + "/file?hash=" + str(examination.document_content).replace('examinations/', '')
        return render(request, 'examination-registration.html',
                      {'exam': examination, 'file_path': file_path, 'role': navbar_staff(request)})


def examination_file(request):
    examination, examination_type = examination_helper(request, 'normal')
    document_path = (settings.MEDIA_ROOT + "/" + str(examination.document_content)).replace('\\', '/')
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


def analyze_single_examination(request):




    unaccepted_examinations = UnacceptedExaminations.objects.filter(rejected_for=None).order_by('id')
    examinations_left = len(unaccepted_examinations)
    unaccepted_examination = None

    if request.POST.get('examination_id'):
        unaccepted_examination = UnacceptedExaminations.objects.get(id=request.POST.get('examination_id'))
    else:
        unaccepted_examination = unaccepted_examinations[0]

    request_uri = request.build_absolute_uri()
    file_path = request_uri + "/file?hash=" + unaccepted_examination.document_content.name.replace(
        'unaccepted_examinations/', '')
    return render(request, 'staff-analyze-examinations.html',
                  {'examination': unaccepted_examination, 'file_path': file_path,
                   'examinations_left': examinations_left, 'role': navbar_staff(request)})


def discard_examination(request):
    examination_id = request.POST.get('examination_id')
    ex = UnacceptedExaminations.objects.get(id=examination_id)
    ex.rejected_for = request.POST.get('rejected_for', '')
    staff = HospitalStaff.objects.get(user=request.user.id)
    ex.rejected_by = staff
    ex.rejected_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    ex.save(update_fields=['rejected_for','rejected_at','rejected_by'])

    return HttpResponseRedirect('/staff/registration/examinations')


def accept_examination(request):

    if request.method != 'POST':
        return HttpResponseNotAllowed()
    authenticated, _, logged_staff = authenticate_staff(request, 'Rejestrator')
    if not authenticated:
        return HttpResponseForbidden()

    logged_staff_user = logged_staff[0].user.id
    examination_id = request.POST.get('examination_id')
    accept_examination_helper(examination_id, logged_staff_user)


    return HttpResponseRedirect('/staff/registration/examinations')


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
    authenticated_l, _, _ = authenticate_staff(request, 'Lekarz')
    if not authenticated:
        if not authenticated_l:
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


def appointment_physician_update(appointment, recommendations):
    appointment.recommendations = recommendations
    appointment.save()
