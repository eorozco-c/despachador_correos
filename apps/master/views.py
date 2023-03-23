from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from apps.usuarios.models import Usuario

# from apps.usuarios.models import Usuario

# Create your views here.

def index(request):
    if request.method == "GET":
        if Usuario.objects.count() == 0:
            return redirect("usuarios:registrar")
        if request.user.is_authenticated:
            return redirect("master:menu")
        else:
            return redirect("usuarios:login")
    return redirect("usuarios:login")

@login_required(login_url='/')
def menu(request):
    # usuarios = Usuario.objects.filter(empresa=request.user.empresa).count()
    context = {
        'appname' : "dashboard",
        # 'usuarios' : usuarios,
    }
    return render(request, "menu.html", context)
