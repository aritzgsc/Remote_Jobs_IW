from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [("app_remote_jobs", "0001_initial")]
    operations = [migrations.CreateModel(name="Habilidad", fields=[
        ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
        ("nombre", models.CharField(max_length=80, unique=True, verbose_name="Nombre")),
        ("slug", models.SlugField(max_length=90, unique=True, help_text="Identificador legible usado en la URL.")),
        ("descripcion", models.TextField(verbose_name="Descripción")),
        ("categoria", models.CharField(max_length=60, default="Tecnología", verbose_name="Categoría")),
    ], options={"verbose_name":"habilidad", "verbose_name_plural":"habilidades", "ordering":["nombre"]})]
