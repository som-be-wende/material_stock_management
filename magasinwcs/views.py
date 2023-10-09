import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import capwords
from django.conf import settings
from django.core.mail import send_mail , EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from soupsieve.util import lower

from smtplib import SMTP_SSL
from email.message import EmailMessage
import pandas as pd
from pretty_html_table import build_table

from magasinwcs.models import *


# Create your views here.


def send_mail(body):
    SENDER_EMAIL = '******@gmail.com'
    MAIL_PASSWORD = '******'
    RECEIVER_EMAIL = '******@gmail.com'

    message = MIMEMultipart()
    message['Subject'] = 'Nouvelle Commande'
    
    body_content = body
    message.attach(MIMEText(body_content, "html"))
    msg_body = message.as_string()
    
    server = SMTP_SSL('smtp.gmail.com')
    server.login(SENDER_EMAIL,MAIL_PASSWORD)
    server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg_body)
    #
    server.quit()

def login(request):
    if len(request.POST) > 0:
        e_mail = lower(request.POST.get('e-mail').strip())
        password = request.POST.get('password').strip()
        result = Employe.objects.filter(email=e_mail, password=password)
        if len(result) > 0:
            user = Employe.objects.get(email=e_mail)
            request.session['user'] = user.id
            return redirect('gestion_materiel')
        else:
            return HttpResponse("Adresse et/ou Mot de passe incorrect", status=409)
    return render(request, 'magasinwcs/login.html')


def deconnxion(request):
    del request.session['user']
    return redirect('login')


def gestion_materiel(request):
    if 'user' in request.session:
        if 'categorie' in request.POST:
            categorie_pk = request.POST.get("categorie")
            categorie = get_object_or_404(Categorie, pk=categorie_pk)
            if categorie.nom == ".Global":
                materiels = Materiel.objects.all().order_by('nom','description')
            else:
                materiels = Materiel.objects.filter(categorie=categorie).order_by('nom','description')
            context = {}
            context["materiels"] = materiels
            context["glob"] = get_object_or_404(Categorie, pk=categorie_pk)
        else:
            context = {}
            context["materiels"] = Materiel.objects.all().order_by('nom','description')
            context["glob"] = Categorie.get_default_categorie()

        context["categories"] = Categorie.objects.all().order_by('nom')
        context["user"] = Employe.objects.get(pk=request.session.get('user'))
        return render(request, 'magasinwcs/gestion_materiel.html', context=context)
    else:
        return redirect('login')


def add_categorie(request):
    categorie_name = capwords(request.POST.get("categorie-nom").strip())
    if categorie_name == '':
        return HttpResponse("Entrer une valeur", status=409)
    categorie, created = Categorie.objects.get_or_create(nom=categorie_name)
    if not created:
        return HttpResponse("La categorie existe déjà", status=409)
    return redirect('gestion_materiel')


def delete_categorie(request):
    categorie_pk = (request.POST.get("categorie_pk"))
    categorie = get_object_or_404(Categorie, pk=categorie_pk)
    if categorie.nom != ".Global":
        categorie.delete()
    return redirect("gestion_materiel")


def add_materiel(request):
    categorie_pk = request.POST.get("categorie")
    categorie = get_object_or_404(Categorie, pk=categorie_pk)
    if categorie.nom == ".Global":
        return HttpResponse("SELCTIONNER/AJOUTER UNE CATEGORIE", status=409)
    materiel_id = str(request.POST.get("materiel-id").strip())
    nom = str(request.POST.get("materiel-nom").strip())
    description = str(request.POST.get("materiel-description").strip())
    if materiel_id == '' or nom == '':
        return HttpResponse("Remplissez les champs", status=409)
    materiel, created = Materiel.objects.get_or_create(id=materiel_id, nom=nom,
                                                       description=description,
                                                       categorie=categorie)
    if not created:
        return HttpResponse("Ce materiel existe déjà", status=409)

    context = {}
    context["categories"] = Categorie.objects.all().order_by('nom')
    context["materiels"] = Materiel.objects.all().order_by('nom','description')
    context["glob"] = Categorie.get_default_categorie()
    context["user"] = Employe.objects.get(pk=request.session.get('user'))
    context["mat"] = 'mat'
    return render(request, 'magasinwcs/gestion_materiel.html', context=context)



def delete_materiel(request, materiel_pk):
    materiel = get_object_or_404(Materiel, pk=materiel_pk)
    materiel.delete()
    return HttpResponse("")


def materiel_update(request):
    if 'user' in request.session:
        if len(request.GET) > 0:
            materiel_pk = request.GET.get('materiel_pk')
            materiel = get_object_or_404(Materiel, id=materiel_pk)
            materiel.nom = request.GET.get('nom').strip()
            materiel.prix_unitaire = int(request.GET.get('prix_unitaire').strip())
            materiel.description = request.GET.get('description').strip()
            categorie_pk = request.GET.get('categorie')
            categorie = get_object_or_404(Categorie, pk=categorie_pk)
            materiel.categorie = categorie
            if materiel_pk != request.GET.get('id').strip():
                materiel.id = request.GET.get('id').strip()
                materiel.save()
                Materiel.objects.filter(id=materiel_pk).delete()
            else:
                materiel.save()
            return redirect('gestion_materiel')
        materiel_id = request.POST.get('materiel_pk')
        materiel = get_object_or_404(Materiel, id=materiel_id)
        categories = Categorie.objects.exclude(nom='.Global')
        user = Employe.objects.get(pk=request.session.get('user'))
        return render(request, 'magasinwcs/materiel_update.html',
                      context={'materiel': materiel, 'categories': categories, 'user': user})
    else:
        return redirect('login')


def gestion_employe(request):
    if 'user' in request.session:
        if 'fonction' in request.POST:
            fonction_pk = request.POST.get("fonction")
            fonction = get_object_or_404(Fonction, pk=fonction_pk)
            if fonction.nom == ".Global":
                employes = Employe.objects.all().order_by('nom','prenom')
            else:
                employes = Employe.objects.filter(fonction=fonction).order_by('nom','prenom')
            context = {}
            context["employes"] = employes
            context["glob"] = get_object_or_404(Fonction, pk=fonction_pk)
        else:
            context = {}
            context["employes"] = Employe.objects.all().order_by('nom','prenom')
            context["glob"] = Fonction.get_default_fonction()

        context["fonctions"] = Fonction.objects.all().order_by('nom')
        context["user"] = Employe.objects.get(pk=request.session.get('user'))
        return render(request, 'magasinwcs/gestion_employe.html', context=context)
    else:
        return redirect('login')


def add_fonction(request):
    fonction_nom = capwords(request.POST.get("fonction-nom").strip())
    if fonction_nom == '':
        return HttpResponse("Entrer une valeur", status=409)
    fonction, created = Fonction.objects.get_or_create(nom=fonction_nom)
    if not created:
        return HttpResponse("La fonction existe déjà", status=409)

    return redirect('gestion_employe')


def delete_fonction(request):
    fonction_pk = (request.POST.get("fonction_pk"))
    fonction = get_object_or_404(Fonction, pk=fonction_pk)
    if fonction.nom != ".Global":
        fonction.delete()
    return redirect("gestion_employe")


def add_employe(request):
    fonction_pk = request.POST.get("fonction")
    fonction = get_object_or_404(Fonction, pk=fonction_pk)
    if fonction.nom == ".Global":
        return HttpResponse("SELCTIONNER/AJOUTER UNE FONCTION", status=409)
    nom = request.POST.get("employe-nom").strip()
    prenom = request.POST.get("employe-prenom").strip()
    if prenom == '' or nom == '':
        return HttpResponse("Remplissez les champs", status=409)
    employe, created = Employe.objects.get_or_create(nom=nom, prenom=prenom, fonction=fonction)
    if not created:
        return HttpResponse("Cet personne existe déjà", status=409)
    
    context = {}
    context["fonctions"] = (Fonction.objects.all().order_by('nom'))
    context["employes"] = (Employe.objects.all().order_by('nom','prenom'))
    context["glob"] = Fonction.get_default_fonction()
    context["user"] = Employe.objects.get(pk=request.session.get('user'))
    context["emp"] = 'emp'

    return render(request, 'magasinwcs/gestion_employe.html', context=context)

def get_employe(request, fonction_pk):
    fonction = get_object_or_404(Fonction, pk=fonction_pk)
    if fonction.nom == ".Global":
        employes = (Employe.objects.all().order_by('nom','prenom'))
    else:
        employes = (fonction.employe_set.all().order_by('nom'))
    return render(request, 'magasinwcs/liste_employe.html', context={"employes": employes})


def delete_employe(request, employe_pk):
    employe = get_object_or_404(Employe, id=employe_pk)
    admin = Administrateur.objects.filter(employe=employe)
    if len(admin) > 0:
        return HttpResponse("Impossible de supprimer un administrateur", status=409)
    else:
        employe.delete()
        return HttpResponse("")


def employe_update(request):
    if 'user' in request.session:
        if len(request.GET) > 0 and 'nom' in request.GET:
            employe_pk = request.GET.get('employe_pk')
            employe = get_object_or_404(Employe, id=employe_pk)
            employe.nom = request.GET.get('nom').strip()
            employe.prenom = request.GET.get('prenom').strip()
            fonction_pk = request.GET.get('fonction')
            fonction = get_object_or_404(Fonction, pk=fonction_pk)
            employe.fonction = fonction
            if 'password' in request.GET:
                employe.email = request.GET.get('email')
                employe.password = request.GET.get('password')
            employe.save()
            return redirect('gestion_employe')
        employe_id = request.POST.get('employe_pk')
        employe = get_object_or_404(Employe, id=employe_id)
        admin = Administrateur.objects.filter(employe=employe)
        if len(admin) > 0 and employe.id != request.session.get('user'):
            return HttpResponse("Impossible de modifier un administrateur à partir de la liste", status=409)
        else:
            fonctions = Fonction.objects.exclude(nom='.Global')
            user = Employe.objects.get(pk=request.session.get('user'))
            return render(request, 'magasinwcs/employe_update.html', context={'employe': employe,
                                                                              'fonctions': fonctions, 'user': user})
    else:
        return redirect('login')


def gestion_client(request):
    if 'user' in request.session:
        context = {"clients": (Client.objects.all().order_by('nom')), "user": Employe.objects.get(pk=request.session.get('user'))}
        return render(request, 'magasinwcs/gestion_client.html', context=context)
    else:
        return redirect('login')


def add_client(request):
    ref = request.POST.get("ref").strip()
    nom = request.POST.get("nom").strip()
    contact = request.POST.get("contact").strip()
    if nom == '' or ref == '':
        return HttpResponse("Remplissez au moins le champ du nom et le champ id", status=409)
    if len(Client.objects.filter(reference=ref))>0:
        return HttpResponse('Id déjà existant', status=409)
    client, created = Client.objects.get_or_create(reference=ref, nom=nom, contact=contact)
    if not created:
        return HttpResponse("Ce client existe déjà", status=409)

    return redirect('gestion_client')


def delete_client(request, client_pk):
    client = get_object_or_404(Client, pk=client_pk)
    client.delete()
    return HttpResponse("")


def client_update(request):
    if 'user' in request.session:
        if 'nom' in request.POST:
            client_pk = request.POST.get('client_pk')
            client = get_object_or_404(Client, id=client_pk)
            ref = request.POST.get('ref').strip()
            if ref != client.reference and len(Client.objects.filter(reference=ref))>0:
                return HttpResponse('Id déjà existant', status=409)
            client.reference = ref
            client.nom = request.POST.get('nom').strip()
            client.contact = request.POST.get('contact').strip()
            client.save()
            return redirect('gestion_client')
        client_id = request.POST.get('client_pk')
        client = get_object_or_404(Client, id=client_id)
        return render(request, 'magasinwcs/client_update.html',
                      context={'client': client, "user": Employe.objects.get(pk=request.session.get('user'))})
    else:
        return redirect('login')


def gestion_utilisation(request):
    if 'user' in request.session:
        utilisations = Utilisation.objects.filter(type='e', statut='n').order_by('date')
        employes = Employe.objects.all().order_by('nom','prenom')
        return render(request, 'magasinwcs/gestion_utilisation.html',
                      context={'utilisations': utilisations, 'employes': employes,
                               'user': Employe.objects.get(pk=request.session.get('user'))})
    else:
        return redirect('login')


def add_utilisation(request):
    if 'v_utilisation' in request.POST:
        user_id = request.session.get('user')
        user = get_object_or_404(Employe, pk=user_id)
        panier = Panier.objects.filter(employe=user,type='utilisation')
        if len(panier)>0:
            for cmd in panier:
                if not cmd.client:
                    utilisation = Utilisation.objects.create(date=cmd.date, materiel=cmd.materiel, quantite=cmd.quantite, employe=cmd.utilisateur, type=cmd.utilisation)
                else:
                    utilisation = Utilisation.objects.create(date=cmd.date, materiel=cmd.materiel, quantite=cmd.quantite, client=cmd.client, employe=cmd.utilisateur, type=cmd.utilisation)
            Panier.objects.filter(employe=user,type='utilisation').delete()
            return redirect('gestion_utilisation')
        else:
            return HttpResponse('Ajouter au moins une utilisation', status=409)
    else:
        user_id = request.session.get('user')
        user = get_object_or_404(Employe, pk=user_id)
        fournisseurs = Fournisseur.objects.all().order_by('nom')
        materiels = Materiel.objects.all().order_by('nom','description')
        paniers = Panier.objects.filter(employe=user,type='utilisation').order_by('-date')
        employes = Employe.objects.all().order_by('nom','prenom')
        clients = Client.objects.all().order_by('nom')
        context = {'clients': clients,'employes': employes,'fournisseurs': fournisseurs, 'materiels': materiels, 'paniers':paniers, 'day': datetime.date.today()}
        return render(request, 'magasinwcs/add_utilisation.html', context=context)


def delete_utilisation(request):
    utilisation_pk = request.POST.get('utilisation_pk')
    if 'materiel_pk' in request.POST:
        quantite = int(request.POST.get('quantite'))
        materiel_pk = request.POST.get('materiel_pk')
        materiel = get_object_or_404(Materiel, pk=materiel_pk)
        materiel.quantite += quantite
        materiel.save()
    utilisation = get_object_or_404(Utilisation, pk=utilisation_pk)
    utilisation.delete()
    return HttpResponse("")


def statut_change(request):
    utilisation_pk = request.POST.get('utilisation_pk')
    utilisation = get_object_or_404(Utilisation, pk=utilisation_pk)
    statut = request.POST.get('statut')
    quantite = int(request.POST.get('quantite'))
    materiel_pk = request.POST.get('materiel_pk')
    materiel = get_object_or_404(Materiel, pk=materiel_pk)
    if statut == 'r':
        materiel.quantite += quantite
        materiel.save()
    elif statut == 'n':
        materiel.quantite -= quantite
        materiel.save()
    utilisation.statut = statut
    utilisation.save()
    return HttpResponse("Statut changé", status=409)


def get_utilisation(request):
    statut = request.POST.get('statut')
    employe_pk = request.POST.get('employe')
    type = request.POST.get('type')
    date = request.POST.get('date')
    if date:
        if statut == 'g':
            if employe_pk == 'g':
                if type == 'g':
                    utilisations = Utilisation.objects.filter(date=date).order_by('-date')
                else:
                    utilisations = Utilisation.objects.filter(type=type,date=date).order_by('-date')
            else:
                employe = get_object_or_404(Employe, pk=employe_pk)
                if type == 'g':
                    utilisations = Utilisation.objects.filter(employe=employe,date=date).order_by('-date')
                else:
                    utilisations = Utilisation.objects.filter(employe=employe, type=type, date=date).order_by('-date')
        else:
            if employe_pk == 'g':
                if type == 'g':
                    utilisations = Utilisation.objects.filter(statut=statut, date=date).order_by('-date')
                else:
                    utilisations = Utilisation.objects.filter(statut=statut, type=type, date=date).order_by('-date')
            else:
                employe = get_object_or_404(Employe, pk=employe_pk)
                if type == 'g':
                    utilisations = employe.utilisation_set.filter(statut=statut, date=date).order_by('-date')
                else:
                    utilisations = employe.utilisation_set.filter(statut=statut, type=type, date=date).order_by('-date')

        return render(request, 'magasinwcs/liste_utilisation.html', context={'utilisations': utilisations}) 

    if statut == 'g':
        if employe_pk == 'g':
            if type == 'g':
                utilisations = Utilisation.objects.all().order_by('-date')
            else:
                utilisations = Utilisation.objects.filter(type=type).order_by('-date')
        else:
            employe = get_object_or_404(Employe, pk=employe_pk)
            if type == 'g':
                utilisations = employe.utilisation_set.all().order_by('-date')
            else:
                utilisations = employe.utilisation_set.filter(type=type).order_by('-date')
    else:
        if employe_pk == 'g':
            if type == 'g':
                utilisations = Utilisation.objects.filter(statut=statut).order_by('-date')
            else:
                utilisations = Utilisation.objects.filter(statut=statut, type=type).order_by('-date')
        else:
            employe = get_object_or_404(Employe, pk=employe_pk)
            if type == 'g':
                utilisations = employe.utilisation_set.filter(statut=statut).order_by('-date')
            else:
                utilisations = employe.utilisation_set.filter(statut=statut, type=type).order_by('-date')

    return render(request, 'magasinwcs/liste_utilisation.html', context={'utilisations': utilisations})


def gestion_fournisseur(request):
    if 'user' in request.session:
        context = {"fournisseurs": (Fournisseur.objects.all().order_by('nom')),
                   'user': Employe.objects.get(pk=request.session.get('user'))}
        return render(request, 'magasinwcs/gestion_fournisseur.html', context=context)
    else:
        return redirect('login')


def add_fournisseur(request):
    ref = request.POST.get('ref')
    if len(Fournisseur.objects.filter(reference=ref)):
        return HttpResponse('Id déjà existant', status=409)
    contact = request.POST.get("contact").strip()
    nom = request.POST.get("nom").strip()
    if nom == '':
        return HttpResponse("Remplissez au moins le champ du nom", status=409)
    fournisseur, created = Fournisseur.objects.get_or_create(reference=ref, nom=nom, contact=contact)
    if not created:
        return HttpResponse("Ce fournisseur existe déjà", status=409)

    return redirect('gestion_fournisseur')


def delete_fournisseur(request, fournisseur_pk):
    fournisseur = get_object_or_404(Fournisseur, pk=fournisseur_pk)
    fournisseur.delete()
    return HttpResponse("")


def fournisseur_update(request):
    if 'user' in request.session:
        if 'nom' in request.POST:
            ref = request.POST.get('ref').strip()
            fournisseur_pk = request.POST.get('fournisseur_pk')
            fournisseur = get_object_or_404(Fournisseur, id=fournisseur_pk)
            if ref != fournisseur.reference and len(Fournisseur.objects.filter(reference=ref)) > 0:
                return HttpResponse('Id déjà existant', status=409)            
            fournisseur.nom = request.POST.get('nom').strip()
            fournisseur.reference = ref
            fournisseur.contact = request.POST.get('contact').strip()
            fournisseur.save()
            return redirect('gestion_fournisseur')
        fournisseur_id = request.POST.get('fournisseur_pk')
        fournisseur = get_object_or_404(Fournisseur, id=fournisseur_id)
        return render(request, 'magasinwcs/fournisseur_update.html',
                      context={'fournisseur': fournisseur,
                               'user': Employe.objects.get(pk=request.session.get('user'))})
    else:
        return redirect('login')


def gestion_commande(request):
    if 'user' in request.session:
        commandes = Commande.objects.filter(traitement='n').order_by('-date')
        materiels = Materiel.objects.all().order_by('nom','description')
        fournisseurs = Fournisseur.objects.all()
        return render(request, 'magasinwcs/gestion_commande.html',
                      context={'commandes': commandes, 'materiels': materiels, 'fournisseurs': fournisseurs,
                               'user': Employe.objects.get(pk=request.session.get('user'))})
    else:
        return redirect('login')


def get_commande(request):
    traitement = request.POST.get('traitement')
    materiel_pk = request.POST.get('materiel')
    fournisseur_pk = request.POST.get('fournisseur')
    date = request.POST.get('date')
    if date:
        if traitement == 'g':
            if materiel_pk == 'g':
                if fournisseur_pk == 'g':
                    commandes = Commande.objects.filter(date=date).order_by('-date')
                else:
                    fournisseur = get_object_or_404(Fournisseur, pk=fournisseur_pk)
                    commandes = Commande.objects.filter(fournisseur=fournisseur,date=date).order_by('-date')
            else:
                materiel = get_object_or_404(Materiel, pk=materiel_pk)
                if fournisseur_pk == 'g':
                    commandes = materiel.commande_set.all().order_by('-date')
                else:
                    fournisseur = get_object_or_404(Fournisseur, pk=fournisseur_pk)
                    commandes = materiel.commande_set.filter(fournisseur=fournisseur,date=date).order_by('-date')
        else:
            if materiel_pk == 'g':
                if fournisseur_pk == 'g':
                    commandes = Commande.objects.filter(traitement=traitement,date=date).order_by('-date')
                else:
                    fournisseur = get_object_or_404(Fournisseur, pk=fournisseur_pk)
                    commandes = Commande.objects.filter(traitement=traitement, fournisseur=fournisseur,date=date).order_by('-date')
            else:
                materiel = get_object_or_404(Materiel, pk=materiel_pk)
                if fournisseur_pk == 'g':
                    commandes = materiel.commande_set.filter(traitement=traitement,date=date).order_by('-date')
                else:
                    fournisseur = get_object_or_404(Fournisseur, pk=fournisseur_pk)
                    commandes = materiel.commande_set.filter(traitement=traitement, fournisseur=fournisseur,date=date).order_by(
                        '-date')

        return render(request, 'magasinwcs/liste_commande.html', context={'commandes': commandes})        
                
    if traitement == 'g':
        if materiel_pk == 'g':
            if fournisseur_pk == 'g':
                commandes = Commande.objects.all().order_by('-date')
            else:
                fournisseur = get_object_or_404(Fournisseur, pk=fournisseur_pk)
                commandes = Commande.objects.filter(fournisseur=fournisseur).order_by('-date')
        else:
            materiel = get_object_or_404(Materiel, pk=materiel_pk)
            if fournisseur_pk == 'g':
                commandes = materiel.commande_set.all().order_by('-date')
            else:
                fournisseur = get_object_or_404(Fournisseur, pk=fournisseur_pk)
                commandes = materiel.commande_set.filter(fournisseur=fournisseur).order_by('-date')
    else:
        if materiel_pk == 'g':
            if fournisseur_pk == 'g':
                commandes = Commande.objects.filter(traitement=traitement).order_by('-date')
            else:
                fournisseur = get_object_or_404(Fournisseur, pk=fournisseur_pk)
                commandes = Commande.objects.filter(traitement=traitement, fournisseur=fournisseur).order_by('-date')
        else:
            materiel = get_object_or_404(Materiel, pk=materiel_pk)
            if fournisseur_pk == 'g':
                commandes = materiel.commande_set.filter(traitement=traitement).order_by('-date')
            else:
                fournisseur = get_object_or_404(Fournisseur, pk=fournisseur_pk)
                commandes = materiel.commande_set.filter(traitement=traitement, fournisseur=fournisseur).order_by(
                    '-date')

    return render(request, 'magasinwcs/liste_commande.html', context={'commandes': commandes})


def add_commande(request):
    
    if 'v_cmd' in request.POST:
        user_id = request.session.get('user')
        user = get_object_or_404(Employe, pk=user_id)
        panier = Panier.objects.filter(employe=user,type='commande')
        if len(panier)>0:
            message = []
            for cmd in panier:
                if not cmd.fournisseur:
                    commande = Commande.objects.create(date=cmd.date, materiel=cmd.materiel, quantite=cmd.quantite)
                    message.append({'Date':commande.date, 'Materiel':commande.materiel.description + ' || ' + commande.materiel.id, 'Quantite':commande.quantite, 'Fournisseur':''})
                else:
                    commande = Commande.objects.create(date=cmd.date, materiel=cmd.materiel, quantite=cmd.quantite, fournisseur=cmd.fournisseur)
                    message.append({'Date':commande.date, 'Materiel':commande.materiel.description + ' || ' + commande.materiel.id, 'Quantite':commande.quantite, 'Fournisseur':commande.fournisseur.nom})
            data = pd.DataFrame(message)
            output = build_table(data, "blue_light")
            send_mail(output)

            Panier.objects.filter(employe=user,type='commande').delete()
            return redirect('gestion_commande')
        else:
            return HttpResponse('Ajouter au moins une commande', status=409)
    else:
        user_id = request.session.get('user')
        user = get_object_or_404(Employe, pk=user_id)
        fournisseurs = Fournisseur.objects.all()
        materiels = Materiel.objects.all().order_by('nom','description')
        paniers = Panier.objects.filter(employe=user,type='commande').order_by('-date')
        context = {'fournisseurs': fournisseurs, 'materiels': materiels, 'paniers':paniers}
        return render(request, 'magasinwcs/add_commande.html', context=context)


def delete_commande(request):
    commande_pk = request.POST.get('commande_pk')
    commande = get_object_or_404(Commande, pk=commande_pk)
    commande.delete()
    return HttpResponse("")


def traitement_change(request):
    commande_pk = request.POST.get('commande_pk')
    commande = get_object_or_404(Commande, pk=commande_pk)
    traitement = request.POST.get('traitement')
    commande.traitement = traitement
    commande.save()
    return HttpResponse("Traitement changé", status=409)


def quantite_change(request):
    commande_pk = request.POST.get('commande_pk')
    commande = get_object_or_404(Commande, pk=commande_pk)
    quantite = request.POST.get('quantite')
    commande.quantite = quantite
    commande.save()
    return HttpResponse("Quantité changée", status=409)


def gestion_reception(request):
    if 'user' in request.session:
        receptions = Reception.objects.all().order_by('date')
        materiels = Materiel.objects.all().order_by('nom','description')
        fournisseurs = Fournisseur.objects.all()
        return render(request, 'magasinwcs/gestion_reception.html',
                      context={'receptions': receptions, 'materiels': materiels, 'fournisseurs': fournisseurs,
                               'user': Employe.objects.get(pk=request.session.get('user'))})
    else:
        return redirect('login')


def add_reception(request):
    if 'v_reception' in request.POST:
        user_id = request.session.get('user')
        user = get_object_or_404(Employe, pk=user_id)
        panier = Panier.objects.filter(employe=user,type='reception')
        if len(panier)>0:
            for cmd in panier:
                materiel =cmd.materiel
                materiel.quantite += cmd.quantite
                materiel.save()
                if not cmd.fournisseur:
                    reception = Reception.objects.create(date=cmd.date, materiel=cmd.materiel, quantite=cmd.quantite, prix_unitaire=cmd.prix_unitaire)
                else:
                    reception = Reception.objects.create(date=cmd.date, materiel=cmd.materiel, quantite=cmd.quantite, fournisseur=cmd.fournisseur, prix_unitaire=cmd.prix_unitaire)
           
            Panier.objects.filter(employe=user,type='reception').delete()
            return redirect('gestion_reception')
        else:
            return HttpResponse('Ajouter au moins une reception', status=409)
    else:
        user_id = request.session.get('user')
        user = get_object_or_404(Employe, pk=user_id)
        fournisseurs = Fournisseur.objects.all().order_by('nom')
        materiels = Materiel.objects.all().order_by('nom','description')
        paniers = Panier.objects.filter(employe=user,type='reception').order_by('-date')
        context = {'fournisseurs': fournisseurs, 'materiels': materiels, 'paniers':paniers}
        return render(request, 'magasinwcs/add_reception.html', context=context)


def delete_reception(request):
    reception_pk = request.POST.get('reception_pk')
    if 'materiel_pk' in request.POST:
        quantite = int(request.POST.get('quantite'))
        materiel_pk = request.POST.get('materiel_pk')
        materiel = get_object_or_404(Materiel, pk=materiel_pk)
        if materiel.quantite >= quantite : 
            materiel.quantite -= quantite
            materiel.save()
        else:
            return HttpResponse('Quantité à annuler suppérieur à la réserve', status=409)
    reception = get_object_or_404(Reception, pk=reception_pk)
    reception.delete()
    return HttpResponse("")


def get_reception(request):
    materiel_pk = request.POST.get('materiel')
    fournisseur_pk = request.POST.get('fournisseur')
    date = request.POST.get('date')
    if date:
        if materiel_pk == 'g':
            if fournisseur_pk == 'g':
                receptions = Reception.objects.filter(date=date)
            else:
                fournisseur = get_object_or_404(Fournisseur, pk=fournisseur_pk)
                receptions = Reception.objects.filter(fournisseur=fournisseur, date=date).order_by('-date')
        else:
            materiel = get_object_or_404(Materiel, pk=materiel_pk)
            if fournisseur_pk == 'g':
                receptions = Reception.objects.filter(materiel=materiel, date=date).order_by('-date')
            else:
                fournisseur = get_object_or_404(Fournisseur, pk=fournisseur_pk)
                receptions = Reception.objects.filter(fournisseur=fournisseur, materiel=materiel,date=date).order_by('-date')

        return render(request, 'magasinwcs/liste_reception.html', context={'receptions': receptions})        
         
    if materiel_pk == 'g':
        if fournisseur_pk == 'g':
            receptions = Reception.objects.all()
        else:
            fournisseur = get_object_or_404(Fournisseur, pk=fournisseur_pk)
            receptions = fournisseur.reception_set.order_by('-date')
    else:
        materiel = get_object_or_404(Materiel, pk=materiel_pk)
        if fournisseur_pk == 'g':
            receptions = materiel.reception_set.order_by('-date')
        else:
            fournisseur = get_object_or_404(Fournisseur, pk=fournisseur_pk)
            receptions = Reception.objects.filter(fournisseur=fournisseur, materiel=materiel).order_by('-date')

    return render(request, 'magasinwcs/liste_reception.html', context={'receptions': receptions})


def gestion_administrateur(request):
    if 'user' in request.session:
        user_id = request.session.get('user')
        user = get_object_or_404(Employe, pk=user_id)
        result = Administrateur.objects.filter(employe=user)
        if len(result) > 0:
            context = {"administrateurs": Administrateur.objects.all(),
                       "user": Employe.objects.get(pk=request.session.get('user')),
                       "admin": Administrateur.objects.get(employe=user),
                       "employes": Employe.objects.filter(administrateur__isnull=True)}
            return render(request, 'magasinwcs/gestion_administrateur.html', context=context)
    else:
        return redirect('login')


def add_administrateur(request):
    if 'user' in request.session:
        user_id = request.session.get('user')
        user = get_object_or_404(Employe, pk=user_id)
        admin = Administrateur.objects.get(employe=user)

        if admin.type == 's':
            employe_pk = request.POST.get('employe_pk')
            if employe_pk == '-1':
                return HttpResponse("choississez un membre du personnel", status=409)
            else:
                employe = get_object_or_404(Employe, pk=employe_pk)
                type = request.POST.get('type')
                e_mail = request.POST.get('email').strip()
                result = Employe.objects.filter(email=e_mail)
                if len(result) > 0:
                    return HttpResponse("Cet email existe déjà", status=409)
                else:
                    password = request.POST.get('password')
                    administrateur, created = Administrateur.objects.get_or_create(employe=employe, type=type)
                    if not created:
                        return HttpResponse("Cette personne est déjà administrateur", status=409)
                    employe.email = e_mail
                    employe.password = password
                    employe.save()
                    return redirect('gestion_administrateur')
        else:
            return HttpResponse("Vous n'êtes pas habilité à ajouter un administrateur", status=409)
    else:
        return redirect('login')


def delete_administrateur(request):
    if 'user' in request.session:
        user_id = request.session.get('user')
        user = get_object_or_404(Employe, pk=user_id)
        admin = Administrateur.objects.get(employe=user)

        if admin.type == 's':
            administrateur_pk = request.POST.get('administrateur_pk')
            if str(admin.id) == str(administrateur_pk):
                return HttpResponse("Vous ne pouvez pas vous supprimer", status=409)
            else:
                administrateur = get_object_or_404(Administrateur, pk=administrateur_pk)
                administrateur.employe.email = ""
                administrateur.employe.password = ""
                administrateur.employe.save()
                administrateur.delete()
            return HttpResponse("")
        else:
            return HttpResponse("Vous n'êtes pas habilité à supprimer un administrateur", status=409)
    else:
        return redirect('login')


def type_change(request):
    if 'user' in request.session:
        user_id = request.session.get('user')
        user = get_object_or_404(Employe, pk=user_id)
        admin = Administrateur.objects.get(employe=user)

        if admin.type == 's':
            administrateur_pk = request.POST.get('administrateur_pk')
            if str(admin.pk) == str(administrateur_pk):
                return HttpResponse("Vous ne pouvez pas modifier votre statut d'administrateur", status=409)
            else:
                administrateur = get_object_or_404(Administrateur, pk=administrateur_pk)
                type = request.POST.get('type')
                administrateur.type = type
                administrateur.save()
                return HttpResponse("Type d'administrateur changé", status=409)
        else:
            return HttpResponse("Vous n'êtes pas habilité à changer le type un administrateur", status=409)
    else:
        return redirect('login')


def add_panier(request):
    if 'user' in request.session:
        user_id = request.session.get('user')
        user = get_object_or_404(Employe, pk=user_id)
        materiel_pk = request.POST.get('materiel_pk')
        quantite = int(request.POST.get('quantite'))
        fournisseur_pk = request.POST.get('fournisseur') 
        if materiel_pk != '-1' and quantite > 0:
            materiel = get_object_or_404(Materiel, id=materiel_pk)
            dte = request.POST.get('date')
            if 'commande' in request.POST:
                if fournisseur_pk != '-1' and fournisseur_pk != '':
                    fournisseur = get_object_or_404(Fournisseur, id=fournisseur_pk)
                    panier, created = Panier.objects.get_or_create(date=dte, employe=user, materiel=materiel, quantite=quantite, fournisseur=fournisseur, type='commande')
                else:
                    panier, created = Panier.objects.get_or_create(date=dte, employe=user, materiel=materiel, quantite=quantite, type='commande' )
                return redirect('add-commande')
            
            if 'reception' in request.POST:
                prix = int(request.POST.get("prix_unitaire"))
                if fournisseur_pk != '-1' and fournisseur_pk != '':
                    fournisseur = get_object_or_404(Fournisseur, id=fournisseur_pk)
                    panier, created = Panier.objects.get_or_create(date=dte, employe=user, materiel=materiel, quantite=quantite, fournisseur=fournisseur,  type='reception', prix_unitaire=prix)
                else:
                    panier, created = Panier.objects.get_or_create(date=dte, employe=user, materiel=materiel, quantite=quantite, type='reception', prix_unitaire=prix )
                return redirect('add-reception')             

            if 'utilisation' in request.POST:
                if materiel.quantite < quantite:
                    return HttpResponse('Quantité en réserve insuffisante', status=409)
                else:
                    client_pk = request.POST.get('client')
                    utilisation = request.POST.get('type')
                    utilisateur_pk =request.POST.get('utilisateur')
                    utilisateur = get_object_or_404(Employe, id=utilisateur_pk)
                    materiel.quantite -= quantite
                    materiel.save()
                    if client_pk != '-1' and client_pk != '':
                        client = get_object_or_404(Client, id=client_pk)
                        panier, created = Panier.objects.get_or_create(date=dte, employe=user, materiel=materiel, quantite=quantite, type='utilisation', utilisateur=utilisateur, client=client,
                                                                        utilisation=utilisation)
                    else:
                            panier, created = Panier.objects.get_or_create(date=dte, employe=user, materiel=materiel, quantite=quantite, type='utilisation', utilisateur=utilisateur, utilisation=utilisation)                  
                    return redirect('add-utilisation')             

        else:
            return HttpResponse("Choississez un materiel", status=409)
    else:
        return redirect('login')


def delete_panier(request):
    if 'user' in request.session:
        panier_pk = request.POST.get('panier_pk')
        panier = get_object_or_404(Panier, id=panier_pk)
        if 'utl' in request.POST:
            materiel = panier.materiel
            materiel.quantite += int(request.POST.get('utl'))
            materiel.save()
        panier.delete()
        return HttpResponse('')
    else:
        return redirect('login')
