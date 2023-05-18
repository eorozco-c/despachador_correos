from django.db import models
from apps.usuarios.models import *
from apps.configuraciones.models import *
from .models import Usuario,  Configuracion


# Create your models here.
class Estado(models.Model):
    nombre = models.CharField(max_length=255,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
        
class Ejecutivo(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    usuario=models.ForeignKey(Usuario, on_delete=models.PROTECT)
    
def get_email(usuario): 
    return usuario.email

class Correo(models.Model):
    subject = models.CharField(max_length=255,blank=True,null=True)
    body = models.TextField(blank=True,null=True)
    desde = models.CharField(max_length=255,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ejecutivo = models.ForeignKey(Usuario, on_delete=models.PROTECT, blank=True, null=True)    
    configuracion = models.ForeignKey(Configuracion, on_delete=models.PROTECT)
    estado = models.ForeignKey(Estado, on_delete=models.PROTECT)