from django import forms
from .models import RatioReferenciaSector


class RatioReferenciaSectorForm(forms.ModelForm):
    """
    Formulario para crear y editar valores de referencia de ratios por sector.
    """
    class Meta:
        model = RatioReferenciaSector
        fields = ['valor_optimo']
        widgets = {
            'valor_optimo': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.0001',
                'placeholder': '0.0000'
            })
        }
        labels = {
            'valor_optimo': ''
        }


class GuardarParametrosSectorForm(forms.Form):
    """
    Formulario para guardar múltiples valores de referencia de ratios para un sector.
    """
    def __init__(self, *args, **kwargs):
        self.sector = kwargs.pop('sector', None)
        self.ratios = kwargs.pop('ratios', [])
        super().__init__(*args, **kwargs)
        
        # Crear un campo para cada ratio
        for ratio in self.ratios:
            field_name = f'ratio_{ratio.id}'
            self.fields[field_name] = forms.DecimalField(
                required=False,
                max_digits=10,
                decimal_places=4,
                widget=forms.NumberInput(attrs={
                    'class': 'form-control',
                    'step': '0.0001',
                    'placeholder': '0.0000'
                })
            )

