# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.contrib.staticfiles.templatetags.staticfiles import static
import datetime

from django.shortcuts import render
from django.http import HttpResponseRedirect

# Create your views here.

from django.core.urlresolvers import reverse_lazy
from django.db import transaction
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from .models import Intervention, Client, moi, Produit
from .forms import ProduitFormSet

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from PIL import Image

pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
pdfmetrics.registerFont(TTFont('VeraIt', 'VeraIt.ttf'))
pdfmetrics.registerFont(TTFont('VeraBI', 'VeraBI.ttf'))

class InterventionList(ListView):
    model = Intervention

class ClientList(ListView):
    model = Client

class InterventionCreate(CreateView):
     model = Intervention
     fields = ['client', 'date_facture']
     success_url = reverse_lazy('intervention-list')

class ClientCreate(CreateView):
     model = Client
     fields = ['nom', 'contact', 'adresse1', 'adresse2', 'code_postal', 'ville']
     success_url = reverse_lazy('intervention-list')

class InterventionProduitCreate(CreateView):
     model = Intervention
     fields = ['client', 'date_facture']
     success_url = reverse_lazy('intervention-list')

     def get_context_data(self, **kwargs):
         data = super(InterventionProduitCreate, self).get_context_data(**kwargs)
         if self.request.POST:
             data['produit'] = ProduitFormSet(self.request.POST)
         else:
             data['produit'] = ProduitFormSet()
         return data

     def form_valid(self, form):
         context = self.get_context_data()
         produit = context['produit']
         with transaction.atomic():
             self.object = form.save()

             if produit.is_valid():
                 produit.instance = self.object
                 produit.save()
         return super(InterventionProduitCreate, self).form_valid(form)


class InterventionUpdate(UpdateView):
     model = Intervention
     success_url = reverse_lazy('intervention-list')
     fields = ['client', 'date_facture']

class ClientUpdate(UpdateView):
     model = Client
     success_url = reverse_lazy('client-list')
     fields = ['nom', 'contact', 'adresse1', 'adresse2', 'code_postal', 'ville']

class MoiUpdate(UpdateView):
     model = moi
     success_url = reverse_lazy('intervention-list')
     fields = ['nom','contact','adresse1','adresse2','code_postal','ville','tel','mail','siret','nom_rib','domiciliation_rib','code_banque_rib','code_guichet_rib','numero_compte_rib','iban_rib','code_bic_rib']
     
class InterventionProduitUpdate(UpdateView):
     model = Intervention
     fields = ['client', 'date_facture']
     success_url = reverse_lazy('intervention-list')

     def get_context_data(self, **kwargs):
         data = super(InterventionProduitUpdate, self).get_context_data(**kwargs)
         if self.request.POST:
             data['produit'] = ProduitFormSet(self.request.POST, instance=self.object)
         else:
             data['produit'] = ProduitFormSet(instance=self.object)
         return data

     def form_valid(self, form):
         context = self.get_context_data()
         Produit = context['produit']
         with transaction.atomic():
             self.object = form.save()

             if Produit.is_valid():
                 Produit.instance = self.object
                 Produit.save()
         return super(InterventionProduitUpdate, self).form_valid(form)

class InterventionDelete(DeleteView):
     model = Intervention
     success_url = reverse_lazy('intervention-list')

class ClientDelete(DeleteView):
     model = Client
     success_url = reverse_lazy('client-list')

def InterventionPDF(request, pk):
    intervention_pdf=Intervention.objects.get(pk=pk)
    ref_facture='FA{0:06}'.format(intervention_pdf.pk)
    moi_pdf=moi.objects.get(pk=1)
    client_pdf=Client.objects.get(nom=intervention_pdf.client)
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Facture {}.pdf"'. format(ref_facture)

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    url_image = 'static/pages/img/logo.png'
    p.drawImage(url_image, 50, 700, width=122, height=60, mask='auto')
    p.setFont('VeraBd', 10)
    ypos=750
    p.drawString(350, ypos, 'Facture N° {}'.format(ref_facture))
    p.setFont('Vera', 10)
    date_echeance=intervention_pdf.date_facture+ datetime.timedelta(30)
    date_fact=intervention_pdf.date_facture.strftime('%d/%m/%Y')
    date_ech=date_echeance.strftime('%d/%m/%Y')
    p.drawString(350, ypos-20, 'Date')
    p.drawString(350, ypos-40, 'Echéance')
    p.drawString(450, ypos-20, date_fact)
    p.drawString(450, ypos-40, date_ech)
    p.setFont('VeraBd', 10)
    ypos=650
    xpos=50
    int=20
    p.drawString(xpos, ypos, moi_pdf.nom)
    p.setFont('Vera', 10)
    ypos-=int
    if (moi_pdf.contact is not ""):
            p.drawString(xpos, ypos, str(ypos))
            ypos-=int
    if (moi_pdf.adresse1 is not ""):
            p.drawString(xpos, ypos, moi_pdf.adresse1)
            ypos-=int
    if (moi_pdf.adresse2 is not ""):
            p.drawString(xpos, ypos, moi_pdf.adresse2)
            ypos-=int
    if (moi_pdf.code_postal is not "" and moi_pdf.ville is not "" ):
            p.drawString(xpos, ypos, moi_pdf.code_postal)
            p.drawString(xpos+40, ypos, moi_pdf.ville)
            ypos-=int
    if (moi_pdf.tel is not ""):
            p.drawString(xpos, ypos, 'Téléphone: {}'.format(moi_pdf.tel))
            ypos-=int
    if (moi_pdf.mail is not ""):
            p.drawString(xpos, ypos, 'Mail: {}'.format(moi_pdf.mail))
            ypos-=int
    if (moi_pdf.siret is not ""):
            p.drawString(xpos, ypos, 'SIRET: {}'.format(moi_pdf.siret))
            ypos-=int

    p.setFont('VeraBd', 10)
    ypos=650
    xpos=350
    p.drawString(xpos, ypos, client_pdf.nom)
    p.setFont('Vera', 10)
    ypos-=int
    if (client_pdf.contact is not ""):
            p.drawString(xpos, ypos, client_pdf.contact)
            ypos-=int
    if (client_pdf.adresse1 is not ""):
            p.drawString(xpos, ypos, client_pdf.adresse1)
            ypos-=int
    if (client_pdf.adresse2 is not ""):
            p.drawString(xpos, ypos, client_pdf.adresse2)
            ypos-=int
    if (client_pdf.code_postal is not "" and client_pdf.ville is not ""):
            p.drawString(xpos, ypos, client_pdf.code_postal)
            p.drawString(xpos+40, ypos, client_pdf.ville)
            ypos-=int

    ypos-=20
    xpos=50
    int=15
    p.setFont('Vera', 10)
    ypos-=int
    if (moi_pdf.nom_rib is not ""):
            p.drawString(xpos, ypos, 'Titulaire du compte: {}'.format(moi_pdf.nom_rib))
            ypos-=int
    if (moi_pdf.domiciliation_rib is not ""):
            p.drawString(xpos, ypos, 'Domiciliation: {}'.format(moi_pdf.domiciliation_rib))
            ypos-=int
    if (moi_pdf.code_banque_rib is not "" and moi_pdf.code_guichet_rib is not ""):
            p.drawString(xpos, ypos, 'Code banque: {}/ Code guichet: {}'.format(moi_pdf.code_banque_rib,moi_pdf.code_guichet_rib))
            ypos-=int
    if (moi_pdf.numero_compte_rib is not ""):
            p.drawString(xpos, ypos, 'Numéro de compte: {}'.format(moi_pdf.numero_compte_rib))
            ypos-=int
    if (moi_pdf.iban_rib is not ""):
            p.drawString(xpos, ypos, 'Code IBAN: {}'.format(moi_pdf.iban_rib))
            ypos-=int
    if (moi_pdf.code_bic_rib is not ""):
            p.drawString(xpos, ypos, 'Code BIC: {}'.format(moi_pdf.code_bic_rib))
            ypos-=int

    ypos-=100

    width, height = A4

    data= [['Description', 'Date', 'Prix unitaire', 'Quantite', 'Montant Net']]
    total=0
    end_line=2

    for produit in Produit.objects.filter(intervention=pk).order_by('date_produit'):
        end_line+=1
        montant=produit.prix_unitaire*produit.quantite
        total+=montant
        data.append([produit.nom,produit.date_produit.strftime('%d/%m/%Y'),produit.prix_unitaire,produit.quantite,str(montant)+' €'])

    data.append(["","","","",""])
    data.append(["","","",'Net à payer',str(total)+' €'])

    table = Table(data, colWidths=[6. * cm, 3. * cm, 2.5 * cm, 2.5 * cm, 3. * cm])
    table.setStyle(TableStyle([('BACKGROUND',(0,0),(4,0),colors.gray), ('TEXTCOLOR',(0,0),(4,0),colors.white),
                               ('FONT',(3,end_line),(4,end_line),'VeraBd'),('ALIGN', (1, 0), (4, end_line), 'CENTER')]))
    table.wrapOn(p, width, height)
    table.drawOn(p, 50, ypos)

    ypos-=15*end_line
    int=10
    p.setFont('Vera', 6)
    p.drawString(50, ypos, 'TVA non applicable, art. 293 B du CGI.')
    ypos-=int
    p.drawString(50, ypos, 'Dispensé d\'immatriculation en application de l\'article L.123-1-1 du code de commerce.')
    ypos-=int
    p.drawString(50, ypos, 'En cas de retard de paiement, une pénalité égale à 3 fois le taux d\'intérêt légal sera exigible (Décret 2009-138 du 9 février 2009).')
    ypos-=int
    p.drawString(50, ypos, 'Pour les professionnels, une indemnité minimum forfaitaire de 40 euros pour frais de recouvrement sera exigible (Décret 2012-1115 du 9 octobre 2012).')
    ypos-=int
    p.drawString(50, ypos, 'Pas d’escompte pour règlement par anticipation.')
    ypos-=int
    p.drawString(50, ypos, 'Conditions de paiement: 30 jours')

    p.setFont('Vera', 10)
    ypos-=20
    p.drawString(50, ypos, 'A l\'intention de : {}'.format(client_pdf.contact))

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    return response


