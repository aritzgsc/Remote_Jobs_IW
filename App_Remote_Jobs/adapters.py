"""Adaptación de las cuentas sociales de OAuth al perfil de Remote Jobs."""

from allauth.core.exceptions import ImmediateHttpResponse
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import redirect

from .models import PerfilUsuario


class AdaptadorCuentaSocialRemoteJobs(DefaultSocialAccountAdapter):
    """Completa el perfil con los datos básicos que Google devuelve con consentimiento."""

    def pre_social_login(self, request, sociallogin):
        super().pre_social_login(request, sociallogin)
        if sociallogin.account.provider != "google":
            return

        proceso = sociallogin.state.get("process")
        if proceso == "connect":
            if not request.user.is_authenticated:
                raise ImmediateHttpResponse(redirect("accounts:login"))

            correo = (request.user.email or "").strip().casefold()
            coincide = bool(correo) and any(
                direccion.verified and direccion.email.strip().casefold() == correo
                for direccion in sociallogin.email_addresses
            )
            if not coincide:
                messages.error(
                    request,
                    "Solo puedes vincular una cuenta de Google con el mismo correo "
                    "electrónico verificado que tienes en Remote Jobs.",
                )
                raise ImmediateHttpResponse(redirect("accounts:profile"))
            return

        if sociallogin.is_existing or proceso == "redirect":
            return

        # Un correo coincidente no autoriza a entrar en una cuenta local.
        for address in sociallogin.email_addresses:
            if get_user_model().objects.filter(email__iexact=address.email).exists():
                messages.info(
                    request,
                    "Ya existe una cuenta con ese correo. Entra con tu contraseña "
                    "y vincula Google desde tu perfil.",
                )
                raise ImmediateHttpResponse(redirect("accounts:login"))

    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form=form)
        provider_data = sociallogin.account.extra_data or {}
        profile, _ = PerfilUsuario.objects.get_or_create(usuario=user)
        update_fields = []

        if not profile.nombre_publico:
            display_name = (
                provider_data.get("name")
                or " ".join(
                    part for part in (
                        provider_data.get("given_name"),
                        provider_data.get("family_name"),
                    ) if part
                )
                or user.get_full_name()
            )
            if display_name:
                profile.nombre_publico = display_name[:80]
                update_fields.append("nombre_publico")

        picture_url = provider_data.get("picture")
        if picture_url and not profile.avatar and not profile.avatar_url:
            # URL proporcionada por Google; no se descarga ni se guarda contenido externo.
            profile.avatar_url = picture_url
            update_fields.append("avatar_url")

        if update_fields:
            update_fields.append("actualizado")
            profile.save(update_fields=update_fields)
        return user
