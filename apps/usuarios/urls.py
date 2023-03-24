from django.urls import path
from .formularios import UserLoginForm
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('', views.ListarUsuarios.as_view(), name="index"),
    path('registrar', views.Registrar.as_view(), name="registrar"),
    path('login',views.Login.as_view(authentication_form=UserLoginForm),name='login'),
    path('perfil/<int:pk>',views.Profile.as_view(),name='perfil'),
    path('crear',views.CrearUsuario.as_view(),name='crear'),
    path('editar/<int:pk>',views.EditarUsuario.as_view(),name='editar'),
    path('predestroy/<int:pk>',views.predestroy,name='predestroy'),
    path('destroy/<int:pk>',views.destroy,name='destroy'),
]