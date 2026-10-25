"""Vista de la portada de Remote Jobs."""

from django.db.models import Count, Prefetch, Q
from django.shortcuts import render

from .consultas import ofertas_publicadas, sugerencias_busqueda
from ..models import Habilidad, Sector



def inicio(request):
    ofertas_destacadas = ofertas_publicadas()[:3]
    sectores = (
        Sector.objects.annotate(
            total_ofertas=Count("ofertas", filter=Q(ofertas__publicada=True), distinct=True)
        )
        .filter(total_ofertas__gt=0)
        .prefetch_related(
            Prefetch("ofertas", queryset=ofertas_publicadas(), to_attr="ofertas_publicadas")
        )
    )
    sectores_con_oferta = [
        {"sector": sector, "oferta": sector.ofertas_publicadas[0]}
        for sector in sectores
        if sector.ofertas_publicadas
    ]
    context = {
        "ofertas_destacadas": ofertas_destacadas,
        "sectores_con_oferta": sectores_con_oferta,
        "total_ofertas": ofertas_publicadas().count(),
        "total_sectores": Sector.objects.count(),
        "total_habilidades": Habilidad.objects.count(),
        "sugerencias_busqueda": sugerencias_busqueda(),
    }
    return render(request, "App_Remote_Jobs/inicio.html", context)
