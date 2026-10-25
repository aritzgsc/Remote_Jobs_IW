import django.core.validators
from django.db import migrations, models
import App_Remote_Jobs.models

class Migration(migrations.Migration):
    dependencies = [("app_remote_jobs", "0004_perfil_usuario")]
    operations = [
        migrations.AddField(model_name="perfilusuario", name="avatar", field=models.ImageField(blank=True, upload_to="avatares/%Y/%m/", validators=[django.core.validators.FileExtensionValidator(["jpg", "jpeg", "png", "webp"]), App_Remote_Jobs.models.validar_tamano_avatar], verbose_name="Foto de perfil", help_text="JPG, PNG o WebP. Máximo 3 MB.")),
    ]
