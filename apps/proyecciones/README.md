# Módulo de Proyección de Ventas

## Descripción
El módulo de **Proyección de Ventas** permite a los usuarios generar proyecciones de ventas para el siguiente año basándose en datos históricos, utilizando tres métodos estadísticos diferentes.

## Funcionalidades Implementadas

### 1. Carga de Datos Históricos
- **Formato**: Archivo Excel (.xlsx, .xls)
- **Estructura requerida**: 3 columnas
  - Columna 1: **Año** (numérico)
  - Columna 2: **Mes** (numérico, 1-12)
  - Columna 3: **Valor** (numérico decimal)

### 2. Métodos de Proyección

#### Incremento Absoluto
Calcula el incremento promedio absoluto entre el primer y último valor histórico, luego lo aplica secuencialmente para proyectar los próximos 12 meses.

**Fórmula**:
```
incremento = (valor_final - valor_inicial) / cantidad_datos
valor_proyectado[i] = valor_final + (incremento × i)
```

#### Incremento Porcentual
Calcula el incremento porcentual promedio y lo aplica de forma compuesta para proyectar.

**Fórmula**:
```
incremento = ((valor_final - valor_inicial) / valor_inicial) / cantidad_datos
valor_proyectado[i] = valor_final × (1 + incremento)^i
```

#### Mínimos Cuadrados
Ajusta una recta de tendencia lineal (y = bx + a) a los datos históricos mediante regresión lineal.

**Fórmula**:
```
y = bx + a
donde b y a se calculan mediante regresión lineal
```

### 3. Visualización de Resultados

#### Gráfica Interactiva
- **Biblioteca**: Chart.js 4.4.0
- **Tipo**: Gráfica de líneas
- **Datasets**:
  - Datos históricos (línea continua azul)
  - Proyección (línea punteada verde)
- **Características**:
  - Tooltips interactivos con formato de moneda
  - Leyenda inferior
  - Responsive

#### Tabla de Proyección
- 12 filas (una por mes proyectado)
- Formato de moneda USD con separadores de miles
- Estilos alternados para mejor legibilidad

#### Estadísticas Rápidas
Panel con 4 tarjetas mostrando:
- Cantidad de meses históricos
- Cantidad de meses proyectados
- Año proyectado
- Método utilizado

### 4. Persistencia de Datos
Los resultados se guardan automáticamente en la tabla `proyeccion_ventas` con:
- Empresa asociada
- Año y mes proyectado
- Método utilizado
- Valor proyectado

## Estructura de Archivos

```
apps/proyecciones/
├── models.py              # Modelos Ventas y ProyeccionVenta
├── views.py               # ProyeccionVentasView, GenerarProyeccionView
├── urls.py                # URLs del módulo
├── migrations/            # Migraciones de base de datos
└── admin.py

templates/proyecciones/
├── proyeccion_form.html        # Formulario de carga
└── proyeccion_resultados.html  # Resultados y gráfica
```

## Modelos de Base de Datos

### Ventas
```python
class Ventas(ModeloBase):
    empresa = ForeignKey(Empresa)
    anio = PositiveSmallIntegerField
    mes = PositiveSmallIntegerField
    valor = DecimalField(15, 2)
    
    Meta:
        unique_together = [['empresa', 'anio', 'mes']]
```

### ProyeccionVenta
```python
class ProyeccionVenta(ModeloBase):
    empresa = ForeignKey(Empresa)
    anio = PositiveSmallIntegerField
    mes = PositiveSmallIntegerField
    metodo = CharField(50)
    valor_proyectado = DecimalField(15, 2)
```

Ambos modelos heredan de `ModeloBase` que proporciona:
- `creado_en` (DateTimeField auto_now_add)
- `actualizado_en` (DateTimeField auto_now)

## URLs

```python
/proyecciones/           # Formulario de carga
/proyecciones/generar/   # Procesamiento POST
```

## Diseño y Estilo

### Paleta de Colores
- **Primary**: `#6366F1` (Violeta)
- **Success**: `#10B981` (Verde)
- **Background**: `#F5F5F7` (Gris claro)
- **Surface**: `#FFFFFF` (Blanco)
- **Text Primary**: `#1F2937` (Negro suave)
- **Text Secondary**: `#6B7280` (Gris)

### Componentes Reutilizables
- Variables CSS de `static/css/variables.css`
- Espaciado consistente con sistema `--spacing-*`
- Border radius con sistema `--radius-*`
- Sombras con sistema `--shadow-*`

### Adaptaciones Realizadas
1. **Diseño consistente** con el resto del sistema
2. **Uso de variables CSS** globales
3. **Herencia de `dashboard/base.html`** para mantener navegación
4. **Mensajes Django** integrados
5. **Responsive design** para móviles

## Dependencias

```txt
Django==5.2.8
pandas          # Procesamiento de Excel
numpy           # Cálculos estadísticos
openpyxl        # Lectura de archivos Excel
```

## Uso

### 1. Preparar Archivo Excel
Crear un archivo Excel con 3 columnas:

| Año  | Mes | Valor     |
|------|-----|-----------|
| 2023 | 1   | 50000.00  |
| 2023 | 2   | 52000.00  |
| 2023 | 3   | 51500.00  |
| ...  | ... | ...       |

### 2. Acceder al Módulo
1. Iniciar sesión en el sistema
2. Navegar a `/proyecciones/`
3. Seleccionar empresa
4. Elegir método de proyección
5. Cargar archivo Excel
6. Click en "Generar Proyección"

### 3. Visualizar Resultados
- Gráfica interactiva con históricos y proyección
- Tabla detallada de valores proyectados
- Ecuación de tendencia (para Mínimos Cuadrados)
- Estadísticas rápidas

## Validaciones

### Servidor
- ✅ Empresa requerida
- ✅ Método requerido
- ✅ Archivo requerido
- ✅ Archivo debe tener al menos 3 columnas
- ✅ Valores deben ser numéricos
- ✅ Se eliminan filas con datos faltantes

### Cliente
- ✅ Formulario HTML5 con `required`
- ✅ Aceptación de solo archivos Excel
- ✅ Indicador visual de archivo seleccionado
- ✅ Drag & drop habilitado

## Mensajes de Usuario

### Éxito
```
✓ Proyección generada exitosamente para el año 2024 con el método Mínimos Cuadrados.
```

### Error
```
✕ El archivo debe tener las columnas: Año, Mes y Valor.
✕ Error procesando el archivo: [detalle del error]
```

## Diferencias con proyecciones-v2

### Mantenido
- ✅ Toda la lógica de cálculo
- ✅ Métodos de proyección
- ✅ Persistencia en base de datos
- ✅ Estructura de modelos

### Adaptado
- 🔄 Diseño UI/UX consistente con el sistema
- 🔄 Class-Based Views en lugar de function-based
- 🔄 Templates con herencia de `dashboard/base.html`
- 🔄 Uso de variables CSS globales
- 🔄 Sistema de mensajes Django
- 🔄 Namespace en URLs (`proyecciones:`)
- 🔄 Modelos heredan de `ModeloBase`

### Mejorado
- ✨ Drag & drop para archivo Excel
- ✨ Estadísticas rápidas visuales
- ✨ Tooltips mejorados en gráfica
- ✨ Responsive design completo
- ✨ Indicadores visuales de selección
- ✨ Mejor manejo de errores

## Arquitectura de Clases

```python
# Vista del formulario
ProyeccionVentasView(LoginRequiredMixin, TemplateView)
    └── get_context_data()

# Vista de procesamiento
GenerarProyeccionView(LoginRequiredMixin, View)
    └── post()
        ├── Validar datos
        ├── Leer Excel con pandas
        ├── Calcular proyección (numpy)
        ├── Guardar en ProyeccionVenta
        └── Renderizar resultados
```

## Mejoras Futuras Sugeridas

1. **Exportar resultados** a Excel/PDF
2. **Comparación de métodos** lado a lado
3. **Validación de archivo** más robusta (plantilla descargable)
4. **Histórico de proyecciones** por empresa
5. **Edición de proyecciones** generadas
6. **Gráficas adicionales** (barras, áreas)
7. **Métricas de precisión** (error medio, R²)
8. **Proyecciones a más de 12 meses**

## Notas Técnicas

- El módulo NO modifica `proyecciones-v2` (se mantiene intacto)
- Compatible con Django 5.2.8
- Requiere MySQL 8.x
- JavaScript vanilla (sin jQuery)
- Chart.js vía CDN (sin npm)

## Troubleshooting

### Error: "Data truncated for column 'valor_proyectado'"

**Problema**: MySQL no puede convertir valores `numpy.float64` directamente a `DecimalField`.

**Solución**: Ya está corregido en el código. Los valores numpy se convierten a `float` de Python antes de guardar:
```python
valor_proyectado=float(valor)  # Conversión explícita
```

**Ver más detalles**: `FIX_NUMPY_CONVERSION.md`

### Error: "El archivo debe tener las columnas: Año, Mes y Valor"

**Causa**: El archivo Excel tiene menos de 3 columnas.

**Solución**: Asegúrate de que el Excel tenga exactamente 3 columnas (puede tener cualquier nombre, pero deben ser 3).

### Error: "Datos insuficientes para proyección"

**Causa**: El archivo Excel no tiene suficientes filas con datos válidos.

**Solución**: Incluye al menos 6 meses de datos históricos. Las filas vacías o con valores no numéricos se ignoran automáticamente.

### Los valores proyectados son muy diferentes a los históricos

**Causa posible**: Datos históricos con mucha variación o método no apropiado.

**Solución**: 
- Prueba con otro método de proyección
- Verifica que los datos históricos sean consistentes
- Para tendencias lineales claras, usa "Mínimos Cuadrados"
- Para crecimiento exponencial, usa "Incremento Porcentual"

## Créditos

- **Implementación original**: proyecciones-v2
- **Adaptación de diseño**: Siguiendo `setupcursor.cursorrules` y convenciones del proyecto
- **Framework**: Django 5.2.8
- **Visualizaciones**: Chart.js 4.4.0
