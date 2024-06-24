from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', include('extract_data.urls')),
    path('', include('process.urls')),
    path('', include('audit_reports.urls')),
    path('', include('analysis.urls')),
]