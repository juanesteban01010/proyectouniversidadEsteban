# Generated by Django 4.2.16 on 2024-10-18 17:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('solicitudes', '0004_rename_email_solicitant_solicitud_email_solicitante_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='OrdenTrabajo',
            new_name='GestionOt',
        ),
    ]
