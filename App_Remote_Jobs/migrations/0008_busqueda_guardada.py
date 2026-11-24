from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("app_remote_jobs", "0007_avatar_url"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]
    operations = [
        migrations.CreateModel(
            name="BusquedaGuardada",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nombre", models.CharField(max_length=80)),
                ("q", models.CharField(blank=True, max_length=120)),
                ("sector", models.CharField(blank=True, max_length=90)),
                ("habilidad", models.CharField(blank=True, max_length=90)),
                ("modalidad", models.CharField(blank=True, max_length=10)),
                ("tipo_empleo", models.CharField(blank=True, max_length=12)),
                ("ubicacion", models.CharField(blank=True, max_length=100)),
                ("salario_desde", models.PositiveIntegerField(blank=True, null=True)),
                ("salario_hasta", models.PositiveIntegerField(blank=True, null=True)),
                ("fecha_desde", models.DateField(blank=True, null=True)),
                ("fecha_hasta", models.DateField(blank=True, null=True)),
                ("orden", models.CharField(blank=True, default="recientes", max_length=20)),
                ("creada", models.DateTimeField(auto_now_add=True)),
                ("usuario", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="busquedas_guardadas", to=settings.AUTH_USER_MODEL)),
            ],
            options={"verbose_name": "búsqueda guardada", "verbose_name_plural": "búsquedas guardadas", "ordering": ["-creada", "-pk"]},
        ),
    ]
