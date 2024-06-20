# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('create-audit-report/', views.create_audit_report, name='create_audit_report'),
    path('reports/', views.audit_report_list, name='audit_report_list'),
    path('reports/<int:report_id>/', views.audit_report_detail, name='audit_report_detail'),
]
