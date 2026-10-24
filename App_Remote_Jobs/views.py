from django.db.models import Count, Q
from django.shortcuts import render
from .models import Habilidad, Oferta, Sector

def inicio(request):
    ofertas = Oferta.objects.filter(publicada=True).select_related("sector").prefetch_related("habilidades").order_by("-fecha_publicacion", "titulo")
    sectores = Sector.objects.annotate(total_ofertas=Count("ofertas", filter=Q(ofertas__publicada=True), distinct=True)).filter(total_ofertas__gt=0)
    return render(request, "App_Remote_Jobs/inicio.html", {
        "ofertas_destacadas": ofertas[:3], "sectores": sectores,
        "total_ofertas": ofertas.count(), "total_sectores": Sector.objects.count(),
        "total_habilidades": Habilidad.objects.count(),
    })
