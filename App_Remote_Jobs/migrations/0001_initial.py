from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [migrations.CreateModel(name="Sector", fields=[
        ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
        ("nombre", models.CharField(max_length=80, unique=True, verbose_name="Nombre")),
        ("slug", models.SlugField(max_length=90, unique=True, help_text="Identificador legible usado en la URL.")),
        ("descripcion", models.TextField(verbose_name="Descripción")),
        ("icono", models.CharField(max_length=12, default="✳", help_text="Símbolo breve para identificar visualmente el sector.")),
        ("orden", models.PositiveSmallIntegerField(default=10, help_text="Menor número = aparece antes.")),
    ], options={"verbose_name":"sector", "verbose_name_plural":"sectores", "ordering":["orden", "nombre"]})]
