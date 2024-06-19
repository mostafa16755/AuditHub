from django.urls import path
from .views import upload_csv, process_csv

urlpatterns = [
    path('upload-csv/', upload_csv, name='upload_csv'),
    path('process-csv/', process_csv, name='process_csv'),
]
