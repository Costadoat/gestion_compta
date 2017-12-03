# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse

from django.db import models
from django.utils import timezone

class moi(models.Model):
    nom = models.CharField(max_length=100)
    contact = models.CharField(max_length=100,blank=True)
    adresse1 = models.CharField(max_length=100)
    adresse2 = models.CharField(max_length=100,blank=True)
    code_postal = models.CharField(max_length=100)
    ville = models.CharField(max_length=100)
    tel = models.CharField(max_length=100)
    mail = models.EmailField(max_length=100)
    siret = models.CharField(max_length=100)
    nom_rib = models.CharField(max_length=100)
    domiciliation_rib = models.CharField(max_length=100)
    code_banque_rib = models.CharField(max_length=100)
    code_guichet_rib = models.CharField(max_length=100)
    numero_compte_rib = models.CharField(max_length=100)
    iban_rib = models.CharField(max_length=100)
    code_bic_rib = models.CharField(max_length=100)
    def __unicode__(self):
        return "%s" % (self.nom)

class Client(models.Model):
    nom = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    adresse1 = models.CharField(max_length=100)
    adresse2 = models.CharField(max_length=100,blank=True)
    code_postal = models.CharField(max_length=100)
    ville = models.CharField(max_length=100)
    def __unicode__(self):
        return "%s" % (self.nom)

class Intervention(models.Model):
    client = models.ForeignKey(Client)
    date_facture = models.DateField(default=timezone.now)

    def get_absolute_url(self):
        return reverse('intervention-update', kwargs={'pk': self.pk})

    def __unicode__(self):
        return "%s %s" % (self.client, self.date_facture)

class Produit(models.Model):
    intervention = models.ForeignKey(Intervention)
    nom = models.CharField(max_length=100)
    date_produit = models.DateField(default=timezone.now)
    prix_unitaire = models.FloatField()
    quantite = models.FloatField()
