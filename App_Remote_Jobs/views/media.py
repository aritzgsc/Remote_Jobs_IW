"""Servicio de avatares locales para la demostración en Render."""

from pathlib import PurePosixPath

from django.core.files.storage import default_storage
from django.http import FileResponse, Http404
from django.views.decorators.http import require_safe


@require_safe
def servir_avatar(request, ruta):
    tipos = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp"}
    tipo = tipos.get(PurePosixPath(ruta).suffix.lower())
    if not tipo:
        raise Http404
    try:
        archivo = default_storage.open(ruta, "rb")
    except (FileNotFoundError, IsADirectoryError):
        raise Http404 from None
    respuesta = FileResponse(archivo, content_type=tipo)
    respuesta["X-Content-Type-Options"] = "nosniff"
    respuesta["Content-Security-Policy"] = "default-src 'none'; sandbox"
    respuesta["Cache-Control"] = "no-store"
    return respuesta
