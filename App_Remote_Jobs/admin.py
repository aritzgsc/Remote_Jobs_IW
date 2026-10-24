from django.contrib import admin
from .models import Sector

@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = ("nombre", "slug", "orden")
    search_fields = ("nombre", "descripcion")
    prepopulated_fields = {"slug": ("nombre",)}
    ordering = ("orden", "nombre")
