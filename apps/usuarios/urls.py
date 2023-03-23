from django.urls import path
from .formularios import UserLoginForm
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('', views.ListarUsuarios.as_view(), name="index"),
    path('registrar', views.Registrar.as_view(), name="registrar"),
    path('login',views.Login.as_view(authentication_form=UserLoginForm),name='login'),
]