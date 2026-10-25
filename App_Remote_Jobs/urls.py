"""Rutas públicas y de cuenta de Remote Jobs."""

from django.urls import include, path

from .views.publicas import inicio
from .views.ofertas import detalle_oferta, lista_ofertas
from .views.sectores import detalle_sector, lista_sectores
from .views.habilidades import detalle_habilidad, lista_habilidades
from .views.favoritos import alternar_favorito, favoritos
from .views.cuentas import iniciar_sesion, registro, cerrar_sesion, perfil, editar_perfil


rutas_cuentas = [
    path("cuenta/entrar/", iniciar_sesion, name="login"),
    path("cuenta/registro/", registro, name="register"),
    path("cuenta/salir/", cerrar_sesion, name="logout"),
    path("perfil/", perfil, name="profile"),
    path("perfil/editar/", editar_perfil, name="profile_edit"),
]

rutas_ofertas = [
    path("", inicio, name="inicio"),
    path("ofertas/", lista_ofertas, name="oferta_list"),
    path("ofertas/<slug:slug>/", detalle_oferta, name="oferta_detail"),
    path("sectores/", lista_sectores, name="sector_list"),
    path("sectores/<slug:slug>/", detalle_sector, name="sector_detail"),
    path("habilidades/", lista_habilidades, name="habilidad_list"),
    path("habilidades/<slug:slug>/", detalle_habilidad, name="habilidad_detail"),
    path("favoritos/", favoritos, name="favoritos"),
    path("favoritos/<int:pk>/alternar/", alternar_favorito, name="alternar_favorito"),
]

urlpatterns = [
    path("", include((rutas_cuentas, "accounts"), namespace="accounts")),
    path("", include((rutas_ofertas, "jobs"), namespace="jobs")),
]
