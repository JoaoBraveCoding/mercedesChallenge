import json
from booking.models import Dealer, Vehicle, Booking
from datetime import datetime


def run():
    # Delete db
    dealers = Dealer.objects.all()
    dealers.delete()
    vehicles = Vehicle.objects.all()
    vehicles.delete()
    bookings = Booking.objects.all()
    bookings.delete()

    json_data = open("datafile/dataset.json")
    data1 = json.load(json_data)

    # Create and save dealers
    for dealer in data1["dealers"]:
        dealer_to_save = Dealer()
        dealer_to_save.id = dealer["id"]
        dealer_to_save.name = dealer["name"]
        dealer_to_save.latitude = dealer["latitude"]
        dealer_to_save.longitude = dealer["longitude"]
        times = ""
        for time in dealer["closed"]:
            times = times + time + " "
        dealer_to_save.closed = times.rstrip()
        dealer_to_save.save()

        # Create and save vehicles
        for vehicle in dealer["vehicles"]:
            vehicle_to_save = Vehicle()
            vehicle_to_save.id = vehicle["id"]
            vehicle_to_save.dealerId = dealer_to_save
            vehicle_to_save.model = vehicle["model"]
            vehicle_to_save.fuel = vehicle["fuel"]
            vehicle_to_save.transmission = vehicle["transmission"]
            # Create availability strings
            availability_to_save = ""
            for availability in vehicle["availability"]:
                availability_to_save += availability
                times = " "
                for time in vehicle["availability"][availability]:
                    times += time + " "
                availability_to_save += times.rstrip() + "\n"
            vehicle_to_save.availability = availability_to_save
            vehicle_to_save.save()

    # Create booking
    for booking in data1["bookings"]:
        booking_to_save = Booking()
        booking_to_save.id = booking["id"]
        booking_to_save.firstName = booking["firstName"]
        booking_to_save.lastName = booking["lastName"]
        booking_to_save.vehicleId = Vehicle.objects.get(id=booking["vehicleId"])
        booking_to_save.pickupDate = datetime.strptime(booking["pickupDate"], '%Y-%m-%dT%H:%M:%S')
        booking_to_save.createdAt = datetime.strptime(booking["createdAt"], '%Y-%m-%dT%H:%M:%S.%f')
        booking_to_save.save()

    json_data.close()
