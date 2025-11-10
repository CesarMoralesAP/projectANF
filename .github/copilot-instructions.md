# Instrucciones de Copilot para ProjectANF

## Resumen del Proyecto
Sistema Django de análisis financiero para la Universidad de El Salvador. Permite a usuarios gestionar catálogos de cuentas contables, ingresar estados financieros (Balance General y Estado de Resultados), calcular ratios financieros automáticamente y comparar empresas contra benchmarks sectoriales.

**Stack**: Django 5.2 + MySQL 8.x + Bootstrap 5 + Python 3.11+

## Arquitectura Core

### Estructura Modular de Apps
El proyecto usa una arquitectura de **múltiples apps Django** donde cada app representa un dominio funcional:

- **`apps/empresas/`**: Sectores económicos y empresas
- **`apps/catalogos/`**: Catálogos de cuentas contables, ratios financieros y mapeos cuenta-ratio
- **`apps/estados/`**: Estados financieros (Balance General / Estado de Resultados) con ítems detallados
- **`apps/parametros/`**: Benchmarks sectoriales de ratios (valores óptimos por sector)
- **`apps/usuarios/`**: Autenticación (usa `django.contrib.auth` estándar)
- **`apps/core/`**: Modelo base abstracto `ModeloBase` con `creado_en` y `actualizado_en`

### Relaciones Clave entre Modelos

```
Empresa (1) ←→ (1) CatalogoCuenta ←→ (N) CuentaContable
                                           ↓ (N)
                                  ItemEstadoFinanciero ←→ (N:1) EstadoFinanciero
```

- **Una empresa tiene UN SOLO catálogo** (`OneToOneField` en `CatalogoCuenta.empresa`)
- Cada `CuentaContable` pertenece a UN catálogo específico (cuenta-empresa-específica)
- `EstadoFinanciero` tiene `unique_together = [['empresa', 'año', 'tipo']]` - solo un estado por empresa/año/tipo
- `MapeoCuentaRatio` vincula cuentas contables específicas de una empresa a componentes genéricos de ratios

### Patrón de Servicios
La lógica de negocio NO va en views. Se encapsula en módulos `servicios/`:

**Ejemplo**: `apps/estados/servicios/procesar_excel_estado.py` maneja la carga masiva de estados financieros desde Excel.

```python
# Incorrecto ❌
class MiView(View):
    def post(self, request):
        # 50 líneas de lógica de negocio aquí...

# Correcto ✅
# En servicios/mi_servicio.py
class MiServicio:
    @staticmethod
    def procesar_datos(datos):
        # Lógica aquí

# En views.py
class MiView(View):
    def post(self, request):
        resultado = MiServicio.procesar_datos(data)
```

## Convenciones Críticas

### Nomenclatura (100% Español)
- **Variables/funciones**: `snake_case` → `obtener_empresas_por_sector()`
- **Clases**: `PascalCase` → `CalculadoraRatios`, `EstadoFinanciero`
- **Constantes**: `SCREAMING_SNAKE_CASE` → `MAX_EMPRESAS_COMPARACION`
- **Archivos**: `snake_case.py` → `procesar_excel_estado.py`
- **Templates**: `snake_case.html` → `estado_financiero.html`

**Nunca mezcles inglés/español** en el mismo identificador.

### Modelos y Base de Datos
- Todos los modelos heredan de `apps.core.models.ModeloBase` (proporciona `creado_en`, `actualizado_en`)
- Usa `db_table` explícito: `class Meta: db_table = 'sector'`
- Usa `select_related()` y `prefetch_related()` para evitar N+1 queries:

```python
# ❌ N+1 queries
empresas = Empresa.objects.all()
for e in empresas:
    print(e.sector.nombre)  # Query por cada empresa

# ✅ Una sola query con JOIN
empresas = Empresa.objects.select_related('sector').all()
```

- Validaciones van en `Model.clean()` y siempre llama `full_clean()` antes de `save()`

### Class-Based Views (CBV)
El proyecto usa **CBVs exclusivamente**. Nunca crees function-based views.

Patrón típico:
```python
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

class MiVistaView(LoginRequiredMixin, TemplateView):
    template_name = 'app/template.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Añadir datos al contexto
        return context
```

Para operaciones POST/DELETE, usa `View` con decorador `@method_decorator(require_http_methods([...]))`:

```python
from django.views import View
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator

@method_decorator(require_http_methods(["POST"]), name='dispatch')
class GuardarDatosView(LoginRequiredMixin, View):
    def post(self, request):
        # Lógica aquí
        return JsonResponse({'success': True})
```

### Manejo de Errores y Mensajes
Usa `django.contrib.messages` para feedback al usuario:

```python
from django.contrib import messages

messages.success(request, 'Operación exitosa')
messages.error(request, f'Error: {e}')
messages.warning(request, 'Advertencia importante')
```

En APIs JSON, retorna estructura consistente:
```python
return JsonResponse({
    'success': True/False,
    'message': 'Descripción',
    'data': {...}  # Opcional
})
```

### Transacciones Atómicas
Para operaciones complejas que modifican múltiples tablas, usa `transaction.atomic()`:

```python
from django.db import transaction

with transaction.atomic():
    estado = EstadoFinanciero.objects.create(...)
    for item_data in items:
        ItemEstadoFinanciero.objects.create(estado_financiero=estado, ...)
```

## Workflows Específicos del Proyecto

### Carga Masiva desde Excel
El proyecto tiene dos flujos de carga Excel:

1. **Catálogos de Cuentas** (`apps/catalogos/utils.py`):
   - `generar_plantilla_excel()` genera plantilla con headers específicos
   - `procesar_excel()` **REEMPLAZA** todas las cuentas del catálogo (elimina existentes)
   - Headers esperados: `['Código de la cuenta', 'Nombre de la cuenta', 'Tipo de cuenta']`

2. **Estados Financieros** (`apps/estados/servicios/`):
   - `generar_plantilla_excel_estado(catalogo, tipo_estado)` genera plantilla personalizada por empresa
   - `procesar_excel_estado(archivo, empresa, año, tipo)` crea/actualiza estado financiero
   - La plantilla incluye SOLO las cuentas del catálogo de la empresa seleccionada

### Mapeo de Ratios Financieros
El sistema tiene una arquitectura de 3 capas para ratios:

1. **`RatioFinanciero`**: Definición genérica (ej. "Razón Corriente")
2. **`ComponenteRatio`**: Elementos de la fórmula (ej. "Activo Corriente", "Pasivo Corriente")
3. **`MapeoCuentaRatio`**: Mapeo específico por empresa que vincula componentes a cuentas reales del catálogo

**Ejemplo**: Para calcular "Razón Corriente" de Banco Agrícola, el sistema busca qué cuenta específica de su catálogo mapearon a "Activo Corriente".

### Validación de Estados Financieros
- `EstadoFinanciero` valida `unique_together` en `clean()` antes de guardar
- `ItemEstadoFinanciero.clean()` verifica que la cuenta pertenezca al catálogo de la empresa
- Tipos de cuenta se filtran por tipo de estado:
  - **Balance General**: `ACTIVO`, `PASIVO`, `PATRIMONIO`
  - **Estado de Resultados**: `INGRESO`, `GASTO`, `RESULTADO`

## Comandos de Desarrollo

### Setup Inicial
```bash
# Crear entorno virtual (Windows PowerShell)
python -m venv venv
venv\Scripts\Activate.ps1

# Instalar dependencias
python -m pip install -r requirements.txt

# Variables de entorno (.env requerido)
DB_NAME=projectanf
DB_USER=root
DB_PASSWORD=tu_contraseña
DB_HOST=127.0.0.1
DB_PORT=3306
```

### Migraciones y Base de Datos
```bash
python manage.py migrate
python manage.py createsuperuser
```

### Comandos de Datos Demo
```bash
python manage.py crear_usuarios_demo   # Crea usuarios de prueba
python manage.py crear_datos_demo      # Crea sectores, empresas
python manage.py crear_ratios_demo     # Crea ratios financieros predefinidos
```

### Ejecutar Servidor
```bash
python manage.py runserver
# URL: http://127.0.0.1:8000
# Login URL: http://127.0.0.1:8000/usuarios/login/
```

## Patrones de Templates

### Componentes Reutilizables
El proyecto usa componentes en `templates/componentes/`:

```django
{% include 'componentes/alerta.html' with mensaje=mensaje tipo='success' %}
{% include 'componentes/modal_confirmacion.html' with titulo='Eliminar' %}
```

**⚠️ IMPORTANTE - Reutilización de Componentes**:
- **SIEMPRE verifica primero** si ya existe un componente en `templates/componentes/` antes de crear uno nuevo
- Componentes existentes: `alerta.html`, `modal_confirmacion.html`
- Si necesitas un modal o alerta, **reutiliza los existentes** pasando parámetros diferentes
- Solo crea componentes nuevos si la funcionalidad es completamente diferente y no se puede adaptar

### CSS Variables (Design System)
En `static/css/variables.css`:
```css
--color-primary: #6366F1;  /* Violeta - Botones principales */
--color-background: #F5F5F7;
--spacing-md: 16px;
--radius-md: 12px;
```

Usa estas variables en lugar de valores hard-coded.

## Testing y Debugging

### Queries SQL Lentas
Activa el debug toolbar o usa:
```python
from django.db import connection
print(connection.queries)  # Imprime todas las queries ejecutadas
```

### Common Pitfalls
1. **No olvides llamar `full_clean()`** antes de `save()` en modelos con validaciones custom
2. **Siempre usa `get_object_or_404`** en lugar de `Model.objects.get()` en views
3. **Verifica existencia de catálogo** antes de intentar acceder a `empresa.catalogo_cuenta`:
   ```python
   try:
       catalogo = CatalogoCuenta.objects.get(empresa=empresa)
   except CatalogoCuenta.DoesNotExist:
       messages.error(request, 'Empresa sin catálogo configurado')
   ```

## URLs y Routing
- **URL principal**: `core/urls.py` incluye apps con `include()`
- **Login redirect**: `LOGIN_REDIRECT_URL = 'empresas:empresa_lista'`
- **Namespace pattern**: `path('estados/', include('apps.estados.urls', namespace='estados'))`

Algunas apps tienen subdirectorios `urls/` para organizar múltiples archivos de URLs.

## Configuración Específica

### MySQL Connector
Usa `mysql.connector.django` (no `django.db.backends.mysql`):
```python
DATABASES = {
    'default': {
        'ENGINE': 'mysql.connector.django',
        # ...
    }
}
```

### Sesiones
```python
SESSION_COOKIE_AGE = 86400  # 24 horas
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
```

### Archivos Estáticos
- `STATIC_URL = '/static/'`
- `STATICFILES_DIRS = [BASE_DIR / 'static']`
- Templates globales en `templates/` (configurado en `settings.TEMPLATES.DIRS`)

## Principios de Desarrollo

### 🔄 Reutilización Primero
**Antes de crear cualquier cosa nueva, pregúntate**:
1. ¿Ya existe un componente, función o clase similar que pueda reutilizar?
2. ¿Puedo adaptar código existente con parámetros adicionales?
3. ¿Esta funcionalidad ya está implementada en otra app?

**Checklist de reutilización**:
- 📁 Componentes de template: revisa `templates/componentes/`
- 🔧 Utilidades: revisa `apps/core/utilidades.py`
- 🎨 Estilos: revisa `static/css/components.css` y `variables.css`
- 📊 Servicios: busca en `apps/*/servicios/` antes de duplicar lógica

### 💡 Simplicidad y Claridad
**Prioriza código simple sobre código "elegante"**:

```python
# ✅ Simple y claro
def calcular_total(valores):
    total = 0
    for valor in valores:
        total += valor
    return total

# ❌ Rebuscado e innecesario
def calcular_total(valores):
    return reduce(lambda x, y: x + y, map(lambda v: v, valores), 0)
```

**Principios**:
- Código legible > Código "inteligente"
- Soluciones directas > Abstracciones complejas innecesarias
- Si necesitas comentar mucho, simplifica el código
- Un desarrollador nuevo debe entender la lógica en menos de 1 minuto

## Anti-Patrones a Evitar
❌ Lógica de negocio en views (usa servicios)  
❌ Duplicar código entre apps (centraliza en `apps/core/`)  
❌ Crear componentes nuevos sin verificar si ya existen  
❌ Hard-coding de valores mágicos (usa constantes o configuración)  
❌ Queries sin `select_related`/`prefetch_related` en loops  
❌ Excepciones genéricas sin logging específico  
❌ Mezclar español/inglés en nombres  
❌ Soluciones complejas cuando hay alternativas simples  
❌ Código "elegante" que sacrifica legibilidad  

## Recursos Adicionales
- **README.md**: Instrucciones completas de instalación y setup de base de datos
- **setupcursor.cursorrules**: Guía detallada de diseño UI/UX, paleta de colores, y arquitectura base de datos
- **requirements.txt**: Dependencias específicas (Django 5.2.8, mysql-connector-python, openpyxl, pandas)

---

**Última actualización**: Generado automáticamente el 10 de noviembre de 2025
