from django.urls import path
from .views import extract_tables, display_all_table_data, download_csv

urlpatterns = [
    path('extract-tables/', extract_tables, name='extract_tables'),
    path('display-all-table-data/', display_all_table_data, name='display_all_table_data'),
    path('download-csv/', download_csv, name='download_csv'),

]
