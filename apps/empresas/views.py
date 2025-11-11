from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Empresa, Sector
from .forms import EmpresaForm
from apps.core.mixins import PermisoEliminarMixin


class EmpresaListView(LoginRequiredMixin, ListView):
    """
    Vista para listar todas las empresas y crear nuevas.
    Maneja GET para mostrar lista y formulario, POST para crear empresa.
    """
    model = Empresa
    template_name = 'empresas/empresa_lista.html'
    context_object_name = 'empresas'
    paginate_by = 10
    form_class = EmpresaForm
    
    def get_queryset(self):
        return Empresa.objects.all().select_related('sector').order_by('nombre')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Verificar si se debe mostrar el formulario
        mostrar_formulario = self.request.GET.get('nueva') == '1'
        
        # Si hay un formulario en kwargs (viene de POST con errores), usarlo
        if 'form' in kwargs:
            context['form'] = kwargs['form']
            context['mostrar_formulario'] = True
        elif mostrar_formulario:
            # Inicializar formulario vacío para GET
            context['form'] = self.form_class()
            context['mostrar_formulario'] = True
        else:
            context['form'] = None
            context['mostrar_formulario'] = False
        
        # Cargar sectores para el select
        context['sectores'] = Sector.objects.all().order_by('nombre')
        
        return context
    
    def post(self, request, *args, **kwargs):
        """
        Maneja la creación de una nueva empresa.
        """
        self.object_list = self.get_queryset()
        form = self.form_class(request.POST)
        
        if form.is_valid():
            empresa = form.save()
            messages.success(request, f'Empresa "{empresa.nombre}" creada exitosamente.')
            return redirect('empresas:empresa_lista')
        else:
            # Si hay errores, renderizar la página con el formulario y errores
            messages.error(request, 'Por favor, corrija los errores en el formulario.')
            context = self.get_context_data(form=form, **kwargs)
            return self.render_to_response(context)
    
    def get(self, request, *args, **kwargs):
        """
        Maneja GET para mostrar la lista y opcionalmente el formulario.
        """
        return super().get(request, *args, **kwargs)


class EmpresaDeleteView(PermisoEliminarMixin, LoginRequiredMixin, DeleteView):
    """
    Vista para eliminar una empresa.
    Solo usuarios con permiso 'delete_empresa' pueden acceder.
    """
    model = Empresa
    success_url = reverse_lazy('empresas:empresa_lista')
    
    def delete(self, request, *args, **kwargs):
        """
        Sobrescribe el método delete para mostrar mensaje personalizado.
        """
        empresa = self.get_object()
        nombre_empresa = empresa.nombre
        empresa.delete()  # Eliminación permanente
        messages.success(request, f'Empresa "{nombre_empresa}" eliminada exitosamente.')
        return redirect(self.success_url)

