"""Vistas de autenticación y gestión de perfiles."""

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.db import transaction
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from ..forms import (
    CambioContrasenaForm,
    DatosCuentaForm,
    InicioSesionForm,
    PerfilUsuarioForm,
    RegistroForm,
)
from ..models import OfertaGuardada, PerfilUsuario



def _destino_seguro(request, destino, fallback):
    if destino and url_has_allowed_host_and_scheme(
        destino,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return destino
    return fallback


@require_POST
def google_oauth_setup_required(request):
    """Explica cómo activar Google OAuth cuando aún no hay credenciales."""
    if settings.GOOGLE_OAUTH_CLIENT_ID and settings.GOOGLE_OAUTH_CLIENT_SECRET:
        # Con credenciales configuradas, el botón de la plantilla envía el POST
        # directamente a django-allauth. Este camino solo es el fallback visual.
        return redirect("accounts:login")
    return render(request, "App_Remote_Jobs/cuentas/configurar_google.html")


def iniciar_sesion(request):
    if request.user.is_authenticated:
        return redirect("accounts:profile")
    destino = request.POST.get("next", request.GET.get("next", ""))
    form = InicioSesionForm(request=request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        auth_login(request, form.get_user())
        messages.success(request, f"¡Qué bien verte, {request.user.get_username()}!")
        return redirect(_destino_seguro(request, destino, reverse("accounts:profile")))
    return render(
        request,
        "App_Remote_Jobs/cuentas/acceso.html",
        {"form": form, "next": destino},
    )


def registro(request):
    if request.user.is_authenticated:
        return redirect("accounts:profile")
    form = RegistroForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        PerfilUsuario.objects.get_or_create(usuario=user)
        auth_login(
            request,
            user,
            backend="App_Remote_Jobs.backends.AutenticacionCorreoONombreUsuario",
        )
        messages.success(request, "Tu cuenta está creada. Completa tu perfil cuando quieras.")
        return redirect("accounts:profile")
    return render(
        request,
        "App_Remote_Jobs/cuentas/registro.html",
        {"form": form},
    )


@require_POST
def cerrar_sesion(request):
    auth_logout(request)
    messages.info(request, "Has cerrado sesión correctamente.")
    return redirect("jobs:inicio")


@login_required
def perfil(request):
    perfil_usuario, _ = PerfilUsuario.objects.get_or_create(usuario=request.user)
    guardadas = OfertaGuardada.objects.filter(usuario=request.user, oferta__publicada=True).count()
    return render(
        request,
        "App_Remote_Jobs/cuentas/perfil.html",
        {"perfil_usuario": perfil_usuario, "total_guardadas": guardadas},
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
            # Los cambios de cuenta y perfil forman una sola operación lógica.
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


class CambioContrasenaView(PasswordChangeView):
    form_class = CambioContrasenaForm
    template_name = "App_Remote_Jobs/cuentas/cambiar_contrasena.html"
    success_url = reverse_lazy("accounts:password_change_done")

    def form_valid(self, form):
        messages.success(self.request, "La contraseña se ha cambiado correctamente.")
        return super().form_valid(form)


class RecuperarContrasenaView(PasswordResetView):
    template_name = "App_Remote_Jobs/cuentas/recuperar_contrasena.html"
    email_template_name = "App_Remote_Jobs/cuentas/recuperacion_contrasena_email.txt"
    subject_template_name = "App_Remote_Jobs/cuentas/recuperacion_contrasena_asunto.txt"
    success_url = reverse_lazy("accounts:password_reset_done")


class RecuperarContrasenaEnviadoView(PasswordResetDoneView):
    template_name = "App_Remote_Jobs/cuentas/recuperacion_enviada.html"


class NuevaContrasenaView(PasswordResetConfirmView):
    template_name = "App_Remote_Jobs/cuentas/nueva_contrasena.html"
    success_url = reverse_lazy("accounts:password_reset_complete")


class ContrasenaRestablecidaView(PasswordResetCompleteView):
    template_name = "App_Remote_Jobs/cuentas/contrasena_restablecida.html"
