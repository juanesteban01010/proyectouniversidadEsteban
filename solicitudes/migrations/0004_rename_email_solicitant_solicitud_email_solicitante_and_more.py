# Generated by Django 4.2.16 on 2024-10-16 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solicitudes', '0003_solicitud_pdv_solicitud_email_solicitant_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='solicitud',
            old_name='email_solicitant',
            new_name='email_solicitante',
        ),
        migrations.AlterField(
            model_name='solicitud',
            name='PDV',
            field=models.CharField(default='', max_length=100),
        ),
    ]
