from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q


class AutenticacionCorreoONombreUsuario(ModelBackend):
    """Autentica con nombre de usuario o correo, sin reducir las protecciones de Django."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        identifier = username or kwargs.get(UserModel.USERNAME_FIELD)
        if not identifier or password is None:
            return None

        manager = UserModel._default_manager
        try:
            if "@" in identifier:
                user = manager.get(email__iexact=identifier.strip())
            else:
                user = manager.get(**{f"{UserModel.USERNAME_FIELD}__iexact": identifier.strip()})
        except (UserModel.DoesNotExist, UserModel.MultipleObjectsReturned):
            # Reduce diferencias de tiempo entre cuentas existentes e inexistentes.
            UserModel().set_password(password)
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
