from django.urls import path
from .views import (
    CatalogoContableView,
    DescargarPlantillaView,
    CargarExcelView,
    AgregarCuentaView,
    EliminarCuentaView
)

app_name = 'catalogos'

urlpatterns = [
    path('', CatalogoContableView.as_view(), name='catalogo_lista'),
    path('descargar-plantilla/', DescargarPlantillaView.as_view(), name='descargar_plantilla'),
    path('cargar-excel/', CargarExcelView.as_view(), name='cargar_excel'),
    path('agregar-cuenta/', AgregarCuentaView.as_view(), name='agregar_cuenta'),
    path('eliminar-cuenta/<int:cuenta_id>/', EliminarCuentaView.as_view(), name='eliminar_cuenta'),
]
