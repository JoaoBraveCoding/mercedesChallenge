from django.db import models


class Dealer(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    name = models.CharField(max_length=200)
    latitude = models.IntegerField(default=0)
    longitude = models.IntegerField(default=0)
    # vehicles = models.ForeignKey(Car, on_delete=models.CASCADE) #TODO might need to change
    closed = models.CharField(max_length=200)  # TODO might need to change


class Availability(models.Model):
    key = models.CharField(max_length=200)
    value = models.CharField(max_length=200)  # TODO might need to change


class Vehicle(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    dealerId = models.ForeignKey(Dealer, on_delete=models.CASCADE)  # TODO might need to change
    model = models.CharField(max_length=200)
    fuel = models.CharField(max_length=200)
    transmission = models.CharField(max_length=200)
    availability = models.ForeignKey(Availability, models.CASCADE)  # TODO might need to change


class Booking(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    vehicleId = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    firstName = models.CharField(max_length=200)
    lastName = models.CharField(max_length=200)
    pickupDate = models.DateTimeField
    createdAt = models.DateTimeField
    canceledAt = models.DateTimeField
    cancelledReason = models.TextField
