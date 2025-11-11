# 🚀 Inicio Rápido - Datos Demo (ACTUALIZADO)

## ⭐ NUEVO: Crear datos de AMBOS bancos con un solo comando

```bash
# Activar entorno virtual (si no está activado)
.\venv\Scripts\Activate.ps1

# Crear datos de Banco Agrícola Y Banco Atlántida con un solo comando
python manage.py crear_todos_los_bancos_demo
```

**¡Eso es todo!** Este comando crea automáticamente datos para **2 bancos**:

### 🏦 Banco Agrícola
- ✅ 50 cuentas contables
- ✅ 3 Balances Generales (2022-2024)
- ✅ 3 Estados de Resultados (2022-2024)
- ✅ 13 mapeos de ratios

### 🏦 Banco Atlántida
- ✅ 50 cuentas contables
- ✅ 3 Balances Generales (2022-2024)
- ✅ 3 Estados de Resultados (2022-2024)
- ✅ 13 mapeos de ratios

### 📈 Compartido
- ✅ 6 ratios financieros predefinidos

---

## Crear datos de un banco específico

### Solo Banco Agrícola
```bash
python manage.py crear_datos_completos_banco_agricola
```

### Solo Banco Atlántida
```bash
python manage.py crear_datos_completos_banco_atlantida
```

---

## Comandos Individuales (opcional)

### Para Banco Agrícola
```bash
python manage.py crear_ratios_demo
python manage.py crear_catalogo_banco_agricola
python manage.py crear_estados_banco_agricola
python manage.py crear_mapeos_banco_agricola
```

### Para Banco Atlántida
```bash
python manage.py crear_ratios_demo
python manage.py crear_catalogo_banco_atlantida
python manage.py crear_estados_banco_atlantida
python manage.py crear_mapeos_banco_atlantida
```

---

## Comparación de Datos Financieros

### Banco Agrícola vs Banco Atlántida (2024)

| Concepto         | Banco Agrícola | Banco Atlántida | Diferencia |
|------------------|----------------|-----------------|------------|
| Total Activo     | $16,945,000    | $26,240,000     | +55%       |
| Total Pasivo     | $14,870,000    | $23,560,000     | +58%       |
| Patrimonio       | $2,075,000     | $2,680,000      | +29%       |
| Utilidad Neta    | $1,022,000     | $1,519,000      | +49%       |

**Banco Atlántida** es aproximadamente **50% más grande** que Banco Agrícola, lo que permite comparaciones realistas entre instituciones de diferentes tamaños.

---

## Verificar datos creados

```bash
python manage.py shell
```

```python
from apps.empresas.models import Empresa
from apps.estados.models import EstadoFinanciero

# Ver ambas empresas
for banco in Empresa.objects.filter(sector__nombre='Bancario'):
    print(f"\n🏦 {banco.nombre}")
    print(f"  Catálogo: {banco.catalogo_cuenta.cuentas.count()} cuentas")
    estados = EstadoFinanciero.objects.filter(empresa=banco)
    print(f"  Estados: {estados.count()}")
    for estado in estados:
        print(f"    - {estado}")
```

---

## Acceder desde el navegador

1. Inicia el servidor:
   ```bash
   python manage.py runserver
   ```

2. Accede a: http://127.0.0.1:8000

3. Navega a:
   - **Empresas**: Ver Banco Agrícola y Banco Atlántida
   - **Catálogos**: Ver cuentas contables de cada banco
   - **Estados**: Ver estados financieros comparativos
   - **Análisis**: Comparar ratios entre ambos bancos

---

## Recrear datos

Los comandos son **idempotentes**: puedes ejecutarlos múltiples veces.

```bash
# Recrear todo desde cero
python manage.py crear_todos_los_bancos_demo
```

---

## Casos de Uso Habilitados

Con dos bancos puedes:

1. ✅ **Comparar rendimiento** entre bancos de diferentes tamaños
2. ✅ **Analizar tendencias** sectoriales
3. ✅ **Calcular promedios** del sector bancario
4. ✅ **Benchmark de ratios** entre competidores
5. ✅ **Visualizar diferencias** en estructura financiera
6. ✅ **Evaluar posicionamiento** relativo en el mercado

---

## Documentación Completa

- **DATOS_DEMO.md**: Guía técnica completa (Banco Agrícola)
- **DATOS_DEMO_ATLANTIDA.md**: Guía técnica de Banco Atlántida
- **RESUMEN_DATOS_DEMO.md**: Resumen visual de todos los datos
- **INICIO_RAPIDO.md**: Este archivo (inicio rápido)

---

## Comandos Disponibles

| Comando | Descripción |
|---------|-------------|
| `crear_todos_los_bancos_demo` | ⭐ Crea datos de ambos bancos |
| `crear_datos_completos_banco_agricola` | Crea datos de Banco Agrícola |
| `crear_datos_completos_banco_atlantida` | Crea datos de Banco Atlántida |
| `crear_ratios_demo` | Crea ratios financieros |
| `crear_catalogo_banco_agricola` | Catálogo de Banco Agrícola |
| `crear_estados_banco_agricola` | Estados de Banco Agrícola |
| `crear_mapeos_banco_agricola` | Mapeos de Banco Agrícola |
| `crear_catalogo_banco_atlantida` | Catálogo de Banco Atlántida |
| `crear_estados_banco_atlantida` | Estados de Banco Atlántida |
| `crear_mapeos_banco_atlantida` | Mapeos de Banco Atlántida |

---

¡Listo para empezar con 2 bancos! 🎉
