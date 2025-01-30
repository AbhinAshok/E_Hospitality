from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(value, css_class):
    """Adds a CSS class to a form widget."""
    if hasattr(value, 'field') and hasattr(value.field.widget, 'attrs'):
        value.field.widget.attrs['class'] = value.field.widget.attrs.get('class', '') + f' {css_class}'
    return value