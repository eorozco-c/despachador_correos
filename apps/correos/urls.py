from django.urls import path

from . import views

app_name = 'correos'

urlpatterns = [
    path('', views.ListarCorreos.as_view(), name="correos"),
    path('ejecutivos', views.ListarEjecutivos.as_view(), name="ejecutivos"),
    path('crear_ejecutivo',views.CrearEjecutivo.as_view(),name='crear_ejecutivo'),
    path('editar_ejecutivo/<int:pk>',views.EditarEjecutivo.as_view(),name='editar_ejecutivo'),
    path('predestroy/<int:pk>',views.predestroy,name='predestroy'),
    path('destroy/<int:pk>',views.destroy,name='destroy'),
    path('ejecutivos_asignados', views.asignar_agentes, name="ejecutivos_asignados"),
    path('desasignar_ejecutivo/<int:pk>', views.desasignar_ejecutivo, name="desasignar_ejecutivo"),
   
]
