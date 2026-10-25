from django.contrib import admin

from .models import Habilidad, Oferta, Sector, PerfilUsuario, OfertaGuardada


@admin.register(Sector)
class SectorAdmin(admin.ModelAdmin):
    list_display = ("icono", "nombre", "slug", "numero_ofertas")
    search_fields = ("nombre", "descripcion")
    prepopulated_fields = {"slug": ("nombre",)}
    ordering = ("orden", "nombre")

    @admin.display(description="Ofertas publicadas")
    def numero_ofertas(self, obj):
        return obj.ofertas.filter(publicada=True).count()


@admin.register(Habilidad)
class HabilidadAdmin(admin.ModelAdmin):
    list_display = ("nombre", "categoria", "slug", "numero_ofertas")
    list_filter = ("categoria",)
    search_fields = ("nombre", "descripcion")
    prepopulated_fields = {"slug": ("nombre",)}

    @admin.display(description="Ofertas publicadas")
    def numero_ofertas(self, obj):
        return obj.ofertas.filter(publicada=True).count()


@admin.register(Oferta)
class OfertaAdmin(admin.ModelAdmin):
    list_display = ("titulo", "empresa", "sector", "modalidad", "tipo_empleo", "fecha_publicacion", "estado")
    list_filter = ("publicada", "modalidad", "tipo_empleo", "sector", "fecha_publicacion")
    search_fields = ("titulo", "empresa", "resumen", "descripcion", "habilidades__nombre")
    prepopulated_fields = {"slug": ("titulo",)}
    filter_horizontal = ("habilidades",)
    date_hierarchy = "fecha_publicacion"
    list_select_related = ("sector",)
    readonly_fields = ("creada", "actualizada")
    fieldsets = (
        ("Información principal", {"fields": ("titulo", "slug", "empresa", "resumen", "sector", "habilidades")}),
        ("Descripción del puesto", {"fields": ("descripcion", "requisitos", "beneficios")}),
        ("Condiciones", {"fields": ("modalidad", "tipo_empleo", "ubicacion", ("salario_min", "salario_max"), "url_solicitud")}),
        ("Publicación", {"fields": ("fecha_publicacion", "publicada", ("creada", "actualizada"))}),
    )

    @admin.display(description="Estado", boolean=True)
    def estado(self, obj):
        return obj.publicada


admin.site.site_header = "Remote Jobs · Administración"
admin.site.site_title = "Remote Jobs Admin"
admin.site.index_title = "Gestión del portal de empleo"


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ("usuario", "nombre_publico", "ubicacion", "actualizado")
    search_fields = ("usuario__username", "usuario__email", "nombre_publico", "titular")
    list_select_related = ("usuario",)
    readonly_fields = ("creado", "actualizado")


@admin.register(OfertaGuardada)
class OfertaGuardadaAdmin(admin.ModelAdmin):
    list_display = ("usuario", "oferta", "guardada_en")
    search_fields = ("usuario__username", "usuario__email", "oferta__titulo", "oferta__empresa")
    list_filter = ("guardada_en", "oferta__modalidad", "oferta__tipo_empleo")
    list_select_related = ("usuario", "oferta")
    readonly_fields = ("guardada_en",)
