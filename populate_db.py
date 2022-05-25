import psycopg2
import datetime
import pandas as pd
import random


conn = psycopg2.connect(
    user='postgres',
    password='postgres',
    host='localhost',
    port=5432,
    database='ikp'
)

query_auth_user = '''
INSERT INTO auth_user (
    id,
    password,
    last_login,
    is_superuser,
    username,
    first_name,
    last_name,
    email,
    is_staff,
    is_active,
    date_joined,
    has_to_change_password,
    last_password_change,
    password_expires
) VALUES (
    %(id)s,
    %(password)s,
    %(last_login)s,
    %(is_superuser)s,
    %(username)s,
    %(first_name)s,
    %(last_name)s,
    %(email)s,
    %(is_staff)s,
    %(is_active)s,
    %(date_joined)s,
    %(has_to_change_password)s,
    %(last_password_change)s,
    %(password_expires)s
)'''

query_staff = '''
INSERT INTO hospital_staff (
    id,
    user_id,
    second_name,
    role,
    title
) VALUES (
    %(id)s,
    %(user_id)s,
    %(second_name)s,
    %(role)s,
    %(title)s
)'''

query_patient = '''
INSERT INTO patients (
    pesel,
    user_id,
    second_name,
    gender,
    phone_number,
    address_prefix,
    address,
    house_number,
    apartment_number,
    city,
    region,
    country,
    birthdate,
    created_at,
    created_by,
    updated_at,
    updated_by
) VALUES (
    %(pesel)s,
    %(user_id)s,
    %(second_name)s,
    %(gender)s,
    %(phone_number)s,
    %(address_prefix)s,
    %(address)s,
    %(house_number)s,
    %(apartment_number)s,
    %(city)s,
    %(region)s,
    %(country)s,
    %(birthdate)s,
    %(created_at)s,
    %(created_by)s,
    %(updated_at)s,
    %(updated_by)s
)'''

query_countries = '''
INSERT INTO d_country (
    country
) VALUES (
    %s
);
'''

query_examinations = '''
INSERT INTO examinations (
    id,
    patient_pesel,
    document_type,
    document_scan,
    uploaded_at,
    uploaded_by,
    accepted_at,
    accepted_by
) VALUES (
    %(id)s,
    %(patient_pesel)s,
    %(document_type)s,
    %(document_scan)s,
    %(uploaded_at)s,
    %(uploaded_by)s,
    %(accepted_at)s,
    %(accepted_by)s
);
'''


def insert_to_db(query, data):
    try:
        conn.rollback()
        cursor = conn.cursor()
        cursor.execute(query, data)
        conn.commit()
        cursor.close()
    except psycopg2.Error as e:
        print(e)


if __name__ == '__main__':
    password = 'pbkdf2_sha256$150000$wEmHEuRlIPeS$zGJVelYcvV7WRIVfWtuEMQ6mTBk+iiRv5wrd7LfWG2Y='
    last_login = None
    is_superuser = True
    is_staff = True
    is_active = True
    date_joined = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    has_to_change_password = True
    last_password_change = date_joined
    password_expires = (datetime.datetime.now() + datetime.timedelta(weeks=2)).strftime('%Y-%m-%d %H:%M')

    staff_id = 3
    patient_id = 1
    examination_id = 0
    random_pesel_list = random.sample(range(10000000000, 99999999999), 1000)
    for x in range(4, 1000):
        username = 'user_' + str(x)
        email = username + '@ikp.pl'
        first_name = 'Example_first_name_'+str(x)
        last_name = 'Example_last_name_'+str(x)
        if x < 10:
            is_superuser = True
            is_staff = True
        elif x < 30:
            is_superuser = False
            is_staff = True
        else:
            is_superuser = False
            is_staff = False
        auth_user_dict = {
            'id': x,
            'password': password,
            'last_login': last_login,
            'is_superuser': is_superuser,
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'is_staff': is_staff,
            'is_active': is_active,
            'date_joined': date_joined,
            'has_to_change_password': has_to_change_password,
            'last_password_change': last_password_change,
            'password_expires': password_expires
        }
        insert_to_db(query_auth_user, auth_user_dict)
        if is_staff:
            # (Administrator), (Lekarz), (Rejestrator)
            if is_superuser:
                role = 'Administrator'
                title = 'mgr.'
            elif x < 15:
                role = 'Rejestrator'
                title = 'mgr.'
            else:
                role = 'Lekarz'
                if x < 20:
                    title = 'dr. hab.'
                else:
                    title = 'dr.'
            hospital_staff_dict = {
                'id': staff_id,
                'user_id': x,
                'second_name': 'Example_second_name_'+str(x),
                'role': role,
                'title': 'dr.'
            }
            insert_to_db(query_staff, hospital_staff_dict)
            staff_id += 1
        else:
            apartment_number = None
            if x % 3 == 0:
                gender = 'M'
                address_prefix = 'Os.'
                apartment_number = x % 10
            elif x % 3 == 1:
                gender = 'F'
                address_prefix = 'Ul.'
            else:
                gender = 'X'
                address_prefix = 'Al.'
            if x % 16 == 0:
                region = 'dolnośląskie'
            elif x % 16 == 1:
                region = 'kujawsko-pomorskie'
            elif x % 16 == 2:
                region = 'lubelskie'
            elif x % 16 == 3:
                region = 'lubuskie'
            elif x % 16 == 4:
                region = 'łódzkie'
            elif x % 16 == 5:
                region = 'małopolskie'
            elif x % 16 == 6:
                region = 'mazowieckie'
            elif x % 16 == 7:
                region = 'opolskie'
            elif x % 16 == 8:
                region = 'podkarpackie'
            elif x % 16 == 9:
                region = 'podlaskie'
            elif x % 16 == 10:
                region = 'pomorskie'
            elif x % 16 == 11:
                region = 'śląskie'
            elif x % 16 == 12:
                region = 'świętokrzyskie'
            elif x % 16 == 13:
                region = 'warmińsko-mazurskie'
            elif x % 16 == 14:
                region = 'wielkopolskie'
            else:
                region = 'zachodniopomorskie'

            patient_dict = {
                'pesel': str(random_pesel_list[patient_id]),
                'user_id': x,
                'second_name': 'Example_second_name_'+str(x),
                'gender': gender,
                'phone_number': '123 456 789',
                'address_prefix': address_prefix,
                'address': 'Niepodległości',
                'house_number': x,
                'apartment_number': apartment_number,
                'city': 'Miasto_' + str(x),
                'region': region,
                'country': 'Polska',
                'birthdate': date_joined,
                'created_at': date_joined,
                'created_by': random.randint(4, 9),
                'updated_at': None,
                'updated_by': None
            }
            insert_to_db(query_patient, patient_dict)

            if patient_id % 3 == 0:
                document_scan = 'exam1.pdf'
                document_type = 'pdf'
            elif patient_id % 3 == 1:
                document_scan = 'exam2.jpg'
                document_type = 'jpg'
            else:
                document_scan = 'exam3.png'
                document_type = 'png'
            examination_dict = {
                'id': examination_id,
                'patient_pesel': str(random_pesel_list[patient_id]),
                'document_scan': document_scan,
                'document_type': document_type,
                'uploaded_at': date_joined,
                'uploaded_by': x,
                'accepted_at': date_joined,
                'accepted_by': random.randint(4, 9)
            }
            insert_to_db(query_examinations, examination_dict)
            examination_id += 1
            patient_id += 1

    df_countries = pd.read_csv('countries.csv')
    for index, value in df_countries.iterrows():
        if value['NAZ_POL_S'] not in ['Niemcy', 'Polska', 'Ukraina']:
            insert_to_db(query_countries, (value['NAZ_POL_S'],))

