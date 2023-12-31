# Generated by Django 4.2.4 on 2023-09-29 22:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('magasinwcs', '0014_administrateur_employe'),
    ]

    operations = [
        migrations.AddField(
            model_name='commande',
            name='prix_unitaire',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='reception',
            name='prix_unitaire',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='Panier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantite', models.IntegerField(default=0)),
                ('prix_unitaire', models.IntegerField(default=0)),
                ('fournisseur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='magasinwcs.fournisseur')),
                ('materiel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='magasinwcs.materiel')),
            ],
        ),
    ]
