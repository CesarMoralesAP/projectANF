from django.urls import path
from .views import EmpresaListView, EmpresaDeleteView

app_name = 'catalogos'

urlpatterns = [
    path('empresas/', EmpresaListView.as_view(), name='empresa_lista'),
    path('empresas/<int:pk>/eliminar/', EmpresaDeleteView.as_view(), name='empresa_eliminar'),
]
