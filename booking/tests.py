import json

from django.test import TestCase, RequestFactory

from .models import Vehicle, Dealer, Booking
from .views import models, fuels, transmissions, dealers, find_dealer, new_booking, cancel_booking
from datetime import datetime


class ListTestCase(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()

        # Create and save some dealers
        dealer = Dealer.objects.create(id="1", name="Rodrigues Dealers", latitude=0, longitude=0,
                                       closed="monday\ntuesday")
        dealer.save()
        dealer = Dealer.objects.create(id="2", name="Semedo Dealers", latitude=-90, longitude=180,
                                       closed="tuesday\nwednesday")
        dealer.save()
        dealer = Dealer.objects.create(id="3", name="Fermoselle Dealers", latitude=90, longitude=90,
                                       closed="thursday\nsaturday")
        dealer.save()
        dealer = Dealer.objects.create(id="4", name="Marçal Dealers", latitude=60, longitude=-180,
                                       closed="sunday\nfriday")
        dealer.save()

        # Create and save some vehicles
        vehicle = Vehicle.objects.create(id="1", dealerId=Dealer.objects.get(id="1"), model="AMG", transmission="AUTO",
                                         fuel="GASOLINE", availability="wednesday 1000 1100\nfriday 1000 1030")
        vehicle.save()
        vehicle = Vehicle.objects.create(id="2", dealerId=Dealer.objects.get(id="1"), model="A", transmission="MANUAL",
                                         fuel="DIESEL", availability="wednesday 1000 1100\nsunday 0800 0830")
        vehicle.save()
        vehicle = Vehicle.objects.create(id="3", dealerId=Dealer.objects.get(id="1"), model="E", transmission="AUTO",
                                         fuel="ELECTRIC", availability="wednesday 1000 1100\nsaturday 1300 1800")
        vehicle.save()
        vehicle = Vehicle.objects.create(id="4", dealerId=Dealer.objects.get(id="2"), model="AMG",
                                         transmission="MANUAL",
                                         fuel="GASOLINE", availability="thursday 1200 2300\nmonday 0600 1500")
        vehicle.save()
        vehicle = Vehicle.objects.create(id="5", dealerId=Dealer.objects.get(id="2"), model="A", transmission="MANUAL",
                                         fuel="DIESEL", availability="thursday 1000 1100\nsaturday 0800 0900\n"
                                                                     "sunday 0800 1000")
        vehicle.save()
        vehicle = Vehicle.objects.create(id="6", dealerId=Dealer.objects.get(id="2"), model="AMG",
                                         transmission="MANUAL",
                                         fuel="DIESEL", availability="thursday 1000 1100\nfriday 1800 1900")
        vehicle.save()
        vehicle = Vehicle.objects.create(id="7", dealerId=Dealer.objects.get(id="3"), model="E", transmission="AUTO",
                                         fuel="ELECTRIC", availability="tuesday 1000 1100\nwednesday 1400 1430")
        vehicle.save()
        vehicle = Vehicle.objects.create(id="8", dealerId=Dealer.objects.get(id="3"), model="E", transmission="AUTO",
                                         fuel="ELECTRIC", availability="tuesday 1100 1300\nfriday 0300 2000")
        vehicle.save()
        vehicle = Vehicle.objects.create(id="9", dealerId=Dealer.objects.get(id="3"), model="AMG",
                                         transmission="MANUAL",
                                         fuel="GASOLINE", availability="tuesday 0900 1400\n")
        vehicle.save()
        vehicle = Vehicle.objects.create(id="10", dealerId=Dealer.objects.get(id="4"), model="A", transmission="AUTO",
                                         fuel="DIESEL", availability="monday 1000 1100")
        vehicle.save()
        vehicle = Vehicle.objects.create(id="11", dealerId=Dealer.objects.get(id="4"), model="AMG",
                                         transmission="MANUAL",
                                         fuel="GASOLINE", availability="wednesday 1000 1100")
        vehicle.save()
        vehicle = Vehicle.objects.create(id="12", dealerId=Dealer.objects.get(id="3"), model="AMG",
                                         transmission="MANUAL",
                                         fuel="DIESEL", availability="monday 1000 1100")
        vehicle.save()

        # Create some bookings
        booking = Booking.objects.create(id="1", vehicleId=Vehicle.objects.get(id="1"), firstName="Jse", lastName="Ana",
                                         pickupDate=datetime.strptime('2018-03-16T10:00:00', '%Y-%m-%dT%H:%M:%S'),
                                         createdAt=datetime.now())
        booking.save()
        booking = Booking.objects.create(id="2", vehicleId=Vehicle.objects.get(id="3"), firstName="Manuel",
                                         lastName="Rambo",
                                         pickupDate=datetime.strptime('2018-03-28T10:00:00', '%Y-%m-%dT%H:%M:%S'),
                                         createdAt=datetime.now(),
                                         canceledAt=datetime.strptime('2018-03-23T10:00:00', '%Y-%m-%dT%H:%M:%S'),
                                         cancelledReason="Dentist")
        booking.save()

    def test_models_list(self):
        request = self.factory.get('/bookingApp/vehicles/models/')
        response = models(request)
        body_unicode = response.content.decode('utf-8')
        body = json.loads(body_unicode)
        self.assertTrue("models" in body)
        content = body['models']
        self.assertTrue("AMG" in content)
        self.assertTrue("E" in content)
        self.assertTrue("A" in content)
        self.assertTrue("1" in content['AMG'])
        self.assertTrue("10" in content['A'])
        self.assertTrue("7" in content['E'])
        self.assertFalse("1" in content['E'])

    def test_fuels_list(self):
        request = self.factory.get('/bookingApp/vehicles/fuels/')
        response = fuels(request)
        body_unicode = response.content.decode('utf-8')
        body = json.loads(body_unicode)
        self.assertTrue("fuels" in body)
        content = body['fuels']
        self.assertTrue("GASOLINE" in content)
        self.assertTrue("DIESEL" in content)
        self.assertTrue("ELECTRIC" in content)
        self.assertTrue("11" in content['GASOLINE'])
        self.assertTrue("9" in content['GASOLINE'])
        self.assertTrue("10" in content['DIESEL'])
        self.assertTrue("6" in content['DIESEL'])
        self.assertTrue("7" in content['ELECTRIC'])
        self.assertTrue("8" in content['ELECTRIC'])

    def test_transmissions_list(self):
        request = self.factory.get('/bookingApp/vehicles/transmissions/')
        response = transmissions(request)
        body_unicode = response.content.decode('utf-8')
        body = json.loads(body_unicode)
        self.assertTrue("transmissions" in body)
        content = body['transmissions']
        self.assertTrue("AUTO" in content)
        self.assertTrue("MANUAL" in content)
        self.assertTrue("1" in content['AUTO'])
        self.assertTrue("10" in content['AUTO'])
        self.assertTrue("11" in content['MANUAL'])
        self.assertTrue("9" in content['MANUAL'])

    def test_dealer_list(self):
        request = self.factory.get('/bookingApp/vehicles/dealers/')
        response = dealers(request)
        body_unicode = response.content.decode('utf-8')
        body = json.loads(body_unicode)
        self.assertTrue("dealers" in body)
        content = body['dealers']
        self.assertTrue("1" in content)
        self.assertTrue("2" in content)
        self.assertTrue("3" in content)
        self.assertTrue("4" in content)
        self.assertTrue("1" in content['1'])
        self.assertTrue("4" in content['2'])
        self.assertTrue("8" in content['3'])
        self.assertTrue("10" in content['4'])

    def test_find_dealer(self):
        request = self.factory.get('/bookingApp/testDrive/find/', HTTP_MODEL="AMG", HTTP_FUEL="DIESEL",
                                   HTTP_TRANSMISSION="MANUAL", HTTP_LATITUDE="38.736819", HTTP_LONGITUDE="-9.138705")
        response = find_dealer(request)
        body_unicode = response.content.decode('utf-8')
        body = json.loads(body_unicode)
        self.assertTrue("dealers" in body)
        content = body['dealers']
        self.assertTrue(len(content) == 2)
        self.assertTrue(content[0]['id'] == "3")
        self.assertTrue(content[1]['id'] == "2")

    def test_new_booking(self):
        request = self.factory.get('/bookingApp/testDrive/new/',
                                   HTTP_PICKUPDATE='2018-03-14T10:00:00',
                                   HTTP_VEHICLEID="1",
                                   HTTP_FIRSTNAME="DANIEL", HTTP_LASTNAME="TESLA")
        response = new_booking(request)
        body_unicode = response.content.decode('utf-8')
        body = json.loads(body_unicode)
        self.assertTrue("return" in body)
        content = body['return']
        self.assertEquals(content, "Test drive booked success")

    def test_new_booking_not_good_pick_up(self):
        request = self.factory.get('/bookingApp/testDrive/new/',
                                   HTTP_PICKUPDATE='2018-03-15T10:00:00',
                                   HTTP_VEHICLEID="1",
                                   HTTP_FIRSTNAME="DANIEL", HTTP_LASTNAME="TESLA")
        response = new_booking(request)
        body_unicode = response.content.decode('utf-8')
        body = json.loads(body_unicode)
        self.assertTrue("error" in body)
        content = body['error']
        self.assertEquals(content, "The vehicle you requested is not available at the time you requested")

    def test_new_booking_double_booking(self):
        request = self.factory.get('/bookingApp/testDrive/new/',
                                   HTTP_PICKUPDATE='2018-03-16T10:00:00',
                                   HTTP_VEHICLEID="1",
                                   HTTP_FIRSTNAME="DANIEL", HTTP_LASTNAME="TESLA")
        response = new_booking(request)
        body_unicode = response.content.decode('utf-8')
        body = json.loads(body_unicode)
        self.assertTrue("error" in body)
        content = body['error']
        self.assertEquals(content, "There is already a test drive for that time and vehicle")

    def test_cancel_booking(self):
        request = self.factory.get('/bookingApp/testDrive/cancel/',
                                   HTTP_ID='1',
                                   HTTP_CANCELLEDREASON="Operation")
        response = cancel_booking(request)
        body_unicode = response.content.decode('utf-8')
        body = json.loads(body_unicode)
        self.assertTrue("return" in body)
        content = body['return']
        self.assertEquals(content, "Test drive canceled successfully")

    def test_double_cancel_booking(self):
        request = self.factory.get('/bookingApp/testDrive/cancel/',
                                   HTTP_ID='2',
                                   HTTP_CANCELLEDREASON="Operation")
        response = cancel_booking(request)
        body_unicode = response.content.decode('utf-8')
        body = json.loads(body_unicode)
        self.assertTrue("error" in body)
        content = body['error']
        self.assertEquals(content, "Booking already canceled")


class ListTestCaseNotPopulated(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_models_list(self):
        request = self.factory.get('/booking/vehicles/models/')
        response = models(request)
        body_unicode = response.content.decode('utf-8')
        body = json.loads(body_unicode)
        self.assertTrue("models" in body)
        content = body['models']
        self.assertTrue(len(content) == 0)

    def test_fuels_list(self):
        request = self.factory.get('/booking/vehicles/fuels/')
        response = fuels(request)
        body_unicode = response.content.decode('utf-8')
        body = json.loads(body_unicode)
        self.assertTrue("fuels" in body)
        content = body['fuels']
        self.assertTrue(len(content) == 0)

    def test_transmissions_list(self):
        request = self.factory.get('/booking/vehicles/transmissions/')
        response = transmissions(request)
        body_unicode = response.content.decode('utf-8')
        body = json.loads(body_unicode)
        self.assertTrue("transmissions" in body)
        content = body['transmissions']
        self.assertTrue(len(content) == 0)

    def test_dealers_list(self):
        request = self.factory.get('/booking/vehicles/dealers/')
        response = dealers(request)
        body_unicode = response.content.decode('utf-8')
        body = json.loads(body_unicode)
        self.assertTrue("dealers" in body)
        content = body['dealers']
        self.assertTrue(len(content) == 0)

    def test_find_dealer(self):
        request = self.factory.get('/bookingApp/testDrive/find/', HTTP_MODEL="AMG", HTTP_FUEL="GASOLINE",
                                   HTTP_TRANSMISSION="AUTO", HTTP_LATITUDE="38.736819", HTTP_LONGITUDE="-9.138705")
        response = find_dealer(request)
        body_unicode = response.content.decode('utf-8')
        body = json.loads(body_unicode)
        self.assertTrue("dealers" in body)
        content = body['dealers']
        self.assertTrue(len(content) == 0)

    def test_find_dealer_no_params(self):
        request = self.factory.get('/bookingApp/testDrive/find/')
        response = find_dealer(request)
        body_unicode = response.content.decode('utf-8')
        body = json.loads(body_unicode)
        self.assertTrue("error" in body)

    def test_new_booking(self):
        request = self.factory.get('/bookingApp/testDrive/new/',
                                   HTTP_PICKUPDATE='2018-03-14T10:00:00',
                                   HTTP_VEHICLEID="1",
                                   HTTP_FIRSTNAME="DANIEL", HTTP_LASTNAME="TESLA")
        response = new_booking(request)
        body_unicode = response.content.decode('utf-8')
        body = json.loads(body_unicode)
        self.assertTrue(response.status_code == 412)
        self.assertTrue("error" in body)

    def test_new_booking_no_params(self):
        request = self.factory.get('/bookingApp/testDrive/new/')
        response = new_booking(request)
        body_unicode = response.content.decode('utf-8')
        body = json.loads(body_unicode)
        self.assertTrue(response.status_code == 412)
        self.assertTrue("error" in body)

    def test_cancel_booking(self):
        request = self.factory.get('/bookingApp/testDrive/cancel/',
                                   HTTP_ID='1',
                                   HTTP_CANCELLEDREASON="Operation")
        response = cancel_booking(request)
        body_unicode = response.content.decode('utf-8')
        body = json.loads(body_unicode)
        self.assertTrue("error" in body)
        content = body['error']
        self.assertEquals(content, "No booking for the given ID")

    def test_cancel_booking_no_params(self):
        request = self.factory.get('/bookingApp/testDrive/cancel/')
        response = cancel_booking(request)
        body_unicode = response.content.decode('utf-8')
        body = json.loads(body_unicode)
        self.assertTrue("error" in body)
