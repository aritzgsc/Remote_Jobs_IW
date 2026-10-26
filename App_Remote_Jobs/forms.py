from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm

from .models import PerfilUsuario

User = get_user_model()


class WidgetClassesMixin:
    """Aplica clases coherentes al HTML generado por Django sin JavaScript."""

    def add_widget_classes(self):
        for field in self.fields.values():
            css = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (css + " form-control").strip()
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs.setdefault("rows", 4)


class RegistroForm(WidgetClassesMixin, UserCreationForm):
    email = forms.EmailField(label="Correo electrónico", max_length=254)
    first_name = forms.CharField(label="Nombre", max_length=150, required=False)
    last_name = forms.CharField(label="Apellidos", max_length=150, required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "first_name", "last_name")
        labels = {
            "username": "Nombre de usuario",
            "first_name": "Nombre",
            "last_name": "Apellidos",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].help_text = "Será visible en tu cuenta si no eliges otro nombre público."
        self.fields["password1"].label = "Contraseña"
        self.fields["password2"].label = "Repite la contraseña"
        self.add_widget_classes()

    def clean_email(self):
        email = self.cleaned_data["email"].strip()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Ya existe una cuenta con ese correo electrónico.")
        return email


class InicioSesionForm(WidgetClassesMixin, AuthenticationForm):
    username = forms.CharField(label="Correo electrónico o nombre de usuario", max_length=254)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].label = "Contraseña"
        self.add_widget_classes()


class DatosCuentaForm(WidgetClassesMixin, forms.ModelForm):
    email = forms.EmailField(label="Correo electrónico", max_length=254)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")
        labels = {"first_name": "Nombre", "last_name": "Apellidos", "email": "Correo electrónico"}
        widgets = {"first_name": forms.TextInput(), "last_name": forms.TextInput(), "email": forms.EmailInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_widget_classes()

    def clean_email(self):
        email = self.cleaned_data["email"].strip()
        if User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Ese correo electrónico ya pertenece a otra cuenta.")
        return email


class PerfilUsuarioForm(WidgetClassesMixin, forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = ("nombre_publico", "titular", "ubicacion", "biografia", "web", "avatar")
        labels = {
            "nombre_publico": "Nombre que se mostrará en tu perfil",
            "titular": "Titular profesional",
            "ubicacion": "Ubicación",
            "biografia": "Sobre mí",
            "web": "Web o portfolio",
            "avatar": "Foto de perfil",
        }
        widgets = {
            "nombre_publico": forms.TextInput(attrs={"placeholder": "Cómo quieres que te llamen"}),
            "titular": forms.TextInput(attrs={"placeholder": "Ej. Estudiante de Ingeniería Informática"}),
            "ubicacion": forms.TextInput(attrs={"placeholder": "Ej. Vitoria-Gasteiz, España"}),
            "biografia": forms.Textarea(attrs={"placeholder": "Cuéntanos brevemente qué te interesa profesionalmente...", "maxlength": 600}),
            "web": forms.URLInput(attrs={"placeholder": "https://tuportfolio.dev"}),
            "avatar": forms.ClearableFileInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_widget_classes()



class CambioContrasenaForm(WidgetClassesMixin, PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_widget_classes()
