from django.urls import path
from apps.analisis.views import (
    AnalisisFinancieroView, 
    ValidarEstadosView,
    AnalisisHorizontalBalanceView,
    AnalisisHorizontalResultadosView,
    AnalisisVerticalBalanceView,
    AnalisisVerticalResultadosView
)

app_name = 'analisis'

urlpatterns = [
    path('', AnalisisFinancieroView.as_view(), name='analisis_financiero'),
    path('validar-estados/', ValidarEstadosView.as_view(), name='validar_estados'),
    path('analisis-horizontal/balance/', AnalisisHorizontalBalanceView.as_view(), name='analisis_horizontal_balance'),
    path('analisis-horizontal/resultados/', AnalisisHorizontalResultadosView.as_view(), name='analisis_horizontal_resultados'),
    path('analisis-vertical/balance/', AnalisisVerticalBalanceView.as_view(), name='analisis_vertical_balance'),
    path('analisis-vertical/resultados/', AnalisisVerticalResultadosView.as_view(), name='analisis_vertical_resultados'),
]

