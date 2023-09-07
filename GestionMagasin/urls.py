"""
URL configuration for GestionMagasin project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from magasinwcs import views

urlpatterns = [
    path('', views.gestion_materiel, name="gestion_materiel"),
    path('gestion_employe/', views.gestion_employe, name="gestion_employe"),
    path('gestion_administrateur/', views.gestion_administrateur, name="gestion_administrateur"),
    path('gestion_client/', views.gestion_client, name="gestion_client"),
    path('gestion_fournisseur/', views.gestion_fournisseur, name="gestion_fournisseur"),
    path('gestion_utilisation/', views.gestion_utilisation, name="gestion_utilisation"),
    path('gestion_commande/', views.gestion_commande, name="gestion_commande"),
    path('gestion_reception/', views.gestion_reception, name="gestion_reception"),
    path('add-categorie/', views.add_categorie, name="add-categorie"),
    path('add-utilisation/', views.add_utilisation, name="add-utilisation"),
    path('add-commande/', views.add_commande, name="add-commande"),
    path('add-reception/', views.add_reception, name="add-reception"),
    path('add-client/', views.add_client, name="add-client"),
    path('add-fournisseur/', views.add_fournisseur, name="add-fournisseur"),
    path('add-fonction/', views.add_fonction, name="add-fonction"),
    path('add-materiel/', views.add_materiel, name="add-materiel"),
    path('add-employe/', views.add_employe, name="add-employe"),
    path('add-administrateur/', views.add_administrateur, name="add-administrateur"),
    path('get-materiel/<int:categorie_pk>/', views.get_materiel, name="get-materiel"),
    path('get-employe/<int:fonction_pk>/', views.get_employe, name="get-employe"),
    path('get-utilisation/', views.get_utilisation, name="get-utilisation"),
    path('get-commande/', views.get_commande, name="get-commande"),
    path('get-reception/', views.get_reception, name="get-reception"),
    path('delete-materiel/<str:materiel_pk>/', views.delete_materiel, name="delete-materiel"),
    path('delete-employe/<str:employe_pk>/', views.delete_employe, name="delete-employe"),
    path('delete-client/<str:client_pk>/', views.delete_client, name="delete-client"),
    path('delete-fournisseur/<str:fournisseur_pk>/', views.delete_fournisseur, name="delete-fournisseur"),
    path('delete-utilisation/', views.delete_utilisation, name="delete-utilisation"),
    path('delete-commande/', views.delete_commande, name="delete-commande"),
    path('delete-reception/', views.delete_reception, name="delete-reception"),
    path('delete-categorie/', views.delete_categorie, name="delete-categorie"),
    path('delete-fonction/', views.delete_fonction, name="delete-fonction"),
    path('delete-administrateur/', views.delete_administrateur, name="delete-administrateur"),
    path('materiel_update/', views.materiel_update, name="materiel_update"),
    path('employe_update/', views.employe_update, name="employe_update"),
    path('client_update/', views.client_update, name="client_update"),
    path('fournisseur_update/', views.fournisseur_update, name="fournisseur_update"),
    path('statut_change/', views.statut_change, name="statut-change"),
    path('type_change/', views.type_change, name="type-change"),
    path('traitement_change/', views.traitement_change, name="traitement-change"),
    path('quantite_change/', views.quantite_change, name="quantite-change"),
    path('login/', views.login, name="login"),
    path('deconnexion/', views.deconnxion, name="deconnexion"),
    path('admin/', admin.site.urls, name="admin"),
]
