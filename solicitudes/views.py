from django.shortcuts import render, redirect
from .forms import SolicitudForm, GestionOtForm, OrdenTrabajoForm
from .models import Solicitud, GestionOt, OrdenTrabajo
from django.http import JsonResponse
import json

# Vista para crear una nueva solicitud
def crear_solicitud(request):
    # Verifica si la solicitud es un POST (envío de formulario)
    if request.method == 'POST':
        # Crea una instancia del formulario con los datos recibidos
        form = SolicitudForm(request.POST)
        # Verifica si el formulario es válido
        if form.is_valid():
            # Guarda la nueva solicitud sin confirmarla aún en la base de datos
            nueva_solicitud = form.save(commit=False)
            # Obtiene el número total de solicitudes para asignar un nuevo número activo
            ultimo_numero = Solicitud.objects.count()
            # Asigna un número activo único a la nueva solicitud
            nueva_solicitud.numero_activo = ultimo_numero + 1
            # Establece el estado inicial de la solicitud
            nueva_solicitud.estado = 'Solicitudes'
            # Guarda la solicitud en la base de datos
            nueva_solicitud.save()
            # Redirige al usuario al formulario de crear solicitud después de guardar
            return redirect('crear_solicitud')
        else:
            # Si hay errores en el formulario, los imprime en la consola
            print("Errores en el formulario:", form.errors)
    else:
        # Si la solicitud no es un POST, crea un formulario vacío
        form = SolicitudForm()

    # Renderiza la plantilla 'crear_solicitud.html' con el formulario
    return render(request, 'solicitudes/crear_solicitud.html', {'form': form})

# Vista para gestionar órdenes de trabajo
def gestion_ot(request):
    # Verifica si la solicitud es un GET (petición de datos)
    if request.method == 'GET':
        # Crea una instancia del formulario de gestión de órdenes de trabajo
        form = GestionOtForm()
        # Obtiene todas las órdenes de trabajo existentes
        ordenes_trabajo = OrdenTrabajo.objects.all()
        # Filtra las solicitudes que aún no tienen gestión de OT asociada
        solicitudes_pendientes = Solicitud.objects.filter(gestionot__isnull=True)

        # Renderiza la plantilla 'gestion_ot.html' con los formularios y datos necesarios
        return render(request, 'solicitudes/gestion_ot.html', {
            'form': form,
            'ordenes_trabajo': ordenes_trabajo,
            'solicitudes': solicitudes_pendientes
        })

# Vista para actualizar el estado de una solicitud
# Modificar la vista para actualizar el estado de la solicitud

from django.http import JsonResponse
import json
from .models import Solicitud, OrdenTrabajo


def actualizar_estado_solicitud(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            numero_solicitud = data.get('numero')
            nuevo_estado = data.get('estado')
            tecnico = data.get('tecnico')
            fecha = data.get('fecha')

            if not numero_solicitud or not nuevo_estado:
                return JsonResponse({'status': 'error', 'message': 'Número y estado son requeridos.'}, status=400)

            if not fecha:
                return JsonResponse({'status': 'error', 'message': 'Fecha de actividad es requerida.'}, status=400)

            try:
                solicitud = Solicitud.objects.get(numero_activo=numero_solicitud)
                solicitud.estado = nuevo_estado
                if tecnico:
                    solicitud.tecnico_asignado = tecnico
                solicitud.fecha_actividad = fecha
                solicitud.save()

                # Crear o actualizar la Orden de Trabajo
                orden_trabajo, created = OrdenTrabajo.objects.update_or_create(
                    numero_solicitud=solicitud.consecutivo,
                    defaults={
                        'tecnico_asignado': tecnico,
                        'fecha_actividad': fecha,
                        'estado': nuevo_estado
                    }
                )

                return JsonResponse({'status': 'ok', 'message': 'Solicitud y Orden de Trabajo actualizadas correctamente'})

            except Solicitud.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Solicitud no encontrada'}, status=404)
            except Exception as e:
                # Capturar cualquier otra excepción y registrar el error
                return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Error al decodificar JSON'}, status=400)


# Vista para listar todas las órdenes de trabajo
def listar_ot(request):
    # Obtiene todas las órdenes de trabajo
    ots = OrdenTrabajo.objects.all()
    # Renderiza la plantilla 'listar_ot.html' con las órdenes de trabajo
    return render(request, 'solicitudes/listar_ot.html', {'ots': ots})




from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Region, PuntoDeVenta, Activo
from .forms import RegionForm, PuntoDeVentaForm, ActivoForm

def gestionar_activos(request):
    regiones = Region.objects.all()
    pdvs = PuntoDeVenta.objects.all()
    activos = Activo.objects.all()
    region_form = RegionForm()
    pdv_form = PuntoDeVentaForm()
    activo_form = ActivoForm()

    if request.method == 'POST':
        if 'crear_region' in request.POST:
            region_form = RegionForm(request.POST)
            if region_form.is_valid():
                region_form.save()
                return redirect('gestionar_activos')
        elif 'crear_pdv' in request.POST:
            pdv_form = PuntoDeVentaForm(request.POST)
            if pdv_form.is_valid():
                pdv_form.save()
                return redirect('gestionar_activos')
        elif 'crear_activo' in request.POST:
            activo_form = ActivoForm(request.POST)
            if activo_form.is_valid():
                activo_form.save()
                return redirect('gestionar_activos')

    return render(request, 'solicitudes/gestionar_activos.html', {
        'regiones': regiones,
        'pdvs': pdvs,
        'activos': activos,
        'region_form': region_form,
        'pdv_form': pdv_form,
        'activo_form': activo_form
    })

def crear_region_ajax(request):
    if request.method == 'POST':
        form = RegionForm(request.POST)
        if form.is_valid():
            region = form.save()
            return JsonResponse({'status': 'ok', 'region': {'id': region.id, 'nombre': region.nombre}})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})

def crear_pdv_ajax(request):
    if request.method == 'POST':
        form = PuntoDeVentaForm(request.POST)
        if form.is_valid():
            pdv = form.save()
            return JsonResponse({'status': 'ok', 'pdv': {'id': pdv.id, 'nombre': pdv.nombre, 'codigo': pdv.codigo, 'region': pdv.region.nombre}})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})

def crear_activo_ajax(request):
    if request.method == 'POST':
        form = ActivoForm(request.POST)
        if form.is_valid():
            activo = form.save()
            return JsonResponse({'status': 'ok', 'activo': {
                'id': activo.id,
                'punto_de_venta': activo.punto_de_venta.nombre if activo.punto_de_venta else None,
                'tipo_equipo': activo.tipo_equipo,
                'nombre_equipo': activo.nombre_equipo,
                'tipo_maquinaria': activo.tipo_maquinaria,
                'tipo_locativo': activo.tipo_locativo
            }})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
