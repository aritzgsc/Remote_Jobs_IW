from django.urls import path
from . import views

app_name = "jobs"
urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("ofertas/", views.lista_ofertas, name="oferta_list"),
    path("ofertas/<slug:slug>/", views.detalle_oferta, name="oferta_detail"),
]
