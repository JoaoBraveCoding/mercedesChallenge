from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('vehicles/models', views.models, name='models'),
    path('vehicles/fuels', views.fuels, name='fuels'),
    path('vehicles/transmissions', views.transmission, name='transmissions'),
    path('dealers', views.dealer, name='dealers'),
    path('dealers/find', views.find_dealer, name='find_dealer'),
    path('new', views.new_booking, name='new_booking'),
    path('cancel', views.cancel_booking, name='cancel_booking')
]