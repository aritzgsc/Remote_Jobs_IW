from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app_remote_jobs", "0006_oferta_guardada"),
    ]

    operations = [
        migrations.AddField(
            model_name="perfilusuario",
            name="avatar_url",
            field=models.URLField(
                blank=True,
                max_length=500,
                help_text="Se rellena automáticamente al crear el perfil con Google; una foto subida manualmente tiene prioridad.",
                verbose_name="URL de la foto del proveedor",
            ),
        ),
    ]
