# 📊 Documentación: Implementación de Tabla de Ventas Históricas

## 🎯 Objetivo
Esta documentación explica cómo completar la funcionalidad de "Calcular Proyección" 
que actualmente está preparada pero requiere la definición de la tabla de ventas históricas.

---

## 📋 Estado Actual

### ✅ YA IMPLEMENTADO:
- Vista `CalcularProyeccionView` en `apps/analisis/views.py`
- URL `/informes-y-analisis/empresa/<id>/proyeccion/calcular/`
- Template `proyeccion_calculada.html`
- Botón activo en `proyeccion_metodos.html`
- Estructura completa para calcular proyecciones
- Método `_calcular_proyecciones()` preparado

### ⏳ PENDIENTE:
- Definir modelo de la tabla de ventas
- Implementar consulta real en `_obtener_datos_historicos()`
- Implementar fórmulas matemáticas en `_calcular_proyecciones()`

---

## 🗃️ Estructura de la Tabla Requerida

La tabla debe tener al menos estos campos:

```python
# Ejemplo de modelo (apps/TU_APP/models.py)

class VentaMensual(ModeloBase):
    """
    Modelo para almacenar ventas mensuales históricas de empresas.
    """
    empresa = models.ForeignKey(
        'empresas.Empresa',
        on_delete=models.CASCADE,
        related_name='ventas_mensuales',
        verbose_name='Empresa'
    )
    
    # CAMPO 1: Período (Mes)
    periodo = models.DateField(
        verbose_name='Período',
        help_text='Fecha del mes (ej: 2024-01-01 para Enero 2024)'
    )
    
    # CAMPO 2: Valor de Venta
    valor_venta = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name='Valor de Venta',
        help_text='Monto total de ventas del período'
    )
    
    class Meta:
        db_table = 'venta_mensual'
        verbose_name = 'Venta Mensual'
        verbose_name_plural = 'Ventas Mensuales'
        ordering = ['empresa', 'periodo']
        unique_together = [['empresa', 'periodo']]
    
    def __str__(self):
        return f"{self.empresa.nombre} - {self.periodo.strftime('%B %Y')}: ${self.valor_venta}"
```

### 📌 Nombres de Columnas Críticos:
- **Campo período:** Puede llamarse `periodo`, `mes`, `fecha_venta`, etc.
- **Campo valor:** Puede llamarse `valor_venta`, `venta`, `monto`, `total_ventas`, etc.

---

## 🔧 Pasos para Completar la Implementación

### PASO 1: Crear el Modelo

1. Define el modelo en el archivo apropiado (ej: `apps/ventas/models.py` o `apps/catalogos/models.py`)
2. Ejecuta las migraciones:
```bash
python manage.py makemigrations
python manage.py migrate
```

### PASO 2: Actualizar la Vista

En `apps/analisis/views.py`, método `_obtener_datos_historicos()`:

**BUSCAR ESTA SECCIÓN:**
```python
def _obtener_datos_historicos(self, empresa):
    """
    ...
    """
    # PLACEHOLDER - Datos de ejemplo para desarrollo
```

**REEMPLAZAR CON:**
```python
def _obtener_datos_historicos(self, empresa):
    """
    Obtiene datos históricos de ventas de la base de datos.
    """
    # Importar el modelo (ajustar según donde lo definas)
    from apps.TU_APP.models import VentaMensual  # ← CAMBIAR "TU_APP"
    
    # Consultar ventas de la empresa
    ventas = VentaMensual.objects.filter(
        empresa=empresa
    ).order_by('periodo').values('periodo', 'valor_venta')
    
    # Si no hay datos, retornar lista vacía
    if not ventas:
        return []
    
    # Formatear datos
    return [
        {
            'mes': venta['periodo'].strftime('%B %Y'),  # Si es DateField
            'venta': float(venta['valor_venta'])
        }
        for venta in ventas
    ]
```

**IMPORTANTE:** Ajustar los nombres de campos según tu modelo:
- `'periodo'` → nombre real de tu campo de fecha
- `'valor_venta'` → nombre real de tu campo de monto

### PASO 3: Implementar Fórmulas de Cálculo (OPCIONAL)

En `apps/analisis/views.py`, método `_calcular_proyecciones()`:

Actualmente retorna los valores sin procesamiento. Aquí puedes implementar:

```python
def _calcular_proyecciones(self, datos_historicos):
    """
    Calcula las proyecciones usando los 3 métodos.
    """
    import numpy as np
    from sklearn.linear_model import LinearRegression
    
    # Extraer datos
    periodos = [d['mes'] for d in datos_historicos]
    valores = [d['venta'] for d in datos_historicos]
    
    # Ejemplo: Mínimos Cuadrados usando scikit-learn
    X = np.array(range(len(valores))).reshape(-1, 1)
    y = np.array(valores)
    
    modelo = LinearRegression()
    modelo.fit(X, y)
    
    # Proyectar 12 meses adelante
    futuro_X = np.array(range(len(valores), len(valores) + 12)).reshape(-1, 1)
    proyeccion_mc = modelo.predict(futuro_X).tolist()
    
    # TODO: Implementar valor_incremental y valor_absoluto
    
    return {
        'valor_incremental': {
            'periodos': periodos + ['...'],  # Agregar períodos futuros
            'valores': valores + [...]  # Agregar valores calculados
        },
        'valor_absoluto': {
            'periodos': periodos + ['...'],
            'valores': valores + [...]
        },
        'minimos_cuadrados': {
            'periodos': periodos + [f'Proyección {i+1}' for i in range(12)],
            'valores': valores + proyeccion_mc
        }
    }
```

---

## 📊 Datos de Ejemplo (Para Testing)

Una vez creado el modelo, puedes agregar datos de prueba:

```python
# En Django shell: python manage.py shell

from apps.empresas.models import Empresa
from apps.TU_APP.models import VentaMensual
from datetime import date
from decimal import Decimal

empresa = Empresa.objects.first()

# Crear ventas de ejemplo (12 meses)
meses = [
    (date(2024, 1, 1), Decimal('15000.00')),
    (date(2024, 2, 1), Decimal('16500.00')),
    (date(2024, 3, 1), Decimal('17800.00')),
    (date(2024, 4, 1), Decimal('18200.00')),
    (date(2024, 5, 1), Decimal('19500.00')),
    (date(2024, 6, 1), Decimal('20100.00')),
    (date(2024, 7, 1), Decimal('21000.00')),
    (date(2024, 8, 1), Decimal('22500.00')),
    (date(2024, 9, 1), Decimal('23800.00')),
    (date(2024, 10, 1), Decimal('24200.00')),
    (date(2024, 11, 1), Decimal('25500.00')),
    (date(2024, 12, 1), Decimal('26800.00')),
]

for periodo, valor in meses:
    VentaMensual.objects.create(
        empresa=empresa,
        periodo=periodo,
        valor_venta=valor
    )
```

---

## ✅ Checklist de Implementación

- [ ] Modelo `VentaMensual` (o similar) creado
- [ ] Migraciones ejecutadas
- [ ] Campo `empresa` como ForeignKey
- [ ] Campo `periodo` (fecha del mes)
- [ ] Campo `valor_venta` (monto)
- [ ] Método `_obtener_datos_historicos()` actualizado con import correcto
- [ ] Nombres de campos ajustados en la consulta
- [ ] Datos de prueba cargados
- [ ] Probado en navegador
- [ ] (OPCIONAL) Fórmulas matemáticas implementadas

---

## 🚀 Después de Implementar

1. Reinicia el servidor Django
2. Ve a: http://127.0.0.1:8000/informes-y-analisis/
3. Selecciona una empresa
4. Haz clic en "🔢 Calcular en la Aplicación"
5. Confirma el cálculo
6. Verifica que se genere el gráfico con datos de la BD

---

## 📝 Notas Adicionales

- **Columnas requeridas:** Solo necesitas `mes` y `venta` (con los nombres que elijas)
- **Relación con Empresa:** Debe existir ForeignKey a `Empresa`
- **Formato de fecha:** Recomendado usar `DateField` para facilitar ordenamiento
- **Valores decimales:** Usar `DecimalField` para precisión financiera
- **Unicidad:** Considerar `unique_together` para evitar duplicados (empresa + periodo)

---

**Última actualización:** 2025-11-10  
**Estado:** ⚙️ Preparado - Pendiente definición de tabla
