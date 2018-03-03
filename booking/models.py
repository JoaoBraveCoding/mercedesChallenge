from django.db import models


class Dealer(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    name = models.CharField(max_length=200)
    latitude = models.IntegerField(default=0)
    longitude = models.IntegerField(default=0)
    closed = models.CharField(max_length=200)

    def __str__(self):
        return "id: " + self.id + "\n" + "name: " + self.name + "\n" + "location: " + str(self.latitude) + " " + str(self.longitude) + \
    "\n" + "closed: " + self.closed

class Availability(models.Model):
    key = models.CharField(max_length=200)
    value = models.CharField(max_length=200)  # TODO might need to change


class Vehicle(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    dealerId = models.ForeignKey(Dealer, on_delete=models.CASCADE)
    model = models.CharField(max_length=200)
    fuel = models.CharField(max_length=200)
    transmission = models.CharField(max_length=200)
    availability = models.ForeignKey(Availability, models.CASCADE)  # TODO might need to change
    def __str__(self):
        return "id: " + self.id

class Booking(models.Model):
    id = models.CharField(max_length=36, primary_key=True)
    vehicleId = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    firstName = models.CharField(max_length=200)
    lastName = models.CharField(max_length=200)
    pickupDate = models.DateTimeField(null=True)
    createdAt = models.DateTimeField(null=True)
    canceledAt = models.DateTimeField(null=True)
    cancelledReason = models.TextField
