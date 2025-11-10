from django import forms
from .models import CuentaContable, TipoCuenta, CatalogoCuenta


class CuentaContableForm(forms.ModelForm):
    """
    Formulario para crear y editar cuentas contables.
    """
    class Meta:
        model = CuentaContable
        fields = ['codigo', 'nombre', 'tipo']
        widgets = {
            'codigo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 0101',
                'required': True
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Activos corrientes',
                'required': True
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }, choices=TipoCuenta.choices),
        }
        labels = {
            'codigo': 'Código de la cuenta',
            'nombre': 'Nombre de la cuenta',
            'tipo': 'Tipo de cuenta',
        }
    
    def __init__(self, *args, **kwargs):
        self.catalogo = kwargs.pop('catalogo', None)
        super().__init__(*args, **kwargs)
        # Agregar asterisco a los labels para indicar que son requeridos
        self.fields['codigo'].label += ' *'
        self.fields['nombre'].label += ' *'
        self.fields['tipo'].label += ' *'
    
    def clean_codigo(self):
        codigo = self.cleaned_data.get('codigo')
        if self.catalogo:
            # Verificar que no exista otra cuenta con el mismo código en el mismo catálogo
            queryset = CuentaContable.objects.filter(
                catalogo=self.catalogo,
                codigo=codigo
            )
            if self.instance.pk:
                queryset = queryset.exclude(pk=self.instance.pk)
            if queryset.exists():
                raise forms.ValidationError(
                    f'Ya existe una cuenta con el código "{codigo}" en este catálogo.'
                )
        return codigo


class CargarExcelForm(forms.Form):
    """
    Formulario para cargar un archivo Excel con cuentas contables.
    """
    archivo = forms.FileField(
        label='Archivo Excel',
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.xlsx,.xls',
            'required': True
        }),
        help_text='Seleccione un archivo Excel (.xlsx o .xls) con las cuentas contables'
    )

