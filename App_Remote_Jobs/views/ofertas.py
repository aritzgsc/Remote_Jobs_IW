"""Vistas para buscar y consultar ofertas de empleo."""

from django.db.models import F, Q
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.utils.dateparse import parse_date

from .consultas import ofertas_publicadas, sugerencias_busqueda
from ..models import Habilidad, Oferta, Sector



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
    return render(
        request,
        "App_Remote_Jobs/ofertas/detalle.html",
        {"oferta": oferta, "otras_ofertas": otras_ofertas},
    )
