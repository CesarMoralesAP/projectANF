# Módulo de Informes y Análisis Financiero

## Descripción
Este módulo permite a los usuarios generar análisis financieros para empresas, verificando la existencia de estados financieros completos antes de proceder con el análisis.

## Funcionalidades Implementadas

### 1. Vista Principal (`AnalisisFinancieroView`)
- **URL**: `/analisis/`
- **Template**: `templates/analisis/analisis_financiero.html`
- Muestra formulario con:
  - Selector de empresa (con sector)
  - Checkboxes para seleccionar múltiples años (últimos 10 años)
  - Botón "Generar Análisis"

### 2. Validación de Estados Financieros (`ValidarEstadosView`)
- **URL**: `/analisis/validar-estados/`
- **Método**: POST (AJAX)
- **Funcionalidad**:
  - Recibe empresa y años seleccionados
  - Verifica que existan **ambos** estados financieros para cada año:
    * Balance General
    * Estado de Resultados
  - Retorna respuesta JSON con:
    * `success`: true/false
    * `mensaje`: Descripción del resultado
    * `estados_faltantes`: Array con detalles de estados faltantes (si los hay)

### 3. Servicio de Validación (`ValidadorEstadosFinancieros`)
- **Ubicación**: `apps/analisis/servicios/validar_estados.py`
- **Método principal**: `validar_estados_por_años(empresa, años)`
- **Lógica**:
  1. Para cada año seleccionado, verifica existencia de Balance General y Estado de Resultados
  2. Si falta alguno, lo agrega a lista de estados faltantes
  3. Construye mensaje descriptivo indicando qué estados faltan por año
  4. Retorna diccionario con validación y mensaje

## Estructura de Archivos

```
apps/analisis/
├── servicios/
│   ├── __init__.py
│   └── validar_estados.py       # Servicio de validación
├── views.py                      # Vistas de análisis
├── urls.py                       # Rutas del módulo
└── ...

templates/analisis/
└── analisis_financiero.html      # Template principal
```

## Flujo de Uso

1. Usuario accede a "Informes y Análisis" desde el menú lateral
2. Selecciona una empresa del dropdown
3. Selecciona uno o más años mediante checkboxes
4. Presiona "Generar Análisis"
5. Sistema valida mediante AJAX:
   - ✅ Si todos los estados existen: Muestra alerta de éxito
   - ❌ Si faltan estados: Muestra alerta de error con detalle de estados faltantes por año
6. Alertas se cierran automáticamente después de 8 segundos

## Mensajes de Validación

### Éxito
```
¡Análisis generado exitosamente para [Empresa]!
Años analizados: 2020, 2021, 2023
```

### Error - Estados Faltantes
```
No se puede generar el análisis. Faltan los siguientes estados financieros:
• Año 2020: Falta Balance General
• Año 2022: Falta Balance General y Estado de Resultados
• Año 2023: Falta Estado de Resultados
```

### Advertencias
- "Debe seleccionar una empresa."
- "Debe seleccionar al menos un año."

## Diseño UI/UX

### Características
- **Grid responsive**: 2 columnas en desktop, 1 en móvil
- **Checkboxes interactivos**: Todo el div es clickeable
- **Visual feedback**: Bordes y fondo cambian al seleccionar años
- **Alertas animadas**: Slideshow desde la derecha, auto-cierre
- **Loading state**: Botón se desactiva y muestra "Validando..." durante procesamiento

### Colores (según variables.css)
- Primary: `#6366F1` (Violeta)
- Background: `#F5F5F7`
- Text Primary: `#1F2937`
- Text Secondary: `#6B7280`
- Border: `#E5E7EB`
- Success: `#10B981`
- Error: `#EF4444`

## Integración con Otros Módulos

### Dependencias
- **`apps.empresas`**: Obtiene lista de empresas con sectores
- **`apps.estados`**: Consulta existencia de estados financieros (`EstadoFinanciero`, `TipoEstadoFinanciero`)

### URLs Conectadas
- Enlace en sidebar del dashboard (`templates/dashboard/base.html`)
- URL principal configurada en `core/urls.py`

## Próximas Mejoras Sugeridas

1. **Generación de análisis real**: Actualmente solo valida. Falta implementar:
   - Análisis horizontal (comparación entre años)
   - Análisis vertical (proporciones dentro de cada año)
   - Cálculo de ratios financieros
   - Comparación con benchmarks sectoriales

2. **Exportación**: Permitir descargar análisis en PDF/Excel

3. **Visualizaciones**: Gráficas de evolución de ratios

4. **Filtros adicionales**: Por sector, comparación multi-empresa

## Pruebas Recomendadas

1. **Caso exitoso**: Seleccionar empresa y años con estados completos
2. **Estados faltantes**: Seleccionar años sin Balance General o Estado de Resultados
3. **Validación de formulario**: Intentar generar sin empresa o sin años
4. **Múltiples años**: Seleccionar 3-4 años y verificar validación de todos
5. **Responsive**: Probar en diferentes tamaños de pantalla

## Comandos Útiles

```bash
# Ejecutar servidor
python manage.py runserver

# Acceder al módulo
http://127.0.0.1:8000/analisis/

# Crear datos de prueba (si no existen)
python manage.py crear_datos_demo
```

---
**Última actualización**: 10 de noviembre de 2025
