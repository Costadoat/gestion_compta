# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.InterventionList.as_view(), name='intervention-list'),
    url(r'add/$', views.InterventionProduitCreate.as_view(), name='intervention-add'),
    url(r'clients/$', views.ClientList.as_view(), name='client-list'),
    url(r'clients/(?P<pk>[0-9]+)/$', views.ClientUpdate.as_view(), name='client-update'),
    url(r'clients/(?P<pk>[0-9]+)/delete/$', views.ClientDelete.as_view(), name='client-delete'),
    url(r'clients/new/$', views.ClientCreate.as_view(), name='client-add'),
    url(r'mon_compte/(?P<pk>[0-9]+)/$', views.MoiUpdate.as_view(), name='moi-update'),
    url(r'(?P<pk>[0-9]+)/$', views.InterventionProduitUpdate.as_view(), name='intervention-update'),
    url(r'(?P<pk>[0-9]+)/delete/$', views.InterventionDelete.as_view(), name='intervention-delete'),
    url(r'(?P<pk>[0-9]+)/pdf/$', views.InterventionPDF, name='intervention-pdf'),
]
