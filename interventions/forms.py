# -*- coding: utf-8 -*-

from django.forms import ModelForm, inlineformset_factory

from .models import Intervention, Produit, Client


class ClientForm(ModelForm):
     class Meta:
         model = Client
         exclude = ()
                               
class InterventionForm(ModelForm):
     class Meta:
         model = Intervention
         exclude = ()


class ProduitForm(ModelForm):
    class Meta:
        model = Produit
        exclude = ()

ProduitFormSet = inlineformset_factory(Intervention, Produit,
                                            form=ProduitForm, extra=1)
