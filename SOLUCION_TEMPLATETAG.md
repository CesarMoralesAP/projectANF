# SOLUCIÓN: Error 'proyecciones_extras' is not a registered tag library

## Problema
```
Error procesando el archivo: 'proyecciones_extras' is not a registered tag library.
```

## Causa
Django **NO reconoce automáticamente** los nuevos templatetags hasta que se reinicia el servidor. Los templatetags se cargan en memoria cuando Django inicia.

## Solución ✅

### Paso 1: Detener el servidor actual
En la terminal donde está corriendo `python manage.py runserver`, presiona:
```
Ctrl + C
```

### Paso 2: Reiniciar el servidor
```bash
# Activar entorno virtual y reiniciar
venv\Scripts\Activate.ps1
python manage.py runserver
```

### Paso 3: Probar el módulo
Accede a: `http://127.0.0.1:8000/proyecciones/`

## Verificación Manual

Si después de reiniciar sigue el error, verifica que los archivos existen:

```
apps/
  proyecciones/
    templatetags/
      __init__.py          ← Debe existir (vacío o con comentario)
      proyecciones_extras.py  ← Debe tener el filtro formato_moneda
```

### Verificar contenido de `__init__.py`
Debe estar vacío o tener solo un comentario. Es necesario para que Python lo reconozca como paquete.

### Verificar contenido de `proyecciones_extras.py`
Debe tener:
```python
from django import template

register = template.Library()

@register.filter(name='formato_moneda')
def formato_moneda(valor):
    try:
        num = float(valor)
        return "{:,.2f}".format(num)
    except (ValueError, TypeError):
        return valor
```

## ¿Por qué pasa esto?

Django carga los templatetags en memoria al iniciar. Cuando creas nuevos templatetags después de que el servidor ya está corriendo, Django no los detecta automáticamente.

**Siempre que agregues/modifiques templatetags, debes reiniciar el servidor.**

## Estado Actual

✅ Archivos creados correctamente  
✅ Código del filtro correcto  
⚠️ **Requiere reinicio del servidor**

---

**IMPORTANTE**: Después de reiniciar, el error desaparecerá y el filtro `formato_moneda` funcionará correctamente.
