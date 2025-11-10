from django import forms
from django.forms import formset_factory
from apps.estados.models import EstadoFinanciero, ItemEstadoFinanciero, TipoEstadoFinanciero
from apps.empresas.models import Empresa
from apps.catalogos.models import CatalogoCuenta, CuentaContable, TipoCuenta
from datetime import datetime


class EstadoFinancieroForm(forms.Form):
    """
    Formulario para seleccionar empresa, año y tipo de estado financiero.
    """
    empresa = forms.ModelChoiceField(
        queryset=Empresa.objects.all().order_by('nombre'),
        required=True,
        label='Empresa',
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_empresa'
        })
    )
    año = forms.IntegerField(
        required=True,
        label='Año',
        initial=lambda: datetime.now().year,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'id': 'id_año',
            'min': '2000',
            'max': '2100'
        })
    )
    tipo = forms.ChoiceField(
        choices=TipoEstadoFinanciero.choices,
        required=True,
        label='Tipo de Estado',
        widget=forms.Select(attrs={
            'class': 'form-control',
            'id': 'id_tipo'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Establecer año actual por defecto si no se proporciona
        if not self.data and not self.initial.get('año'):
            self.fields['año'].initial = datetime.now().year


class ItemEstadoFinancieroForm(forms.Form):
    """
    Formulario para un item individual del estado financiero.
    """
    cuenta_id = forms.IntegerField(
        required=True,
        widget=forms.HiddenInput()
    )
    monto = forms.DecimalField(
        max_digits=15,
        decimal_places=2,
        required=False,
        initial=0.00,
        widget=forms.NumberInput(attrs={
            'class': 'form-control monto-input',
            'step': '0.01',
            'min': '0'
        })
    )


ItemEstadoFinancieroFormSet = formset_factory(
    ItemEstadoFinancieroForm,
    extra=0,
    can_delete=False
)


class CargarExcelEstadoForm(forms.Form):
    """
    Formulario para cargar un archivo Excel con datos del estado financiero.
    """
    archivo = forms.FileField(
        label='Archivo Excel',
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.xlsx,.xls',
            'required': True
        }),
        help_text='Seleccione un archivo Excel (.xlsx o .xls) con los datos del estado financiero'
    )
    
    def clean_archivo(self):
        archivo = self.cleaned_data.get('archivo')
        if archivo:
            # Validar extensión
            if not archivo.name.endswith(('.xlsx', '.xls')):
                raise forms.ValidationError('El archivo debe ser un archivo Excel (.xlsx o .xls)')
            
            # Validar tamaño (máximo 10MB)
            if archivo.size > 10 * 1024 * 1024:
                raise forms.ValidationError('El archivo no puede ser mayor a 10MB')
        
        return archivo

