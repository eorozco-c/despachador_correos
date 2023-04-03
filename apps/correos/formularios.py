from django import forms
from .models import Usuario
from django.core.exceptions import ValidationError
from apps.validaciones import obtenerUsuario, validarLongitud, validarEmail, validarLetras
from django.contrib.auth.forms import AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

class FormularioNuevoEjecutivo(forms.ModelForm):

    class Meta:        
        model = Usuario
        fields = ["first_name", "last_name","email"]


    def clean_first_name(self):
        first_name = self.cleaned_data["first_name"]
        validarLetras(first_name,"nombre")
        validarLongitud(first_name,"nombre",2,15)
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data["last_name"]
        validarLetras(last_name,"apellido")
        validarLongitud(last_name,"apellido",2,15)
        return last_name
    
    def clean_email(self):
        email = self.cleaned_data["email"]
        validarEmail(email)
        if obtenerUsuario(email=email):
            raise ValidationError("Correo ya existe")
        return email


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            *self.fields,
           Submit('submit', 'Enviar', css_class='d-grid gap-2 col-2 mx-auto mt-2 ')
        )

class FormularioNuevoEjecutivoUpdate(forms.ModelForm):
    class Meta:        
        model = Usuario
        fields = ["first_name", "last_name","email"]

    def clean_first_name(self):
        first_name = self.cleaned_data["first_name"]
        validarLetras(first_name,"nombre")
        validarLongitud(first_name,"nombre",2,15)
        return first_name
    
    def clean_last_name(self):
        last_name = self.cleaned_data["last_name"]
        validarLetras(last_name,"apellido")
        validarLongitud(last_name,"apellido",2,15)
        return last_name
    
    def clean_email(self):
        email = self.cleaned_data["email"]
        validarEmail(email)
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            *self.fields,
           Submit('submit', 'Enviar', css_class='d-grid gap-2 col-2 mx-auto mt-2 ')
        )

