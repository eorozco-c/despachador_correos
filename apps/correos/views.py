from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from .models import Correo, Usuario
import datetime
from .formularios import FormularioNuevoEjecutivo, FormularioNuevoEjecutivoUpdate

# Create your views here.
@method_decorator(login_required, name='dispatch')
class ListarCorreos(ListView):
    template_name = 'correos/correos_list.html'
    model = Correo

    def get_context_data(self, **kwargs):
        context = super(ListarCorreos, self).get_context_data(**kwargs)
        context['appname'] = "correos"
        fecha_ini = self.request.GET.get('fecha_ini')
        fecha_fin = self.request.GET.get('fecha_fin')
        tipo= self.request.GET.get('tipo')
        if fecha_ini and fecha_fin:
            context['fecha_ini'] = fecha_ini
            context['fecha_fin'] = fecha_fin
        else:
            context['fecha_ini'] = datetime.datetime.now().strftime("%Y-%m-%d 00:00")
            context['fecha_fin'] = datetime.datetime.now().strftime("%Y-%m-%d 23:59")
        if tipo:
            context['tipo'] = tipo
        else:
            context['tipo'] = 0
        return context
        
    def get_queryset(self):
        fecha_ini = self.request.GET.get('fecha_ini')
        fecha_fin = self.request.GET.get('fecha_fin')
        tipo= self.request.GET.get('tipo')
        valor=self.request.GET.get('valor')
        #consultar por Ejecutivo
        if tipo == "1":
            return Correo.objects.filter(created_at__range = (fecha_ini,fecha_fin), ejecutivo__id_usuario__email__icontains = valor )
        #consultar por Remitente
        if tipo == "2":
            return Correo.objects.filter(created_at__range = (fecha_ini,fecha_fin), desde__icontains = valor )
        #consultar por Subject
        if tipo == "3":
            return Correo.objects.filter(created_at__range = (fecha_ini,fecha_fin), subject__icontains = valor )
        #consultar por Estado
        if tipo == "4":
            return Correo.objects.filter(created_at__range = (fecha_ini,fecha_fin), estado__nombre__icontains = valor )
        #solo por fecha
        else:
            return Correo.objects.filter(created_at__range = (fecha_ini,fecha_fin))
        
    def get(self, *args, **kwargs):
        if self.request.user.is_superuser:
            return super().get(*args, **kwargs)
        else:
            return redirect(reverse_lazy('master:menu'))
    
@method_decorator(login_required, name='dispatch')
class ListarEjecutivos(ListView):
    template_name = 'correos/ejecutivos_list.html'
    model = Usuario

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['appname'] = "ejecutivos"
        return context
    
    def get(self, *args, **kwargs):
        if self.request.user.is_superuser:
            return super().get(*args, **kwargs)
        else:
            return redirect(reverse_lazy('master:menu'))
    
    def get_queryset(self):
        return Usuario.objects.filter(is_superuser = False, is_staff = False)

@method_decorator(login_required, name='dispatch')
class CrearEjecutivo(CreateView):
    template_name = "correos/ejecutivos.html"
    form_class = FormularioNuevoEjecutivo
    model= Usuario
    success_url = reverse_lazy("correos:ejecutivos")

    def form_valid(self,form):
        usuario = form.save(commit = False)
        usuario.username = usuario.email
        usuario.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CrearEjecutivo, self).get_context_data(**kwargs)
        context['legend'] = "Nuevo Ejecutivo"
        context['appname'] = "ejecutivos"
        return context
    
    def get(self, request):
        if self.request.user.is_superuser:
            return super().get(request)
        return redirect("master:index")        

@method_decorator(login_required, name='dispatch')
class EditarEjecutivo(UpdateView):
    template_name = "formularios/generico.html"
    model = Usuario
    form_class = FormularioNuevoEjecutivoUpdate
    success_url = reverse_lazy("correos:ejecutivos")

    def get_context_data(self, **kwargs):
        context = super(EditarEjecutivo, self).get_context_data(**kwargs)
        context['legend'] = "Editar Ejecutivo"
        context['appname'] = "Ejecutivos"
        return context
    
    def form_valid(self,form):
        usuario = form.save(commit = False)
        usuario_instance = Usuario.objects.get(id=self.kwargs['pk'])
        if usuario.password != usuario_instance.password:
            usuario.set_password(usuario.password)
        usuario.save()
        return super().form_valid(form)

    def get(self, request,pk):
        if self.request.user.is_superuser:
            return super().get(request)
        return redirect("master:index")

@login_required(login_url="/")
def predestroy(request,pk):
    if request.method == "GET":
        try:
            usuario = Usuario.objects.get(id=pk)
        except:
            return redirect("usuarios:index")
        context={
            'id' : usuario.id,
            'nombre': usuario.first_name,
            'apellido' : usuario.last_name,
            'email' : usuario.email,
        }
        return JsonResponse(context)
    return redirect("correos:ejecutivos")

@login_required(login_url="/")
def destroy(request,pk):
    if request.method == "GET":
        if request.user.is_superuser:
            try:
                usuario = Usuario.objects.get(id=pk)
            except:
                return redirect("correos:ejecutivos")
            usuario.delete()
    return redirect("usuarios:index")    
