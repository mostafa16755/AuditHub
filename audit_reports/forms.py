from django import forms
from .models import AuditReport

class AuditReportForm(forms.ModelForm):
    class Meta:
        model = AuditReport
        fields = ['company', 'content', 'addressee', 'introductory_paragraph', 
                  'managements_responsibility', 'auditors_responsibility',
                  'scope_paragraph', 'opinion_paragraph', 'basis_of_opinion']
