from django import template

register = template.Library()


@register.filter(name='to_unit')
def to_unit(celsius_value, unit_code):
    """
    Custom template filter — checklist-ის "custom template tag ან filter
    (მინ. 1)" მოთხოვნისთვის.

    გამოყენება template-ში: {{ weather.temperature|to_unit:temp_unit }}
    """
    if celsius_value is None:
        return '—'
    try:
        celsius_value = float(celsius_value)
    except (TypeError, ValueError):
        return celsius_value

    if unit_code == 'F':
        fahrenheit = celsius_value * 9 / 5 + 32
        return f'{fahrenheit:.1f}°F'
    return f'{celsius_value:.1f}°C'


@register.simple_tag
def anomaly_badge(is_anomaly):
    """დამატებითი simple_tag — ვიზუალური badge ანომალიისთვის."""
    return '⚠️ ანომალია' if is_anomaly else '✓ ნორმალური'
