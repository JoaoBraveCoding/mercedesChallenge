from django.urls import path

from . import views

urlpatterns = [
    path('vehicles/models', views.models, name='models'),
    path('vehicles/fuels', views.fuels, name='fuels'),
    path('vehicles/transmissions', views.transmissions, name='transmissions'),
    path('vehicles/dealers', views.dealers, name='dealers'),
    path('testDrive/find', views.find_dealer, name='find_dealer'),
    path('testDrive/new', views.new_booking, name='new_booking'),
    path('testDrive/cancel', views.cancel_booking, name='cancel_booking')
]