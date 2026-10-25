"""Relación entre una cuenta y sus ofertas guardadas."""

from django.conf import settings
from django.db import models


class OfertaGuardada(models.Model):
    """Oferta guardada por una cuenta concreta, persistente entre sesiones."""

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ofertas_guardadas",
        verbose_name="Usuario",
    )
    oferta = models.ForeignKey(
        "Oferta",
        on_delete=models.CASCADE,
        related_name="guardados",
        verbose_name="Oferta",
    )
    guardada_en = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de guardado")

    class Meta:
        ordering = ["-guardada_en"]
        verbose_name = "oferta guardada"
        verbose_name_plural = "ofertas guardadas"
        constraints = [
            models.UniqueConstraint(fields=["usuario", "oferta"], name="unique_saved_offer_per_user")
        ]

    def __str__(self):
        return f"{self.usuario.get_username()} · {self.oferta.titulo}"
