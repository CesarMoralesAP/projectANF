"""
Filtros de template personalizados para el módulo de proyecciones.
"""
from django import template

register = template.Library()


@register.filter(name='formato_moneda')
def formato_moneda(valor):
    """
    Formatea un número como moneda con separadores de miles.
    Ejemplo: 50000.50 -> 50,000.50
    """
    try:
        # Convertir a float si no lo es
        num = float(valor)
        
        # Formatear con separador de miles
        return "{:,.2f}".format(num)
    except (ValueError, TypeError):
        return valor
