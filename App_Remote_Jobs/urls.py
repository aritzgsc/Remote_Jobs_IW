from django.urls import path
from . import views

app_name = "jobs"
urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("ofertas/", views.lista_ofertas, name="oferta_list"),
    path("ofertas/<slug:slug>/", views.detalle_oferta, name="oferta_detail"),
    path("sectores/", views.lista_sectores, name="sector_list"),
    path("sectores/<slug:slug>/", views.detalle_sector, name="sector_detail"),
    path("habilidades/", views.lista_habilidades, name="habilidad_list"),
    path("habilidades/<slug:slug>/", views.detalle_habilidad, name="habilidad_detail"),
]
