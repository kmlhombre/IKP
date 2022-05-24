DROP TABLE public.patient_permissions_module_zgody;
DROP TABLE public.patient_permissions_module_pacjenci;
DROP TABLE public.campaign_notifications;
DROP TABLE public.campaigns;
DROP TABLE public.appointment_notifications;
DROP TABLE public.appointments;
DROP TABLE public.unaccepted_examinations;
DROP TABLE public.examinations;
DROP TABLE public.patients_old;
DROP TABLE public.patients;
DROP TABLE public.hospital_staff;
DROP TABLE public.timetable;
DROP TABLE public.rooms;
DROP TABLE public.campaign_types;
DROP TABLE public.departments;
DROP TABLE public.d_country;
DROP TABLE public.d_region;
DROP TABLE public.d_staff_title;
DROP TABLE public.d_staff_role;
DROP TABLE public.d_gender;
DROP TABLE public.d_appointment_type;
DROP TABLE public.d_address_prefix;
DROP TABLE public.django_session;
DROP TABLE public.django_migrations;
DROP TABLE public.django_admin_log;
DROP TABLE public.auth_user_user_permissions;
DROP TABLE public.auth_user_groups;
DROP TABLE public.auth_user;
DROP TABLE public.auth_group_permissions;
DROP TABLE public.auth_group;
DROP TABLE public.auth_permission;
DROP TABLE public.django_content_type;

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
	country varchar(40) primary key
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
	country varchar(40) NOT NULL references public.d_country(country),
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
	country varchar(40) references public.d_country(country),
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
	document_scan text NOT NULL ,
	document_type text NOT NULL ,
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
	referral bytea,
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