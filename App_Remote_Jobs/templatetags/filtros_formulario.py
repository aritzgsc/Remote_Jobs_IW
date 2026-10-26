"""Filtros pequeños para mantener las plantillas de formularios reutilizables."""

from django import template

register = template.Library()


@register.filter
def add_class(bound_field, css_class):
    """Añade una clase CSS al widget sin cambiar el formulario original."""
    attrs = bound_field.field.widget.attrs.copy()
    current = attrs.get("class", "")
    attrs["class"] = " ".join(dict.fromkeys((current + " " + str(css_class)).split()))
    return bound_field.as_widget(attrs=attrs)
