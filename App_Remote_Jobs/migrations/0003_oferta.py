import django.core.validators
import django.db.models.deletion
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [("app_remote_jobs", "0002_habilidad")]
    operations = [migrations.CreateModel(name="Oferta", fields=[
        ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
        ("titulo", models.CharField(max_length=140, verbose_name="Título de la oferta")),
        ("slug", models.SlugField(max_length=160, unique=True, help_text="Identificador legible usado en la URL.")),
        ("empresa", models.CharField(max_length=100)),
        ("resumen", models.CharField(max_length=240, help_text="Frase breve visible en los listados.")),
        ("descripcion", models.TextField(help_text="Descripción completa del puesto.")),
        ("requisitos", models.TextField(help_text="Un requisito por línea.")),
        ("beneficios", models.TextField(blank=True, help_text="Un beneficio por línea (opcional).")),
        ("modalidad", models.CharField(max_length=10, choices=[("remoto", "Remoto"), ("hibrido", "Híbrido")], default="remoto")),
        ("tipo_empleo", models.CharField(max_length=12, choices=[("junior", "Primer empleo · Junior"), ("practicas", "Prácticas")], default="junior")),
        ("ubicacion", models.CharField(max_length=100, default="España")),
        ("salario_min", models.PositiveIntegerField(null=True, blank=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name="Salario mínimo anual (€)")),
        ("salario_max", models.PositiveIntegerField(null=True, blank=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name="Salario máximo anual (€)")),
        ("url_solicitud", models.URLField(blank=True, verbose_name="URL externa para solicitar")),
        ("fecha_publicacion", models.DateField(verbose_name="Fecha de publicación")),
        ("publicada", models.BooleanField(default=True, help_text="Desmarca para ocultar la oferta en la web pública.")),
        ("creada", models.DateTimeField(auto_now_add=True)),
        ("actualizada", models.DateTimeField(auto_now=True)),
        ("sector", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="ofertas", to="app_remote_jobs.sector")),
        ("habilidades", models.ManyToManyField(blank=True, related_name="ofertas", to="app_remote_jobs.habilidad")),
    ], options={"verbose_name":"oferta", "verbose_name_plural":"ofertas", "ordering":["-fecha_publicacion", "titulo"]})]
