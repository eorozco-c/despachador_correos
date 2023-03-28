from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django.core.exceptions import ValidationError

from apps.validaciones import validarEmail
from .models import Casilla,  Configuracion

class FormularioCasilla(forms.ModelForm):
    class Meta:
        model = Casilla
        fields = ["email", "password"]

        widgets = {
            "password" : forms.PasswordInput(render_value=True),
        }

    def clean_email(self):
        email = self.cleaned_data["email"]
        validarEmail(email)
        return email
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
           *self.fields,
           Submit('submit', 'Enviar', css_class='d-grid gap-2 col-2 mx-auto mt-2 text-light border botonnew')
        )

#Formulario de Configuraciones

class FormularioConfiguracion(forms.ModelForm):

    class Meta:        
        model = Configuracion
        fields = ["casilla","tipo_servicio","id_usuario","id_tenant","id_app","id_key","api_key","protocolo"]

        labels ={
                    "casilla" : "Casilla de Correo",
                    "tipo_servicio" : "Tipo de Servicio"
                } 
      
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            *self.fields,
           Submit('submit', 'Enviar', css_class='d-grid gap-2 col-2 mx-auto mt-2 ')
        )
