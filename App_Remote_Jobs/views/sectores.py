"""Vistas del directorio de sectores profesionales."""

from django.db.models import Count, F, Q
from django.shortcuts import get_object_or_404, render

from .consultas import ofertas_publicadas
from ..models import Oferta, Sector



def lista_sectores(request):
    sectores = Sector.objects.annotate(
        total_ofertas=Count("ofertas", filter=Q(ofertas__publicada=True), distinct=True)
    )
    q = request.GET.get("q", "").strip()[:100]
    orden = request.GET.get("orden", "nombre").strip()
    if q:
        sectores = sectores.filter(Q(nombre__icontains=q) | Q(descripcion__icontains=q))
    if orden == "ofertas":
        sectores = sectores.order_by("-total_ofertas", "nombre")
    elif orden == "nombre_desc":
        sectores = sectores.order_by("-nombre")
    else:
        orden = "nombre"
        sectores = sectores.order_by("nombre")
    return render(
        request,
        "App_Remote_Jobs/sectores/lista.html",
        {"sectores": sectores, "q": q, "orden": orden},
    )



def detalle_sector(request, slug):
    sector = get_object_or_404(Sector, slug=slug)
    ofertas = ofertas_publicadas().filter(sector=sector)
    modalidad = request.GET.get("modalidad", "").strip()
    tipo_empleo = request.GET.get("tipo", "").strip()
    orden = request.GET.get("orden", "recientes").strip()
    if modalidad in Oferta.Modalidad.values:
        ofertas = ofertas.filter(modalidad=modalidad)
    else:
        modalidad = ""
    if tipo_empleo in Oferta.TipoEmpleo.values:
        ofertas = ofertas.filter(tipo_empleo=tipo_empleo)
    else:
        tipo_empleo = ""
    if orden == "titulo":
        ofertas = ofertas.order_by("titulo")
    elif orden == "salario":
        ofertas = ofertas.order_by(F("salario_max").desc(nulls_last=True), "titulo")
    else:
        orden = "recientes"
        ofertas = ofertas.order_by("-fecha_publicacion", "titulo")
    return render(
        request,
        "App_Remote_Jobs/sectores/detalle.html",
        {"sector": sector, "ofertas": ofertas, "modalidad_seleccionada": modalidad,
         "tipo_seleccionado": tipo_empleo, "orden": orden},
    )
