from django.db import models
import json


class Dealer(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    name = models.CharField(max_length=200)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    closed = models.CharField(max_length=200)

    def __str__(self):
        return "id: " + self.id + "\n" + "name: " + self.name + "\n" + "location: " + str(self.latitude) + " " + str(
            self.longitude) + \
               "\n" + "closed: " + self.closed


class Vehicle(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    dealerId = models.ForeignKey(Dealer, on_delete=models.CASCADE)
    model = models.CharField(max_length=200)
    fuel = models.CharField(max_length=200)
    transmission = models.CharField(max_length=200)
    availability = models.TextField(null=True)

    def __str__(self):
        return "id: " + self.id

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

class Booking(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    vehicleId = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    firstName = models.CharField(max_length=200)
    lastName = models.CharField(max_length=200)
    pickupDate = models.DateTimeField(null=True)
    createdAt = models.DateTimeField(null=True)
    canceledAt = models.DateTimeField(null=True)
    cancelledReason = models.TextField(null=True)
