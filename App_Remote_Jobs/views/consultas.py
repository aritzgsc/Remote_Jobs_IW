"""Consultas compartidas por las vistas públicas."""


from ..models import Oferta



def ofertas_publicadas():
    return (
        Oferta.objects.filter(publicada=True)
        .select_related("sector")
        .prefetch_related("habilidades")
        .order_by("-fecha_publicacion", "titulo")
    )



def sugerencias_busqueda():
    """Sugerencias HTML nativas; no necesitan JavaScript ni peticiones AJAX."""
    return (
        Oferta.objects.filter(publicada=True)
        .order_by("-fecha_publicacion", "titulo")
        .values_list("titulo", "empresa")[:50]
    )
