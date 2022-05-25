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