from my_modules import page_works, exceptions
from django.shortcuts import render
from django.db import connection
from pathlib import Path
import datetime
import os

cursor = connection.cursor()

base_dir = Path('__file__').resolve().parent.parent
text_files_dir = os.path.join(base_dir, 'text_files')
# Create your views here.


def test_page(request):

    data_dict = {
        'page_name': 'test_page',
    }

    user_dict = page_works.get_active_user(request)

    try:
        data_dict['user_type'] = user_dict['user_type']
        data_dict['login_status'] = 'true'
    except KeyError:
        data_dict['login_status'] = 'false'

    return render(request, 'main_app/test_page.html', context=data_dict)


def login_page(request):

    data_dict = {
        'page_name': 'login_page',
        'login_status': 'false',
    }

    try:
        page_works.request_verify(request, False)
    except exceptions.LogoutRequiredException:
        return home_page(request)

    return render(request, 'main_app/login_page.html', context=data_dict)


def login(request):

    try:
        page_works.request_verify(request, False)
    except exceptions.LogoutRequiredException:
        return home_page(request)

    if request.method == 'GET':
        return login_page(request)

    username = request.POST.get('username')
    get_password = request.POST.get('password')
    user = "null"

    command = f"select id, password from user where username like '{username}'"
    cursor.execute(command)

    user_id, password = cursor.fetchall()[0]

    user = user_id.split('-')[0]

    if user == 'null':
        return login_page(request)

    password_verified = False

    if password == get_password:
        password_verified = True

    if password_verified:

        command = (
            "SELECT name FROM user " +
            "WHERE username LIKE '{}'".format(username)
        )
        cursor.execute(command)

        name = cursor.fetchall()[0][0]

        command = (
            "INSERT INTO logged_in_users (userid, expires) " +
            "VALUES ('{}', DATE_ADD(NOW(), INTERVAL 3 DAY))".format(user_id)
        )
        cursor.execute(command)

        command = (
            "SELECT MAX(session_id) FROM logged_in_users"
        )
        cursor.execute(command)

        session_id = int(cursor.fetchall()[0][0])

        cookie_content = "{}_{}".format(session_id, username)

        cookie_expires = datetime.datetime.now() + datetime.timedelta(hours=66)
        cookie_expires = cookie_expires.strftime("%a, %d-%b-%Y %H:%M:%S GMT")

        data_dict = {
            'name': name,
            'logged_in_username': username,
            'user_type': user,
            'login_status': 'true',
        }

        if user == 'S':
            data_dict['page_name'] = 'student_home_page'
            response = render(request, 'main_app/student_home_page.html', context=data_dict)
        else:
            data_dict['page_name'] = 'hostel_owner_home_page'
            response = render(request, 'main_app/hostel_owner_home_page.html', context=data_dict)

        response.set_cookie('_login_session', cookie_content, expires=cookie_expires)

        return response
    else:
        data_dict = {
            'username': username,
            'page_name': 'login_page',
            'login_status': 'false',
        }
        return render(request, 'main_app/login_page.html', context=data_dict)


def logout(request):
    try:
        page_works.request_verify(request, True)
    except exceptions.LoginRequiredException:
        return login_page(request)

    user_dict = page_works.get_active_user(request)

    session_id = user_dict['session_id']

    command = (
        "DELETE FROM logged_in_users WHERE session_id={}".format(session_id)
    )
    cursor.execute(command)

    return login_page(request)


def landing_page(request):
    data_dict = {
        'page_name': 'landing_page',
        'login_status': 'false',
    }

    try:
        page_works.request_verify(request, False)
    except exceptions.LogoutRequiredException:
        return home_page(request)

    return render(request, 'main_app/landing_page.html', context=data_dict)


def home_page(request):
    try:
        page_works.request_verify(request, True)
    except exceptions.LoginRequiredException:
        return login_page(request)

    user_dict = page_works.get_active_user(request)

    if user_dict['user_type'] == 'S':
        return student_home_page(request)
    else:
        return hostel_owner_home_page(request)


def student_home_page(request):

    try:
        page_works.request_verify(request, True)
    except exceptions.LoginRequiredException:
        return login_page(request)

    user_dict = page_works.get_active_user(request)

    data_dict = {
        'name': user_dict['name'],
        'logged_in_username': user_dict['name'],
        'user_type': user_dict['user_type'],
        'page_name': 'student_home_page',
        'login_status': 'true',
    }

    return render(request, 'main_app/student_home_page.html', context=data_dict)


def hostel_owner_home_page(request):

    try:
        page_works.request_verify(request, True)
    except exceptions.LoginRequiredException:
        return login_page(request)

    user_dict = page_works.get_active_user(request)

    data_dict = {
        'name': user_dict['name'],
        'logged_in_username': user_dict['name'],
        'user_type': user_dict['user_type'],
        'page_name': 'hostel_owner_home_page',
        'login_status': 'true',
    }

    return render(request, 'main_app/hostel_owner_home_page.html', context=data_dict)


def add_hostel_page(request):

    try:
        page_works.request_verify(request, True)
    except exceptions.LoginRequiredException:
        return login_page(request)

    user_dict = page_works.get_active_user(request)

    data_dict = {
        'name': user_dict['name'],
        'logged_in_username': user_dict['name'],
        'user_type': user_dict['user_type'],
        'page_name': 'hostel_owner_home_page',
        'login_status': 'true',
    }

    file = open(text_files_dir + '\\thanas.txt', 'r')

    thanas = file.readlines()

    file.close()

    data_dict['thanas'] = thanas

    return render(request, 'main_app/add_hostel_page.html', context=data_dict)


def add_hostel(request):
    #receiving data from frontend
    name = request.POST.get('name')
    thana = request.POST.get('thana')
    postal_code = request.POST.get('postal_code')
    house_no = request.POST.get('house_no')
    road_no = request.POST.get('road_no')
    electricity_bil = request.POST.get('electricity_bill')
    other_valid_doc = request.POST.get('other_valid_doc')
    image = request.POST.get('image')

    #print(f'{name} {thana} {postal_code} {house_no} {road_no} {electricity_bil} {other_valid_doc} {image}')

    #fetching number of hostel from hostel table
    command = f'SELECT COUNT(*) FROM hostel'
    cursor.execute(command)
    data = cursor.fetchall()

    #generating new hostel id
    hostel_id = f'HOS-{str(data[0][0]+1)}'

    #feteching hostel owner name from session
    hostel_owner_username = page_works.get_active_user(request)['username']

    #fetecing hostel owner id
    command = f'SELECT user.id FROM user WHERE user.username = "{hostel_owner_username}"'
    cursor.execute(command)
    hostel_owner_id = cursor.fetchall()[0][0]

    #inserting data in hostel table
    command = f'INSERT INTO hostel VALUES("{hostel_id}", "{hostel_owner_id}", "{name}", "{thana}", "{road_no}", "{house_no}", "{postal_code}", "{electricity_bil}", "{other_valid_doc}", "{image}", 0, 1)'

    # print(hostel_id)
    # print(hostel_owner_username)
    # print(command)
    cursor.execute(command)
    return hostel_owner_home_page(request)
