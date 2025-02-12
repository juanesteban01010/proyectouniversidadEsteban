# Generated by Django 4.2.16 on 2024-10-16 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solicitudes', '0002_remove_solicitud_titulo'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitud',
            name='PDV',
            field=models.CharField(default='valor_predeterminado', max_length=100),
        ),
        migrations.AddField(
            model_name='solicitud',
            name='email_solicitant',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='solicitud',
            name='fecha_creacion',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
