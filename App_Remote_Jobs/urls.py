from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeDoneView
from django.urls import include, path

from . import views, vistas_cuentas

rutas_cuentas = [
    path("cuenta/entrar/", vistas_cuentas.iniciar_sesion, name="login"),
    path("cuenta/registro/", vistas_cuentas.registro, name="register"),
    path("cuenta/salir/", vistas_cuentas.cerrar_sesion, name="logout"),
    path("perfil/", vistas_cuentas.perfil, name="profile"),
]

rutas_ofertas = [
    path("", views.inicio, name="inicio"),
    path("ofertas/", views.lista_ofertas, name="oferta_list"),
    path("ofertas/<slug:slug>/", views.detalle_oferta, name="oferta_detail"),
    path("sectores/", views.lista_sectores, name="sector_list"),
    path("sectores/<slug:slug>/", views.detalle_sector, name="sector_detail"),
    path("habilidades/", views.lista_habilidades, name="habilidad_list"),
    path("habilidades/<slug:slug>/", views.detalle_habilidad, name="habilidad_detail"),
]

urlpatterns = [
    path("", include((rutas_cuentas, "accounts"), namespace="accounts")),
    path("", include((rutas_ofertas, "jobs"), namespace="jobs")),
]
