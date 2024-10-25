from django import forms
from .models import Solicitud, GestionOt, OrdenTrabajo

class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = ['consecutivo', 'creado_por', 'descripcion_problema', 'numero_activo', 'email_solicitante', 'PDV', 'fecha_creacion']

class GestionOtForm(forms.ModelForm):
    class Meta:
        model = GestionOt
        fields = ['solicitud', 'tecnico']  # Puedes incluir otros campos si lo deseas

class OrdenTrabajoForm(forms.ModelForm):
    class Meta:
        model = OrdenTrabajo
        fields = ['numero_solicitud', 'tecnico_asignado', 'estado', 'fecha_actividad']
        widgets = {
            'numero_solicitud': forms.TextInput(attrs={'readonly': 'readonly'}),  # Este campo será solo lectura
            'fecha_actividad': forms.DateInput(attrs={'type': 'date'}),
        }

from django import forms
from .models import Region, PuntoDeVenta, Activo

class RegionForm(forms.ModelForm):
    class Meta:
        model = Region
        fields = ['nombre']

class PuntoDeVentaForm(forms.ModelForm):
    class Meta:
        model = PuntoDeVenta
        fields = ['nombre', 'codigo', 'region']

class ActivoForm(forms.ModelForm):
    class Meta:
        model = Activo
        fields = ['punto_de_venta', 'tipo_equipo', 'nombre_equipo', 'tipo_maquinaria', 'tipo_locativo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo_maquinaria'].widget.attrs['class'] = 'maquinaria-field'
        self.fields['tipo_locativo'].widget.attrs['class'] = 'locativo-field'
        self.fields['nombre_equipo'].widget.attrs['class'] = 'maquinaria-field'
        self.fields['tipo_maquinaria'].widget.attrs['class'] = 'maquinaria-field'
        self.fields['tipo_locativo'].widget.attrs['class'] = 'locativo-field'
