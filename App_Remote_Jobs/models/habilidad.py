"""Modelo para tecnologías y competencias profesionales."""

from django.db import models
from django.urls import reverse


class Habilidad(models.Model):
    """Tecnología, herramienta o competencia requerida en las ofertas."""

    nombre = models.CharField(max_length=80, unique=True, verbose_name="Nombre")
    slug = models.SlugField(max_length=90, unique=True, help_text="Identificador legible usado en la URL.")
    descripcion = models.TextField(verbose_name="Descripción")
    categoria = models.CharField(max_length=60, default="Tecnología", verbose_name="Categoría")

    class Meta:
        ordering = ["nombre"]
        verbose_name = "habilidad"
        verbose_name_plural = "habilidades"

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse("jobs:habilidad_detail", kwargs={"slug": self.slug})
