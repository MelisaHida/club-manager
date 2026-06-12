from django import forms #Importa la clase forms de Django para crear formularios basados en modelos.
from .models import Socio


class SocioForm(forms.ModelForm):  # Define una clase formulario que hereda de forms.ModelForm, lo que permite crear un formulario basado en el modelo Socio desde socios.models.
    class Meta:  #creamos la clase Meta para especificar el modelo y los campos que se incluirán en el formulario.
        model = Socio # Especifica que el formulario se basa en el modelo Socio.
        fields = [
            'nombre', 'apellido', 'email', 'telefono', 'dni',
            'tipo', 'estado', 'cantidad_familiares',
            'calle', 'ciudad', 'provincia',
        ]
        widgets = {                 #Nos va a permitir ver en cada campo una referencia de ayuda para que el usuario sepa qué tipo de información debe ingresar.     
            'nombre': forms.TextInput(attrs={'placeholder': 'Juan'}),
            'apellido': forms.TextInput(attrs={'placeholder': 'Pérez'}),
            'email': forms.EmailInput(attrs={'placeholder': 'juan@email.com'}),
            'telefono': forms.TextInput(attrs={'placeholder': '11-1234-5678'}),
            'dni': forms.TextInput(attrs={'placeholder': '12345678'}),
            'calle': forms.TextInput(attrs={'placeholder': 'Av. Corrientes 1234'}),
            'ciudad': forms.TextInput(attrs={'placeholder': 'Buenos Aires'}),
            'provincia': forms.TextInput(attrs={'placeholder': 'Buenos Aires'}),
        }

    def clean_cantidad_familiares(self):    #Sirve para validar la cantidad de familiares en función del tipo de socio seleccionado. Si el tipo es 'familiar' y la cantidad es menor a 1, se lanza una excepción de validación.
        tipo = self.cleaned_data.get('tipo')
        cantidad = self.cleaned_data.get('cantidad_familiares', 0)
        if tipo == 'familiar' and cantidad < 1:
            raise forms.ValidationError("Un socio familiar debe tener al menos 1 familiar.")
        return cantidad

    def nombre_completo(self):    
        nombre = self.cleaned_data.get('nombre', '')
        apellido = self.cleaned_data.get('apellido', '')
        return f"{nombre} {apellido}"
