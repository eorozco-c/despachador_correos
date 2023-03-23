from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Usuario(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        for field_name in ['first_name', 'last_name']:
            val = getattr(self, field_name, False)
            if val:
                setattr(self, field_name, val.capitalize())
        super(Usuario, self).save(*args, **kwargs)