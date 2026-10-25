import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL), ("app_remote_jobs", "0003_oferta")]
    operations = [migrations.CreateModel(name="PerfilUsuario", fields=[
        ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
        ("nombre_publico", models.CharField(blank=True, max_length=80, verbose_name="Nombre visible")),
        ("titular", models.CharField(blank=True, max_length=120, verbose_name="Titular profesional")),
        ("ubicacion", models.CharField(blank=True, max_length=100, verbose_name="Ubicación")),
        ("biografia", models.TextField(blank=True, max_length=600, verbose_name="Sobre mí")),
        ("web", models.URLField(blank=True, verbose_name="Web o portfolio")),
        ("creado", models.DateTimeField(auto_now_add=True)),
        ("actualizado", models.DateTimeField(auto_now=True)),
        ("usuario", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="perfil", to=settings.AUTH_USER_MODEL, verbose_name="Usuario")),
    ], options={"verbose_name":"perfil de usuario", "verbose_name_plural":"perfiles de usuario", "ordering":["usuario__username"]})]
