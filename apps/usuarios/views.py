from django.shortcuts import redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import RedirectView
from .forms import FormularioLogin


class VistaLogin(LoginView):
    """
    Vista basada en clase para el inicio de sesión.
    """
    template_name = 'usuarios/login.html'
    form_class = FormularioLogin
    redirect_authenticated_user = True
    
    def get_success_url(self):
        """Redirige después de un login exitoso."""
        return reverse_lazy('empresas:empresa_lista')
    
    def form_valid(self, form):
        """Maneja un formulario válido."""
        usuario = form.get_user()
        nombre_completo = usuario.get_full_name() if usuario.get_full_name() else usuario.email
        messages.success(self.request, 'Inicio de sesión exitoso')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """Maneja un formulario inválido."""
        # El formulario ya maneja los errores de validación y los muestra en el template
        # No necesitamos agregar un mensaje adicional aquí para evitar duplicados
        return super().form_invalid(form)


class VistaLogout(LogoutView):
    """
    Vista basada en clase para cerrar sesión.
    """
    next_page = reverse_lazy('usuarios:login')
    http_method_names = ['post', 'get']  # Permitir GET y POST para compatibilidad
    
    def dispatch(self, request, *args, **kwargs):
        """Muestra mensaje al cerrar sesión."""
        if request.user.is_authenticated:
            messages.success(request, 'Sesión cerrada exitosamente.')
        return super().dispatch(request, *args, **kwargs)
