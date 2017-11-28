# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Register your models here.
from django.contrib import admin

from .models import Intervention, Produit, Client

admin.site.register(Intervention)
admin.site.register(Produit)
admin.site.register(Client)