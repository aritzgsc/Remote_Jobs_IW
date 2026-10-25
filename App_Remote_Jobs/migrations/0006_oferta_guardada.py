import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL), ("app_remote_jobs", "0005_avatar_perfil")]
    operations = [
        migrations.CreateModel(name="OfertaGuardada", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("guardada_en", models.DateTimeField(auto_now_add=True, verbose_name="Fecha de guardado")),
            ("oferta", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="guardados", to="app_remote_jobs.oferta", verbose_name="Oferta")),
            ("usuario", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="ofertas_guardadas", to=settings.AUTH_USER_MODEL, verbose_name="Usuario")),
        ], options={"verbose_name":"oferta guardada", "verbose_name_plural":"ofertas guardadas", "ordering":["-guardada_en"]}),
        migrations.AddConstraint(model_name="ofertaguardada", constraint=models.UniqueConstraint(fields=("usuario", "oferta"), name="unique_saved_offer_per_user")),
    ]
