CREATE DATABASE IF NOT EXISTS ikp_hcp;
USE ikp_hcp;

CREATE TABLE IF NOT EXISTS public.auth_group
(
    id int PRIMARY KEY,
    name varchar(150) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS public.django_content_type
(
    id int PRIMARY KEY,
    app_label varchar(100) NOT NULL,
    model varchar(100) NOT NULL,
    CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model)
);

CREATE TABLE IF NOT EXISTS public.auth_permission
(
    id int PRIMARY KEY,
    name varchar(255) NOT NULL,
    content_type_id int REFERENCES public.django_content_type(id),
    codename varchar(100) NOT NULL,
    UNIQUE (content_type_id, codename)
);

CREATE TABLE IF NOT EXISTS public.auth_group_permissions
(
    id int NOT NULL,
    group_id int NOT NULL,
    permission_id int NOT NULL,
    CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id),
    CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id),
    CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id)
        REFERENCES public.auth_permission (id),
    CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id)
        REFERENCES public.auth_group (id)
);

CREATE TABLE IF NOT EXISTS public.auth_user
(
    id int NOT NULL,
    password varchar(128) NOT NULL,
    last_login timestamp,
    is_superuser boolean NOT NULL,
    username varchar(25) NOT NULL,
    first_name varchar(25) NOT NULL,
    last_name varchar(30) NOT NULL,
    email varchar(50) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp NOT NULL,
	has_to_change_password boolean NOT NULL,
	last_password_change timestamp NOT NULL,
	password_expires timestamp NOT NULL,
    CONSTRAINT auth_user_pkey PRIMARY KEY (id),
    CONSTRAINT auth_user_username_key UNIQUE (username)
);

CREATE TABLE IF NOT EXISTS public.auth_user_groups
(
    id int NOT NULL,
    user_id int NOT NULL,
    group_id int NOT NULL,
    CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id),
    CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq UNIQUE (user_id, group_id),
    CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id)
        REFERENCES public.auth_group (id),
    CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id)
        REFERENCES public.auth_user (id)
);

CREATE TABLE IF NOT EXISTS public.auth_user_user_permissions
(
    id int NOT NULL,
    user_id int NOT NULL,
    permission_id int NOT NULL,
    CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id),
    CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq UNIQUE (user_id, permission_id),
    CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id)
        REFERENCES public.auth_permission (id),
    CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id)
        REFERENCES public.auth_user (id)
);

CREATE TABLE IF NOT EXISTS public.django_admin_log
(
    id int NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr varchar(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id int,
    user_id int NOT NULL,
    CONSTRAINT django_admin_log_pkey PRIMARY KEY (id),
    CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id)
        REFERENCES public.django_content_type (id),
    CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id)
        REFERENCES public.auth_user (id),
    CONSTRAINT django_admin_log_action_flag_check CHECK (action_flag >= 0)
);

CREATE TABLE IF NOT EXISTS public.django_migrations
(
    id int NOT NULL,
    app varchar(255) NOT NULL,
    name varchar(255) NOT NULL,
    applied timestamp with time zone NOT NULL,
    CONSTRAINT django_migrations_pkey PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.django_session
(
    session_key varchar(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL,
    CONSTRAINT django_session_pkey PRIMARY KEY (session_key)
);

CREATE TABLE IF NOT EXISTS public.d_address_prefix
(
	prefix varchar(3) primary key
);

CREATE TABLE IF NOT EXISTS public.d_appointment_type
(
	appointment_type varchar(40) primary key
);

CREATE TABLE IF NOT EXISTS public.d_gender
(
	gender varchar(3) primary key
);

CREATE TABLE IF NOT EXISTS public.d_staff_role
(
	role_name varchar(25) primary key
);

CREATE TABLE IF NOT EXISTS public.d_staff_title
(
	title varchar(25) primary key
);

CREATE TABLE IF NOT EXISTS public.d_region
(
	region varchar(30) primary key
);

CREATE TABLE IF NOT EXISTS public.d_country
(
	country varchar(50) primary key
);

CREATE TABLE IF NOT EXISTS public.departments
(
	department varchar(100) primary key
);

CREATE TABLE IF NOT EXISTS public.campaign_types
(
    camp_name varchar(20) PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS public.rooms
(
	id int primary key,
	department varchar(100) NOT NULL references public.departments(department),
	room_name varchar(50) NOT NULL,
	floor_nr int,
	description varchar(300)
);

CREATE TABLE IF NOT EXISTS public.timetable
(
	id int primary key,
	department varchar(100) NOT NULL references public.departments(department),
	appointment_type varchar(40) NOT NULL references public.d_appointment_type(appointment_type),
	opening_time timestamp NOT NULL,
	closing_time timestamp NOT NULL,
	free_slots int NOT NULL
);

CREATE TABLE IF NOT EXISTS public.hospital_staff
(
	id int primary key,
	user_id int NOT NULL references public.auth_user(id),
	second_name varchar(25),
	role varchar(25) NOT NULL references public.d_staff_role(role_name),
	title varchar(25) references public.d_staff_title(title)
);

CREATE TABLE IF NOT EXISTS public.patients
(
	pesel char(11) primary key,
	user_id int NOT NULL references public.auth_user(id),
	second_name varchar(25),
	gender varchar(3) NOT NULL references public.d_gender(gender),
	phone_number varchar(14),
	address_prefix varchar(3) references public.d_address_prefix(prefix),
	address varchar(35) NOT NULL,
	house_number varchar(5) NOT NULL,
	apartment_number varchar(10),
	city varchar(60) NOT NULL,
	region varchar(30) NOT NULL references public.d_region(region),
	country varchar(50) NOT NULL references public.d_country(country),
	birthdate date NOT NULL,
	created_at timestamp NOT NULL,
	created_by int NOT NULL references public.hospital_staff(id),
	updated_at timestamp,
	updated_by int references public.hospital_staff(id)
);


CREATE TABLE IF NOT EXISTS public.patients_old
(
	id int,
	pesel char(11),
	first_name varchar(25),
	last_name varchar(30),
	second_name varchar(25),
	gender varchar(3) references public.d_gender(gender),
	phone_number varchar(14),
	address_prefix varchar(3) references public.d_address_prefix(prefix),
	address varchar(35),
	house_number varchar(5),
	apartment_number varchar(10),
	city varchar(60),
	region varchar(30) references public.d_region(region),
	country varchar(50) references public.d_country(country),
	birthdate date,
	email varchar(50),
	modified_by int references public.hospital_staff(id),
	valid_from timestamp,
	valid_to timestamp,
	primary key(id, pesel)
);

CREATE TABLE IF NOT EXISTS public.examinations
(
	id int primary key,
	patient_pesel char(11) NOT NULL references public.patients(pesel),
	document_content text NOT NULL ,
	document_type text NOT NULL ,
	description varchar(50),
	uploaded_at timestamp NOT NULL ,
	uploaded_by int NOT NULL references public.auth_user(id),
	accepted_at timestamp NOT NULL ,
	accepted_by int NOT NULL references public.hospital_staff(id)
);

CREATE TABLE IF NOT EXISTS public.unaccepted_examinations
(
	id int primary key,
	patient_pesel char(11) NOT NULL references public.patients(pesel),
	document_content text NOT NULL ,
	document_type text NOT NULL ,
	description varchar(50),
	uploaded_at timestamp NOT NULL ,
	rejected_at timestamp,
	rejected_by int references public.hospital_staff(id),
	rejected_for varchar(300)
);

CREATE TABLE IF NOT EXISTS public.appointments 
(
	id int primary key,
	patient_pesel char(11) NOT NULL references public.patients(pesel),
	appointment_date timestamp,
	department varchar(100) NOT NULL references public.departments(department),
	room int references public.rooms(id),
	doctor int references public.hospital_staff(id),
	appointment_type varchar(40) NOT NULL references public.d_appointment_type(appointment_type),
	suggested_date date NOT NULL,
	referral text,
	nfz boolean NOT NULL,
	recommendations text,
	accepted_at timestamp,
	accepted_by int references public.hospital_staff(id),
	updated_at timestamp,
	updated_by int references public.hospital_staff(id)
);

CREATE TABLE IF NOT EXISTS public.appointment_notifications
(
	id int primary key,
	email varchar(50),
	phone_number varchar(14),
	notification_text text NOT NULL ,
	email_sent boolean default False,
	phone_number_sent boolean default False,
	appointment_id int NOT NULL references public.appointments(id)
);

CREATE TABLE IF NOT EXISTS public.campaigns
(
	id int primary key,
    camp_name varchar(20) references public.campaign_types(camp_name),
	age_from int,
	age_to int,
	gender varchar(3) references public.d_gender(gender),
	active_from timestamp NOT NULL ,
	active_to timestamp NOT NULL ,
	description text NOT NULL 
);

CREATE TABLE IF NOT EXISTS public.campaign_notifications
(
	id int primary key,
	patient_pesel char(11) NOT NULL references public.patients(pesel),
	email varchar(50),
	phone_number varchar(14),
	notification_text text NOT NULL ,
	email_sent boolean default False,
	phone_number_sent boolean default False,
	campaign_id int NOT NULL references public.campaigns(id)
);

CREATE TABLE IF NOT EXISTS public.patient_permissions_module_pacjenci
(
	id_pacjent   int primary key,
    pesel        char(11) references public.patients(pesel),
    imie         VARCHAR(40) NOT NULL,
    nazwisko     VARCHAR(40) NOT NULL,
    zrodlo       VARCHAR(10),
    wprowadzil   VARCHAR(20),
    data_wprow   DATE NOT NULL,
    zmodyfikowal VARCHAR(20),
    data_akt     DATE
);

CREATE TABLE IF NOT EXISTS public.patient_permissions_module_zgody (
    id_zgoda   int primary key not null,
    id_pacjent int references public.patient_permissions_module_pacjenci(id_pacjent),
    rodzaj     VARCHAR(20) NOT NULL,
    wazna_od   DATE NOT NULL,
    wazna_do   DATE,
    skan       bytea NOT NULL,
    wprowadzil VARCHAR(20) NOT NULL,
    data_wprow DATE NOT NULL,
    usunal     VARCHAR(20),
    data_usun  DATE
);

insert into public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, has_to_change_password, last_password_change, password_expires)
values
(0, 'pbkdf2_sha256$150000$wEmHEuRlIPeS$zGJVelYcvV7WRIVfWtuEMQ6mTBk+iiRv5wrd7LfWG2Y=', null, True, 'admin', 'Jan', 'Kowalski', 'jan_kowalski@ikp.pl', True, True, '2022-05-11 08:00', True, '2022-05-11 08:00', '2022-06-11 08:00'),
(1, 'pbkdf2_sha256$150000$wEmHEuRlIPeS$zGJVelYcvV7WRIVfWtuEMQ6mTBk+iiRv5wrd7LfWG2Y=', null, False, 'lekarz', 'Janina', 'Kowalska', 'janina_kowalska@ikp.pl', True, True, '2022-05-11 08:00', True, '2022-05-11 08:00', '2022-06-11 08:00'),
(2, 'pbkdf2_sha256$150000$wEmHEuRlIPeS$zGJVelYcvV7WRIVfWtuEMQ6mTBk+iiRv5wrd7LfWG2Y=', null, False, 'rejestrator', 'Janusz', 'Kowalski', 'janusz_kowalski@ikp.pl', True, True, '2022-05-11 08:00', True, '2022-05-11 08:00', '2022-06-11 08:00'),
(3, 'pbkdf2_sha256$150000$wEmHEuRlIPeS$zGJVelYcvV7WRIVfWtuEMQ6mTBk+iiRv5wrd7LfWG2Y=', null, False, 'tomaka123', 'Tomasz', 'Akaban', 'tomakaban@ikp.pl', False, True, '2022-05-11 08:00', True, '2022-05-11 08:00', '2022-05-25 08:00');

insert into public.d_address_prefix (prefix)
values ('Os.'), ('Ul.'), ('Al.');

insert into public.d_appointment_type (appointment_type)
values ('Wizyta kontrolna'), ('Zabieg');

insert into public.d_gender (gender)
values ('M'), ('F'), ('X');

insert into public.d_staff_role (role_name)
values ('Administrator'), ('Lekarz'), ('Rejestrator');

insert into public.d_staff_title (title)
values ('dr. hab.'), ('dr.'), ('mgr.');

insert into public.d_country (country)
values ('Polska'), ('Niemcy'), ('Ukraina');

insert into public.d_region (region)
values 
    ('dolnośląskie'),
    ('kujawsko-pomorskie'),
    ('lubelskie'),
    ('lubuskie'),
    ('łódzkie'),
    ('małopolskie'),
    ('mazowieckie'),
    ('opolskie'),
    ('podkarpackie'),
    ('podlaskie'),
    ('pomorskie'),
    ('śląskie'),
    ('świętokrzyskie'),
    ('warmińsko-mazurskie'),
    ('wielkopolskie'),
    ('zachodniopomorskie');

insert into public.campaign_types (camp_name)
values ('Badania'), ('Szczepienia');

insert into public.departments (department)
values ('Oddział Mikrochirurgi Oka'), ('Oddział Kardiologiczny');

insert into public.rooms (id, department, room_name, floor_nr, description)
values 
(0, 'Oddział Mikrochirurgi Oka', '12a - Pracownia laserowa', 1, 'Pracownia ze specjalistycznym laserem'),
(1, 'Oddział Kardiologiczny', '1 - Pracownia EKG', 0, 'Nowoczesna pracownia EKG');

insert into public.timetable (id, department, appointment_type, opening_time, closing_time, free_slots)
values
(0, 'Oddział Mikrochirurgi Oka', 'Wizyta kontrolna', '2022-05-12 08:00:00', '2022-05-12 16:00:00', 16),
(1, 'Oddział Mikrochirurgi Oka', 'Wizyta kontrolna', '2022-05-13 08:00:00', '2022-05-13 13:00:00', 10),
(2, 'Oddział Mikrochirurgi Oka', 'Zabieg', '2022-05-16 08:00:00', '2022-05-16 16:00:00', 16),
(3, 'Oddział Mikrochirurgi Oka', 'Wizyta kontrolna', '2022-05-17 08:00:00', '2022-05-17 10:00:00', 4),
(4, 'Oddział Kardiologiczny', 'Wizyta kontrolna', '2022-05-12 08:00:00', '2022-05-12 12:00:00', 4),
(5, 'Oddział Kardiologiczny', 'Wizyta kontrolna', '2022-05-12 08:00:00', '2022-05-12 10:00:00', 2),
(6, 'Oddział Kardiologiczny', 'Wizyta kontrolna', '2022-05-12 08:00:00', '2022-05-12 12:00:00', 4),
(7, 'Oddział Kardiologiczny', 'Wizyta kontrolna', '2022-05-12 08:00:00', '2022-05-12 10:00:00', 2);

insert into public.hospital_staff (id, user_id, second_name, role, title)
values 
(0, 0, null, 'Administrator', 'mgr.'),
(1, 1, 'Dagmara', 'Lekarz', 'dr. hab.'),
(2, 2, null, 'Rejestrator', null);

insert into public.patients (pesel, user_id, second_name, gender, phone_number, address_prefix, address, house_number, apartment_number, city, region, country, birthdate, created_at, created_by, updated_at, updated_by)
values
(79060300671, 3, 'Jan', 'M', '+48123456789', 'Al.', 'Niepodległości', 14, 3, 'Poznań', 'wielkopolskie', 'Polska', '1979-06-03', '2022-05-11 08:00', 0, null, null);

insert into public.campaigns (id, camp_name, age_from, age_to, gender, active_from, active_to, description)
values
(0, 'Badania', 60, null, null, '2022-05-12 10:00:00', '2022-06-12 10:00:00', 'Bezpłatne badanie wzroku dla seniorów 60+ przez miesiac.');