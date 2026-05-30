from django import forms
from .models import Socio


class SocioForm(forms.ModelForm):
    class Meta:
        model = Socio
        fields = [
            'nombre', 'apellido', 'email', 'telefono', 'dni',
            'tipo', 'estado', 'cantidad_familiares',
            'calle', 'ciudad', 'provincia',
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Juan'}),
            'apellido': forms.TextInput(attrs={'placeholder': 'Pérez'}),
            'email': forms.EmailInput(attrs={'placeholder': 'juan@email.com'}),
            'telefono': forms.TextInput(attrs={'placeholder': '11-1234-5678'}),
            'dni': forms.TextInput(attrs={'placeholder': '12345678'}),
            'calle': forms.TextInput(attrs={'placeholder': 'Av. Corrientes 1234'}),
            'ciudad': forms.TextInput(attrs={'placeholder': 'Buenos Aires'}),
            'provincia': forms.TextInput(attrs={'placeholder': 'Buenos Aires'}),
        }

    def clean_cantidad_familiares(self):
        tipo = self.cleaned_data.get('tipo')
        cantidad = self.cleaned_data.get('cantidad_familiares', 0)
        if tipo == 'familiar' and cantidad < 1:
            raise forms.ValidationError("Un socio familiar debe tener al menos 1 familiar.")
        return cantidad

    def nombre_completo(self):
        nombre = self.cleaned_data.get('nombre', '')
        apellido = self.cleaned_data.get('apellido', '')
        return f"{nombre} {apellido}"
