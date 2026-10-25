"""Vistas para gestionar ofertas guardadas por usuario."""

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .consultas import ofertas_publicadas
from ..models import OfertaGuardada



@login_required
def favoritos(request):
    ofertas = (
        ofertas_publicadas()
        .filter(guardados__usuario=request.user)
        .order_by("-guardados__guardada_en", "titulo")
        .distinct()
    )
    return render(
        request,
        "App_Remote_Jobs/favoritos.html",
        {"ofertas": ofertas, "total_guardadas": ofertas.count()},
    )



@login_required
@require_POST
def alternar_favorito(request, pk):
    oferta = get_object_or_404(ofertas_publicadas(), pk=pk)
    guardada = OfertaGuardada.objects.filter(usuario=request.user, oferta=oferta).first()
    if guardada:
        guardada.delete()
    else:
        OfertaGuardada.objects.get_or_create(usuario=request.user, oferta=oferta)

    destino = request.POST.get("next", "")
    if not destino or not destino.startswith("/") or not url_has_allowed_host_and_scheme(
        destino, allowed_hosts={request.get_host()}, require_https=request.is_secure()
    ):
        destino = reverse("jobs:favoritos")
    return redirect(destino)
