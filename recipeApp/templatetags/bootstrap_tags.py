from django import template

register = template.Library()

@register.filter(name='bootstrap_toggle')
def bootstrap_toggle(boolean_field):
    if boolean_field:
        return f'<input type="checkbox" class="form-check-input" checked>'
    else:
        return f'<input type="checkbox" class="form-check-input">'
