from django.urls import path
from .views import (
    EstadoFinancieroView,
    DescargarPlantillaEstadoView,
    GuardarEstadoFinancieroView,
    CargarExcelEstadoView,
    VerEstadoFinancieroView,
    EditarEstadoFinancieroView,
    EliminarEstadoFinancieroView
)

app_name = 'estados'

urlpatterns = [
    path('', EstadoFinancieroView.as_view(), name='estado_financiero'),
    path('descargar-plantilla/', DescargarPlantillaEstadoView.as_view(), name='descargar_plantilla'),
    path('guardar/', GuardarEstadoFinancieroView.as_view(), name='guardar_estado'),
    path('cargar-excel/', CargarExcelEstadoView.as_view(), name='cargar_excel'),
    path('ver/<int:estado_id>/', VerEstadoFinancieroView.as_view(), name='ver_estado'),
    path('editar/<int:estado_id>/', EditarEstadoFinancieroView.as_view(), name='editar_estado'),
    path('eliminar/<int:estado_id>/', EliminarEstadoFinancieroView.as_view(), name='eliminar_estado'),
]

