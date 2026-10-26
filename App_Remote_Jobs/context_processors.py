"""Datos globales de la cuenta y del contador de ofertas guardadas."""
from django.conf import settings

from .models import PerfilUsuario, OfertaGuardada


def contexto_favoritos(request):
    favorite_ids = []
    favorite_count = 0
    current_profile = None
    if request.user.is_authenticated:
        queryset = OfertaGuardada.objects.filter(usuario=request.user, oferta__publicada=True)
        favorite_count = queryset.count()
        favorite_ids = list(queryset.values_list("oferta_id", flat=True))
        try:
            current_profile = request.user.perfil
        except PerfilUsuario.DoesNotExist:
            current_profile, _ = PerfilUsuario.objects.get_or_create(usuario=request.user)
    google_oauth_enabled = bool(
        getattr(settings, "GOOGLE_OAUTH_CLIENT_ID", "")
        and getattr(settings, "GOOGLE_OAUTH_CLIENT_SECRET", "")
    )
    return {
        "favorite_ids": favorite_ids,
        "favorite_count": favorite_count,
        "google_oauth_enabled": google_oauth_enabled,
        "current_profile": current_profile,
    }
