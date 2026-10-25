"""Vistas públicas de Remote Jobs. Toda la interacción se resuelve en el servidor."""
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, F, Prefetch, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.dateparse import parse_date
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .models import Habilidad, Oferta, Sector


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


def _entero_get(request, nombre):
    """Devuelve un entero no negativo válido de GET, o None si está vacío/no es válido."""
    valor = request.GET.get(nombre, "").strip()
    if not valor:
        return None
    if len(valor) > 9:
        return None
    try:
        numero = int(valor)
    except (TypeError, ValueError):
        return None
    return numero if numero >= 0 else None


def _fecha_get(request, nombre):
    valor = request.GET.get(nombre, "").strip()
    if not valor:
        return None
    try:
        return parse_date(valor)
    except (TypeError, ValueError):
        return None


def _query_string_sin_pagina(request):
    parametros = request.GET.copy()
    parametros.pop("page", None)
    return parametros.urlencode()


def _contexto_filtros_ofertas(request, ofertas):
    """Aplica filtros combinables y devuelve los valores para repintar el formulario."""
    q = request.GET.get("q", "").strip()[:120]
    sector_slug = request.GET.get("sector", "").strip()
    habilidad_slug = request.GET.get("habilidad", "").strip()
    modalidad = request.GET.get("modalidad", "").strip()
    tipo_empleo = request.GET.get("tipo", "").strip()
    ubicacion = request.GET.get("ubicacion", "").strip()[:100]
    salario_desde = _entero_get(request, "salario_desde")
    salario_hasta = _entero_get(request, "salario_hasta")
    fecha_desde = _fecha_get(request, "fecha_desde")
    fecha_hasta = _fecha_get(request, "fecha_hasta")
    orden = request.GET.get("orden", "recientes").strip()

    if q:
        ofertas = ofertas.filter(
            Q(titulo__icontains=q)
            | Q(empresa__icontains=q)
            | Q(resumen__icontains=q)
            | Q(descripcion__icontains=q)
            | Q(requisitos__icontains=q)
            | Q(habilidades__nombre__icontains=q)
            | Q(sector__nombre__icontains=q)
        ).distinct()
    if sector_slug and Sector.objects.filter(slug=sector_slug).exists():
        ofertas = ofertas.filter(sector__slug=sector_slug)
    else:
        sector_slug = ""
    if habilidad_slug and Habilidad.objects.filter(slug=habilidad_slug).exists():
        ofertas = ofertas.filter(habilidades__slug=habilidad_slug)
    else:
        habilidad_slug = ""
    if modalidad in Oferta.Modalidad.values:
        ofertas = ofertas.filter(modalidad=modalidad)
    else:
        modalidad = ""
    if tipo_empleo in Oferta.TipoEmpleo.values:
        ofertas = ofertas.filter(tipo_empleo=tipo_empleo)
    else:
        tipo_empleo = ""
    if ubicacion:
        ofertas = ofertas.filter(ubicacion__icontains=ubicacion)
    if salario_desde is not None:
        ofertas = ofertas.filter(
            Q(salario_max__gte=salario_desde)
            | Q(salario_max__isnull=True, salario_min__gte=salario_desde)
        )
    if salario_hasta is not None:
        ofertas = ofertas.filter(
            Q(salario_min__lte=salario_hasta)
            | Q(salario_min__isnull=True, salario_max__lte=salario_hasta)
        )
    if salario_desde is not None and salario_hasta is not None and salario_desde > salario_hasta:
        ofertas = ofertas.none()
    if fecha_desde:
        ofertas = ofertas.filter(fecha_publicacion__gte=fecha_desde)
    if fecha_hasta:
        ofertas = ofertas.filter(fecha_publicacion__lte=fecha_hasta)

    ordenes = {
        "recientes": ("-fecha_publicacion", "titulo"),
        "antiguas": ("fecha_publicacion", "titulo"),
        "titulo": ("titulo", "-fecha_publicacion"),
        "salario_desc": (F("salario_max").desc(nulls_last=True), "-fecha_publicacion"),
        "salario_asc": (F("salario_min").asc(nulls_last=True), "-fecha_publicacion"),
    }
    if orden not in ordenes:
        orden = "recientes"
    ofertas = ofertas.order_by(*ordenes[orden])

    # Las fechas o cantidades inválidas se ignoran y el formulario queda en blanco para ese campo.
    query_values = {
        "q": q,
        "sector_seleccionado": sector_slug,
        "habilidad_seleccionada": habilidad_slug,
        "modalidad_seleccionada": modalidad,
        "tipo_seleccionado": tipo_empleo,
        "ubicacion": ubicacion,
        "salario_desde": salario_desde if salario_desde is not None else "",
        "salario_hasta": salario_hasta if salario_hasta is not None else "",
        "fecha_desde": fecha_desde.isoformat() if fecha_desde else "",
        "fecha_hasta": fecha_hasta.isoformat() if fecha_hasta else "",
        "orden": orden,
    }
    filtros_activos = bool(
        q or sector_slug or habilidad_slug or modalidad or tipo_empleo or ubicacion
        or salario_desde is not None or salario_hasta is not None or fecha_desde or fecha_hasta
        or orden != "recientes"
    )
    return ofertas, query_values, filtros_activos


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


def lista_ofertas(request):
    ofertas, filtros, hay_filtros = _contexto_filtros_ofertas(request, ofertas_publicadas())
    paginator = Paginator(ofertas, 9)
    page_obj = paginator.get_page(request.GET.get("page"))
    context = {
        "page_obj": page_obj,
        "ofertas": page_obj.object_list,
        "sectores": Sector.objects.order_by("nombre"),
        "habilidades": Habilidad.objects.order_by("nombre"),
        "sugerencias_busqueda": sugerencias_busqueda(),
        "hay_filtros": hay_filtros,
        "query_string": _query_string_sin_pagina(request),
        **filtros,
    }
    return render(request, "App_Remote_Jobs/ofertas/lista.html", context)


def detalle_oferta(request, slug):
    oferta = get_object_or_404(ofertas_publicadas(), slug=slug)
    otras_ofertas = ofertas_publicadas().filter(sector=oferta.sector).exclude(pk=oferta.pk)[:3]
    return render(request, "App_Remote_Jobs/ofertas/detalle.html", {"oferta": oferta, "otras_ofertas": otras_ofertas})



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
    return render(request, "App_Remote_Jobs/sectores/lista.html", {"sectores": sectores, "q": q, "orden": orden})


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


