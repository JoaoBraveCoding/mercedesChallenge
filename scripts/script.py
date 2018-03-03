#import os
import json

#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mercedes.settings")

# your imports, e.g. Django models
from booking.models import *


def run():
    json_data = open("datafile/dataset.json")
    data1 = json.load(json_data)

    print("I was executed")

    json_data.close()

    # e.g. add a new location
    # l = Location()
    # l.name = 'Berlin'
    # l.save()
    #
    # # this is an example to access your model
    # locations = Location.objects.all()
    # print locations
    #
    # # e.g. delete the location
    # berlin = Location.objects.filter(name='Berlin')
    # print berlin
    # berlin.delete()
