"""Inicio de la zona personal, sin duplicar las vistas de cuenta."""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from ..models import BusquedaGuardada, OfertaGuardada


@login_required
def mi_espacio(request):
    return render(request, "App_Remote_Jobs/espacio.html", {
        "total_busquedas": BusquedaGuardada.objects.filter(usuario=request.user).count(),
        "total_favoritos": OfertaGuardada.objects.filter(usuario=request.user, oferta__publicada=True).count(),
    })
