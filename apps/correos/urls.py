from django.urls import path

from . import views

app_name = 'correos'

urlpatterns = [
    path('', views.ListarCorreos.as_view(), name="correos"),
]
