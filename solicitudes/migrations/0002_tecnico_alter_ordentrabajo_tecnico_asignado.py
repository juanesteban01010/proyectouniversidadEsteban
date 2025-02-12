# Generated by Django 4.2.16 on 2024-10-23 18:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('solicitudes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tecnico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='ordentrabajo',
            name='tecnico_asignado',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='solicitudes.tecnico'),
        ),
    ]
