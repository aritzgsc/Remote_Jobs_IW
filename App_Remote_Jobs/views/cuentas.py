"""Vistas de autenticación y gestión de perfiles."""

from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from ..forms import DatosCuentaForm, InicioSesionForm, PerfilUsuarioForm, RegistroForm
from ..models import OfertaGuardada, PerfilUsuario



def iniciar_sesion(request):
    if request.user.is_authenticated:
        return redirect("accounts:profile")
    form = InicioSesionForm(request=request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        auth_login(request, form.get_user())
        return redirect("accounts:profile")
    return render(
        request,
        "App_Remote_Jobs/cuentas/acceso.html",
        {"form": form},
    )


def registro(request):
    if request.user.is_authenticated:
        return redirect("accounts:profile")
    form = RegistroForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        usuario = form.save()
        PerfilUsuario.objects.get_or_create(usuario=usuario)
        auth_login(request, usuario, backend="django.contrib.auth.backends.ModelBackend")
        messages.success(request, "Tu cuenta está creada.")
        return redirect("accounts:profile")
    return render(
        request,
        "App_Remote_Jobs/cuentas/registro.html",
        {"form": form},
    )


@require_POST
def cerrar_sesion(request):
    auth_logout(request)
    return redirect("jobs:inicio")


@login_required
def perfil(request):
    perfil_usuario, _ = PerfilUsuario.objects.get_or_create(usuario=request.user)
    total_guardadas = OfertaGuardada.objects.filter(usuario=request.user, oferta__publicada=True).count()
    return render(
        request,
        "App_Remote_Jobs/cuentas/perfil.html",
        {"perfil_usuario": perfil_usuario, "total_guardadas": total_guardadas},
    )


@login_required
def editar_perfil(request):
    perfil_usuario, _ = PerfilUsuario.objects.get_or_create(usuario=request.user)
    if request.method == "POST":
        datos_form = DatosCuentaForm(request.POST, instance=request.user)
        perfil_form = PerfilUsuarioForm(request.POST, request.FILES, instance=perfil_usuario)
        datos_validos = datos_form.is_valid()
        perfil_valido = perfil_form.is_valid()
        if datos_validos and perfil_valido:
            # Los datos de cuenta y de perfil forman una única operación lógica.
            with transaction.atomic():
                datos_form.save()
                perfil_form.save()
            messages.success(request, "Tu perfil se ha actualizado.")
            return redirect("accounts:profile")
    else:
        datos_form = DatosCuentaForm(instance=request.user)
        perfil_form = PerfilUsuarioForm(instance=perfil_usuario)
    return render(
        request,
        "App_Remote_Jobs/cuentas/editar_perfil.html",
        {"datos_form": datos_form, "perfil_form": perfil_form, "perfil_usuario": perfil_usuario},
    )
