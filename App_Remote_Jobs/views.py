from django.shortcuts import get_object_or_404, render
from .models import Habilidad, Oferta, Sector

def ofertas_publicadas():
    return Oferta.objects.filter(publicada=True).select_related("sector").prefetch_related("habilidades").order_by("-fecha_publicacion", "titulo")

def inicio(request):
    ofertas = ofertas_publicadas()
    sectores = Sector.objects.all()
    return render(request, "App_Remote_Jobs/inicio.html", {"ofertas_destacadas": ofertas[:3], "sectores": sectores, "total_ofertas": ofertas.count(), "total_sectores": Sector.objects.count(), "total_habilidades": Habilidad.objects.count()})

def lista_ofertas(request):
    ofertas = ofertas_publicadas()
    return render(request, "App_Remote_Jobs/ofertas/lista.html", {"ofertas": ofertas})

def detalle_oferta(request, slug):
    oferta = get_object_or_404(ofertas_publicadas(), slug=slug)
    return render(request, "App_Remote_Jobs/ofertas/detalle.html", {"oferta": oferta})
