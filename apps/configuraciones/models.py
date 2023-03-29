from django.db import models

# Create your models here.
class Casilla(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email
    
class TipoServicio(models.Model):
    nombre = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

class Configuracion(models.Model):
    #nombre = models.CharField(max_length=45)
    protocolo = models.CharField(max_length=10,blank=True,null=True)
    id_usuario = models.CharField(max_length=255,blank=True,null=True)
    id_tenant = models.CharField(max_length=255,blank=True,null=True)
    id_app = models.CharField(max_length=255,blank=True,null=True)
    id_key = models.CharField(max_length=255,blank=True,null=True)
    api_key = models.CharField(max_length=255,blank=True,null=True)
    casilla = models.ForeignKey(Casilla, on_delete=models.PROTECT)
    tipo_servicio = models.ForeignKey(TipoServicio, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

