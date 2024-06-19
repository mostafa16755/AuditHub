# app/urls.py

from django.urls import path
from .views import analyse_data,CSVdisplaying

urlpatterns = [
    path('analyse/', analyse_data, name='analyse_data'),
    path("csv/",CSVdisplaying,name="csv"),
]
