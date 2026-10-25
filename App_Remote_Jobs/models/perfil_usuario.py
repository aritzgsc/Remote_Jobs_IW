"""Perfil público asociado a la cuenta de Django."""
from django.conf import settings
from django.db import models
from django.urls import reverse

class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="perfil", verbose_name="Usuario")
    nombre_publico = models.CharField(max_length=80, blank=True, verbose_name="Nombre visible")
    titular = models.CharField(max_length=120, blank=True, verbose_name="Titular profesional")
    ubicacion = models.CharField(max_length=100, blank=True, verbose_name="Ubicación")
    biografia = models.TextField(max_length=600, blank=True, verbose_name="Sobre mí")
    web = models.URLField(blank=True, verbose_name="Web o portfolio")
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
        if nombre: return nombre
        nombre_completo = self.usuario.get_full_name().strip()
        return nombre_completo or self.usuario.get_username()

    @property
    def iniciales(self):
        nombre = self.nombre_mostrado
        partes = [parte for parte in nombre.split() if parte]
        if len(partes) > 1: return (partes[0][0] + partes[-1][0]).upper()
        return nombre[:2].upper()

    def get_absolute_url(self):
        return reverse("accounts:profile")
