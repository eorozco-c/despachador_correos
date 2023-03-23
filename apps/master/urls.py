from django.urls import path
from . import views

app_name = 'master'

urlpatterns = [
    path('', views.index, name='index'),
    path('menu/', views.menu, name='menu'),
]
