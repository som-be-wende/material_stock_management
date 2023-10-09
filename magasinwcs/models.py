from django.db import models


# Create your models here.

class Categorie(models.Model):
    nom = models.CharField(max_length=60)

    @classmethod
    def get_default_categorie(cls) -> "Categorie":
        categorie, _ = cls.objects.get_or_create(nom=".Global")
        return categorie

    def __unicode__(self):
        return self.nom

    def __str__(self):
        return self.nom


class Materiel(models.Model):
    id = models.CharField(max_length=30, primary_key=True)
    nom = models.CharField(max_length=40)
    description = models.CharField(max_length=200, blank=True)
    quantite = models.IntegerField(default=0)
    prix_unitaire = models.IntegerField(default=0)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)

    @classmethod
    def __unicode__(cls):
        return cls.id + ' ' + cls.nom

    def __str__(self):
        return self.id + ' ' + self.nom


class Fonction(models.Model):
    nom = models.CharField(max_length=60)

    @classmethod
    def get_default_fonction(cls) -> "Fonction":
        fonction, _ = cls.objects.get_or_create(nom=".Global")
        return fonction

    def __unicode__(self):
        return self.nom

    def __str__(self):
        return self.nom


class Employe(models.Model):
    nom = models.CharField(max_length=30)
    prenom = models.CharField(max_length=70)
    fonction = models.ForeignKey(Fonction, on_delete=models.CASCADE)
    email = models.EmailField(null=True, blank=True, unique=True)
    password = models.CharField(max_length=20, default='AZERTY')

    @classmethod
    def __unicode__(cls):
        return cls.nom + ' ' + cls.prenom

    def __str__(self):
        return self.nom + ' ' + self.prenom


class Administrateur(models.Model):
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, null=True)
    type = models.CharField(max_length=1, choices=[("s", "super-admin"), ("n", "normal")], default="n")


    @classmethod
    def __unicode__(cls):
        return cls.employe.nom + ' ' + cls.employe.prenom

    def __str__(self):
        return self.employe.nom + ' ' + self.employe.prenom


class Client(models.Model):
    reference = models.CharField(max_length=50, unique=True, blank=True, null=True)
    nom = models.CharField(max_length=60)
    contact = models.CharField(max_length=60, blank=True)

    @classmethod
    def __unicode__(cls):
        return cls.nom

    def __str__(self):
        return self.nom


class Utilisation(models.Model):
    date = models.DateField(null=True, blank=True)
    materiel = models.ForeignKey(Materiel, on_delete=models.CASCADE)
    quantite = models.IntegerField(default=0)
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, models.SET_NULL, blank=True, null=True)
    type = models.CharField(max_length=1, choices=[("u", "utilisation"), ("e", "emprunt")], default="e")
    statut = models.CharField(max_length=1, choices=[("r", "remis"), ("n", "non-remis")], default="n")

    @classmethod
    def __unicode__(cls):
        return str(cls.date) + ' ' + cls.materiel.nom

    def __str__(self):
        return str(self.date) + ' ' + self.materiel.nom


class Fournisseur(models.Model):
    reference = models.CharField(max_length=50, unique=True, blank=True, null=True)
    nom = models.CharField(max_length=60)
    contact = models.CharField(max_length=60)

    @classmethod
    def __unicode__(cls):
        return cls.nom

    def __str__(self):
        return self.nom


class Commande(models.Model):
    date = models.DateField(null=True, blank=True)
    materiel = models.ForeignKey(Materiel, on_delete=models.CASCADE)
    quantite = models.IntegerField(default=0)
    fournisseur = models.ForeignKey(Fournisseur, models.SET_NULL, blank=True, null=True)
    traitement = models.CharField(max_length=1, choices=[("t", "traitré"), ("n", "non-traité")], default="n")

    @classmethod
    def __unicode__(cls):
        return str(cls.date) + ' ' + cls.materiel.nom

    def __str__(self):
        return str(self.date) + ' ' + self.materiel.nom


class Reception(models.Model):
    date = models.DateField(null=True, blank=True)
    materiel = models.ForeignKey(Materiel, on_delete=models.CASCADE)
    quantite = models.IntegerField(default=0)
    prix_unitaire = models.IntegerField(default=0)
    fournisseur = models.ForeignKey(Fournisseur, models.SET_NULL, blank=True, null=True)

    @classmethod
    def __unicode__(cls):
        return str(cls.date) + ' ' + cls.materiel.nom

    def __str__(self):
        return str(self.date) + ' ' + self.materiel.nom


class Panier(models.Model):
    date = models.DateField(null=True, blank=True)
    employe = models.ForeignKey(Employe, on_delete=models.CASCADE, related_name='employe')
    materiel = models.ForeignKey(Materiel, on_delete=models.CASCADE)
    quantite = models.IntegerField(default=0)
    prix_unitaire = models.IntegerField(default=0)
    type = models.CharField(max_length=20, blank=True)
    utilisateur = models.ForeignKey(Employe, on_delete=models.CASCADE,blank=True,related_name='utilisateur', null=True)
    client = models.ForeignKey(Client, models.SET_NULL, blank=True, null=True)
    utilisation = models.CharField(max_length=1, choices=[("u", "utilisation"), ("e", "emprunt")], default="e", blank=True)
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE, blank=True, null=True)