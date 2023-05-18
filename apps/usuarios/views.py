from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.contrib.auth.views import LoginView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Q

from .models import Usuario
from .formularios import FormularioRegistro, FormularioEditarRegistro, FormularioActualizarPass,FormularioNuevoUsuario, FormularioNuevoUsuarioUpdate

# Create your views here.
class Login(LoginView):
    template_name = 'registration/login.html'

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse_lazy('master:menu'))
        else:
            return super().get(*args, **kwargs)

class Registrar(CreateView):
    template_name = "formularios/generico.html"
    form_class = FormularioRegistro
    success_url = reverse_lazy("master:index")

    def form_valid(self,form):
        usuario = form.save(commit = False)
        usuario.username = usuario.email
        usuario.set_password(usuario.password)
        usuario.is_staff = True
        usuario.save()
        login(self.request, usuario)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(Registrar, self).get_context_data(**kwargs)
        context['legend'] = "Registro de Usuario"
        return context

    def get(self, request):
        if Usuario.objects.count() == 0:
            return super().get(request)
        return redirect("master:index")

class Profile(UpdateView):
    template_name = "registration/perfil.html"
    model = Usuario
    form_class = FormularioEditarRegistro

    def post(self, request, *args, **kwargs):
        if "changePassword" in request.POST:
            change_pass = FormularioActualizarPass(request.POST,instance=self.request.user)
            formRegistro = FormularioEditarRegistro(instance=self.request.user)
            if change_pass.is_valid():
                usuario = change_pass.save(commit = False)
                usuario.set_password(usuario.password)
                usuario.save()
                login(request, usuario)
                messages.success(request,'Actualizado correctamente.')
                return redirect("usuarios:perfil", pk=self.request.user.id)
            else:
                context = {
                    "form" : formRegistro,
                    "change_pass" : change_pass,
                }
                return render(request,"registration/perfil.html",context)

        elif "editProfile" in request.POST:
            change_pass = FormularioActualizarPass()
            formRegistro = FormularioEditarRegistro(request.POST,instance=self.request.user)
            if formRegistro.is_valid():
                usuario = formRegistro.save()
                messages.success(request,'Actualizado correctamente.')
                return redirect("usuarios:perfil", pk=self.request.user.id)
            else:
                context = {
                    "form" : formRegistro,
                    "change_pass" : change_pass,
                }
                return render(request,"registration/perfil.html",context)
            
    def get_context_data(self, **kwargs):
        context = super(Profile, self).get_context_data(**kwargs)
        context["change_pass"] = FormularioActualizarPass(instance=self.request.user)
        context["appname"] = "editar_perfil"
        return context

    def get(self, request, pk):
        usuario = self.get_object()
        if self.request.user != usuario:
            return redirect("master:index")
        return super().get(request)

@method_decorator(login_required, name='dispatch')
class ListarUsuarios(ListView):
    template_name = 'usuarios/usuarios_list.html'
    model = Usuario

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['appname'] = "usuarios"
        return context
    
    def get(self, *args, **kwargs):
        if self.request.user.is_superuser:
            return super().get(*args, **kwargs)
        else:
            return redirect(reverse_lazy('master:menu'))
        
    def get_queryset(self):
        return Usuario.objects.filter(Q(is_superuser = True) | Q(is_staff = True))

@method_decorator(login_required, name='dispatch')
class CrearUsuario(CreateView):
    template_name = "formularios/generico.html"
    form_class = FormularioNuevoUsuario
    success_url = reverse_lazy("usuarios:index")

    def form_valid(self,form):
        usuario = form.save(commit = False)
        usuario.username = usuario.email
        usuario.set_password(usuario.password)
        usuario.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CrearUsuario, self).get_context_data(**kwargs)
        context['legend'] = "Nuevo Usuario"
        context['appname'] = "usuarios"
        return context
    
    def get(self, request):
        if self.request.user.is_superuser:
            return super().get(request)
        return redirect("master:index")
    
@method_decorator(login_required, name='dispatch')
class EditarUsuario(UpdateView):
    template_name = "formularios/generico.html"
    model = Usuario
    form_class = FormularioNuevoUsuarioUpdate
    success_url = reverse_lazy("usuarios:index")

    def get_context_data(self, **kwargs):
        context = super(EditarUsuario, self).get_context_data(**kwargs)
        context['legend'] = "Editar Usuario"
        context['appname'] = "usuarios"
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
    return redirect("usuarios:index")

@login_required(login_url="/")
def destroy(request,pk):
    if request.method == "GET":
        if request.user.is_superuser:
            try:
                usuario = Usuario.objects.get(id=pk)
            except:
                return redirect("usuarios:index")
            usuario.is_active = False
            usuario.save()
    return redirect("usuarios:index")
