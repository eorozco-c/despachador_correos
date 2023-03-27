from django.urls import path

from . import views

app_name = 'configuraciones'

urlpatterns = [
    path('casillas/', views.ListarCasillas.as_view(), name='casillas'),
    path('casillas/crear/', views.CrearCasilla.as_view(), name='crear_casilla'),
    path('casillas/editar/<int:pk>/', views.EditarCasilla.as_view(), name='editar_casilla'),
    path('casillas/predestroy/<int:pk>/', views.predestroy_casilla, name='predestroy_casilla'),
    path('casillas/destroy/<int:pk>/', views.destroy_casilla, name='destroy_casilla'),
]