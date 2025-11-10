from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """
    Obtiene un valor de un diccionario usando una clave.
    Uso en template: {{ dictionary|get_item:key }}
    """
    if dictionary is None:
        return None
    return dictionary.get(str(key))


@register.filter
def get_item_int(dictionary, key):
    """
    Obtiene un valor de un diccionario usando una clave y lo convierte a int.
    Uso en template: {{ dictionary|get_item_int:key }}
    """
    if dictionary is None:
        return None
    value = dictionary.get(str(key))
    if value is not None:
        return int(value)
    return None

