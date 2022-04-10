# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Appointments(models.Model):
    patient_pesel = models.ForeignKey('Patient', models.DO_NOTHING, db_column='patient_pesel')
    appointment_date = models.DateTimeField()
    department = models.ForeignKey('Departments', models.DO_NOTHING)
    room = models.ForeignKey('Rooms', models.DO_NOTHING, blank=True, null=True)
    doctor = models.ForeignKey('HospitalStaff', models.DO_NOTHING, related_name='doctor_HospitalStaff')
    appointment_type = models.ForeignKey('DAppointmentType', models.DO_NOTHING, db_column='appointment_type')
    required_at = models.DateTimeField()
    referral = models.BinaryField(blank=True, null=True)
    nfz = models.BooleanField()
    recommendations = models.TextField(blank=True, null=True)
    accepted_at = models.DateTimeField(blank=True, null=True)
    accepted_by = models.ForeignKey('HospitalStaff', models.DO_NOTHING, db_column='accepted_by', blank=True, null=True, related_name='accepted_HospitalStaff')
    updated_at = models.DateTimeField(blank=True, null=True)
    updated_by = models.ForeignKey('HospitalStaff', models.DO_NOTHING, db_column='updated_by', blank=True, null=True, related_name='updated_HospitalStaff')

    class Meta:
        managed = False
        db_table = 'appointments'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Campaigns(models.Model):
    age_from = models.IntegerField(blank=True, null=True)
    age_to = models.IntegerField(blank=True, null=True)
    gender = models.ForeignKey('DGender', models.DO_NOTHING, db_column='gender', blank=True, null=True)
    active_from = models.DateTimeField()
    active_to = models.DateTimeField()
    description = models.CharField(max_length=1000)

    class Meta:
        managed = False
        db_table = 'campaigns'


class CampaingnsAgreement(models.Model):
    pesel = models.ForeignKey('Patient', models.DO_NOTHING, db_column='pesel', unique=True)
    agreement_on_email = models.BooleanField(blank=True, null=True)
    agreement_on_phone = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'campaingns_agreement'


class DAddressPrefix(models.Model):
    prefix = models.CharField(unique=True, max_length=6)

    class Meta:
        managed = False
        db_table = 'd_address_prefix'


class DAppointmentType(models.Model):
    appointment_type = models.TextField(unique=True)

    class Meta:
        managed = False
        db_table = 'd_appointment_type'


class DGender(models.Model):
    gender = models.TextField(unique=True)

    class Meta:
        managed = False
        db_table = 'd_gender'


class DStaffRole(models.Model):
    role_name = models.CharField(unique=True, max_length=20)

    class Meta:
        managed = False
        db_table = 'd_staff_role'


class DStaffTitle(models.Model):
    title = models.TextField(unique=True)

    class Meta:
        managed = False
        db_table = 'd_staff_title'


class Departments(models.Model):
    name = models.TextField()

    class Meta:
        managed = False
        db_table = 'departments'


class DjangoAdminLog(models.Model):
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
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
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
    patient_pesel = models.ForeignKey('Patient', models.DO_NOTHING, db_column='patient_pesel')
    document_url = models.TextField()
    document_type = models.TextField()
    uploaded_at = models.DateTimeField()
    uploaded_by = models.ForeignKey('HospitalStaff', models.DO_NOTHING, db_column='uploaded_by', blank=True, null=True, related_name='uploaded_HospitalStaff')
    accepted_at = models.DateTimeField()
    accepted_by = models.ForeignKey('HospitalStaff', models.DO_NOTHING, db_column='accepted_by')

    class Meta:
        managed = False
        db_table = 'examinations'


class Notifications(models.Model):
    patient_pesel = models.ForeignKey('Patient', models.DO_NOTHING, db_column='patient_pesel')
    email = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=14, blank=True, null=True)
    expiration_date = models.DateTimeField()
    text = models.TextField(blank=True, null=True)
    sent_flag = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'notifications'


class HospitalStaff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.IntegerField(primary_key=True)
    second_name = models.CharField(max_length=50)
    role = models.ForeignKey(DStaffRole, models.DO_NOTHING, db_column='role')
    title = models.ForeignKey(DStaffTitle, models.DO_NOTHING, db_column='title', blank=True, null=True)
    last_password_change = models.DateTimeField(blank=True, null=True)
    has_to_change_password = models.BooleanField(blank=True, null=True)
    password_expires = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'hospital_staff'


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pesel = models.CharField(primary_key=True, max_length=11)
    second_name = models.CharField(max_length=50)
    gender = models.ForeignKey(DGender, models.DO_NOTHING, db_column='gender')
    phone_number = models.CharField(max_length=14)
    address_prefix = models.ForeignKey(DAddressPrefix, models.DO_NOTHING, db_column='address_prefix', blank=True, null=True)
    address = models.CharField(max_length=25)
    house_number = models.IntegerField()
    house_number_supplement = models.CharField(max_length=5, blank=True, null=True)
    city = models.CharField(max_length=25)
    region = models.CharField(max_length=50)
    country = models.CharField(max_length=3)
    birthdate = models.DateField()
    created_at = models.DateTimeField()
    created_by = models.DateTimeField()
    updated_at = models.DateTimeField()
    updated_by = models.DateTimeField()
    last_password_change = models.DateTimeField(blank=True, null=True)
    has_to_change_password = models.BooleanField(blank=True, null=True)
    password_expires = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'patient'


class PatientOld(models.Model):
    pesel = models.ForeignKey(Patient, models.DO_NOTHING, db_column='pesel', blank=True, null=True)
    first_name = models.CharField(max_length=25, blank=True, null=True)
    last_name = models.CharField(max_length=25, blank=True, null=True)
    second_name = models.CharField(max_length=50, blank=True, null=True)
    gender = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=14, blank=True, null=True)
    address = models.CharField(max_length=25, blank=True, null=True)
    house_number = models.IntegerField(blank=True, null=True)
    house_number_supplement = models.CharField(max_length=5, blank=True, null=True)
    city = models.CharField(max_length=25, blank=True, null=True)
    region = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=3, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    modified_by = models.DateTimeField()
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'patient_old'


class Rooms(models.Model):
    department = models.ForeignKey(Departments, models.DO_NOTHING)
    room_name = models.TextField(blank=True, null=True)
    floor_nr = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rooms'


class Timetable(models.Model):
    department = models.ForeignKey(Departments, models.DO_NOTHING)
    appointment_type = models.ForeignKey(DAppointmentType, models.DO_NOTHING, db_column='appointment_type')
    opening_time = models.DateTimeField(blank=True, null=True)
    closing_time = models.DateTimeField(blank=True, null=True)
    free_slots = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'timetable'


class UnacceptedExaminations(models.Model):
    patient_pesel = models.ForeignKey(Patient, models.DO_NOTHING, db_column='patient_pesel')
    document_url = models.TextField()
    document_type = models.TextField()
    uploaded_at = models.DateTimeField()
    rejected_at = models.DateTimeField(blank=True, null=True)
    rejected_by = models.ForeignKey(HospitalStaff, models.DO_NOTHING, db_column='rejected_by', blank=True, null=True)
    rejected_for = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'unaccepted_examinations'
