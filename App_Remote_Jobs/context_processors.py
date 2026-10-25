"""Datos globales de perfil y ofertas guardadas para la navegación."""

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
    return {
        "favorite_ids": favorite_ids,
        "favorite_count": favorite_count,
        "current_profile": current_profile,
    }
