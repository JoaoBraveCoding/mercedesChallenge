from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('models', views.models, name='models'),
    path('fuels', views.fuels, name='fuels'),
    path('transmissions', views.transmission, name='transmissions'),
    path('dealers', views.dealer, name='dealers')
]