"""Modelo principal de las ofertas de empleo y prácticas."""

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse

from .habilidad import Habilidad
from .sector import Sector


class Oferta(models.Model):
    """Oferta de primer empleo o prácticas, publicada en remoto o híbrido."""

    class Modalidad(models.TextChoices):
        REMOTO = "remoto", "Remoto"
        HIBRIDO = "hibrido", "Híbrido"

    class TipoEmpleo(models.TextChoices):
        JUNIOR = "junior", "Primer empleo · Junior"
        PRACTICAS = "practicas", "Prácticas"

    titulo = models.CharField(max_length=140, verbose_name="Título de la oferta")
    slug = models.SlugField(max_length=160, unique=True, help_text="Identificador legible usado en la URL.")
    empresa = models.CharField(max_length=100)
    resumen = models.CharField(max_length=240, help_text="Frase breve visible en los listados.")
    descripcion = models.TextField(help_text="Descripción completa del puesto.")
    requisitos = models.TextField(help_text="Un requisito por línea.")
    beneficios = models.TextField(blank=True, help_text="Un beneficio por línea (opcional).")
    sector = models.ForeignKey(Sector, on_delete=models.PROTECT, related_name="ofertas")
    habilidades = models.ManyToManyField(Habilidad, related_name="ofertas", blank=True)
    modalidad = models.CharField(max_length=10, choices=Modalidad.choices, default=Modalidad.REMOTO)
    tipo_empleo = models.CharField(max_length=12, choices=TipoEmpleo.choices, default=TipoEmpleo.JUNIOR)
    ubicacion = models.CharField(max_length=100, default="España")
    salario_min = models.PositiveIntegerField(
        null=True, blank=True, validators=[MinValueValidator(0)], verbose_name="Salario mínimo anual (€)"
    )
    salario_max = models.PositiveIntegerField(
        null=True, blank=True, validators=[MinValueValidator(0)], verbose_name="Salario máximo anual (€)"
    )
    url_solicitud = models.URLField(blank=True, verbose_name="URL externa para solicitar")
    fecha_publicacion = models.DateField(verbose_name="Fecha de publicación")
    publicada = models.BooleanField(default=True, help_text="Desmarca para ocultar la oferta en la web pública.")
    creada = models.DateTimeField(auto_now_add=True)
    actualizada = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-fecha_publicacion", "titulo"]
        verbose_name = "oferta"
        verbose_name_plural = "ofertas"

    def __str__(self):
        return f"{self.titulo} · {self.empresa}"

    def clean(self):
        super().clean()
        if self.salario_min is not None and self.salario_max is not None and self.salario_max < self.salario_min:
            raise ValidationError({"salario_max": "El salario máximo no puede ser inferior al mínimo."})

    def get_absolute_url(self):
        return reverse("jobs:oferta_detail", kwargs={"slug": self.slug})

    @property
    def iniciales_empresa(self):
        partes = [parte for parte in self.empresa.replace("&", " ").split() if parte]
        return "".join(parte[0] for parte in partes[:2]).upper()

    @property
    def etiqueta_salario(self):
        if self.salario_min is not None and self.salario_max is not None:
            return f"{self.salario_min:,}–{self.salario_max:,} € / año".replace(",", ".")
        if self.salario_min is not None:
            return f"Desde {self.salario_min:,} € / año".replace(",", ".")
        if self.salario_max is not None:
            return f"Hasta {self.salario_max:,} € / año".replace(",", ".")
        return "Salario a convenir"

    @property
    def lista_requisitos(self):
        return [linea.strip() for linea in self.requisitos.splitlines() if linea.strip()]

    @property
    def lista_beneficios(self):
        return [linea.strip() for linea in self.beneficios.splitlines() if linea.strip()]
