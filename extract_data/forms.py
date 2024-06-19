# forms.py
from django import forms

class DatabaseConnectionForm(forms.Form):
    db_type = forms.CharField(max_length=100)
    db_host = forms.CharField(max_length=100)
    db_name = forms.CharField(max_length=100)
    db_user = forms.CharField(max_length=100)
    db_password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    db_port = forms.IntegerField(required=False)
