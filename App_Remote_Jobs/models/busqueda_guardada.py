"""Filtros de búsqueda conservados por cada cuenta."""
from django.conf import settings
from django.db import models
from django.urls import reverse
from urllib.parse import urlencode


class BusquedaGuardada(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="busquedas_guardadas")
    nombre = models.CharField(max_length=80)
    q = models.CharField(max_length=120, blank=True)
    sector = models.CharField(max_length=90, blank=True)
    habilidad = models.CharField(max_length=90, blank=True)
    modalidad = models.CharField(max_length=10, blank=True)
    tipo_empleo = models.CharField(max_length=12, blank=True)
    ubicacion = models.CharField(max_length=100, blank=True)
    salario_desde = models.PositiveIntegerField(null=True, blank=True)
    salario_hasta = models.PositiveIntegerField(null=True, blank=True)
    fecha_desde = models.DateField(null=True, blank=True)
    fecha_hasta = models.DateField(null=True, blank=True)
    orden = models.CharField(max_length=20, blank=True, default="recientes")
    creada = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-creada", "-pk"]
        verbose_name = "búsqueda guardada"
        verbose_name_plural = "búsquedas guardadas"

    def __str__(self):
        return self.nombre

    def url_filtros(self):
        filtros = {"q": self.q, "sector": self.sector, "habilidad": self.habilidad,
                   "modalidad": self.modalidad, "tipo": self.tipo_empleo, "ubicacion": self.ubicacion,
                   "salario_desde": self.salario_desde, "salario_hasta": self.salario_hasta,
                   "fecha_desde": self.fecha_desde.isoformat() if self.fecha_desde else "",
                   "fecha_hasta": self.fecha_hasta.isoformat() if self.fecha_hasta else "", "orden": self.orden}
        return reverse("jobs:oferta_list") + "?" + urlencode({k: v for k, v in filtros.items() if v not in (None, "")})
