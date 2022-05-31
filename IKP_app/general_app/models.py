# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User

from general_app.validators import validate_file_size_10


class AppointmentNotifications(models.Model):
    id = models.IntegerField(primary_key=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=14, blank=True, null=True)
    notification_text = models.TextField()
    email_sent = models.BooleanField(blank=True, null=True)
    phone_number_sent = models.BooleanField(blank=True, null=True)
    appointment = models.ForeignKey('Appointments', models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'appointment_notifications'


class Appointments(models.Model):
    id = models.IntegerField(primary_key=True)
    patient_pesel = models.ForeignKey('Patients', models.DO_NOTHING, db_column='patient_pesel')
    appointment_date = models.DateTimeField(blank=True, null=True)
    department = models.ForeignKey('Departments', models.DO_NOTHING, db_column='department')
    room = models.ForeignKey('Rooms', models.DO_NOTHING, db_column='room', blank=True, null=True)
    doctor = models.ForeignKey('HospitalStaff', models.DO_NOTHING, db_column='doctor', blank=True, null=True)
    appointment_type = models.ForeignKey('DAppointmentType', models.DO_NOTHING, db_column='appointment_type')
    suggested_date = models.DateField()
    referral = models.BinaryField(blank=True, null=True)
    nfz = models.BooleanField()
    recommendations = models.TextField(blank=True, null=True)
    accepted_at = models.DateTimeField(blank=True, null=True)
    accepted_by = models.ForeignKey('HospitalStaff', models.DO_NOTHING, db_column='accepted_by', blank=True, null=True, related_name='accepted_HospitalStaff')
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)
    updated_by = models.ForeignKey('HospitalStaff', models.DO_NOTHING, db_column='updated_by', blank=True, null=True, related_name='updated_HospitalStaff')

    class Meta:
        managed = True
        db_table = 'appointments'


class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=25)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    has_to_change_password = models.BooleanField()
    last_password_change = models.DateTimeField()
    password_expires = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class CampaignNotifications(models.Model):
    id = models.IntegerField(primary_key=True)
    patient_pesel = models.ForeignKey('Patients', models.DO_NOTHING, db_column='patient_pesel')
    email = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=14, blank=True, null=True)
    notification_text = models.TextField()
    email_sent = models.BooleanField(blank=True, null=True)
    phone_number_sent = models.BooleanField(blank=True, null=True)
    campaign = models.ForeignKey('Campaigns', models.DO_NOTHING)

    class Meta:
        managed = True
        db_table = 'campaign_notifications'


class CampaignTypes(models.Model):
    camp_name = models.CharField(primary_key=True, max_length=20)

    class Meta:
        managed = True
        db_table = 'campaign_types'


class Campaigns(models.Model):
    id = models.IntegerField(primary_key=True)
    camp_name = models.ForeignKey(CampaignTypes, models.DO_NOTHING, db_column='camp_name', blank=True, null=True)
    age_from = models.IntegerField(blank=True, null=True)
    age_to = models.IntegerField(blank=True, null=True)
    gender = models.ForeignKey('DGender', models.DO_NOTHING, db_column='gender', blank=True, null=True)
    active_from = models.DateTimeField()
    active_to = models.DateTimeField()
    description = models.TextField()

    class Meta:
        managed = True
        db_table = 'campaigns'


class DAddressPrefix(models.Model):
    prefix = models.CharField(primary_key=True, max_length=3)

    class Meta:
        managed = True
        db_table = 'd_address_prefix'


class DAppointmentType(models.Model):
    appointment_type = models.CharField(primary_key=True, max_length=40)

    class Meta:
        managed = True
        db_table = 'd_appointment_type'


class DCountry(models.Model):
    country = models.CharField(primary_key=True, max_length=50)

    class Meta:
        managed = True
        db_table = 'd_country'


class DGender(models.Model):
    gender = models.CharField(primary_key=True, max_length=3)

    class Meta:
        managed = True
        db_table = 'd_gender'


class DRegion(models.Model):
    region = models.CharField(primary_key=True, max_length=30)

    class Meta:
        managed = True
        db_table = 'd_region'


class DStaffRole(models.Model):
    role_name = models.CharField(primary_key=True, max_length=25)

    class Meta:
        managed = True
        db_table = 'd_staff_role'


class DStaffTitle(models.Model):
    title = models.CharField(primary_key=True, max_length=25)

    class Meta:
        managed = True
        db_table = 'd_staff_title'


class Departments(models.Model):
    department = models.CharField(primary_key=True, max_length=100)

    class Meta:
        managed = True
        db_table = 'departments'


class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.IntegerField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Examinations(models.Model):
    id = models.IntegerField(primary_key=True)
    patient_pesel = models.ForeignKey('Patients', models.DO_NOTHING, db_column='patient_pesel')
    document_scan = models.TextField()
    document_type = models.TextField()
    uploaded_at = models.DateTimeField()
    uploaded_by = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='uploaded_by')
    accepted_at = models.DateTimeField()
    accepted_by = models.ForeignKey('HospitalStaff', models.DO_NOTHING, db_column='accepted_by', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'examinations'


class HospitalStaff(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    second_name = models.CharField(max_length=25, blank=True, null=True)
    role = models.ForeignKey(DStaffRole, models.DO_NOTHING, db_column='role')
    title = models.ForeignKey(DStaffTitle, models.DO_NOTHING, db_column='title', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'hospital_staff'


class PatientPermissionsModulePacjenci(models.Model):
    id_pacjent = models.IntegerField(primary_key=True)
    pesel = models.ForeignKey('Patients', models.DO_NOTHING, db_column='pesel', blank=True, null=True)
    imie = models.CharField(max_length=40)
    nazwisko = models.CharField(max_length=40)
    zrodlo = models.CharField(max_length=10, blank=True, null=True)
    wprowadzil = models.CharField(max_length=20, blank=True, null=True)
    data_wprow = models.DateField()
    zmodyfikowal = models.CharField(max_length=20, blank=True, null=True)
    data_akt = models.DateField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'patient_permissions_module_pacjenci'


class PatientPermissionsModuleZgody(models.Model):
    id_zgoda = models.IntegerField(primary_key=True)
    id_pacjent = models.ForeignKey(PatientPermissionsModulePacjenci, models.DO_NOTHING, db_column='id_pacjent', blank=True, null=True)
    rodzaj = models.CharField(max_length=20)
    wazna_od = models.DateField()
    wazna_do = models.DateField(blank=True, null=True)
    skan = models.BinaryField()
    wprowadzil = models.CharField(max_length=20)
    data_wprow = models.DateField()
    usunal = models.CharField(max_length=20, blank=True, null=True)
    data_usun = models.DateField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'patient_permissions_module_zgody'


class Patients(models.Model):
    pesel = models.CharField(primary_key=True, max_length=11)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    second_name = models.CharField(max_length=25, blank=True, null=True)
    gender = models.ForeignKey(DGender, models.DO_NOTHING, db_column='gender')
    phone_number = models.CharField(max_length=14, blank=True, null=True)
    address_prefix = models.ForeignKey(DAddressPrefix, models.DO_NOTHING, db_column='address_prefix', blank=True, null=True)
    address = models.CharField(max_length=35)
    house_number = models.CharField(max_length=5)
    apartment_number = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=60)
    region = models.ForeignKey(DRegion, models.DO_NOTHING, db_column='region')
    country = models.ForeignKey(DCountry, models.DO_NOTHING, db_column='country')
    birthdate = models.DateField()
    created_at = models.DateTimeField()
    created_by = models.ForeignKey(HospitalStaff, models.DO_NOTHING, db_column='created_by', related_name='created_HospitalStaff_patient')
    updated_at = models.DateTimeField(blank=True, null=True)
    updated_by = models.ForeignKey(HospitalStaff, models.DO_NOTHING, db_column='updated_by', blank=True, null=True, related_name='updated_HospitalStaff_patient')

    class Meta:
        managed = True
        db_table = 'patients'


class PatientsOld(models.Model):
    id = models.IntegerField(primary_key=True)
    pesel = models.CharField(max_length=11)
    first_name = models.CharField(max_length=25, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    second_name = models.CharField(max_length=25, blank=True, null=True)
    gender = models.ForeignKey(DGender, models.DO_NOTHING, db_column='gender', blank=True, null=True)
    phone_number = models.CharField(max_length=14, blank=True, null=True)
    address_prefix = models.ForeignKey(DAddressPrefix, models.DO_NOTHING, db_column='address_prefix', blank=True, null=True)
    address = models.CharField(max_length=35, blank=True, null=True)
    house_number = models.CharField(max_length=5, blank=True, null=True)
    apartment_number = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length=60, blank=True, null=True)
    region = models.ForeignKey(DRegion, models.DO_NOTHING, db_column='region', blank=True, null=True)
    country = models.ForeignKey(DCountry, models.DO_NOTHING, db_column='country', blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    modified_by = models.ForeignKey(HospitalStaff, models.DO_NOTHING, db_column='modified_by', blank=True, null=True)
    valid_from = models.DateTimeField(blank=True, null=True)
    valid_to = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'patients_old'
        unique_together = (('id', 'pesel'),)


class Rooms(models.Model):
    id = models.IntegerField(primary_key=True)
    department = models.ForeignKey(Departments, models.DO_NOTHING, db_column='department')
    room_name = models.CharField(max_length=50)
    floor_nr = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'rooms'


class Timetable(models.Model):
    id = models.IntegerField(primary_key=True)
    department = models.ForeignKey(Departments, models.DO_NOTHING, db_column='department')
    appointment_type = models.ForeignKey(DAppointmentType, models.DO_NOTHING, db_column='appointment_type')
    opening_time = models.DateTimeField()
    closing_time = models.DateTimeField()
    free_slots = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'timetable'


class UnacceptedExaminations(models.Model):
    id = models.IntegerField(primary_key=True)
    patient_pesel = models.ForeignKey(Patients, models.DO_NOTHING, db_column='patient_pesel')
    document_content = models.FileField(upload_to='unaccepted_examinations', validators=[validate_file_size_10])
    document_type = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    rejected_at = models.DateTimeField(blank=True, null=True)
    rejected_by = models.ForeignKey(HospitalStaff, models.DO_NOTHING, db_column='rejected_by', blank=True, null=True)
    rejected_for = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'unaccepted_examinations'
