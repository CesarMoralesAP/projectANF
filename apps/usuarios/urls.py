from django.urls import path
from django.views.generic import RedirectView
from .views import VistaLogin, VistaLogout

app_name = 'usuarios'

urlpatterns = [
    path('', VistaLogin.as_view(), name='login'),
    path('login/', VistaLogin.as_view(), name='login'),
    path('logout/', VistaLogout.as_view(), name='logout'),
]

