from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from .models import Habilidad, Oferta, Sector

def ofertas_publicadas():
    return Oferta.objects.filter(publicada=True).select_related("sector").prefetch_related("habilidades").order_by("-fecha_publicacion", "titulo")

def sugerencias_busqueda():
    return Oferta.objects.filter(publicada=True).order_by("-fecha_publicacion").values_list("titulo", "empresa")[:50]

def inicio(request):
    ofertas = ofertas_publicadas()
    return render(request, "App_Remote_Jobs/inicio.html", {"ofertas_destacadas": ofertas[:3], "sectores": Sector.objects.all(), "total_ofertas": ofertas.count(), "total_sectores": Sector.objects.count(), "total_habilidades": Habilidad.objects.count(), "sugerencias_busqueda": sugerencias_busqueda()})

def lista_ofertas(request):
    q = request.GET.get("q", "").strip()[:120]
    ofertas = ofertas_publicadas()
    sector = request.GET.get("sector", "").strip()
    habilidad = request.GET.get("habilidad", "").strip()
    modalidad = request.GET.get("modalidad", "").strip()
    tipo = request.GET.get("tipo", "").strip()
    if q:
        ofertas = ofertas.filter(Q(titulo__icontains=q) | Q(empresa__icontains=q) | Q(resumen__icontains=q) | Q(descripcion__icontains=q) | Q(requisitos__icontains=q) | Q(sector__nombre__icontains=q) | Q(habilidades__nombre__icontains=q)).distinct()
    if sector and Sector.objects.filter(slug=sector).exists(): ofertas = ofertas.filter(sector__slug=sector)
    else: sector = ""
    if habilidad and Habilidad.objects.filter(slug=habilidad).exists(): ofertas = ofertas.filter(habilidades__slug=habilidad)
    else: habilidad = ""
    if modalidad in Oferta.Modalidad.values: ofertas = ofertas.filter(modalidad=modalidad)
    else: modalidad = ""
    if tipo in Oferta.TipoEmpleo.values: ofertas = ofertas.filter(tipo_empleo=tipo)
    else: tipo = ""
    return render(request, "App_Remote_Jobs/ofertas/lista.html", {"ofertas": ofertas, "q": q, "sector_seleccionado": sector, "habilidad_seleccionada": habilidad, "modalidad_seleccionada": modalidad, "tipo_seleccionado": tipo, "sectores": Sector.objects.all(), "habilidades": Habilidad.objects.all(), "sugerencias_busqueda": sugerencias_busqueda()})

def detalle_oferta(request, slug):
    oferta = get_object_or_404(ofertas_publicadas(), slug=slug)
    return render(request, "App_Remote_Jobs/ofertas/detalle.html", {"oferta": oferta})
