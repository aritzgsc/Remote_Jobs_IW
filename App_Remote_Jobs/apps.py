from django.apps import AppConfig

class AppRemoteJobsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "App_Remote_Jobs"
    label = "app_remote_jobs"
    verbose_name = "Remote Jobs"

    def ready(self):
        from . import signals  # noqa: F401
