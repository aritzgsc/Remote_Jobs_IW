from django.contrib import admin
from .models import Habilidad, Sector

@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = ("nombre", "slug", "orden")
    search_fields = ("nombre", "descripcion")
    prepopulated_fields = {"slug": ("nombre",)}
    ordering = ("orden", "nombre")

@admin.register(Habilidad)
class HabilidadAdmin(admin.ModelAdmin):
    list_display = ("nombre", "categoria", "slug")
    list_filter = ("categoria",)
    search_fields = ("nombre", "descripcion")
    prepopulated_fields = {"slug": ("nombre",)}
