import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HostelChai.settings')
import django
django.setup()

from django.db import connection
from django.conf import settings
from PIL import Image

cursor = connection.cursor()

command = f'select hostel_id from hostel'
cursor.execute(command)

hostel_ids = [id[0] for id in list(cursor.fetchall())]

print(hostel_ids)
