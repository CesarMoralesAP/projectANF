from django.urls import path
from apps.analisis.views import AnalisisFinancieroView, ValidarEstadosView

app_name = 'analisis'

urlpatterns = [
    path('', AnalisisFinancieroView.as_view(), name='analisis_financiero'),
    path('validar-estados/', ValidarEstadosView.as_view(), name='validar_estados'),
]

