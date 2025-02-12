# Generated by Django 4.2.16 on 2024-10-24 02:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OrdenTrabajo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_solicitud', models.IntegerField()),
                ('tecnico_asignado', models.CharField(max_length=100)),
                ('fecha_actividad', models.DateTimeField(blank=True, null=True)),
                ('estado', models.CharField(choices=[('solicitudes', 'Solicitudes'), ('en proceso', 'OT en Proceso'), ('en revision', 'OT en Revisión'), ('finalizada', 'OT Finalizada')], default='solicitudes', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Solicitud',
            fields=[
                ('consecutivo', models.AutoField(primary_key=True, serialize=False)),
                ('creado_por', models.CharField(max_length=100)),
                ('descripcion_problema', models.TextField()),
                ('numero_activo', models.IntegerField()),
                ('email_solicitante', models.EmailField(max_length=254, null=True)),
                ('fecha_creacion', models.DateTimeField(blank=True, null=True)),
                ('PDV', models.CharField(default='', max_length=100)),
                ('estado', models.CharField(choices=[('solicitudes', 'Solicitudes'), ('en proceso', 'OT en Proceso'), ('en revision', 'OT en Revisión'), ('finalizada', 'OT Finalizada')], default='solicitudes', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='PuntoDeVenta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('codigo', models.CharField(max_length=10, unique=True)),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='puntos_de_venta', to='solicitudes.region')),
            ],
        ),
        migrations.CreateModel(
            name='GestionOt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tecnico', models.CharField(max_length=100)),
                ('fecha_asignacion', models.DateField(auto_now_add=True)),
                ('solicitud', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='solicitudes.solicitud')),
            ],
        ),
        migrations.CreateModel(
            name='Activo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_equipo', models.CharField(choices=[('maquinaria', 'Maquinaria'), ('locativo', 'Locativo')], max_length=10)),
                ('nombre_equipo', models.CharField(blank=True, max_length=100, null=True)),
                ('tipo_maquinaria', models.CharField(blank=True, choices=[('maquina_helado', 'Máquina de Helado Suave'), ('congelador', 'Congelador'), ('vitrina', 'Vitrina')], max_length=20, null=True)),
                ('tipo_locativo', models.CharField(blank=True, choices=[('muebles', 'Muebles'), ('paredes', 'Paredes'), ('techo', 'Techo'), ('cortinas', 'Cortinas')], max_length=20, null=True)),
                ('punto_de_venta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='activos', to='solicitudes.puntodeventa')),
            ],
        ),
    ]
