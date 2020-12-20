import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HostelChai.settings')
import django
django.setup()


from django.db import connection
from pathlib import Path
cursor = connection.cursor()


base_dir = Path('__file__').resolve().parent.parent
media_files_dir = os.path.join(base_dir, 'media')
main_app_media_dir = os.path.join(media_files_dir, 'main_app')


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
        self.electricity_bill = [f'{main_app_media_dir}\\', hostel[7]]
        self.hostel_document = [f'{main_app_media_dir}\\', hostel[8]]
        self.photo = [f'{main_app_media_dir}\\', hostel[9]]
        self.verified = hostel[10]
        self.active = hostel[11]

    def create(self, data):
        self.hostel_id = data['hostel_id']
        self.hostel_owner_id = data['hostel_owner_id']
        self.hostel_name = data['hostel_name']
        self.thana = data['thana']
        self.road_number = data['road_number']
        self.house_number = data['house_number']
        self.postal_code = data['postal_code']
        self.electricity_bill = [f'{main_app_media_dir}\\', data['electricity_bill']]
        self.hostel_document = [f'{main_app_media_dir}\\', data['hostel_document']]
        self.photo = [f'{main_app_media_dir}\\', data['photo']]
        self.verified = data['verified']
        self.active = data['active']

    def save(self):
        command = f'select count(*) from hostel where hostel_id like "{self.hostel_id}"'
        cursor.execute(command)
        hostel_count = cursor.fetchall()[0][0]

        if hostel_count == 0:
            command = f'INSERT INTO hostel VALUES("{self.hostel_id}", "{self.hostel_owner_id}", "{self.hostel_name}", "{self.thana}", "{self.road_number}", "{self.house_number}", "{self.postal_code}", "{self.electricity_bill[1]}", "{self.hostel_document[1]}", "{self.photo[1]}", {self.verified}, {self.active})'
        else:
            command = f'UPDATE hostel SET hostel_name="{self.hostel_name}", thana="{self.thana}", road_number="{self.road_number}", house_number="{self.house_number}", postal_code="{self.postal_code}", electricity_bill="{self.electricity_bill[1]}", hostel_document="{self.hostel_document[1]}", photo="{self.photo[1]}", verified={self.verified}, active={self.active} WHERE hostel_id="{self.hostel_id}"'

        cursor.execute(command)
