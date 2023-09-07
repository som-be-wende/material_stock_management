from string import capwords
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from soupsieve.util import lower

from magasinwcs.models import *


# Create your views here.


def sendmail(message):
    email = 'magasinwcs@gmail.com'
    send_mail(
        'Nouvelle Commande',
        message,
        'settings.EMAIL_HOST_USER',
        [email],
        fail_silently=False
    )


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
            return HttpResponse("Adresse et/ou Mot de passe incorrect")
    return render(request, 'magasinwcs/login.html')


def deconnxion(request):
    del request.session['user']
    return redirect('login')


def gestion_materiel(request):
    if 'user' in request.session:
        context = {}
        context["categories"] = (Categorie.objects.all())
        context["materiels"] = reversed(Materiel.objects.all())
        context["glob"] = Categorie.get_default_categorie()
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

    return render(request, 'magasinwcs/categorie.html', context={"categorie": categorie})


def delete_categorie(request):
    categorie_pk = (request.POST.get("categorie_pk"))
    categorie = get_object_or_404(Categorie, pk=categorie_pk)
    if categorie.nom != "Global":
        categorie.delete()
    return redirect("gestion_materiel")


def add_materiel(request):
    categorie_pk = request.POST.get("categorie_pk")
    categorie = get_object_or_404(Categorie, pk=categorie_pk)
    if categorie.nom == "Global":
        return HttpResponse('<script>alert("SELCTIONNER/AJOUTER UNE CATEGORIE")</script>')
    materiel_id = request.POST.get("materiel-id").strip()
    nom = request.POST.get("materiel-nom").strip()
    description = request.POST.get("materiel-description").strip()
    if materiel_id == '' or nom == '':
        return HttpResponse("Remplissez les champs", status=409)
    materiel, created = Materiel.objects.get_or_create(id=materiel_id, nom=nom,
                                                       description=description,
                                                       categorie=categorie)
    if not created:
        return HttpResponse("Ce materiel existe déjà", status=409)

    return render(request, 'magasinwcs/liste_materiel.html', context={"materielplus": materiel})


def get_materiel(request, categorie_pk):
    categorie = get_object_or_404(Categorie, pk=categorie_pk)
    if categorie.nom == "Global":
        materiels = reversed(Materiel.objects.all())
    else:
        materiels = reversed(categorie.materiel_set.all())
    return render(request, 'magasinwcs/liste_materiel.html', context={"materiels": materiels})


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
            materiel.description = request.GET.get('description').strip()
            categorie_pk = request.GET.get('categorie')
            categorie = get_object_or_404(Categorie, pk=categorie_pk)
            materiel.categorie = categorie
            materiel.save()
            return redirect('gestion_materiel')
        materiel_id = request.POST.get('materiel_pk')
        materiel = get_object_or_404(Materiel, id=materiel_id)
        categories = Categorie.objects.exclude(nom='Global')
        user = Employe.objects.get(pk=request.session.get('user'))
        return render(request, 'magasinwcs/materiel_update.html',
                      context={'materiel': materiel, 'categories': categories, 'user': user})
    else:
        return redirect('login')


def gestion_employe(request):
    if 'user' in request.session:
        context = {}
        context["fonctions"] = (Fonction.objects.all())
        context["employes"] = reversed(Employe.objects.all())
        context["glob"] = Fonction.get_default_fonction()
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

    return render(request, 'magasinwcs/fonction.html', context={"fonction": fonction})


def delete_fonction(request):
    fonction_pk = (request.POST.get("fonction_pk"))
    fonction = get_object_or_404(Fonction, pk=fonction_pk)
    if fonction.nom != "Global":
        fonction.delete()
    return redirect("gestion_employe")


def add_employe(request):
    fonction_pk = request.POST.get("fonction_pk")
    fonction = get_object_or_404(Fonction, pk=fonction_pk)
    if fonction.nom == "Global":
        return HttpResponse('<script>alert("SELCTIONNER/AJOUTER UNE FONCTION")</script>')
    nom = request.POST.get("employe-nom").strip()
    prenom = request.POST.get("employe-prenom").strip()
    if prenom == '' or nom == '':
        return HttpResponse("Remplissez les champs", status=409)
    employe, created = Employe.objects.get_or_create(nom=nom, prenom=prenom, fonction=fonction)
    if not created:
        return HttpResponse("Cet personne existe déjà", status=409)

    return render(request, 'magasinwcs/liste_employe.html', context={"employeplus": employe})


def get_employe(request, fonction_pk):
    fonction = get_object_or_404(Fonction, pk=fonction_pk)
    if fonction.nom == "Global":
        employes = reversed(Employe.objects.all())
    else:
        employes = reversed(fonction.employe_set.all())
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
            fonctions = Fonction.objects.exclude(nom='Global')
            user = Employe.objects.get(pk=request.session.get('user'))
            return render(request, 'magasinwcs/employe_update.html', context={'employe': employe,
                                                                              'fonctions': fonctions, 'user': user})
    else:
        return redirect('login')


def gestion_client(request):
    if 'user' in request.session:
        context = {"clients": (Client.objects.all()), "user": Employe.objects.get(pk=request.session.get('user'))}
        return render(request, 'magasinwcs/gestion_client.html', context=context)
    else:
        return redirect('login')


def add_client(request):
    nom = request.POST.get("nom").strip()
    contact = request.POST.get("contact").strip()
    if nom == '':
        return HttpResponse("Remplissez au moins le champ du nom", status=409)
    client, created = Client.objects.get_or_create(nom=nom, contact=contact)
    if not created:
        return HttpResponse("Ce client existe déjà", status=409)

    return render(request, 'magasinwcs/liste_client.html', context={"clientplus": client})


def delete_client(request, client_pk):
    client = get_object_or_404(Client, pk=client_pk)
    client.delete()
    return HttpResponse("")


def client_update(request):
    if 'user' in request.session:
        if len(request.GET) > 0:
            client_pk = request.GET.get('client_pk')
            client = get_object_or_404(Client, id=client_pk)
            client.nom = request.GET.get('nom').strip()
            client.contact = request.GET.get('contact').strip()
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
        employes = Employe.objects.all()
        return render(request, 'magasinwcs/gestion_utilisation.html',
                      context={'utilisations': utilisations, 'employes': employes,
                               'user': Employe.objects.get(pk=request.session.get('user'))})
    else:
        return redirect('login')


def add_utilisation(request):
    materiel_pk = request.POST.get('materiel_pk')
    materiel = get_object_or_404(Materiel, id=materiel_pk)
    if 'quantite' in request.POST:
        quantite = int(request.POST.get('quantite'))

        if quantite == 0:
            return HttpResponse("Ajouter une quantite>0", status=409)
        else:
            date = request.POST.get('date')
            utilisateur_pk = request.POST.get('utilisateur')
            employe = get_object_or_404(Employe, id=utilisateur_pk)
            type = request.POST.get('type')
            client_pk = request.POST.get('client')
            if materiel.quantite < quantite:
                return HttpResponse("Quantite insuffisante", status=409)
            materiel.quantite -= quantite
            materiel.save()
            if client_pk == "-1":
                utilisation, created = Utilisation.objects.get_or_create(date=date, materiel=materiel,
                                                                         quantite=quantite, employe=employe,
                                                                         type=type)
            else:
                client = get_object_or_404(Client, id=client_pk)
                utilisation, created = Utilisation.objects.get_or_create(date=date, materiel=materiel,
                                                                         quantite=quantite, employe=employe,
                                                                         client=client, type=type)
        return redirect('gestion_materiel')

    else:
        employes = Employe.objects.all()
        clients = Client.objects.all()
        context = {'employes': employes, 'clients': clients, 'materiel': materiel}
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
    utilisation.statut = statut
    utilisation.save()
    return HttpResponse("Statut changé", status=409)


def get_utilisation(request):
    statut = request.POST.get('statut')
    employe_pk = request.POST.get('employe')
    type = request.POST.get('type')
    if statut == 'g':
        if employe_pk == 'g':
            if type == 'g':
                utilisations = Utilisation.objects.all().order_by('date')
            else:
                utilisations = Utilisation.objects.filter(type=type).order_by('date')
        else:
            employe = get_object_or_404(Employe, pk=employe_pk)
            if type == 'g':
                utilisations = employe.utilisation_set.all().order_by('date')
            else:
                utilisations = employe.utilisation_set.filter(type=type).order_by('date')
    else:
        if employe_pk == 'g':
            if type == 'g':
                utilisations = Utilisation.objects.filter(statut=statut).order_by('date')
            else:
                utilisations = Utilisation.objects.filter(statut=statut, type=type).order_by('date')
        else:
            employe = get_object_or_404(Employe, pk=employe_pk)
            if type == 'g':
                utilisations = employe.utilisation_set.filter(statut=statut).order_by('date')
            else:
                utilisations = employe.utilisation_set.filter(statut=statut, type=type).order_by('date')

    return render(request, 'magasinwcs/liste_utilisation.html', context={'utilisations': utilisations})


def gestion_fournisseur(request):
    if 'user' in request.session:
        context = {"fournisseurs": (Fournisseur.objects.all()),
                   'user': Employe.objects.get(pk=request.session.get('user'))}
        return render(request, 'magasinwcs/gestion_fournisseur.html', context=context)
    else:
        return redirect('login')


def add_fournisseur(request):
    contact = request.POST.get("contact").strip()
    nom = request.POST.get("nom").strip()
    if nom == '':
        return HttpResponse("Remplissez au moins le champ du nom", status=409)
    fournisseur, created = Fournisseur.objects.get_or_create(nom=nom, contact=contact)
    if not created:
        return HttpResponse("Ce fournisseur existe déjà", status=409)

    return render(request, 'magasinwcs/liste_fournisseur.html', context={"fournisseurplus": fournisseur})


def delete_fournisseur(request, fournisseur_pk):
    fournisseur = get_object_or_404(Fournisseur, pk=fournisseur_pk)
    fournisseur.delete()
    return HttpResponse("")


def fournisseur_update(request):
    if 'user' in request.session:
        if len(request.GET) > 0:
            fournisseur_pk = request.GET.get('fournisseur_pk')
            fournisseur = get_object_or_404(Fournisseur, id=fournisseur_pk)
            fournisseur.nom = request.GET.get('nom').strip()
            fournisseur.contact = request.GET.get('contact').strip()
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
        commandes = Commande.objects.all
        materiels = Materiel.objects.all()
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
    if traitement == 'g':
        if materiel_pk == 'g':
            if fournisseur_pk == 'g':
                commandes = Commande.objects.all().order_by('date')
            else:
                fournisseur = get_object_or_404(Fournisseur, pk=fournisseur_pk)
                commandes = Commande.objects.filter(fournisseur=fournisseur).order_by('date')
        else:
            materiel = get_object_or_404(Materiel, pk=materiel_pk)
            if fournisseur_pk == 'g':
                commandes = materiel.commande_set.all().order_by('date')
            else:
                fournisseur = get_object_or_404(Fournisseur, pk=fournisseur_pk)
                commandes = materiel.commande_set.filter(fournisseur=fournisseur).order_by('date')
    else:
        if materiel_pk == 'g':
            if fournisseur_pk == 'g':
                commandes = Commande.objects.filter(traitement=traitement).order_by('date')
            else:
                fournisseur = get_object_or_404(Fournisseur, pk=fournisseur_pk)
                commandes = Commande.objects.filter(traitement=traitement, fournisseur=fournisseur).order_by('date')
        else:
            materiel = get_object_or_404(Materiel, pk=materiel_pk)
            if fournisseur_pk == 'g':
                commandes = materiel.commande_set.filter(traitement=traitement).order_by('date')
            else:
                fournisseur = get_object_or_404(Fournisseur, pk=fournisseur_pk)
                commandes = materiel.commande_set.filter(traitement=traitement, fournisseur=fournisseur).order_by(
                    'date')

    return render(request, 'magasinwcs/liste_commande.html', context={'commandes': commandes})


def add_commande(request):
    materiel_pk = request.POST.get('materiel_pk')
    materiel = get_object_or_404(Materiel, id=materiel_pk)
    if 'quantite' in request.POST:
        quantite = int(request.POST.get('quantite'))
        date = request.POST.get('date')
        fournisseur_pk = request.POST.get('fournisseur')
        if fournisseur_pk == "-1":
            commande, created = Commande.objects.get_or_create(date=date, materiel=materiel, quantite=quantite)
            message = 'Id:  ' + materiel_pk + "\n" + 'Nom:  ' + materiel.nom + "\n" + 'quantite:  ' + str(quantite) + "\n" + \
                      'Fournisseur:  '
        else:
            fournisseur = get_object_or_404(Fournisseur, id=fournisseur_pk)
            commande, created = Commande.objects.get_or_create(date=date, materiel=materiel,
                                                               quantite=quantite, fournisseur=fournisseur)
            message = 'Id:  ' + materiel_pk + "\n" + 'Nom:  ' + materiel.nom + "\n" + 'quantite:  ' + str(quantite) + "\n" + \
                      'Fournisseur:  ' + fournisseur.nom + "\n"
        sendmail(message=message)
        return redirect('gestion_commande')

    else:
        fournisseurs = Fournisseur.objects.all()
        context = {'fournisseurs': fournisseurs, 'materiel': materiel}
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
        materiels = Materiel.objects.all()
        fournisseurs = Fournisseur.objects.all()
        return render(request, 'magasinwcs/gestion_reception.html',
                      context={'receptions': receptions, 'materiels': materiels, 'fournisseurs': fournisseurs,
                               'user': Employe.objects.get(pk=request.session.get('user'))})
    else:
        return redirect('login')


def add_reception(request):
    materiel_pk = request.POST.get('materiel_pk')
    materiel = get_object_or_404(Materiel, id=materiel_pk)
    if 'quantite' in request.POST:
        quantite = int(request.POST.get('quantite'))
        if quantite == 0:
            return HttpResponse("Ajouter une quantite>0", status=409)
        else:
            date = request.POST.get('date')
            fournisseur_pk = request.POST.get('fournisseur')
            materiel.quantite += quantite
            materiel.save()
            if fournisseur_pk == "-1":
                reception, created = Reception.objects.get_or_create(date=date, materiel=materiel, quantite=quantite)
            else:
                fournisseur = get_object_or_404(Fournisseur, pk=fournisseur_pk)
                utilisation, created = Reception.objects.get_or_create(date=date, materiel=materiel,
                                                                       quantite=quantite, fournisseur=fournisseur)
        return redirect('gestion_materiel')

    else:
        fournisseurs = Fournisseur.objects.all()
        context = {'fournisseurs': fournisseurs, 'materiel': materiel}
        return render(request, 'magasinwcs/add_reception.html', context=context)


def delete_reception(request):
    reception_pk = request.POST.get('reception_pk')
    if 'materiel_pk' in request.POST:
        quantite = int(request.POST.get('quantite'))
        materiel_pk = request.POST.get('materiel_pk')
        materiel = get_object_or_404(Materiel, pk=materiel_pk)
        materiel.quantite -= quantite
        materiel.save()
    reception = get_object_or_404(Reception, pk=reception_pk)
    reception.delete()
    return HttpResponse("")


def get_reception(request):
    materiel_pk = request.POST.get('materiel')
    fournisseur_pk = request.POST.get('fournisseur')
    if materiel_pk == 'g':
        if fournisseur_pk == 'g':
            receptions = Reception.objects.all()
        else:
            fournisseur = get_object_or_404(Fournisseur, pk=fournisseur_pk)
            receptions = fournisseur.reception_set.order_by('date')
    else:
        materiel = get_object_or_404(Materiel, pk=materiel_pk)
        if fournisseur_pk == 'g':
            receptions = materiel.reception_set.order_by('date')
        else:
            fournisseur = get_object_or_404(Fournisseur, pk=fournisseur_pk)
            receptions = Reception.objects.filter(fournisseur=fournisseur, materiel=materiel)

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
