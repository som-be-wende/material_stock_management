# Generated by Django 4.2.4 on 2023-09-02 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('magasinwcs', '0006_utilisation_quantite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commande',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
