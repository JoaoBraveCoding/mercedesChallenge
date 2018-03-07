import math
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


def find_dealer(request):
    vehicles = Vehicle.objects.filter(model=request.META.get("HTTP_MODEL"), fuel=request.META.get("HTTP_FUEL"),
                                      transmission=request.META.get("HTTP_TRANSMISSION"))
    dealers_id = vehicles.values_list('dealerId', flat=True).distinct()
    if len(dealers_id) == 0:
        return HttpResponse(0)
    dealers = Dealer.objects.filter(pk__in=dealers_id)

    user_pos = (float(request.META.get("HTTP_LATITUDE")), float(request.META.get("HTTP_LONGITUDE")))
    best_distance = -1
    for dealer in dealers:
        current_distance = distance(user_pos, (dealer.latitude, dealer.longitude))
        if current_distance < best_distance or best_distance == -1:
            best_distance = current_distance
            best_dealer = dealer

    json_response = {"id": best_dealer.id, "name": best_dealer.name, "latitude": best_dealer.latitude,
                     "longitude": best_dealer.longitude}

    json_response_pretty = {"dealers": json_response}
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


def distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371  # km

    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (math.sin(d_lat / 2) * math.sin(d_lat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(d_lon / 2) * math.sin(d_lon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return radius * c
