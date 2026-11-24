"""Crear y recuperar los filtros privados de una cuenta."""
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods, require_POST

from ..forms import BusquedaGuardadaForm
from ..models import BusquedaGuardada


@login_required
def mis_busquedas(request):
    busquedas = BusquedaGuardada.objects.filter(usuario=request.user)
    return render(request, "App_Remote_Jobs/busquedas/lista.html", {"busquedas": busquedas})


@login_required
@require_http_methods(["GET", "POST"])
def crear_busqueda(request):
    inicial = {nombre: request.GET.get(clave, "") for nombre, clave in (
        ("q", "q"), ("sector", "sector"), ("habilidad", "habilidad"),
        ("modalidad", "modalidad"), ("tipo_empleo", "tipo"), ("ubicacion", "ubicacion"),
        ("salario_desde", "salario_desde"), ("salario_hasta", "salario_hasta"),
        ("fecha_desde", "fecha_desde"), ("fecha_hasta", "fecha_hasta"), ("orden", "orden"))}
    if not inicial["orden"]:
        inicial["orden"] = "recientes"
    formulario = BusquedaGuardadaForm(request.POST or None, initial=inicial)
    if request.method == "POST" and formulario.is_valid():
        busqueda = formulario.save(commit=False)
        busqueda.usuario = request.user
        busqueda.save()
        return redirect("jobs:mis_busquedas")
    return render(request, "App_Remote_Jobs/busquedas/formulario.html", {"form": formulario})


@login_required
def abrir_busqueda(request, pk):
    busqueda = get_object_or_404(BusquedaGuardada, pk=pk, usuario=request.user)
    return redirect(busqueda.url_filtros())


@login_required
@require_POST
def borrar_busqueda(request, pk):
    busqueda = get_object_or_404(BusquedaGuardada, pk=pk, usuario=request.user)
    busqueda.delete()
    return redirect("jobs:mis_busquedas")
