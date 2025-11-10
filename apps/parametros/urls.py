from django.urls import path
from .views import ParametrosSectorialesView, GuardarParametrosSectorView

app_name = 'parametros'

urlpatterns = [
    path('', ParametrosSectorialesView.as_view(), name='parametros_sectoriales'),
    path('guardar-parametros/', GuardarParametrosSectorView.as_view(), name='guardar_parametros'),
]
