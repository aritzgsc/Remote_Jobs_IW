"""Perfil público asociado a la cuenta de Django."""

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse


def validar_tamano_avatar(archivo):
    """Rechaza imágenes de perfil superiores a 3 MiB."""
    if archivo.size > 3 * 1024 * 1024:
        raise ValidationError("La imagen no puede superar los 3 MB.")


class PerfilUsuario(models.Model):
    """Información pública opcional asociada a una cuenta de Django."""

    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="perfil",
        verbose_name="Usuario",
    )
    nombre_publico = models.CharField(max_length=80, blank=True, verbose_name="Nombre visible")
    titular = models.CharField(max_length=120, blank=True, verbose_name="Titular profesional")
    ubicacion = models.CharField(max_length=100, blank=True, verbose_name="Ubicación")
    biografia = models.TextField(max_length=600, blank=True, verbose_name="Sobre mí")
    web = models.URLField(blank=True, verbose_name="Web o portfolio")
    avatar = models.ImageField(
        upload_to="avatares/%Y/%m/",
        blank=True,
        validators=[FileExtensionValidator(["jpg", "jpeg", "png", "webp"]), validar_tamano_avatar],
        verbose_name="Foto de perfil",
        help_text="JPG, PNG o WebP. Máximo 3 MB.",
    )
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "perfil de usuario"
        verbose_name_plural = "perfiles de usuario"
        ordering = ["usuario__username"]

    def __str__(self):
        return f"Perfil de {self.usuario.get_username()}"

    @property
    def nombre_mostrado(self):
        nombre = self.nombre_publico.strip()
        if nombre:
            return nombre
        nombre_completo = self.usuario.get_full_name().strip()
        return nombre_completo or self.usuario.get_username()

    @property
    def iniciales(self):
        nombre = self.nombre_mostrado
        partes = [parte for parte in nombre.split() if parte]
        if len(partes) > 1:
            return (partes[0][0] + partes[-1][0]).upper()
        return nombre[:2].upper()

    def get_absolute_url(self):
        return reverse("accounts:profile")
