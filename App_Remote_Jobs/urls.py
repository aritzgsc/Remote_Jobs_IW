"""Rutas públicas y de cuenta de Remote Jobs."""

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeDoneView
from django.urls import include, path

from .views.publicas import inicio
from .views.ofertas import detalle_oferta, lista_ofertas
from .views.sectores import detalle_sector, lista_sectores
from .views.habilidades import detalle_habilidad, lista_habilidades
from .views.favoritos import alternar_favorito, favoritos
from .views.cuentas import (
    iniciar_sesion,
    registro,
    cerrar_sesion,
    perfil,
    editar_perfil,
    google_oauth_setup_required,
    CambioContrasenaView,
    RecuperarContrasenaView,
    RecuperarContrasenaEnviadoView,
    NuevaContrasenaView,
    ContrasenaRestablecidaView,
)


rutas_cuentas = [
    path("cuenta/entrar/", iniciar_sesion, name="login"),
    path("cuenta/registro/", registro, name="register"),
    path("cuenta/salir/", cerrar_sesion, name="logout"),
    path("perfil/", perfil, name="profile"),
    path("perfil/editar/", editar_perfil, name="profile_edit"),
    path("cuenta/contrasena/cambiar/", CambioContrasenaView.as_view(), name="password_change"),
    path(
        "cuenta/contrasena/cambiada/",
        login_required(
            PasswordChangeDoneView.as_view(
                template_name="App_Remote_Jobs/cuentas/contrasena_cambiada.html"
            )
        ),
        name="password_change_done",
    ),
    path("cuenta/contrasena/recuperar/", RecuperarContrasenaView.as_view(), name="password_reset"),
    path("cuenta/contrasena/recuperar/enviado/", RecuperarContrasenaEnviadoView.as_view(), name="password_reset_done"),
    path("cuenta/contrasena/nueva/<str:uidb64>/<str:token>/", NuevaContrasenaView.as_view(), name="password_reset_confirm"),
    path("cuenta/contrasena/restablecida/", ContrasenaRestablecidaView.as_view(), name="password_reset_complete"),
    path("cuenta/entrar/google/configuracion/", google_oauth_setup_required, name="google_oauth_setup"),
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
