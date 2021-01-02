import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HostelChai.settings')
import django
django.setup()

from my_modules import classes
from django.db import connection
from django.conf import settings
from pathlib import Path
from django.conf import settings
from PIL import Image

cursor = connection.cursor()

base_dir = settings.BASE_DIR
text_files_dir = os.path.join(base_dir, 'text_files')
temp_files_dir = os.path.join(base_dir, 'temp_files')

file2 = open(f'{os.path.join(settings.BASE_DIR, "text_files")}/institution_names.txt', 'w')
file = open(f'{os.path.join(settings.BASE_DIR, "text_files")}/temp.txt', 'r')

while True:
    line = file.readline()
    if line == '':
        break
    line = file.readline()
    line = file.readline()
    ins_name = line.split('>')[2].split('<')[0]
    location = file.readline().split('>')[1].split('<')[0]
    print(f'Location: {location}')

    if location == 'Dhaka' or location == 'Dhaka ...':
        file2.write(f'{ins_name}\n')
        print(f'writting: {ins_name}')

    line = file.readline()
    line = file.readline()
