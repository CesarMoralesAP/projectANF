from django import forms
from apps.estados.models import Empresa, Sector

class EmpresaForm(forms.ModelForm):
    catalogo_excel = forms.FileField(
        required=False,
        label="Catálogo de Cuentas (Excel)",
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Empresa
        fields = ['nombre', 'sector'] 
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre de la empresa'
            }),
            'sector': forms.Select(attrs={'class': 'form-select'}),
        }
