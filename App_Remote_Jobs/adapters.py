"""Adaptación de las cuentas sociales de OAuth al perfil de Remote Jobs."""

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from .models import PerfilUsuario


class AdaptadorCuentaSocialRemoteJobs(DefaultSocialAccountAdapter):
    """Completa el perfil con los datos básicos que Google devuelve con consentimiento."""

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
