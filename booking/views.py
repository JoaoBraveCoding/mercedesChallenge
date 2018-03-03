from django.http import HttpResponse
from .models import Dealer, Booking, Vehicle
import json


# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def models(request):
    return HttpResponse(list_by('model'))


def fuels(request):
    return HttpResponse(list_by('fuel'))


def transmission(request):
    return HttpResponse(list_by('transmission'))


def dealer(request):
    dealers = Vehicle.objects.order_by('dealerId').values_list('dealerId', flat=True).distinct()
    json_response = {}
    for deal in dealers:
        json_response.setdefault(deal, [])
    for car in Vehicle.objects.all():
        json_response[car.dealerId.id].append(car.id)

    json_response_pretty = {'dealers': json_response}
    return HttpResponse(json.dumps(json_response_pretty))


def list_by(attribute):
    attribute_types = Vehicle.objects.order_by(attribute).values_list(attribute, flat=True).distinct()
    json_response = {}
    for atr in attribute_types:
        json_response.setdefault(atr, [])
    for car in Vehicle.objects.all():
        json_response[car.__getattribute__(attribute)].append(car.id)

    json_response_pretty = {attribute + 's': json_response}
    return HttpResponse(json.dumps(json_response_pretty))
