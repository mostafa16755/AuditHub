# forms.py
from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import CustomUser

class SignupForm(forms.Form):
    username = forms.CharField(label='Username', max_length=150)
    name = forms.CharField(label='Name', max_length=100)
    id = forms.CharField(label='ID', max_length=100)
    email = forms.EmailField(label='Email', max_length=254)
    company = forms.CharField(label='Company', max_length=500)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)