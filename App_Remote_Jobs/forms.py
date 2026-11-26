from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, SetPasswordForm, UserCreationForm

from .models import BusquedaGuardada, PerfilUsuario

User = get_user_model()


class WidgetClassesMixin:
    """Aplica clases coherentes al HTML generado por Django sin JavaScript."""

    def add_widget_classes(self):
        for nombre, field in self.fields.items():
            css = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (css + " form-control").strip()
            if field.help_text and not field.widget.attrs.get("aria-describedby"):
                # Mismo ID que usa la plantilla de campos compartida.
                field.widget.attrs["aria-describedby"] = f"{self[nombre].auto_id}_helptext"
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


class EstablecerContrasenaForm(WidgetClassesMixin, SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_widget_classes()


class BusquedaGuardadaForm(WidgetClassesMixin, forms.ModelForm):
    class Meta:
        model = BusquedaGuardada
        fields = ("nombre", "q", "sector", "habilidad", "modalidad", "tipo_empleo", "ubicacion", "salario_desde", "salario_hasta", "fecha_desde", "fecha_hasta", "orden")
        widgets = {"fecha_desde": forms.DateInput(attrs={"type": "date"}),
                   "fecha_hasta": forms.DateInput(attrs={"type": "date"})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import Habilidad, Oferta, Sector
        self.fields["sector"] = forms.ChoiceField(required=False, choices=[("", "Todos los sectores")] + list(Sector.objects.values_list("slug", "nombre")))
        self.fields["habilidad"] = forms.ChoiceField(required=False, choices=[("", "Todas las habilidades")] + list(Habilidad.objects.values_list("slug", "nombre")))
        self.fields["modalidad"] = forms.ChoiceField(required=False, choices=[("", "Cualquiera")] + list(Oferta.Modalidad.choices))
        self.fields["tipo_empleo"] = forms.ChoiceField(required=False, choices=[("", "Cualquiera")] + list(Oferta.TipoEmpleo.choices))
        self.fields["orden"] = forms.ChoiceField(
            required=False,
            choices=[
                ("recientes", "Recientes"), ("antiguas", "Antiguas"),
                ("titulo", "Título"), ("salario_desc", "Mayor salario"),
                ("salario_asc", "Menor salario"),
            ],
        )
        self.add_widget_classes()

    def clean_nombre(self):
        valor = self.cleaned_data["nombre"].strip()
        if not valor:
            raise forms.ValidationError("Da un nombre a tu búsqueda.")
        return valor

    def clean(self):
        datos = super().clean()
        desde, hasta = datos.get("salario_desde"), datos.get("salario_hasta")
        if desde is not None and hasta is not None and desde > hasta:
            self.add_error("salario_hasta", "No puede ser inferior al salario mínimo.")
        if datos.get("fecha_desde") and datos.get("fecha_hasta") and datos["fecha_desde"] > datos["fecha_hasta"]:
            self.add_error("fecha_hasta", "No puede ser anterior a la fecha inicial.")
        return datos
