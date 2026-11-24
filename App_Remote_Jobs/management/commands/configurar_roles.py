"""Crea grupos de edición del portal; no asigna permisos privados."""
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from App_Remote_Jobs.models import Oferta, Sector, Habilidad


ROLES = {
    "Editor de ofertas": {Oferta: ("view", "add", "change"), Sector: ("view",), Habilidad: ("view",)},
    "Gestor de catálogo": {Oferta: ("view",), Sector: ("view", "add", "change"), Habilidad: ("view", "add", "change")},
}


class Command(BaseCommand):
    help = "Crea grupos E4 idempotentes, sin dar acceso a cuentas ni datos personales."

    def handle(self, *args, **kwargs):
        for nombre, modelos in ROLES.items():
            grupo, _ = Group.objects.get_or_create(name=nombre)
            permisos = []
            for modelo, acciones in modelos.items():
                content_type = ContentType.objects.get_for_model(modelo)
                for accion in acciones:
                    permisos.append(Permission.objects.get(content_type=content_type, codename=f"{accion}_{modelo._meta.model_name}"))
            grupo.permissions.set(permisos)
            self.stdout.write(f"{nombre}: {len(permisos)} permisos")
