from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from apps.usuarios.models import Usuario
from apps.configuraciones.models import TipoServicio
from apps.correos.models import Estado, Ejecutivo, Correo
from datetime import datetime
from django.db.models.functions import TruncDate
import json

# Create your views here.
def index(request):
    if request.method == "GET":
        if TipoServicio.objects.count() == 0:
            TipoServicio.objects.bulk_create([
                TipoServicio(nombre="Microsoft"),
                TipoServicio(nombre="Google"),
                TipoServicio(nombre="Otro"),
            ])
        if Estado.objects.count() == 0:
            Estado.objects.bulk_create([
                Estado(nombre="En Proceso"),
                Estado(nombre="Despachado"),
            ])
        if Usuario.objects.count() == 0:
            return redirect("usuarios:registrar")
        if request.user.is_authenticated:
            return redirect("master:menu")
        else:
            return redirect("usuarios:login")
    return redirect("usuarios:login")

@login_required(login_url='/')
def menu(request):
    fecha_ini = datetime.today().strftime("%Y-%m-%d 00:00")
    fecha_fin = datetime.today().strftime("%Y-%m-%d 23:59")
    ejecutivos = Ejecutivo.objects.count()
    correos_despachados = Correo.objects.filter(created_at__range= [fecha_ini,fecha_fin]).count()
    registros_por_dia = list(Correo.objects.annotate(
                        dia=TruncDate('created_at')
                        ).values('dia').annotate(
                         cantidad=Count('id')
                        ).order_by('dia'))[-30:]
    #change dia to string
    for registro in registros_por_dia:
        registro['dia'] = registro['dia'].strftime("%Y-%m-%d")
    #convert to json
    registros_por_dia = json.dumps(registros_por_dia)
    context = {
        'appname' : "dashboard",
        'ejecutivos' : ejecutivos,
        'correos_despachados' : correos_despachados,
        'registros_por_dia' :registros_por_dia,
    }
    return render(request, "menu.html", context)