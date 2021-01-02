import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HostelChai.settings')
import django
django.setup()


from django.db import connection
cursor = connection.cursor()

from . import classes


def load_hostels():

    command = f'select hostel_id from hostel'
    cursor.execute(command)

    hostel_ids = [id[0] for id in list(cursor.fetchall())]

    hostels = []

    for hostel_id in hostel_ids:
        hostels.append(classes.Hostel())
        hostels[-1].load(hostel_id)

    return hostels


def load_hostel_ratings():
    command = f'select student_user_id, hostel_id from rating_hostel'
    cursor.execute(command)

    s_u_id_h_id = [[id[0], id[1]] for id in list(cursor.fetchall())]

    ratings = []

    for id in s_u_id_h_id:
        ratings.append(classes.HostelRating())
        ratings[-1].load(id[0], id[1])

    return ratings

def load_advertisements():
    command = f'select ads_id from advertise'
    cursor.execute(command)

    ads_ids = [id[0] for id in list(cursor.fetchall())]

    ads = []

    for ads_id in ads_ids:
        ads.append(classes.Advertise())
        ads[-1].load(ads_id)

    return ads
