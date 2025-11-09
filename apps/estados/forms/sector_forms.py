from django import forms
from apps.estados.models import Sector
import json

class SectorForm(forms.ModelForm):
    ratios_keys = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )
    ratios_values = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )

    class Meta:
        model = Sector
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del sector'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción breve'}),
        }

    def save(self, commit=True):
        sector = super().save(commit=False)
        keys = self.data.getlist('ratio_name[]')
        values = self.data.getlist('ratio_value[]')

        ratios = {}
        for i, key in enumerate(keys):
            if key.strip():
                try:
                    ratios[key.strip()] = float(values[i])
                except (ValueError, IndexError):
                    ratios[key.strip()] = None

        sector.valor_referencia = ratios
        if commit:
            sector.save()
        return sector