from django.contrib import admin
from .models import Habilidad, Oferta, Sector

@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = ("icono", "nombre", "slug", "orden")
    search_fields = ("nombre", "descripcion")
    prepopulated_fields = {"slug": ("nombre",)}
    ordering = ("orden", "nombre")

@admin.register(Habilidad)
class HabilidadAdmin(admin.ModelAdmin):
    list_display = ("nombre", "categoria", "slug")
    list_filter = ("categoria",)
    search_fields = ("nombre", "descripcion")
    prepopulated_fields = {"slug": ("nombre",)}

@admin.register(Oferta)
class OfertaAdmin(admin.ModelAdmin):
    list_display = ("titulo", "empresa", "sector", "modalidad", "tipo_empleo", "fecha_publicacion", "publicada")
    list_filter = ("publicada", "modalidad", "tipo_empleo", "sector")
    search_fields = ("titulo", "empresa", "resumen", "descripcion")
    prepopulated_fields = {"slug": ("titulo",)}
    filter_horizontal = ("habilidades",)
