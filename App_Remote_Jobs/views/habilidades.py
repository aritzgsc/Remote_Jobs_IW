"""Vistas del directorio de habilidades profesionales."""

from django.db.models import Count, F, Q
from django.shortcuts import get_object_or_404, render

from .consultas import ofertas_publicadas
from ..models import Habilidad, Oferta



def lista_habilidades(request):
    habilidades = Habilidad.objects.annotate(
        total_ofertas=Count("ofertas", filter=Q(ofertas__publicada=True), distinct=True)
    )
    q = request.GET.get("q", "").strip()[:100]
    categoria = request.GET.get("categoria", "").strip()
    orden = request.GET.get("orden", "nombre").strip()
    if q:
        habilidades = habilidades.filter(
            Q(nombre__icontains=q) | Q(descripcion__icontains=q) | Q(categoria__icontains=q)
        )
    categorias = list(
        Habilidad.objects.order_by("categoria").values_list("categoria", flat=True).distinct()
    )
    if categoria in categorias:
        habilidades = habilidades.filter(categoria=categoria)
    else:
        categoria = ""
    if orden == "ofertas":
        habilidades = habilidades.order_by("-total_ofertas", "nombre")
    elif orden == "categoria":
        habilidades = habilidades.order_by("categoria", "nombre")
    else:
        orden = "nombre"
        habilidades = habilidades.order_by("nombre")
    return render(
        request,
        "App_Remote_Jobs/habilidades/lista.html",
        {"habilidades": habilidades, "q": q, "categoria_seleccionada": categoria,
         "categorias": categorias, "orden": orden},
    )



def detalle_habilidad(request, slug):
    habilidad = get_object_or_404(Habilidad, slug=slug)
    ofertas = ofertas_publicadas().filter(habilidades=habilidad)
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
        "App_Remote_Jobs/habilidades/detalle.html",
        {"habilidad": habilidad, "ofertas": ofertas, "modalidad_seleccionada": modalidad,
         "tipo_seleccionado": tipo_empleo, "orden": orden},
    )
