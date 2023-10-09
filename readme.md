# GESTION-Magasin-WCS

## Modèle

- Categorie
  - nom

- Materiel
  - id
  - nom
  - description
  - quantite
  - prix_unitaire
  - categorie

- Fonction
  - nom

- Employe
  - id
  - nom
  - prenom
  - fonction

- Administrateur
  - email
  - password
  - employe
  - type 

- Utilisation
  - date
  - materiel
  - quantite
  - employe
  - client
  - type
  - statut

- client
  - nom 
  - contact

- Commande
  - id
  - date
  - materiel
  - quantite
  - prix_unitaire
  - fournisseur

- Fournisseur
  - nom
  - contact

- Panier
  - date
  - employe
  - materiel
  - quantite
  - prix_unitaire
  - client
  - utilisateur
  - utilisation
  - fournisseur
  - type


- Reception 
  - id
  - date
  - materiel
  - quantite
  - prix_unitaire
  - fournisseur

## Fonctionnalités
[x] Ajouter une categorie  
[x] Supprimer une categorie  
[x] Ajouter une instance de materiel (reliée à une catégorie)  
[x] Modifier les attributs d'une instance de materiel  
[x] Supprimer une instance de materiel  
[x] Afficher le matériel d'une catégorie
[x] Ajouter une fonction  
[x] Supprimer une fonction  
[x] Ajouter un employe  
[x] Supprimer un employe  
[x] modifer un employe  
[x] Ajouter un administrateur(possible que par un super-admin)  
[x] Supprimer un administrateur(possible que par un super-admin)  
[x] Ajouter un client  
[x] Supprimer un client  
[x] Modifier un client  
[x] Ajouter une utilisation  
[x] Supprimer une utilisation  
[x] Annuler une utilisation  
[x] Modifier le statut d'une utilisation
[x] Afficher l'utilisation par employe/statut/type  
[x] Ajouter un fournisseur  
[x] Modifier un fournisseur  
[x] Supprimer un fournisseur  
[x] Ajouter une commande et envoyer un mail avec les références à Mr Jaafar    
[x] Modifier une commande  
[x] Supprimer une commande 
[x] Afficher les commandes par materiel/fournisseur/traitement  
[x] Ajouter une livraison  
[x] Modifier une livraison  
[x] Supprimer une livraison  
[x] Afficher les receptions par materiel/fournisseur    
