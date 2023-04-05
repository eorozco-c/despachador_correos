from django.shortcuts import redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy

from .models import Configuracion, Casilla
from .formularios import FormularioCasilla, FormularioConfiguracion


# Create your views here.
@method_decorator(login_required, name='dispatch')
class ListarCasillas(ListView):
    template_name = "configuraciones/casillas_list.html"
    model = Casilla

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['appname'] = "casillas"
        return context
    
    def get(self, *args, **kwargs):
        if self.request.user.is_superuser:
            return super().get(*args, **kwargs)
        else:
            return redirect(reverse_lazy('master:menu'))
        
@method_decorator(login_required, name='dispatch')
class CrearCasilla(CreateView):
    template_name = "configuraciones/configuraciones.html"
    model = Casilla
    form_class = FormularioCasilla
    success_url = reverse_lazy("configuraciones:casillas")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['legend'] = "Crear Casilla"
        context['appname'] = "casillas"
        return context

    def get(self, *args, **kwargs):
        if self.request.user.is_superuser:
            return super().get(*args, **kwargs)
        else:
            return redirect(reverse_lazy('master:menu'))
        
@method_decorator(login_required, name='dispatch')
class EditarCasilla(UpdateView):
    template_name = "configuraciones/configuraciones.html"
    model = Casilla
    form_class = FormularioCasilla
    success_url = reverse_lazy("configuraciones:casillas")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['legend'] = "Editar Casilla"
        context['appname'] = "casillas"
        return context

    def get(self, *args, **kwargs):
        if self.request.user.is_superuser:
            return super().get(*args, **kwargs)
        else:
            return redirect(reverse_lazy('master:menu'))
        
@login_required(login_url="/")
def predestroy_casilla(request, pk):
    if request.method == "GET":
        try:
            casilla = Casilla.objects.get(id=pk)
        except:
            return redirect("usuarios:index")
        context={
            'id' : casilla.id,
            'email' : casilla.email,
        }
        return JsonResponse(context)
    return redirect("usuarios:index")

@login_required(login_url="/")
def destroy_casilla(request, pk):
    if request.method == "GET":
        try:
            casilla = Casilla.objects.get(id=pk)
            casilla.delete()
            messages.success(request, "Casilla eliminada correctamente",extra_tags='success')
        except:
            messages.success(request, "Error al eliminar la casilla",extra_tags='danger')
    return redirect("configuraciones:casillas")

# Crear configuracion.
@method_decorator(login_required, name='dispatch')
class CrearConfiguracion(CreateView):
    template_name = "configuraciones/configuraciones.html"
    model = Configuracion
    form_class = FormularioConfiguracion

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['legend'] = "Crear Configuración"
        context['appname'] = "Nueva Configuración"
        return context

    def get(self, *args, **kwargs):
        if Configuracion.objects.count() != 0:
            ultimo_id = Configuracion.objects.last().id 
            return redirect("configuraciones:editar_configuracion",pk = ultimo_id)
        if self.request.user.is_superuser:
            return super().get(*args, **kwargs)
        else:
            return redirect("marter:menu")
        
    def get_success_url(self):
        return reverse_lazy('configuraciones:editar_configuracion', kwargs={'pk': self.object.id})
    
# Modificar configuracion.
@method_decorator(login_required, name='dispatch')
class EditarConfiguracion(UpdateView):
    template_name = "configuraciones/configuraciones.html"
    model = Configuracion
    form_class = FormularioConfiguracion

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['legend'] = "Editar Configuración"
        context['appname'] = "configuraciones"
        return context

    def get(self, *args, **kwargs):
        if self.request.user.is_superuser:
            return super().get(*args, **kwargs)
        else:
            return redirect(reverse_lazy('master:menu'))
   
    def get_object(self):
        return Configuracion.objects.last()
    
    def get_success_url(self):
        return reverse_lazy('configuraciones:editar_configuracion', kwargs={'pk': self.object.id})