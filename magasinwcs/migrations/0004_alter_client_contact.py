# Generated by Django 4.2.4 on 2023-09-01 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('magasinwcs', '0003_alter_employe_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='contact',
            field=models.CharField(blank=True, max_length=60),
        ),
    ]