# Fix: Error de Conversión numpy.float64 a DecimalField

## Problema Identificado

```
Error procesando el archivo: (1265, "1265: Data truncated for column 'valor_proyectado' at row 1", None)
```

## Causa Raíz

El error tiene **DOS causas combinadas**:

1. **Tipo de dato**: MySQL no puede convertir directamente valores de tipo `numpy.float64` a campos `DecimalField`
2. **Precisión decimal**: El campo `decimal(15,2)` solo acepta **2 decimales**, pero numpy genera valores con muchos más decimales (ej: `50000.123456789`)

Cuando numpy realiza cálculos (como `a + b * x_proj`), devuelve arrays con tipo `numpy.float64` con alta precisión decimal, pero MySQL con `decimal(15,2)` trunca cualquier valor con más de 2 decimales.

## Solución Aplicada

**Archivo modificado**: `apps/proyecciones/views.py` línea ~107

### Antes (Causaba el error):
```python
ProyeccionVenta.objects.create(
    empresa=empresa,
    anio=anio_proj,
    mes=mes_numero,
    metodo=metodo,
    valor_proyectado=valor  # ❌ numpy.float64 con muchos decimales
)
```

### Después (Corregido):
```python
# Convertir y redondear a 2 decimales para decimal(15,2)
valor_redondeado = round(float(valor), 2)
ProyeccionVenta.objects.create(
    empresa=empresa,
    anio=anio_proj,
    mes=mes_numero,
    metodo=metodo,
    valor_proyectado=valor_redondeado  # ✅ float con máximo 2 decimales
)
```

**Cambios realizados**:
1. `float(valor)` - Convierte `numpy.float64` a `float` de Python
2. `round(..., 2)` - Redondea a exactamente 2 decimales para cumplir con `decimal(15,2)`

## ¿Por qué no pasó en proyecciones-v2?

En el código original de `proyecciones-v2`, el problema existía pero podía pasar desapercibido dependiendo de:
1. La versión de MySQL/mysql-connector
2. El modo estricto de MySQL
3. La configuración de `managed=False` en los modelos

## Verificación

Para verificar que el fix funciona:

```bash
# Activar entorno virtual
venv\Scripts\Activate.ps1

# Probar conversión
python test_conversion.py

# Probar módulo completo
python manage.py runserver
# Ir a http://127.0.0.1:8000/proyecciones/
```

## Tipos de Conversión Seguros

```python
# De numpy a Python para Django
numpy_value = np.float64(123.45)
python_value = float(numpy_value)  # ✓ Seguro para DecimalField

# También funciona con arrays
numpy_array = np.array([1.1, 2.2, 3.3])
python_list = [float(v) for v in numpy_array]  # ✓ Seguro
```

## Estado

✅ **CORREGIDO** - El módulo ahora convierte correctamente los valores de numpy antes de guardar en la base de datos.

---
**Fecha**: 10 de noviembre de 2025
