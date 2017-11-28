# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from django import template
from django.contrib.auth.models import User, Group

# Create your views here.

from django.http import HttpResponse, Http404

#def index(request):
#    return HttpResponse("Hello, world. You're at the polls index.")

def index(request):
    nom_du_lycee="Lycée Dorian"
    return render(request, 'pages/index.html')

def home(request):
    return render(request, 'pages/home.html')


