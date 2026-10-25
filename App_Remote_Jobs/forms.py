from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

User = get_user_model()

class WidgetClassesMixin:
    def add_widget_classes(self):
        for field in self.fields.values():
            field.widget.attrs["class"] = (field.widget.attrs.get("class", "") + " form-control").strip()

class RegistroForm(WidgetClassesMixin, UserCreationForm):
    email = forms.EmailField(label="Correo electrónico", max_length=254)
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs); self.add_widget_classes()

class InicioSesionForm(WidgetClassesMixin, AuthenticationForm):
    username = forms.CharField(label="Nombre de usuario o correo", max_length=254)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs); self.add_widget_classes()
