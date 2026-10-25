from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from .forms import InicioSesionForm, RegistroForm
from .models import PerfilUsuario

def iniciar_sesion(request):
    form = InicioSesionForm(request=request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        auth_login(request, form.get_user())
        return redirect("accounts:profile")
    return render(request, "App_Remote_Jobs/cuentas/acceso.html", {"form": form})

def registro(request):
    form = RegistroForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        usuario = form.save()
        PerfilUsuario.objects.get_or_create(usuario=usuario)
        auth_login(request, usuario, backend="django.contrib.auth.backends.ModelBackend")
        messages.success(request, "Tu cuenta está creada.")
        return redirect("accounts:profile")
    return render(request, "App_Remote_Jobs/cuentas/registro.html", {"form": form})

@require_POST
def cerrar_sesion(request):
    auth_logout(request)
    return redirect("jobs:inicio")

@login_required
def perfil(request):
    perfil_usuario, _ = PerfilUsuario.objects.get_or_create(usuario=request.user)
    return render(request, "App_Remote_Jobs/cuentas/perfil.html", {"perfil_usuario": perfil_usuario, "total_guardadas": 0})
