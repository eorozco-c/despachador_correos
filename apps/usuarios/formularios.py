from django import forms
from .models import Usuario
from django.core.exceptions import ValidationError
from apps.validaciones import obtenerUsuario, validarLongitud, validarEmail, validarLetras
from django.contrib.auth.forms import AuthenticationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.EmailField(widget=forms.TextInput(
        attrs={
            'class': 'form-control form-control-user inputnew p-2', 
            'placeholder': 'USUARIO'
            }), 
            label="")
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control form-control-user inputnew mt-3 p-2',
            'placeholder': 'CONTRASEÑA',
        }),
        label="")
    
class FormularioRegistro(forms.ModelForm):
    confirmarPassword = forms.CharField(max_length=255, label="Confirmar Password")
    confirmarPassword.widget = forms.PasswordInput()

    class Meta:        
        model = Usuario
        fields = ["first_name", "last_name","is_superuser", "email","password","confirmarPassword"]

        widgets = {
            "password" : forms.PasswordInput(),
        }

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
        usuario = obtenerUsuario(email=email)
        if usuario:
            raise ValidationError("Correo ya existe")
        return email

    def clean(self):
        password = self.cleaned_data["password"]
        confirm = self.cleaned_data["confirmarPassword"]
        if len(password) < 8 or len(password) > 50:
            raise ValidationError({"password" : f"contraseña debe tener entre 8 y 50 caracteres."})
        if password != confirm:
            raise ValidationError({"password" : "Las contraseñas no coinciden."})
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
           *self.fields,
           Submit('submit', 'Enviar', css_class='d-grid gap-2 col-2 mx-auto mt-2 text-light border botonnew')
        )
        