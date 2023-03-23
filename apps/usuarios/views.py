from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.contrib.auth.views import LoginView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth import login

from .models import Usuario
from .formularios import FormularioRegistro

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


