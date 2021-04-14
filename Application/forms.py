from django import forms
from models.models import *


class SalidaLoteForm(forms.ModelForm):
    class Meta:
        model = SalidaLote
        fields = [
            'cantidad_salida',
            'lote',
            'descripcion',
        ]
        labels = {
            'cantidad_salida': 'Cantidad Salida',
            'lote': 'Lote',
            'descripcion': 'descripcion',
        }
        widgets = {
            'cantidad_salida': forms.TextInput(attrs={'class': 'form-control'}),
            'lote': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
        }
