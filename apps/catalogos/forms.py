from django import forms
from .models import Empresa, Sector


class EmpresaForm(forms.ModelForm):
    """
    Formulario para crear y editar empresas.
    Solo incluye nombre y sector (sin NIT).
    """
    class Meta:
        model = Empresa
        fields = ['nombre', 'sector']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Industrias ABC S.A.',
                'required': True
            }),
            'sector': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
        }
        labels = {
            'nombre': 'Nombre de la Empresa',
            'sector': 'Sector',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Cargar solo sectores activos
        self.fields['sector'].queryset = Sector.objects.filter(activo=True).order_by('nombre')
        self.fields['sector'].empty_label = 'Seleccione un sector'
        # Agregar asterisco a los labels para indicar que son requeridos
        self.fields['nombre'].label += ' *'
        self.fields['sector'].label += ' *'

