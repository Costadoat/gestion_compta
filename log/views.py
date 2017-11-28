# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

# Create your views here.
# this login required decorator is to not allow to any
# view without authenticating

@login_required(login_url="login/")
def home(request):
    return render(request,"/")

#@register.filter(name='has_group')
def has_group(user, group_name):
    group =  Group.objects.get(name=group_name)
    return group in user.groups.all()
