"""
Mixins personalizados para control de permisos en las vistas.
"""
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy


class PermisoEliminarMixin(UserPassesTestMixin):
    """
    Mixin que verifica si el usuario tiene permiso para eliminar.
    Solo los usuarios con permisos de 'delete' pueden acceder.
    Los superusuarios siempre tienen acceso.
    """
    
    def test_func(self):
        """
        Verifica si el usuario tiene permiso de eliminación.
        """
        user = self.request.user
        
        # Los superusuarios siempre tienen acceso
        if user.is_superuser:
            return True
        
        # Obtener el nombre del modelo
        model_name = self.model._meta.model_name
        app_label = self.model._meta.app_label
        
        # Verificar si tiene el permiso específico de delete
        permission_codename = f'{app_label}.delete_{model_name}'
        
        return user.has_perm(permission_codename)
    
    def handle_no_permission(self):
        """
        Qué hacer cuando el usuario NO tiene permiso.
        """
        messages.error(
            self.request,
            '❌ No tienes permisos para eliminar registros. Contacta al administrador.'
        )
        # Redirigir a la página anterior o a una URL de respaldo
        return redirect(self.request.META.get('HTTP_REFERER', '/'))


class PermisoCrearMixin(UserPassesTestMixin):
    """
    Mixin que verifica si el usuario tiene permiso para crear.
    """
    
    def test_func(self):
        user = self.request.user
        
        if user.is_superuser:
            return True
        
        model_name = self.model._meta.model_name
        app_label = self.model._meta.app_label
        permission_codename = f'{app_label}.add_{model_name}'
        
        return user.has_perm(permission_codename)
    
    def handle_no_permission(self):
        messages.error(
            self.request,
            '❌ No tienes permisos para crear registros.'
        )
        return redirect(self.request.META.get('HTTP_REFERER', '/'))


class PermisoEditarMixin(UserPassesTestMixin):
    """
    Mixin que verifica si el usuario tiene permiso para editar.
    """
    
    def test_func(self):
        user = self.request.user
        
        if user.is_superuser:
            return True
        
        model_name = self.model._meta.model_name
        app_label = self.model._meta.app_label
        permission_codename = f'{app_label}.change_{model_name}'
        
        return user.has_perm(permission_codename)
    
    def handle_no_permission(self):
        messages.error(
            self.request,
            '❌ No tienes permisos para editar registros.'
        )
        return redirect(self.request.META.get('HTTP_REFERER', '/'))
