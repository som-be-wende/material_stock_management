# Generated by Django 4.2.4 on 2023-09-30 00:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('magasinwcs', '0018_panier_type_alter_panier_fournisseur'),
    ]

    operations = [
        migrations.AlterField(
            model_name='panier',
            name='fournisseur',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='magasinwcs.fournisseur'),
        ),
    ]
