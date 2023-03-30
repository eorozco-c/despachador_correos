from django.db import models
from apps.usuarios.models import *
from apps.configuraciones.models import *


# Create your models here.
class Estado(models.Model):
    nombre = models.DateField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
        
class Ejecutivo(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    id_usuario=models.ForeignKey(Usuario, on_delete=models.PROTECT)

class Correo(models.Model):
    subject = models.CharField(max_length=255,blank=True,null=True)
    body = models.CharField(max_length=255,blank=True,null=True)
    desde = models.CharField(max_length=255,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ejecutivo = models.ForeignKey(Ejecutivo, on_delete=models.PROTECT)
    configuracion = models.ForeignKey(Configuracion, on_delete=models.PROTECT)
    estado = models.ForeignKey(Estado, on_delete=models.PROTECT)