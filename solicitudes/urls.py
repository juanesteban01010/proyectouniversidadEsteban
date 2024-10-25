from django.urls import path
from .views import crear_solicitud, gestion_ot, actualizar_estado_solicitud, listar_ot
from .views import gestionar_activos, crear_region_ajax, crear_pdv_ajax, crear_activo_ajax

urlpatterns = [
    path('crear_solicitud/', crear_solicitud, name='crear_solicitud'),
    path('gestion_ot/', gestion_ot, name='gestion_ot'),
    path('actualizar_estado_solicitud/', actualizar_estado_solicitud, name='actualizar_estado_solicitud'),
    path('listar_ot/', listar_ot, name='listar_ot'),
    path('activos/', gestionar_activos, name='gestionar_activos'),
    path('activos/crear_region/', crear_region_ajax, name='crear_region_ajax'),
    path('activos/crear_pdv/', crear_pdv_ajax, name='crear_pdv_ajax'),
    path('activos/crear_activo/', crear_activo_ajax, name='crear_activo_ajax'),
]
