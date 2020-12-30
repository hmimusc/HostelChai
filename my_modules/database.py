import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HostelChai.settings')
import django
django.setup()


from django.db import connection
cursor = connection.cursor()

from .classes import *


def load_hostels():

    command = f'select hostel_id from hostel'
    cursor.execute(command)

    hostel_ids = [id[0] for id in list(cursor.fetchall())]

    hostels = []

    for hostel_id in hostel_ids:
        hostels.append(Hostel())
        hostels[-1].load(hostel_id)

    return hostels
