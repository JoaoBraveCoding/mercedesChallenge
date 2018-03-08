# MB.io - SINFO Test Drive Challenge API (backend) 2018 #

## Dependencies
To be able to run the server you have to have installed the following dependencies

[0] python3.6
[1] django2.0.2
[2] django-extensions

-------------------------------------------------------------------------------

## Run the server
To run the server you have to execute the following command in the root of the project:

```
./run.sh
```
## Run the tests
To run the tests you have to execute the following command in the root of the project:

```
python manage.py test
```

-------------------------------------------------------------------------------

## API documentation
List functionality:
127.0.0.1:8000/bookingApp/vehicles/models
input: none
output:json with each model corresponding to a list of vehicles id for that model

127.0.0.1:8000/bookingApp/vehicles/fuels
input: none
output:json with each type of fuel corresponding to a list of vehicles id for that type of fuel

127.0.0.1:8000/bookingApp/vehicles/transmissions
input: none
output:json with each type of transmissions corresponding to a list of vehicles id for that type of transmissions

127.0.0.1:8000/bookingApp/vehicles/dealers
input: none
output:json with each dealers corresponding to a list of vehicles id that that dealer owns

127.0.0.1:8000/bookingApp/testDrive/find
input: model, fuel, transmission, latitude, longitude
output:json with each dealer that has the vehicle with the specified requirements organized by proximity

127.0.0.1:8000/bookingApp/testDrive/new
input: vehicleID, pickupDate, firstName, lastName
output:json with either a result or error field

127.0.0.1:8000/bookingApp/testDrive/cancel
input: id, cancelledReason
output:json with either a result or error field

-------------------------------------------------------------------------------
#Choices limitations and improvements
I chosen to implement this challenge in python because I had already implemented
a REST server in java and I wanted to lear how to do it in python.
I think the current structure of the project is not optimal for scaling and if I were
to continue to work on it I would restructure the way the code is distributed through the
files in order to have more modular code.
Regarding improvements in terms of code I would like to have implemented a rule to not
book testDrives in the past but if I had done it because of the way the project is structured
if I were to run the tests in a date after the date specified in the tests the tests would fail
I also would've liked to have implemented more efficient code because I did this project
as a side project I did not had much time to invest on it sadly.

-------------------------------------------------------------------------------
**FIM**
