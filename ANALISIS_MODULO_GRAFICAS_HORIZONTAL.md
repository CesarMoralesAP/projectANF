# Análisis del Módulo de Análisis Horizontal - Gráficas de Evolución Temporal

## 📋 Tabla de Contenidos
1. [Resumen Ejecutivo](#resumen-ejecutivo)
2. [Arquitectura General](#arquitectura-general)
3. [Flujo de Datos Completo](#flujo-de-datos-completo)
4. [Análisis Horizontal - Backend](#análisis-horizontal---backend)
5. [Generación de Gráficas - Frontend](#generación-de-gráficas---frontend)
6. [Estructura de Datos JSON](#estructura-de-datos-json)
7. [Componentes Visuales](#componentes-visuales)
8. [Puntos Críticos y Consideraciones](#puntos-críticos-y-consideraciones)
9. [Diagrama de Flujo](#diagrama-de-flujo)

---

## 🎯 Resumen Ejecutivo

El módulo de **Análisis Horizontal** permite visualizar la **evolución temporal de los montos de cuentas contables año tras año**. El sistema calcula variaciones absolutas y porcentuales entre períodos consecutivos y genera gráficas interactivas usando **Chart.js 4.4.0**.

### Características Principales:
- ✅ Análisis para Balance General y Estado de Resultados
- ✅ Cálculo de variaciones absolutas y porcentuales
- ✅ Gráficas de línea con tendencias (positiva/negativa)
- ✅ Modal interactivo con estadísticas detalladas
- ✅ Visualización con colores dinámicos según variación
- ✅ Tabla de datos con métricas calculadas

---

## 🏗️ Arquitectura General

```
┌─────────────────────────────────────────────────────────────────┐
│                    MÓDULO DE ANÁLISIS                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   VIEWS      │  │  SERVICIOS   │  │   MODELS     │          │
│  │  (views.py)  │─→│ (analisis_   │─→│ (models.py)  │          │
│  │              │  │  horizontal. │  │              │          │
│  │              │  │  py)         │  │              │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│         │                  │                  │                  │
│         ↓                  ↓                  ↓                  │
│  ┌──────────────────────────────────────────────────┐          │
│  │          BASE DE DATOS (MySQL 8.x)                │          │
│  │  - estados_financieros                            │          │
│  │  - items_estado_financiero                        │          │
│  │  - cuentas_contables                              │          │
│  │  - catalogos_cuenta                               │          │
│  └──────────────────────────────────────────────────┘          │
│                          │                                       │
│                          ↓                                       │
│  ┌──────────────────────────────────────────────────┐          │
│  │          TEMPLATE HTML + JavaScript               │          │
│  │  - analisis_financiero.html                       │          │
│  │  - Chart.js 4.4.0 (CDN)                          │          │
│  │  - JavaScript dinámico                            │          │
│  └──────────────────────────────────────────────────┘          │
│                          │                                       │
│                          ↓                                       │
│  ┌──────────────────────────────────────────────────┐          │
│  │     VISUALIZACIÓN (Modal + Gráfica)               │          │
│  └──────────────────────────────────────────────────┘          │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Flujo de Datos Completo

### 1️⃣ **Selección de Parámetros (Usuario)**

El usuario desde `templates/analisis/analisis_financiero.html`:

```html
<!-- Selecciona empresa y años -->
<select id="selectEmpresa" name="empresa_id">
    <option value="1">Banco Agrícola (Bancario)</option>
</select>

<!-- Selecciona años (mínimo 2 para análisis horizontal) -->
<input type="checkbox" name="años[]" value="2020">
<input type="checkbox" name="años[]" value="2021">
<input type="checkbox" name="años[]" value="2022">
```

### 2️⃣ **Validación de Estados Financieros**

```javascript
// 1. Submit del formulario → ValidarEstadosView
form.addEventListener('submit', function(e) {
    e.preventDefault();
    
    fetch("{% url 'analisis:validar_estados' %}", {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Estados válidos → calcular ratios
            renderizarRatios(data.ratios, data.años);
        }
    });
});
```

**Backend (`apps/analisis/views.py`)**:

```python
class ValidarEstadosView(LoginRequiredMixin, View):
    def post(self, request):
        empresa_id = request.POST.get('empresa_id')
        años_seleccionados = request.POST.getlist('años[]')
        
        # Validar existencia de estados financieros
        resultado = ValidadorEstadosFinancieros.validar_estados_por_años(
            empresa, años
        )
        
        if resultado['valido']:
            # Calcular ratios (no relevante para gráficas horizontales)
            ratios_data = CalculadoraRatios.calcular_ratios_por_años(
                empresa, años, usuario=request.user
            )
            
            return JsonResponse({
                'success': True,
                'ratios': ratios_convertidos,
                'años': años
            })
```

### 3️⃣ **Carga de Análisis Horizontal**

Cuando el usuario cambia a la pestaña "Análisis Horizontal":

```javascript
// Event listener en tab-button
tabButtons.forEach(button => {
    button.addEventListener('click', function() {
        const tabId = this.getAttribute('data-tab');
        
        if (tabId === 'horizontal' && datosAnalisisActual.años.length >= 2) {
            cargarAnalisisHorizontal(); // ← Llama a backend
        }
    });
});
```

**Llamada AJAX al Backend**:

```javascript
function cargarAnalisisHorizontalBalance() {
    const formData = new FormData();
    formData.append('empresa_id', datosAnalisisActual.empresaId);
    datosAnalisisActual.años.forEach(año => {
        formData.append('años[]', año);
    });
    
    fetch("{% url 'analisis:analisis_horizontal_balance' %}", {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            renderizarAnalisisHorizontal(data, 'balance');
        }
    });
}
```

---

## 🔧 Análisis Horizontal - Backend

### **Archivo**: `apps/analisis/servicios/analisis_horizontal.py`

#### **Clase Principal**: `AnalizadorHorizontal`

```python
class AnalizadorHorizontal:
    @staticmethod
    def analizar_balance_general(empresa, años):
        """
        Realiza el análisis horizontal del Balance General.
        
        Args:
            empresa: Instancia de Empresa
            años: Lista de años ordenados (de menor a mayor)
        
        Returns:
            dict: Datos estructurados para el análisis horizontal
        """
```

#### **Paso 1: Validación de Años**

```python
# Validar que haya al menos 2 años
if len(años) < 2:
    return {
        'error': 'Se necesitan al menos 2 años para análisis horizontal.'
    }
```

#### **Paso 2: Obtener Estados Financieros**

```python
# Obtener estados financieros de Balance General
estados = EstadoFinanciero.objects.filter(
    empresa=empresa,
    año__in=años,
    tipo=TipoEstadoFinanciero.BALANCE_GENERAL
).prefetch_related('items__cuenta_contable').order_by('año')
```

**Optimización N+1**: Usa `prefetch_related('items__cuenta_contable')` para evitar queries adicionales.

#### **Paso 3: Obtener Cuentas Contables**

```python
# Obtener todas las cuentas únicas del catálogo
cuentas_ids = set()
for estado in estados:
    cuentas_ids.update(estado.items.values_list('cuenta_contable_id', flat=True))

# Obtener información de las cuentas
cuentas = CuentaContable.objects.filter(
    id__in=cuentas_ids,
    tipo__in=[TipoCuenta.ACTIVO, TipoCuenta.PASIVO, TipoCuenta.PATRIMONIO]
).select_related('catalogo').order_by('tipo', 'codigo')
```

#### **Paso 4: Construir Estructura de Datos**

```python
# Estructura: Dict con ID de cuenta como key
datos_cuentas = {}
for cuenta in cuentas:
    datos_cuentas[cuenta.id] = {
        'id': cuenta.id,
        'codigo': cuenta.codigo,
        'nombre': cuenta.nombre,
        'tipo': cuenta.tipo,
        'tipo_display': cuenta.get_tipo_display(),
        'montos_por_año': {}  # ← Aquí se llenan los montos
    }
```

#### **Paso 5: Llenar Montos por Año**

```python
# Llenar montos por año para cada cuenta
for estado in estados:
    año = estado.año
    for item in estado.items.all():
        cuenta_id = item.cuenta_contable_id
        if cuenta_id in datos_cuentas:
            datos_cuentas[cuenta_id]['montos_por_año'][año] = item.monto
```

**Resultado**: Cada cuenta tiene un diccionario `{2020: 150000, 2021: 175000, 2022: 200000}`

#### **Paso 6: Calcular Variaciones entre Años Consecutivos**

```python
# Calcular variaciones entre años consecutivos
años_ordenados = sorted(años)
variaciones_info = []

for i in range(len(años_ordenados) - 1):
    año_base = años_ordenados[i]
    año_siguiente = años_ordenados[i + 1]
    variaciones_info.append({
        'año_base': año_base,
        'año_siguiente': año_siguiente,
        'label': f'{año_base}-{año_siguiente}'  # Ej: "2020-2021"
    })
```

**Ejemplo de `variaciones_info`**:
```json
[
    {
        "año_base": 2020,
        "año_siguiente": 2021,
        "label": "2020-2021"
    },
    {
        "año_base": 2021,
        "año_siguiente": 2022,
        "label": "2021-2022"
    }
]
```

#### **Paso 7: Calcular Variaciones por Cuenta**

```python
# Calcular variaciones para cada cuenta
for cuenta_id, datos in datos_cuentas.items():
    datos['variaciones'] = {}
    
    for var_info in variaciones_info:
        año_base = var_info['año_base']
        año_siguiente = var_info['año_siguiente']
        label = var_info['label']
        
        monto_base = datos['montos_por_año'].get(año_base)
        monto_siguiente = datos['montos_por_año'].get(año_siguiente)
        
        if monto_base is not None and monto_siguiente is not None:
            # Variación absoluta: Diferencia simple
            variacion_absoluta = monto_siguiente - monto_base
            
            # Variación porcentual
            if monto_base != 0:
                variacion_porcentual = (variacion_absoluta / abs(monto_base)) * 100
            else:
                variacion_porcentual = None  # División por cero
            
            datos['variaciones'][label] = {
                'variacion_absoluta': variacion_absoluta,
                'variacion_porcentual': variacion_porcentual
            }
```

**Ejemplo de variaciones calculadas**:
```json
{
    "id": 15,
    "codigo": "1101",
    "nombre": "Efectivo y Equivalentes",
    "montos_por_año": {
        2020: 150000,
        2021: 175000,
        2022: 200000
    },
    "variaciones": {
        "2020-2021": {
            "variacion_absoluta": 25000,
            "variacion_porcentual": 16.67
        },
        "2021-2022": {
            "variacion_absoluta": 25000,
            "variacion_porcentual": 14.29
        }
    }
}
```

#### **Paso 8: Organizar Cuentas por Tipo**

```python
# Organizar cuentas por tipo (ACTIVO, PASIVO, PATRIMONIO)
cuentas_por_tipo = {
    TipoCuenta.ACTIVO: [],
    TipoCuenta.PASIVO: [],
    TipoCuenta.PATRIMONIO: []
}

for cuenta_data in datos_cuentas.values():
    tipo = cuenta_data['tipo']
    if tipo in cuentas_por_tipo:
        cuentas_por_tipo[tipo].append(cuenta_data)
```

#### **Paso 9: Retornar JSON Estructurado**

```python
return {
    'success': True,
    'empresa': {
        'id': empresa.id,
        'nombre': empresa.nombre,
        'sector': empresa.sector.nombre
    },
    'años': años_ordenados,
    'variaciones_info': variaciones_info,
    'cuentas_por_tipo': {
        'ACTIVO': cuentas_por_tipo[TipoCuenta.ACTIVO],
        'PASIVO': cuentas_por_tipo[TipoCuenta.PASIVO],
        'PATRIMONIO': cuentas_por_tipo[TipoCuenta.PATRIMONIO]
    }
}
```

---

## 📊 Generación de Gráficas - Frontend

### **Archivo**: `templates/analisis/analisis_financiero.html`

#### **Paso 1: Renderizar Tabla HTML con Botones de Gráfica**

```javascript
function renderizarAnalisisHorizontal(data, tipo) {
    const containerId = tipo === 'balance' 
        ? 'tabla-horizontal-balance' 
        : 'tabla-horizontal-resultados';
    const container = document.getElementById(containerId);
    
    let html = '<table class="tabla-horizontal">';
    
    // Headers de tabla
    html += '<thead><tr>';
    html += '<th class="col-cuenta">Cuenta</th>';
    
    // Columnas de años
    data.años.forEach(año => {
        html += `<th class="col-año">${año}</th>`;
    });
    
    // Columnas de variaciones
    data.variaciones_info.forEach(varInfo => {
        html += `<th class="col-variacion">Variación<br>${varInfo.label}</th>`;
    });
    html += '</tr></thead>';
    
    // Body de la tabla (filas de cuentas)
    html += '<tbody>';
    
    // ... (continúa)
}
```

#### **Paso 2: Botón de Gráfica por Cuenta**

Cada fila de cuenta tiene un botón con data-attribute:

```javascript
// Columna de cuenta con botón de gráfica
const cuentaDataJson = JSON.stringify({
    id: cuenta.id,
    codigo: cuenta.codigo,
    nombre: cuenta.nombre,
    montos: cuenta.montos_por_año  // ← CRÍTICO para la gráfica
}).replace(/"/g, '&quot;');

html += `
    <td class="col-cuenta">
        <button class="btn-graficar" 
                data-cuenta="${cuentaDataJson}" 
                title="Graficar evolución de esta cuenta">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6..." />
            </svg>
        </button>
        <div class="cuenta-info">
            <span class="cuenta-codigo">${cuenta.codigo}</span>
            <span class="cuenta-nombre">${cuenta.nombre}</span>
        </div>
    </td>
`;
```

#### **Paso 3: Event Listener para Gráfica**

```javascript
function agregarEventListenersGrafica(containerId) {
    const container = document.getElementById(containerId);
    const botones = container.querySelectorAll('.btn-graficar');
    
    botones.forEach(boton => {
        boton.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            try {
                // Extraer datos de cuenta desde data-attribute
                const cuentaData = JSON.parse(
                    this.getAttribute('data-cuenta').replace(/&quot;/g, '"')
                );
                
                // Mostrar modal con gráfica
                graficarCuenta(cuentaData);
            } catch (error) {
                console.error('Error al procesar datos:', error);
            }
        });
    });
}
```

#### **Paso 4: Generar Modal con Gráfica**

```javascript
function mostrarModalGrafica(cuentaData) {
    // Obtener años y montos
    const años = [...datosAnalisisActual.años].sort((a, b) => a - b);
    const montos = años.map(año => cuentaData.montos[año] || 0);
    
    // Verificar que haya datos
    if (montos.every(m => m === 0 || m === null)) {
        mostrarAlerta('No hay datos disponibles', 'warning');
        return;
    }
    
    // Crear HTML del modal
    const modalHtml = `
        <div id="modalGrafica" class="modal-grafica-overlay">
            <div class="modal-grafica-content">
                <div class="modal-grafica-header">
                    <h3>${cuentaData.codigo} - ${cuentaData.nombre}</h3>
                    <button id="btnCerrarModalGrafica">X</button>
                </div>
                <div class="modal-grafica-body">
                    <!-- Canvas para Chart.js -->
                    <div class="grafica-chart-container">
                        ${generarGraficaSimple(años, montos, cuentaData.nombre)}
                    </div>
                    
                    <!-- Tabla de datos -->
                    <div class="grafica-datos-tabla">
                        ${generarTablaDatos(años, montos)}
                    </div>
                    
                    <!-- Estadísticas -->
                    <div class="grafica-stats">
                        ${generarEstadisticasCuenta(años, montos)}
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    
    // Animación y event listeners...
}
```

#### **Paso 5: Crear Gráfica con Chart.js**

```javascript
function crearGraficaLineal(canvasId, años, montos, nombreCuenta) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    
    // Determinar color según tendencia
    const tendencia = montos[montos.length - 1] - montos[0];
    const colorLinea = tendencia > 0 
        ? 'rgb(16, 185, 129)'    // Verde (positivo)
        : tendencia < 0 
            ? 'rgb(239, 68, 68)'  // Rojo (negativo)
            : 'rgb(107, 114, 128)'; // Gris (neutral)
    
    const colorFondo = tendencia > 0 
        ? 'rgba(16, 185, 129, 0.1)'  // Verde claro
        : tendencia < 0 
            ? 'rgba(239, 68, 68, 0.1)'  // Rojo claro
            : 'rgba(107, 114, 128, 0.1)'; // Gris claro
    
    // Crear instancia de Chart.js
    new Chart(ctx, {
        type: 'line',  // ← Gráfica de línea
        data: {
            labels: años,  // [2020, 2021, 2022]
            datasets: [{
                label: 'Monto (USD)',
                data: montos,  // [150000, 175000, 200000]
                borderColor: colorLinea,
                backgroundColor: colorFondo,
                borderWidth: 3,
                fill: true,  // Rellenar área bajo la línea
                tension: 0.4,  // Curva suave (0 = líneas rectas)
                pointRadius: 6,
                pointHoverRadius: 8,
                pointBackgroundColor: colorLinea,
                pointBorderColor: '#fff',
                pointBorderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: { display: false },
                title: {
                    display: true,
                    text: `Evolución de ${nombreCuenta}`,
                    font: { size: 16, weight: 'bold' }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            let label = 'Monto: ';
                            label += formatearMonto(context.parsed.y);
                            
                            // Agregar variación porcentual
                            if (context.dataIndex > 0) {
                                const actual = context.parsed.y;
                                const anterior = montos[context.dataIndex - 1];
                                if (anterior !== 0) {
                                    const variacion = ((actual - anterior) / Math.abs(anterior) * 100).toFixed(2);
                                    label += ` (${variacion >= 0 ? '+' : ''}${variacion}%)`;
                                }
                            }
                            
                            return label;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    ticks: {
                        callback: function(value) {
                            return '$' + value.toLocaleString('es-SV');
                        }
                    },
                    title: {
                        display: true,
                        text: 'Monto (USD)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Año'
                    }
                }
            }
        }
    });
}
```

#### **Configuración de Chart.js**:

| Propiedad | Valor | Descripción |
|-----------|-------|-------------|
| `type` | `'line'` | Gráfica de línea (evolución temporal) |
| `tension` | `0.4` | Curva suave (0-1, donde 0 = recta) |
| `fill` | `true` | Rellena área bajo la línea |
| `borderWidth` | `3` | Grosor de la línea |
| `pointRadius` | `6` | Tamaño de los puntos |
| `beginAtZero` | `false` | No fuerza Y=0 (mejor para montos grandes) |

---

## 📦 Estructura de Datos JSON

### **Respuesta del Backend** (`analizar_balance_general()`)

```json
{
    "success": true,
    "empresa": {
        "id": 1,
        "nombre": "Banco Agrícola",
        "sector": "Bancario"
    },
    "años": [2020, 2021, 2022],
    "variaciones_info": [
        {
            "año_base": 2020,
            "año_siguiente": 2021,
            "label": "2020-2021"
        },
        {
            "año_base": 2021,
            "año_siguiente": 2022,
            "label": "2021-2022"
        }
    ],
    "cuentas_por_tipo": {
        "ACTIVO": [
            {
                "id": 15,
                "codigo": "1101",
                "nombre": "Efectivo y Equivalentes",
                "tipo": "ACTIVO",
                "tipo_display": "Activo",
                "montos_por_año": {
                    "2020": "150000.00",
                    "2021": "175000.00",
                    "2022": "200000.00"
                },
                "variaciones": {
                    "2020-2021": {
                        "variacion_absoluta": "25000.00",
                        "variacion_porcentual": 16.67
                    },
                    "2021-2022": {
                        "variacion_absoluta": "25000.00",
                        "variacion_porcentual": 14.29
                    }
                }
            },
            {
                "id": 16,
                "codigo": "1102",
                "nombre": "Inversiones",
                "montos_por_año": {
                    "2020": "500000.00",
                    "2021": "450000.00",
                    "2022": "480000.00"
                },
                "variaciones": {
                    "2020-2021": {
                        "variacion_absoluta": "-50000.00",
                        "variacion_porcentual": -10.00
                    },
                    "2021-2022": {
                        "variacion_absoluta": "30000.00",
                        "variacion_porcentual": 6.67
                    }
                }
            }
        ],
        "PASIVO": [...],
        "PATRIMONIO": [...]
    }
}
```

### **Datos de Gráfica (data-cuenta)**

```json
{
    "id": 15,
    "codigo": "1101",
    "nombre": "Efectivo y Equivalentes",
    "montos": {
        "2020": 150000,
        "2021": 175000,
        "2022": 200000
    }
}
```

---

## 🎨 Componentes Visuales

### **1. Tabla de Análisis Horizontal**

```css
.tabla-horizontal {
    width: 100%;
    border-collapse: collapse;
    background: var(--color-surface);
    font-size: var(--font-size-sm);
}

.tabla-horizontal tbody tr:hover {
    background: rgba(99, 102, 241, 0.02);
}
```

**Estructura de columnas**:
1. **Cuenta** (código + nombre + botón gráfica)
2. **Año 1** (monto)
3. **Año 2** (monto)
4. **Año N** (monto)
5. **Variación 1-2** (% y monto absoluto)
6. **Variación 2-3** (% y monto absoluto)

### **2. Botón de Gráfica**

```html
<button class="btn-graficar" data-cuenta="{...}">
    <svg viewBox="0 0 24 24">
        <!-- Ícono de barras -->
    </svg>
</button>
```

```css
.btn-graficar {
    background: transparent;
    border: none;
    padding: 6px;
    cursor: pointer;
    border-radius: var(--radius-sm);
    transition: all 0.2s ease;
}

.btn-graficar:hover {
    background: rgba(99, 102, 241, 0.1);
}
```

### **3. Modal de Gráfica**

```css
.modal-grafica-overlay {
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 10000;
}

.modal-grafica-content {
    background: var(--color-surface);
    border-radius: var(--radius-lg);
    width: 100%;
    max-width: 900px;
    max-height: 90vh;
    overflow: hidden;
}
```

### **4. Canvas de Chart.js**

```html
<div class="grafica-chart-container">
    <canvas id="chartCanvas_1234567890" style="max-height: 400px;"></canvas>
</div>
```

### **5. Tabla de Datos**

```html
<table class="tabla-datos-grafica">
    <thead>
        <tr>
            <th>Año</th>
            <th>Monto</th>
            <th>Variación</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td class="td-año">2020</td>
            <td class="td-monto">$150,000.00</td>
            <td class="td-variacion">-</td>
        </tr>
        <tr>
            <td class="td-año">2021</td>
            <td class="td-monto">$175,000.00</td>
            <td class="td-variacion">
                <span class="variacion-valor positiva">+16.67%</span>
            </td>
        </tr>
    </tbody>
</table>
```

### **6. Tarjetas de Estadísticas**

```html
<div class="stats-grid">
    <div class="stat-card">
        <div class="stat-label">Promedio</div>
        <div class="stat-value">$175,000.00</div>
    </div>
    <div class="stat-card">
        <div class="stat-label">Máximo</div>
        <div class="stat-value">$200,000.00</div>
    </div>
    <div class="stat-card">
        <div class="stat-label">Mínimo</div>
        <div class="stat-value">$150,000.00</div>
    </div>
    <div class="stat-card">
        <div class="stat-label">Variación Total</div>
        <div class="stat-value positiva">+33.33%</div>
    </div>
</div>
```

```javascript
function generarEstadisticasCuenta(años, montos) {
    const montosValidos = montos.filter(m => m !== null && m !== undefined);
    const promedio = montosValidos.reduce((a, b) => a + b, 0) / montosValidos.length;
    const maximo = Math.max(...montosValidos);
    const minimo = Math.min(...montosValidos);
    const variacionTotal = ((montosValidos[montosValidos.length - 1] - montosValidos[0]) 
        / Math.abs(montosValidos[0]) * 100);
    
    return `<!-- HTML de tarjetas -->`;
}
```

---

## ⚠️ Puntos Críticos y Consideraciones

### **1. Chart.js NO está cargado en el template base**

❌ **Problema actual**: `templates/dashboard/base.html` **NO incluye Chart.js**.

✅ **Solución necesaria**: Agregar en `analisis_financiero.html`:

```html
{% block extra_js %}
<!-- Chart.js CDN -->
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>

<!-- Código JavaScript del análisis -->
<script>
    // ... todo el código de análisis ...
</script>
{% endblock %}
```

**Confirmación**: El template `proyecciones/proyeccion_resultados.html` SÍ carga Chart.js:
```html
<!-- Chart.js -->
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
```

### **2. Conversión de Decimal a Float**

⚠️ **Problema**: Django Decimal no es serializable a JSON.

✅ **Solución implementada**:

```python
def convertir_decimales(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, dict):
        return {key: convertir_decimales(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convertir_decimales(item) for item in obj]
    return obj
```

```python
# En las vistas
resultado_convertido = convertir_decimales(resultado)
return JsonResponse(resultado_convertido)
```

### **3. Prevención de Errores de División por Cero**

```python
# Calcular variación porcentual
if monto_base != 0:
    variacion_porcentual = (variacion_absoluta / abs(monto_base)) * 100
else:
    variacion_porcentual = None  # ← Evita división por cero
```

### **4. Manejo de Datos Faltantes**

```javascript
// Verificar que haya datos antes de graficar
if (montos.every(m => m === 0 || m === null || m === undefined)) {
    mostrarAlerta('No hay datos disponibles para graficar esta cuenta', 'warning');
    return;
}
```

### **5. Optimización de Queries (N+1)**

```python
# ✅ CORRECTO: Usa prefetch_related
estados = EstadoFinanciero.objects.filter(
    empresa=empresa,
    año__in=años,
    tipo=TipoEstadoFinanciero.BALANCE_GENERAL
).prefetch_related('items__cuenta_contable').order_by('año')

# ❌ INCORRECTO: Generaría N+1 queries
estados = EstadoFinanciero.objects.filter(...)
for estado in estados:
    for item in estado.items.all():  # ← Query por cada estado
        ...
```

### **6. IDs Únicos para Canvas**

```javascript
// Generar ID único para evitar conflictos
const canvasId = 'chartCanvas_' + Date.now();
const html = `<canvas id="${canvasId}"></canvas>`;

// Crear gráfica después de que el DOM esté listo
setTimeout(() => {
    crearGraficaLineal(canvasId, años, montos, nombreCuenta);
}, 100);
```

### **7. Cierre de Modal con ESC**

```javascript
// Cerrar con tecla ESC
document.addEventListener('keydown', function escHandler(e) {
    if (e.key === 'Escape') {
        cerrarModalGrafica();
        document.removeEventListener('keydown', escHandler);  // ← Remover listener
    }
});
```

### **8. Colores Dinámicos según Tendencia**

```javascript
// Calcular tendencia general
const tendencia = montos[montos.length - 1] - montos[0];

const colorLinea = tendencia > 0 
    ? 'rgb(16, 185, 129)'    // Verde → Aumento
    : tendencia < 0 
        ? 'rgb(239, 68, 68)'  // Rojo → Disminución
        : 'rgb(107, 114, 128)'; // Gris → Sin cambio
```

### **9. Formato de Moneda**

```javascript
function formatearMonto(monto) {
    if (monto === null || monto === undefined) return 'N/A';
    const num = parseFloat(monto);
    return new Intl.NumberFormat('es-SV', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    }).format(num);
}

// Resultado: "$150,000.00"
```

### **10. Validación de Años Mínimos**

```javascript
// Análisis horizontal requiere al menos 2 años
if (datosAnalisisActual.años.length < 2) {
    mostrarAlerta('Se necesitan al menos 2 años para el análisis horizontal.', 'warning');
    return;
}
```

---

## 📊 Diagrama de Flujo

```
┌─────────────────────────────────────────────────────────────────┐
│                   INICIO: Usuario en Dashboard                   │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ↓
┌─────────────────────────────────────────────────────────────────┐
│  1. Seleccionar Empresa y Años (mínimo 2 para horizontal)       │
│     - Empresa: "Banco Agrícola"                                  │
│     - Años: [2020, 2021, 2022]                                   │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ↓
┌─────────────────────────────────────────────────────────────────┐
│  2. Submit Formulario → ValidarEstadosView (POST)                │
│     URL: /analisis/validar-estados/                              │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ↓
                       ┌────────┴────────┐
                       │  ¿Estados       │
                       │  válidos?       │
                       └────────┬────────┘
                                │
                    ┌───────────┴───────────┐
                    │ NO                   │ SÍ
                    ↓                       ↓
         ┌──────────────────┐   ┌──────────────────────────┐
         │ Mostrar error    │   │ Calcular Ratios          │
         │ y terminar       │   │ Renderizar tabla inicial │
         └──────────────────┘   └───────────┬──────────────┘
                                            │
                                            ↓
┌─────────────────────────────────────────────────────────────────┐
│  3. Usuario cambia a pestaña "Análisis Horizontal"              │
│     Event: tab-button click                                      │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ↓
┌─────────────────────────────────────────────────────────────────┐
│  4. Llamada AJAX → AnalisisHorizontalBalanceView (POST)          │
│     URL: /analisis/analisis-horizontal/balance/                  │
│     Datos: empresa_id, años[]                                    │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ↓
┌─────────────────────────────────────────────────────────────────┐
│  5. Backend: AnalizadorHorizontal.analizar_balance_general()     │
│     - Obtener estados financieros (prefetch)                     │
│     - Extraer cuentas y montos por año                           │
│     - Calcular variaciones absolutas y porcentuales              │
│     - Organizar por tipo (ACTIVO, PASIVO, PATRIMONIO)           │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ↓
┌─────────────────────────────────────────────────────────────────┐
│  6. Frontend: renderizarAnalisisHorizontal(data, 'balance')      │
│     - Generar HTML de tabla                                      │
│     - Agregar botón "Graficar" por cada cuenta                   │
│     - data-cuenta = {id, codigo, nombre, montos}                 │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ↓
┌─────────────────────────────────────────────────────────────────┐
│  7. Usuario hace clic en botón "Graficar" de una cuenta         │
│     Event: btn-graficar click                                    │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ↓
┌─────────────────────────────────────────────────────────────────┐
│  8. Extraer datos de data-cuenta attribute                       │
│     cuentaData = {                                               │
│       id: 15,                                                    │
│       codigo: "1101",                                            │
│       nombre: "Efectivo y Equivalentes",                         │
│       montos: {2020: 150000, 2021: 175000, 2022: 200000}        │
│     }                                                            │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ↓
┌─────────────────────────────────────────────────────────────────┐
│  9. Preparar datos para gráfica                                  │
│     años = [2020, 2021, 2022]                                    │
│     montos = [150000, 175000, 200000]                            │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ↓
                       ┌────────┴────────┐
                       │  ¿Hay datos     │
                       │  válidos?       │
                       └────────┬────────┘
                                │
                    ┌───────────┴───────────┐
                    │ NO                   │ SÍ
                    ↓                       ↓
         ┌──────────────────┐   ┌──────────────────────────┐
         │ Mostrar alerta   │   │ Generar HTML de modal    │
         │ "Sin datos"      │   │ con canvas + tabla       │
         └──────────────────┘   └───────────┬──────────────┘
                                            │
                                            ↓
┌─────────────────────────────────────────────────────────────────┐
│  10. Insertar modal en DOM y mostrar con animación              │
│      - Modal overlay + content                                   │
│      - Header (título + botón cerrar)                            │
│      - Body (canvas + tabla + stats)                             │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ↓
┌─────────────────────────────────────────────────────────────────┐
│  11. Ejecutar crearGraficaLineal(canvasId, años, montos)        │
│      - Determinar color según tendencia (verde/rojo/gris)       │
│      - Crear instancia de Chart.js                              │
│      - type: 'line'                                              │
│      - data: {labels: años, datasets: [{data: montos}]}         │
│      - options: tooltips, scales, plugins                       │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ↓
┌─────────────────────────────────────────────────────────────────┐
│  12. Chart.js renderiza la gráfica en el canvas                  │
│      - Línea con color dinámico                                  │
│      - Puntos en cada año                                        │
│      - Área rellena bajo la línea                                │
│      - Tooltips con variación porcentual                         │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ↓
┌─────────────────────────────────────────────────────────────────┐
│  13. Generar tabla de datos y estadísticas                       │
│      Tabla:                                                      │
│      - Año | Monto | Variación %                                │
│      Estadísticas:                                               │
│      - Promedio, Máximo, Mínimo, Variación Total                │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ↓
┌─────────────────────────────────────────────────────────────────┐
│  14. Usuario interactúa con modal                                │
│      - Hover sobre puntos → tooltip con info                     │
│      - Click en "X" o ESC → cerrarModalGrafica()                │
│      - Click fuera del contenido → cerrar modal                  │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ↓
┌─────────────────────────────────────────────────────────────────┐
│  15. Cerrar modal con animación y remover del DOM               │
│      - modal.classList.remove('active')                          │
│      - setTimeout(() => modal.remove(), 300)                     │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ↓
                        ┌───────────────┐
                        │  FIN          │
                        └───────────────┘
```

---

## 🔍 Resumen de Archivos Clave

| Archivo | Propósito | Elementos Clave |
|---------|-----------|-----------------|
| `apps/analisis/views.py` | Vistas CBV | `AnalisisHorizontalBalanceView`, `AnalisisHorizontalResultadosView` |
| `apps/analisis/servicios/analisis_horizontal.py` | Lógica de negocio | `AnalizadorHorizontal.analizar_balance_general()` |
| `apps/analisis/models.py` | Modelo de BD | `ValorRatioCalculado` (para ratios, NO para análisis horizontal) |
| `apps/estados/models.py` | Modelos de datos | `EstadoFinanciero`, `ItemEstadoFinanciero` |
| `templates/analisis/analisis_financiero.html` | UI y JavaScript | Tabs, tabla, modal, Chart.js |
| `templates/dashboard/base.html` | Template base | Sidebar, header, estructura |

---

## 📝 Conclusiones

1. **Flujo completo**: Backend calcula → Frontend renderiza → Usuario grafica
2. **Chart.js 4.4.0**: Biblioteca para gráficas (CDN, NO incluida en base template)
3. **Datos JSON**: Backend retorna estructura con montos y variaciones
4. **Modal dinámico**: Gráfica + tabla + estadísticas generadas en JavaScript
5. **Colores dinámicos**: Verde (aumento), rojo (disminución), gris (neutral)
6. **Optimización**: Prefetch para evitar N+1, conversión Decimal → float
7. **Interactividad**: Tooltips con variación %, cierre con ESC, animaciones CSS
8. **Validación**: Mínimo 2 años, verificación de datos, división por cero

---

**Fecha de Análisis**: 11 de noviembre de 2025  
**Versión del Sistema**: Django 5.2 + Chart.js 4.4.0  
**Documentado por**: GitHub Copilot
