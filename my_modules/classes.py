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

    def create(self, data, files):
        pass

    def save(self):
        pass


class HostelOwner(User):

    def __init__(self):
        User.__init__(self)
        pass

    def load(self, user_id):
        User.load(self, user_id)
        pass

    def create(self, data, file):

        user_data = {}
        user_files = {}

        User.create(self, user_data, user_files)
        pass


class Student(User):

    def __init__(self):
        User.__init__(self)
        pass

    def load(self, user_id):
        User.load(self, user_id)
        pass

    def create(self, data, file):

        user_data = {}
        user_files = {}

        User.create(self, user_data, user_files)
        pass


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


class Rating:

    def __init__(self):
        pass


class HostelRating(Rating):

    def __init__(self):
        Rating.__init__(self)
        pass


class StudentRating(Rating):

    def __init__(self):
        Rating.__init__(self)
        pass


class Review:

    def __init__(self):
        pass
