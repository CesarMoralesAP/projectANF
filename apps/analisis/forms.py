from django import forms
from .models import ProyeccionFinanciera, OrigenDatos


class SubirProyeccionForm(forms.ModelForm):
    """
    Formulario para subir proyección desde archivo Excel.
    """
    class Meta:
        model = ProyeccionFinanciera
        fields = ['nombre', 'descripcion', 'archivo']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Proyección 2025',
                'required': True
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción opcional de la proyección...',
                'rows': 3
            }),
            'archivo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.xlsx,.xls',
                'required': True
            }),
        }
        labels = {
            'nombre': 'Nombre de la Proyección',
            'descripcion': 'Descripción',
            'archivo': 'Archivo Excel',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Marcar campos requeridos
        self.fields['nombre'].label += ' *'
        self.fields['archivo'].label += ' *'
        
        # Agregar help text
        self.fields['archivo'].help_text = (
            'El archivo debe contener tres hojas: '
            '"valor incremental", "valor absoluto" y "minimos cuadrados" '
            'con las columnas "Mes" y "Venta".'
        )
    
    def clean_archivo(self):
        """
        Valida el archivo subido.
        """
        archivo = self.cleaned_data.get('archivo')
        
        if archivo:
            # Validar extensión
            nombre_archivo = archivo.name.lower()
            if not (nombre_archivo.endswith('.xlsx') or nombre_archivo.endswith('.xls')):
                raise forms.ValidationError(
                    'Solo se permiten archivos Excel (.xlsx, .xls)'
                )
            
            # Validar tamaño (máximo 5MB)
            if archivo.size > 5 * 1024 * 1024:
                raise forms.ValidationError(
                    'El archivo no debe superar 5MB'
                )
        
        return archivo
