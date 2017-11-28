# -*- coding: utf-8 -*-
# from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.forms import AuthenticationForm


# If you don't do this you cannot use Bootstrap CSS
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Utilisateur", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Mot de passe", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'password', 'name': 'password'}))
