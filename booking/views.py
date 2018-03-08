from datetime import datetime
import math
from operator import itemgetter

from django.http import HttpResponse, HttpResponseBadRequest
from django.core.exceptions import ObjectDoesNotExist


from .models import Dealer, Booking, Vehicle
import json
import uuid



def models(request):
    return HttpResponse(list_by('model'))


def fuels(request):
    return HttpResponse(list_by('fuel'))


def transmissions(request):
    return HttpResponse(list_by('transmission'))


def dealers(request):
    dealers = Vehicle.objects.order_by('dealerId').values_list('dealerId', flat=True).distinct()
    json_response = {}

    # Build json response
    for deal in dealers:
        json_response.setdefault(deal, [])
    for car in Vehicle.objects.all():
        json_response[car.dealerId.id].append(car.id)
    json_response_pretty = {'dealers': json_response}

    return HttpResponse(json.dumps(json_response_pretty))


def find_dealer(request):
    if request.META.get("HTTP_MODEL") is None or request.META.get("HTTP_FUEL") is None \
            or request.META.get("HTTP_TRANSMISSION") is None:
        return HttpResponseBadRequest(
            json.dumps({"error": "One or more fields missing in the message header, the header has to have"
                                                                            "model fuel and transmission"}), status=412)
    vehicles = Vehicle.objects.filter(model=request.META.get("HTTP_MODEL"), fuel=request.META.get("HTTP_FUEL"),
                                      transmission=request.META.get("HTTP_TRANSMISSION"))
    dealers_id = vehicles.values_list('dealerId', flat=True).distinct()

    # Check if there are any dealers for the requested specs
    if len(dealers_id) == 0:
        return HttpResponse(json.dumps({"dealers": []}))
    dealers = Dealer.objects.filter(pk__in=dealers_id)

    # Get user position
    user_pos = (float(request.META.get("HTTP_LATITUDE")), float(request.META.get("HTTP_LONGITUDE")))
    if not (-90 <= user_pos[0] <= 90) and not (-180 <= user_pos[1] <= 180):
        return HttpResponseBadRequest(json.dumps({"error": "Invalid user localization please check latitude and "
                                                           "longitude values"}), status=412)

    # Create an array with every dealer and the distance to the client and sort that array
    dealers_to_return = []
    for dealer in dealers:
        current_distance = distance(user_pos, (dealer.latitude, dealer.longitude))
        dealers_to_return.append([dealer, current_distance])
    dealers_to_return = sorted(dealers_to_return, key=itemgetter(1))

    # Build json response
    json_response = []
    for dealer in dealers_to_return:
        to_append = {"id": dealer[0].id, "name": dealer[0].name, "latitude": dealer[0].latitude,
                     "longitude": dealer[0].longitude}
        json_response.append(to_append)
    json_response_pretty = {"dealers": json_response}

    return HttpResponse(json.dumps(json_response_pretty))


def new_booking(request):
    if request.META.get("HTTP_PICKUPDATE") is None or request.META.get("HTTP_VEHICLEID") is None \
            or request.META.get("HTTP_FIRSTNAME") is None or request.META.get("HTTP_LASTNAME") is None:
        return HttpResponseBadRequest(
            json.dumps({"error": "One or more fields missing in the message header, the header has to have pickupdate "
                                 "vehicleID firstname and lastname"}), status=412)

    desired_time_slot = datetime.strptime(request.META.get("HTTP_PICKUPDATE"), '%Y-%m-%dT%H:%M:%S')
    try:
        desired_vehicle = Vehicle.objects.get(id=request.META.get("HTTP_VEHICLEID"))
    except ObjectDoesNotExist:
        return HttpResponseBadRequest(json.dumps({"error": "No vehicle for the given ID"}), status=412)

    bookings = Booking.objects.filter(vehicleId=desired_vehicle.id, canceledAt__isnull=True,
                                      cancelledReason__isnull=True)

    # Parse vehicle availability weekdays and times
    vehicle_availability = desired_vehicle.availability.splitlines()
    for i in range(len(vehicle_availability)):
        vehicle_availability[i] = vehicle_availability[i].split(' ')

    # Check if the vehicle has availability for requested date and time
    if not exists_availability(desired_time_slot, vehicle_availability):
        return HttpResponse(
            json.dumps({"error": "The vehicle you requested is not available at the time you requested"}), status=412)

    # Check if there are no double booking
    if not no_double_booking(desired_time_slot, bookings):
        return HttpResponse(json.dumps({"error": "There is already a test drive for that time and vehicle"}),
                            status=412)

    # Create and save the booking
    booking_to_save = Booking.objects.create(id=uuid.uuid4(), vehicleId=desired_vehicle,
                                             firstName=request.META.get("HTTP_FIRSTNAME"),
                                             lastName=request.META.get("HTTP_LASTNAME"),
                                             pickupDate=desired_time_slot,
                                             createdAt=datetime.now())
    booking_to_save.save()

    return HttpResponse(json.dumps({"return": "Test drive booked success"}))


def cancel_booking(request):
    booking_to_cancel = Booking.objects.get(id=request.META.get("HTTP_ID"))
    booking_to_cancel.cancelledReason = request.META.get("HTTP_CANCELLEDREASON")
    booking_to_cancel.canceledAt = datetime.now()
    booking_to_cancel.save()

    return HttpResponse(json.dumps({"return": "Test drive canceled successfully"}))


def list_by(attribute):
    attribute_types = Vehicle.objects.order_by(attribute).values_list(attribute, flat=True).distinct()

    # Build json response
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


def exists_availability(desired_time_slot, vehicle_availability):
    for i in range(len(vehicle_availability)):
        if vehicle_availability[i][0] == desired_time_slot.strftime('%A').lower():
            for j in range(1, len(vehicle_availability[i])):
                if desired_time_slot.strftime('%H%M') == vehicle_availability[i][j]:
                    return True
    return False


def no_double_booking(desired_time_slot, bookings):
    for booking in bookings:
        if desired_time_slot == booking.pickupDate:
            return False
    return True
