from my_modules import page_works, exceptions, classes
from django.shortcuts import render
from django.db import connection
from pathlib import Path
import datetime
import os

cursor = connection.cursor()

base_dir = Path('__file__').resolve().parent.parent
text_files_dir = os.path.join(base_dir, 'text_files')
temp_files_dir = os.path.join(base_dir, 'temp_files')


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

    data_dict['image'] = 'H-1_HOS-4_electbill.png'

    data_dict['days'] = range(32)[1:]
    data_dict['months'] = 'January,February,March,April,May,June,July,August,September,October,November,December'.split(',')
    data_dict['years'] = range(2022)[1990:]

    return render(request, 'main_app/test_page.html', context=data_dict)


def setup_admin_page(request):
    return render(request, 'main_app/setup_admin_page.html', context={})


def setup_admin(request):

    name = request.POST.get('name')
    username = request.POST.get('username')
    password = request.POST.get('password')
    gender = request.POST.get('gender')
    phone = request.POST.get('phone')
    email = request.POST.get('email')
    address = request.POST.get('address')

    command = f'select count(*) from user where id like "A%"'
    cursor.execute(command)
    user_id = f'A-{cursor.fetchall()[0][0] + 1}'

    command = f'insert into user values ("{user_id}", "{name}", "{username}", "{password}", "null", CURRENT_DATE , "null", "null", "{gender}", "{phone}", "{email}", "{address}", 1, 9)'
    cursor.execute(command)

    return login_page(request)


def error_404(request, exception=''):

    try:
        page_works.request_verify(request, True)

        user_dict = page_works.get_active_user(request)

        data_dict = {
            'name': user_dict['name'],
            'logged_in_username': user_dict['username'],
            'user_type': user_dict['user_type'],
            'page_name': '404_page',
            'login_status': 'true',
        }

    except exceptions.LoginRequiredException:
        pass

    return render(request, 'main_app/404_page.html', context=data_dict)


def error_500(request, template_name='500.html'):

    data_dict = {}

    try:
        page_works.request_verify(request, True)

        user_dict = page_works.get_active_user(request)

        data_dict = {
            'name': user_dict['name'],
            'logged_in_username': user_dict['username'],
            'user_type': user_dict['user_type'],
            'page_name': '404_page',
            'login_status': 'true',
        }
    except exceptions.LoginRequiredException:
        pass

    return render(request, template_name, context=data_dict)


def requests_loader_page(request):

    try:
        page_works.request_verify(request, True)
    except exceptions.LoginRequiredException:
        return login_page(request)

    try:
        page_works.user_verify(request, 'A')
    except exceptions.UserRequirementException:
        return home_page(request)

    user_dict = page_works.get_active_user(request)

    data_dict = {
        'name': user_dict['name'],
        'logged_in_username': user_dict['username'],
        'user_type': user_dict['user_type'],
        'page_name': 'admin_hostel_loader_page',
        'login_status': 'true',
    }

    command = 'select hostel_id from hostel where verified=0'
    cursor.execute(command)

    hostels = cursor.fetchall()

    hostels = [hostel[0] for hostel in hostels]

    data_dict['hostels'] = hostels
    data_dict['checked'] = ['', 'checked', '']

    return render(request, 'main_app/requests_loader_page.html', context=data_dict)


def requests_loader(request):

    try:
        page_works.request_verify(request, True)
    except exceptions.LoginRequiredException:
        return login_page(request)

    try:
        page_works.user_verify(request, 'A')
    except exceptions.UserRequirementException:
        return home_page(request)

    req_type = request.POST.get('req_type')

    # print(f'[+] req_type: {req_type}')

    if req_type == 'hostels':
        return hostel_loader_page(request)
    else:
        return home_page(request)


def hostel_loader_page(request):

    try:
        page_works.request_verify(request, True)
    except exceptions.LoginRequiredException:
        return login_page(request)

    try:
        page_works.user_verify(request, 'A')
    except exceptions.UserRequirementException:
        return home_page(request)

    if 'hostel_id' in request.POST:
        hostel_id = request.POST.get('hostel_id')
    else:
        return requests_loader_page(request)

    hostel = classes.Hostel()
    hostel.load(hostel_id)

    command = f'select name, phone_number from user where id like "{hostel.hostel_owner_id}"'
    cursor.execute(command)

    hostel_owner_name, phone_number = cursor.fetchall()[0]

    user_dict = page_works.get_active_user(request)

    data_dict = {
        'name': user_dict['name'],
        'logged_in_username': user_dict['username'],
        'user_type': user_dict['user_type'],
        'page_name': 'admin_home_page',
        'login_status': 'true',
        'hostel_name': hostel.hostel_name,
        'hostel_owner_name': hostel_owner_name,
        'phone_number': phone_number,
        'hostel_id': hostel.hostel_id,
        'hostel_house_number': hostel.house_number,
        'hostel_road_number': hostel.road_number,
        'hostel_thana': hostel.thana,
        'hostel_postal_code': hostel.postal_code,
        'hostel_photo': hostel.photo,
        'hostel_electricity_bill': hostel.electricity_bill,
        'hostel_document': hostel.hostel_document,
    }

    return render(request, 'main_app/hostel_loader_page.html', context=data_dict)


def approve_hostel(request):

    try:
        page_works.request_verify(request, True)
    except exceptions.LoginRequiredException:
        return login_page(request)

    try:
        page_works.user_verify(request, 'A')
    except exceptions.UserRequirementException:
        return home_page(request)

    hostel_id = request.POST.get('hostel_id')
    command = f'update hostel set verified=1, active=1 where hostel_id like "{hostel_id}"'
    cursor.execute(command)

    return hostel_owner_home_page(request)


def registration_page(request):

    try:
        page_works.request_verify(request, False)
    except exceptions.LogoutRequiredException:
        return home_page(request)

    data_dict = {
        'page_name': 'registration_page',
        'login_status': 'false',
    }

    return render(request, 'main_app/registration_page.html', context=data_dict)


def student_registration(request):

    try:
        page_works.request_verify(request, False)
    except exceptions.LogoutRequiredException:
        return home_page(request)

    return login_page(request)


def hostel_owner_registration(request):

    try:
        page_works.request_verify(request, False)
    except exceptions.LogoutRequiredException:
        return home_page(request)

    hostel_owner = classes.HostelOwner()

    hostel_owner.create({
        'name':  request.POST.get('h_name'),
        'username': request.POST.get('h_username'),
        'password': request.POST.get('h_password'),
        'dob': request.POST.get('h_dob'),
        'gender': request.POST.get('h_gender'),
        'email': request.POST.get('h_email'),
        'phone_number': request.POST.get('h_phone_number'),
        'occupation': request.POST.get('occupation'),
        'permanent_address': request.POST.get('h_permanent_address'),
    }, {
        'profile_picture': request.FILES.get(),
        'nid': '',
        'birth_certificate': '',
    })

    return login_page(request)


def login_page(request):

    try:
        page_works.request_verify(request, False)
    except exceptions.LogoutRequiredException:
        return home_page(request)

    data_dict = {
        'page_name': 'login_page',
        'login_status': 'false',
    }

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

    try:
        user_id, password = cursor.fetchall()[0]
    except IndexError:
        return login_page(request)

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
        elif user == 'H':
            data_dict['page_name'] = 'hostel_owner_home_page'
            response = render(request, 'main_app/hostel_owner_home_page.html', context=data_dict)
        elif user == 'A':
            data_dict['page_name'] = 'admin_home_page'
            response = render(request, 'main_app/admin_home_page.html', context=data_dict)
        else:
            return logout(request)

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
    elif user_dict['user_type'] == 'H':
        return hostel_owner_home_page(request)
    elif user_dict['user_type'] == 'A':
        return admin_home_page(request)
    else:
        return logout(request)


def admin_home_page(request):

    try:
        page_works.request_verify(request, True)
    except exceptions.LoginRequiredException:
        return login_page(request)

    try:
        page_works.user_verify(request, 'A')
    except exceptions.UserRequirementException:
        return home_page(request)

    user_dict = page_works.get_active_user(request)

    data_dict = {
        'name': user_dict['name'],
        'logged_in_username': user_dict['username'],
        'user_type': user_dict['user_type'],
        'page_name': 'admin_home_page',
        'login_status': 'true',
    }

    return render(request, 'main_app/admin_home_page.html', context=data_dict)


def student_home_page(request):

    try:
        page_works.request_verify(request, True)
    except exceptions.LoginRequiredException:
        return login_page(request)

    try:
        page_works.user_verify(request, 'S')
    except exceptions.UserRequirementException:
        return home_page(request)

    user_dict = page_works.get_active_user(request)

    data_dict = {
        'name': user_dict['name'],
        'logged_in_username': user_dict['username'],
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
        'logged_in_username': user_dict['username'],
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
        'logged_in_username': user_dict['username'],
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

    try:
        page_works.request_verify(request, True)
    except exceptions.LoginRequiredException:
        return login_page(request)

    try:
        page_works.user_verify(request, 'H')
    except exceptions.UserRequirementException:
        return home_page(request)

    hostel_owner_id = page_works.get_active_user(request)['userid']
    name = request.POST.get('name')
    thana = request.POST.get('thana')
    postal_code = request.POST.get('postal_code')
    house_no = request.POST.get('house_no')
    road_no = request.POST.get('road_no')

    new_hostel = classes.Hostel()
    new_hostel.create({
            'hostel_owner_id': hostel_owner_id,
            'hostel_name': name,
            'thana': thana,
            'road_number': road_no,
            'house_number': house_no,
            'postal_code': postal_code,
        }, {
            'electricity_bill': request.FILES['electricity_bill'],
            'hostel_document': request.FILES['other_valid_doc'],
            'photo': request.FILES['image'],
        }
    )

    new_hostel.save()

    return hostel_owner_home_page(request)


def complaint_box_page(request):

    try:
        page_works.request_verify(request, True)
    except exceptions.LoginRequiredException:
        return login_page(request)

    user_dict = page_works.get_active_user(request)

    data_dict = {
        'name': user_dict['name'],
        'logged_in_username': user_dict['username'],
        'user_type': user_dict['user_type'],
        'page_name': 'complaint_box_page',
        'login_status': 'true',
    }

    return render(request, 'main_app/complaint_box_page.html', context=data_dict)


def complaint_box(request):

    try:
        page_works.request_verify(request, True)
    except exceptions.LoginRequiredException:
        return login_page(request)

    try:
        page_works.request_verify(request, True)
    except exceptions.LoginRequiredException:
        return login_page(request)

    user_id = page_works.get_active_user(request)['userid']
    subject = request.POST.get('subject')
    complaint = request.POST.get('details')

    new_complaint = classes.Complaint()

    new_complaint.create(
        {
            'user_id': user_id,
            'subject': subject,
            'complaint': complaint,
        },
        {
            'photo': request.FILES['photo'],
        }
    )

    return home_page(request)
