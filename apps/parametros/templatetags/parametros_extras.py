from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """
    Obtiene un valor de un diccionario usando una clave.
    Intenta con la clave como int, str, o el tipo original.
    Uso en template: {{ dictionary|get_item:key }}
    """
    if dictionary is None:
        return None
    
    # Intentar con la clave tal cual
    value = dictionary.get(key)
    if value is not None:
        return value
    
    # Intentar convertir la clave a int si es posible
    try:
        key_int = int(key)
        value = dictionary.get(key_int)
        if value is not None:
            return value
    except (ValueError, TypeError):
        pass
    
    # Intentar convertir la clave a str
    try:
        key_str = str(key)
        value = dictionary.get(key_str)
        if value is not None:
            return value
    except (ValueError, TypeError):
        pass
    
    return None

