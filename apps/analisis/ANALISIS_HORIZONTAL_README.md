# Análisis Horizontal - Documentación

## Resumen
Se ha implementado la funcionalidad de **Análisis Horizontal** para el Balance General y Estado de Resultados. Esta funcionalidad permite comparar estados financieros entre diferentes años y calcular variaciones absolutas y porcentuales.

## Características Implementadas

### 1. Validación de Años
- **Mínimo requerido**: 2 años para realizar el análisis
- Si el usuario selecciona solo 1 año, se muestra una alerta indicando que se necesitan al menos 2 años
- Los años se ordenan automáticamente de menor a mayor

### 2. Cálculo de Variaciones
Para cada cuenta contable se calculan:

- **Variación Absoluta**: Diferencia monetaria entre años consecutivos
  ```
  Variación Absoluta = Monto Año Siguiente - Monto Año Base
  ```

- **Variación Porcentual**: Cambio porcentual respecto al año base
  ```
  Variación Porcentual = (Variación Absoluta / |Monto Año Base|) × 100
  ```

### 3. Columnas Dinámicas
Si el usuario selecciona más de 2 años:
- **Años consecutivos**: Ej. 2020, 2021, 2022
  - Se crean columnas: "Variación 2020-2021" y "Variación 2021-2022"

- **Años no consecutivos**: Ej. 2019, 2021, 2023
  - Se crean columnas: "Variación 2019-2021" y "Variación 2021-2023"
  - Siempre se respeta el orden cronológico (menor a mayor)

### 4. Visualización por Categorías
Los datos se organizan por tipo de cuenta:

**Balance General:**
- Activos
- Pasivos
- Patrimonio

**Estado de Resultados:**
- Ingresos
- Gastos
- Resultado

### 5. Indicadores Visuales
- **Variación Positiva**: Color verde, símbolo "+"
- **Variación Negativa**: Color rojo, símbolo "-"
- **Sin Variación**: Color gris
- **Datos No Disponibles**: "N/A"

### 6. Botón de Gráfica
Cada cuenta tiene un botón de icono de gráfica que permite:
- Visualizar los montos de esa cuenta específica a lo largo de los años seleccionados
- Actualmente muestra un mensaje indicando que está en desarrollo
- La estructura está lista para implementar gráficas interactivas

## Estructura de Archivos

### Backend

#### Servicio: `apps/analisis/servicios/analisis_horizontal.py`
Clase `AnalizadorHorizontal` con dos métodos principales:

1. **`analizar_balance_general(empresa, años)`**
   - Obtiene estados financieros de Balance General
   - Filtra cuentas tipo: ACTIVO, PASIVO, PATRIMONIO
   - Calcula variaciones entre años consecutivos
   - Retorna datos estructurados por tipo de cuenta

2. **`analizar_estado_resultados(empresa, años)`**
   - Obtiene estados financieros de Estado de Resultados
   - Filtra cuentas tipo: INGRESO, GASTO, RESULTADO
   - Calcula variaciones entre años consecutivos
   - Retorna datos estructurados por tipo de cuenta

#### Vistas: `apps/analisis/views.py`
Dos nuevas vistas CBV:

1. **`AnalisisHorizontalBalanceView`**
   - Ruta: `/analisis/analisis-horizontal/balance/`
   - Método: POST
   - Requiere: `empresa_id`, `años[]` (mínimo 2)
   - Retorna: JSON con datos del análisis o mensaje de error

2. **`AnalisisHorizontalResultadosView`**
   - Ruta: `/analisis/analisis-horizontal/resultados/`
   - Método: POST
   - Requiere: `empresa_id`, `años[]` (mínimo 2)
   - Retorna: JSON con datos del análisis o mensaje de error

#### URLs: `apps/analisis/urls.py`
```python
path('analisis-horizontal/balance/', AnalisisHorizontalBalanceView.as_view(), name='analisis_horizontal_balance'),
path('analisis-horizontal/resultados/', AnalisisHorizontalResultadosView.as_view(), name='analisis_horizontal_resultados'),
```

### Frontend

#### Template: `templates/analisis/analisis_financiero.html`

**Nuevos estilos CSS:**
- `.tabla-horizontal`: Estilos para la tabla de análisis
- `.btn-graficar`: Botón icono para gráficas
- `.valor-variacion`: Contenedor para variaciones
- `.variacion-porcentual`: Badge con colores según variación
- `.tipo-header`: Encabezados de categorías
- `.toast-message`: Mensajes de notificación

**Nuevas funciones JavaScript:**

1. **`cargarAnalisisHorizontal()`**
   - Punto de entrada principal
   - Verifica que haya al menos 2 años
   - Carga ambos análisis (Balance y Resultados)

2. **`cargarAnalisisHorizontalBalance()`**
   - Hace POST a la API de análisis horizontal del Balance
   - Maneja la respuesta y renderiza los datos

3. **`cargarAnalisisHorizontalResultados()`**
   - Hace POST a la API de análisis horizontal del Estado de Resultados
   - Maneja la respuesta y renderiza los datos

4. **`renderizarAnalisisHorizontal(data, tipo)`**
   - Construye dinámicamente la tabla HTML
   - Crea columnas para cada año seleccionado
   - Crea columnas para cada variación calculada
   - Aplica formato a montos y porcentajes
   - Agrega colores según el tipo de variación

5. **`graficarCuenta(cuentaId, cuentaNombre)`**
   - Placeholder para funcionalidad de gráficas
   - Preparado para mostrar gráfica de evolución de la cuenta

6. **Funciones auxiliares:**
   - `formatearMonto(monto)`: Formato de moneda USD
   - `formatearPorcentaje(porcentaje)`: Formato de porcentaje con signo

## Flujo de Uso

1. Usuario selecciona una empresa
2. Usuario selecciona 2 o más años (checkbox)
3. Usuario hace clic en "Generar Análisis"
4. Sistema valida estados financieros y calcula ratios
5. Usuario navega a la pestaña "Análisis Horizontal"
6. Sistema carga automáticamente los datos si hay 2+ años
7. Usuario puede alternar entre "Balance General" y "Estado de Resultados"
8. Usuario puede hacer clic en el icono de gráfica de cualquier cuenta

## Manejo de Datos

### Almacenamiento Temporal
Los cálculos **NO se persisten en la base de datos**. Se calculan en tiempo real y se almacenan en:

```javascript
datosAnalisisActual = {
    empresaId: null,
    años: [],
    horizontalBalance: null,
    horizontalResultados: null
}
```

### Optimización
- Los datos se cargan bajo demanda (lazy loading)
- Se cachean en memoria durante la sesión del usuario
- Solo se recalculan cuando el usuario selecciona una nueva empresa o años diferentes

## Casos Especiales Manejados

1. **Monto Base = 0**: Variación porcentual = N/A
2. **Cuenta sin datos en un año**: Monto = N/A, Variación = N/A
3. **Menos de 2 años**: Muestra alerta y no permite continuar
4. **Estados financieros faltantes**: Mensaje de error descriptivo
5. **Años no consecutivos**: Se calculan variaciones respetando el orden cronológico

## Extensibilidad

### Para agregar funcionalidad de gráficas:

1. Implementar la función `graficarCuenta()` en JavaScript
2. Crear un modal o sidebar para mostrar la gráfica
3. Usar una librería como Chart.js o ApexCharts
4. Obtener los datos de `datosAnalisisActual` para construir la gráfica
5. Mostrar evolución temporal de la cuenta seleccionada

Ejemplo de estructura de datos disponible:
```javascript
{
    cuentaId: 123,
    cuentaNombre: "Activo Corriente",
    años: [2020, 2021, 2022],
    montos: [50000, 55000, 48000]
}
```

## Próximos Pasos Sugeridos

1. ✅ Análisis Horizontal del Balance General
2. ✅ Análisis Horizontal del Estado de Resultados
3. 🔲 Implementar gráficas interactivas por cuenta
4. 🔲 Análisis Vertical (estructura porcentual)
5. 🔲 Exportación a PDF/Excel
6. 🔲 Comparación con múltiples empresas del mismo sector

## Tecnologías Utilizadas

- **Backend**: Django 5.2, Python 3.11+
- **Frontend**: JavaScript Vanilla, CSS Variables
- **Base de Datos**: MySQL 8.x
- **Patrón**: Class-Based Views (CBV), Servicios, AJAX con Fetch API
