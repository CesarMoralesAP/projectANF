"""
Template tags personalizados para verificar permisos de usuario.
"""
from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def tiene_permiso_eliminar(context, modelo):
    """
    Verifica si el usuario actual tiene permiso para eliminar un modelo específico.
    
    Uso en template:
        {% tiene_permiso_eliminar 'empresas.empresa' as puede_eliminar %}
        {% if puede_eliminar %}
            <button>Eliminar</button>
        {% endif %}
    """
    user = context['request'].user
    
    # Superusuarios siempre tienen permiso
    if user.is_superuser:
        return True
    
    # Verificar permiso específico de delete
    # modelo debe estar en formato 'app_label.model_name'
    return user.has_perm(f'delete_{modelo}')


@register.simple_tag(takes_context=True)
def puede_eliminar(context, app_label, model_name):
    """
    Verifica si el usuario puede eliminar un modelo específico.
    
    Uso en template:
        {% puede_eliminar 'empresas' 'empresa' as puede %}
        {% if puede %}
            <button>Eliminar</button>
        {% endif %}
    """
    user = context['request'].user
    
    if user.is_superuser:
        return True
    
    permission_codename = f'{app_label}.delete_{model_name}'
    return user.has_perm(permission_codename)


@register.filter
def tiene_grupo(user, grupo_nombre):
    """
    Verifica si el usuario pertenece a un grupo específico.
    
    Uso en template:
        {% if request.user|tiene_grupo:"Administrador" %}
            <button>Admin only</button>
        {% endif %}
    """
    return user.groups.filter(name=grupo_nombre).exists()


@register.filter
def es_administrador(user):
    """
    Verifica si el usuario es administrador (superuser o del grupo Administrador).
    
    Uso en template:
        {% if request.user|es_administrador %}
            <button>Eliminar</button>
        {% endif %}
    """
    return user.is_superuser or user.groups.filter(name='Administrador').exists()


@register.filter
def es_gerente(user):
    """
    Verifica si el usuario es gerente de administración.
    
    Uso en template:
        {% if request.user|es_gerente %}
            <span>Gerente</span>
        {% endif %}
    """
    return user.groups.filter(name='Gerente de Administración').exists()
