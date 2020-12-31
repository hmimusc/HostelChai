import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HostelChai.settings')
import django

django.setup()

from django.db import connection
from django.conf import settings
from PIL import Image

cursor = connection.cursor()


class User:

    def __init__(self):
        pass

    def load(self, user_id):
        pass

    def create(self, user_type, data, files):

        command = f'select count(*) from user where user_type={user_type}'
        cursor.execute(command)

        user_type_count = cursor.fetchall()[0][0]
        user_type_string = ''

        if user_type == 0:
            user_type_string = 'S'
        elif user_type == 1:
            user_type_string = 'H'
        elif user_type == 9:
            user_type_string = 'A'

        self.user_type = user_type
        self.id = f'{user_type_string}-{user_type_count + 1}'
        self.name = data['name']
        self.username = data['username']
        self.password = data['password']
        self.dob = data['dob']
        self.gender = data['gender']
        self.phone_number = data['phone_number']
        self.email = data['email']
        self.permanent_address = data['permanent_address']

        self.profile_picture = f'{self.id}_profile_picture.png'
        self.nid = f'{self.id}_nid.png'
        self.birth_certificate = f'{self.id}_birth_certificate.png'

        self.files = {
            'profile_picture': Image.open(files['profile_picture']),
            'nid': Image.open(files['nid']),
            'birth_certificate': Image.open(files['birth_certificate']),
        }

        self.verified = 0

    def save(self):

        self.files['profile_picture'].save(f'{settings.MEDIA_ROOT}/{self.profile_picture}')
        self.files['nid'].save(f'{settings.MEDIA_ROOT}/{self.nid}')
        self.files['birth_certificate'].save(f'{settings.MEDIA_ROOT}/{self.birth_certificate}')

        command = f'select count(*) from user where id like "{self.id}"'
        cursor.execute(command)
        user_count = cursor.fetchall()[0][0]

        if user_count == 0:
            command = (
                f'insert into user values (' +
                f'"{self.id}", ' +
                f'"{self.name}", ' +
                f'"{self.username}", ' +
                f'"{self.password}", ' +
                f'"{self.profile_picture}", ' +
                f'"{self.dob}", ' +
                f'"{self.nid}", ' +
                f'"{self.birth_certificate}", ' +
                f'"{self.gender}", ' +
                f'"{self.phone_number}", ' +
                f'"{self.email}", ' +
                f'"{self.permanent_address}", ' +
                f'{self.verified}, ' +
                f'{self.user_type}' +
                f')'
            )
            cursor.execute(command)
        else:
            command = (
                f'update user set ' +
                f'id="{self.id}", ' +
                f'name="{self.name}", ' +
                f'username="{self.username}", ' +
                f'password="{self.password}", ' +
                f'profile_picture="{self.profile_picture}", ' +
                f'dob="{self.dob}", ' +
                f'nid="{self.nid}", ' +
                f'birth_certificate="{self.birth_certificate}", ' +
                f'gender="{self.gender}", ' +
                f'phone_number="{self.phone_number}", ' +
                f'email="{self.email}", ' +
                f'permanent_address="{self.permanent_address}", ' +
                f'verified={self.verified}, ' +
                f'user_type={self.user_type}'
            )
            cursor.execute(command)


class HostelOwner(User):

    def __init__(self):
        User.__init__(self)
        pass

    def load_hostel_owner(self, user_id):
        pass

    def create_hostel_owner(self, data, files):

        User.create(self, 1, {
            'name': data['name'],
            'username': data['username'],
            'password': data['password'],
            'dob': data['dob'],
            'gender': data['gender'],
            'email': data['email'],
            'phone_number': data['phone_number'],
            'permanent_address': data['permanent_address'],
        }, {
            'profile_picture': files['profile_picture'],
            'nid': files['nid'],
            'birth_certificate': files['birth_certificate'],
        })

        self.user_id = self.id
        self.occupation = data['occupation']
        self.due = 0
        self.active = 0

    def save_hostel_owner(self):
        User.save(self)

        command = f'select count(*) from hostel_owner where user_id like "{self.id}"'
        cursor.execute(command)

        hostel_owner_count = cursor.fetchall()[0][0]

        if hostel_owner_count == 0:
            command = f'insert into hostel_owner values ("{self.user_id}", "{self.occupation}", {self.due}, {self.verified})'
            cursor.execute(command)
        else:
            command = (
                f'update hostel_owner set ' +
                f'user_id={self.user_id} ' +
                f'occupation={self.occupation} ' +
                f'due={self.due} ' +
                f'verified={self.verified}'
            )
            cursor.execute(command)


class Student(User):

    def __init__(self):
        User.__init__(self)
        pass

    def load_student(self, user_id):
        pass

    def create_student(self, data, files):

        User.create(self, 0, {
            'name': data['name'],
            'username': data['username'],
            'password': data['password'],
            'dob': data['dob'],
            'gender': data['gender'],
            'email': data['email'],
            'phone_number': data['phone_number'],
            'permanent_address': data['permanent_address'],
        }, {
            'profile_picture': files['profile_picture'],
            'nid': files['nid'],
            'birth_certificate': files['birth_certificate'],
        })

        self.user_id = self.id
        self.institution = data['institution']
        self.degree = data['degree']
        self.student_id = data['student_id']
        self.current_hostel_id = 'null'

    def save_student(self):
        User.save(self)

        command = f'select count(*) from student where user_id like "{self.id}"'
        cursor.execute(command)

        student_count = cursor.fetchall()[0][0]

        if student_count == 0:
            command = (
                f'insert into student(user_id, institution, degree, student_id) values ( ' +
                f'"{self.user_id}", ' +
                f'"{self.institution}", ' +
                f'"{self.degree}", ' +
                f'"{self.student_id}" ' +
                f')'
            )
            cursor.execute(command)
        else:
            command = (
                f'update student set ' +
                f'user_id="{self.user_id}"' +
                f'institution="{self.institution}" ' +
                f'degree="{self.degree}" ' +
                f'student_id="{self.student_id}" ' +
                f'current_hostel_id="{self.current_hostel_id}"'
            )
            cursor.execute(command)


class Hostel:

    def __init__(self):
        pass

    def load(self, hostel_id):
        command = f'select * from hostel where hostel_id like "{hostel_id}"'
        cursor.execute(command)

        hostel = cursor.fetchall()[0]

        self.hostel_id = hostel_id
        self.hostel_owner_id = hostel[1]
        self.hostel_name = hostel[2]
        self.thana = hostel[3]
        self.road_number = hostel[4]
        self.house_number = hostel[5]
        self.postal_code = hostel[6]
        self.electricity_bill = hostel[7]
        self.hostel_document = hostel[8]
        self.photo = hostel[9]
        self.verified = hostel[10]
        self.active = hostel[11]

    def create(self, data, files):

        command = f'SELECT COUNT(*) FROM hostel'
        cursor.execute(command)

        self.hostel_id = f'HOS-{str(cursor.fetchall()[0][0] + 1)}'
        self.hostel_owner_id = data['hostel_owner_id']
        self.hostel_name = data['hostel_name']
        self.thana = data['thana']
        self.road_number = data['road_number']
        self.house_number = data['house_number']
        self.postal_code = data['postal_code']
        self.electricity_bill = f'{self.hostel_owner_id}_{self.hostel_id}_electricity_bill.png'
        self.hostel_document = f'{self.hostel_owner_id}_{self.hostel_id}_hostel_document.png'
        self.photo = f'{self.hostel_owner_id}_{self.hostel_id}_photo.png'
        self.verified = 0
        self.active = 0

        self.files = {
            'electricity_bill': Image.open(files['electricity_bill']),
            'hostel_document': Image.open(files['hostel_document']),
            'photo': Image.open(files['photo']),
        }

    def save(self):
        command = f'select count(*) from hostel where hostel_id like "{self.hostel_id}"'
        cursor.execute(command)
        hostel_count = cursor.fetchall()[0][0]

        if hostel_count == 0:

            self.files['electricity_bill'].save(f'{settings.MEDIA_ROOT}/{self.electricity_bill}')
            self.files['hostel_document'].save(f'{settings.MEDIA_ROOT}/{self.hostel_document}')
            self.files['photo'].save(f'{settings.MEDIA_ROOT}/{self.photo}')

            command = f'INSERT INTO hostel VALUES("{self.hostel_id}", "{self.hostel_owner_id}", "{self.hostel_name}", "{self.thana}", "{self.road_number}", "{self.house_number}", "{self.postal_code}", "{self.electricity_bill}", "{self.hostel_document}", "{self.photo}", {self.verified}, {self.active})'
        else:
            command = f'UPDATE hostel SET hostel_name="{self.hostel_name}", thana="{self.thana}", road_number="{self.road_number}", house_number="{self.house_number}", postal_code="{self.postal_code}", electricity_bill="{self.electricity_bill}", hostel_document="{self.hostel_document}", photo="{self.photo}", verified={self.verified}, active={self.active} WHERE hostel_id="{self.hostel_id}"'

        cursor.execute(command)


class Advertise:

    def __init__(self):
        pass

    def load(self):
        pass

    def create(self):
        pass

    def save(self):
        pass


class Complaint:

    def __init__(self):
        pass

    def load(self, complaint_id):
        command = f'SELECT * FROM complaint_box where complaint_id = {complaint_id}'
        cursor.execute(command)

        complaint = cursor.fetchall()[0]

        self.complaint_id = complaint_id
        self.user_id = complaint[1]
        self.subject = complaint[2]
        self.complaint = complaint[3]
        self.photo = complaint[4]
        self.resolved = complaint[5]

    def create(self, data, files):
        command = 'SELECT COUNT(*) FROM complaint_box'
        cursor.execute(command)

        self.complaint_id = cursor.fetchall()[0][0] + 1
        self.user_id = data['user_id']
        self.subject = data['subject']
        self.complaint = data['complaint']
        self.photo = f'{self.user_id}_complaint-{self.complaint_id}_evidence.png'
        self.resolved = 0

        self.files = {
            'photo': Image.open(files['photo'])
        }

    def save(self):
        command = f'SELECT COUNT(*) FROM complaint_box WHERE complaint_id = {self.complaint_id}'
        cursor.execute(command)
        complaint_count = cursor.fetchall()[0][0]

        if complaint_count == 0:
            self.files['photo'].save(f'{settings.MEDIA_ROOT}/{self.photo}')
            command = f'INSERT INTO complaint_box VALUES ({self.complaint_id},"{self.user_id}","{self.subject}","{self.complaint}","{self.photo}",{self.resolved})'
        else:
            command = f'UPDATE complaint_box SET user_id = "{self.user_id}", subject = "{self.subject}", complaint = "{self.complaint}", photo = "{self.photo}", resolved = {self.resolved} WHERE complaint_id = {self.complaint_id}'
        cursor.execute(command)


class Transaction:

    def __init__(self):
        pass

    def load(self):
        pass

    def create(self):
        pass

    def save(self):
        pass


class ReceivedTransaction(Transaction):

    def __init__(self):
        Transaction.__init__(self)
        pass

    def load(self):
        pass

    def create(self):
        pass

    def save(self):
        pass


class PaymentRequest(Transaction):

    def __init__(self):
        Transaction.__init__(self)
        pass

    def load(self):
        pass

    def create(self):
        pass

    def save(self):
        pass


class HostelRating:

    def __init__(self):
        pass


class StudentRating:

    def __init__(self):
        pass


class HostelReview:

    def __init__(self):
        pass
