# models.py
from datetime import timezone
from django.db import models

class Solicitud(models.Model):
    consecutivo = models.AutoField(primary_key=True)
    creado_por = models.CharField(max_length=100)
    descripcion_problema = models.TextField()
    numero_activo = models.IntegerField()
    email_solicitante = models.EmailField(max_length=254, null=True)
    fecha_creacion = models.DateTimeField(blank=True, null=True)
    PDV = models.CharField(max_length=100, default='') 
    estado = models.CharField(max_length=20, choices=[
        ('solicitudes', 'Solicitudes'),
        ('en proceso', 'OT en Proceso'),
        ('en revision', 'OT en Revisión'),
        ('finalizada', 'OT Finalizada')
    ], default='solicitudes')


    def __str__(self):
        return f"Solicitud {self.consecutivo}"
    
class GestionOt(models.Model):
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE)
    tecnico = models.CharField(max_length=100)
    fecha_asignacion = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"GestionOt {self.solicitud}"
    
class OrdenTrabajo(models.Model):

    numero_solicitud = models.IntegerField()
    tecnico_asignado = models.CharField(max_length=100)
    fecha_actividad = models.DateTimeField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=[
        ('solicitudes', 'Solicitudes'),
        ('en proceso', 'OT en Proceso'),
        ('en revision', 'OT en Revisión'),
        ('finalizada', 'OT Finalizada')
    ], default='solicitudes')

    def __str__(self):
        return f"OT-{self.numero_solicitud} - {self.tecnico_asignado}"
    
from django.db import models

class Region(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
    
    

class PuntoDeVenta(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10, unique=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='puntos_de_venta')

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"

class Activo(models.Model):
    TIPO_EQUIPO_CHOICES = [
        ('maquinaria', 'Maquinaria'),
        ('locativo', 'Locativo')
    ]

    TIPO_MAQUINARIA_CHOICES = [
        ('maquina_helado', 'Máquina de Helado Suave'),
        ('congelador', 'Congelador'),
        ('vitrina', 'Vitrina')
    ]

    TIPO_LOCATIVO_CHOICES = [
        ('muebles', 'Muebles'),
        ('paredes', 'Paredes'),
        ('techo', 'Techo'),
        ('cortinas', 'Cortinas')
    ]

    punto_de_venta = models.ForeignKey(PuntoDeVenta, on_delete=models.CASCADE, related_name='activos', null=True, blank=True)
    tipo_equipo = models.CharField(max_length=10, choices=TIPO_EQUIPO_CHOICES)
    nombre_equipo = models.CharField(max_length=100, blank=True, null=True)
    tipo_maquinaria = models.CharField(max_length=20, choices=TIPO_MAQUINARIA_CHOICES, blank=True, null=True)
    tipo_locativo = models.CharField(max_length=20, choices=TIPO_LOCATIVO_CHOICES, blank=True, null=True)

    def __str__(self):
        return f"{self.tipo_equipo} - {self.nombre_equipo or self.tipo_maquinaria or self.tipo_locativo}"
