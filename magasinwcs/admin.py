from django.contrib import admin

# Register your models here.
from magasinwcs.models import Categorie, Client, Employe, Fournisseur, Materiel, Utilisation, Reception, Commande, \
    Administrateur, Fonction, Panier

admin.site.register(Categorie)
admin.site.register(Client)
admin.site.register(Employe)
admin.site.register(Fournisseur)
admin.site.register(Materiel)
admin.site.register(Utilisation)
admin.site.register(Reception)
admin.site.register(Commande)
admin.site.register(Fonction)
admin.site.register(Administrateur)
admin.site.register(Panier)