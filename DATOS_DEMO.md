# Comandos de Gestión - Datos Demo de Banco Agrícola

Este directorio contiene comandos de gestión de Django para crear datos de demostración completos para Banco Agrícola.

## Comandos Disponibles

### 1. `crear_ratios_demo`
Crea los ratios financieros predefinidos del sistema (Liquidez, Endeudamiento, Rentabilidad).

**Ubicación**: `apps/catalogos/management/commands/crear_ratios_demo.py`

```bash
python manage.py crear_ratios_demo
```

**Crea**:
- 6 ratios financieros (Razón Corriente, Prueba Ácida, Ratio de Endeudamiento, Cobertura de Intereses, ROE, ROA)
- Sus componentes correspondientes

### 2. `crear_catalogo_banco_agricola`
Crea el catálogo de cuentas contables completo para Banco Agrícola.

**Ubicación**: `apps/catalogos/management/commands/crear_catalogo_banco_agricola.py`

```bash
python manage.py crear_catalogo_banco_agricola
```

**Crea**:
- Sector "Bancario"
- Empresa "Banco Agrícola"
- Catálogo de cuentas con ~50 cuentas contables organizadas en:
  - Activos (Corrientes y No Corrientes)
  - Pasivos (Corrientes y No Corrientes)
  - Patrimonio
  - Ingresos
  - Gastos
  - Resultados

**Estructura de cuentas**:
```
1. Activo
  1.1 Activo Corriente
    1.1.01 Caja y Bancos
    1.1.02 Cuentas por cobrar comerciales
    1.1.03 Otras cuentas por cobrar
    1.1.04 Inventarios
    1.1.05 Gastos pagados por anticipado
  1.2 Activo No Corriente
    1.2.01 Inversiones en Valores
    1.2.02 Activo Fijo Neto
    1.2.03 Cartera de Créditos
  1.3 Total Activo

2. Pasivo
  2.1 Pasivo Corriente
    2.1.01 Sobregiros y préstamos bancarios
    2.1.02 Cuentas por pagar comerciales
    2.1.03 Otras cuentas por pagar
    2.1.04 Parte corriente deuda largo plazo
    2.1.05 Depósitos de Clientes
  2.2 Pasivo No Corriente
    2.2.01 Provisión CTS
    2.2.02 Deuda a largo plazo
    2.2.03 Obligaciones Financieras
  2.3 Total Pasivo

3. Patrimonio
  3.1 Capital Social
  3.2 Resultados Acumulados
  3.3 Reservas
  3.4 Total Patrimonio

4. Ingresos
  4.1 Ingresos Financieros
    4.1.01 Intereses por Préstamos
    4.1.02 Comisiones por Servicios
  4.2 Otros Ingresos
  4.3 Total Ingresos

5. Gastos
  5.1 Gastos Operativos
    5.1.01 Gastos de Personal
    5.1.02 Gastos Administrativos
    5.1.03 Depreciación
  5.2 Gastos Financieros
    5.2.01 Intereses por Obligaciones
  5.3 Provisiones
    5.3.01 Provisión para Créditos Incobrables
  5.4 Total Gastos

6. Resultados
  6.1 Utilidad Operativa
  6.2 Utilidad antes de Impuestos
  6.3 Impuesto a la Renta
  6.4 Utilidad Neta
```

### 3. `crear_estados_banco_agricola`
Crea estados financieros completos para 3 años (2022, 2023, 2024).

**Ubicación**: `apps/estados/management/commands/crear_estados_banco_agricola.py`

```bash
python manage.py crear_estados_banco_agricola
```

**Crea**:
- 3 Balances Generales (años 2022, 2023, 2024)
- 3 Estados de Resultados (años 2022, 2023, 2024)

**Datos financieros de ejemplo**:

| Año  | Total Activo | Total Pasivo | Patrimonio | Utilidad Neta |
|------|--------------|--------------|------------|---------------|
| 2022 | $13,105,000  | $11,570,000  | $1,535,000 | $805,000      |
| 2023 | $14,950,000  | $13,155,000  | $1,795,000 | $896,000      |
| 2024 | $16,945,000  | $14,870,000  | $2,075,000 | $1,022,000    |

**Nota**: Los datos numéricos son ficticios pero mantienen la ecuación contable:
```
Activo = Pasivo + Patrimonio
Utilidad Neta = Ingresos - Gastos - Impuestos
```

### 4. `crear_mapeos_banco_agricola`
Crea los mapeos entre cuentas contables y componentes de ratios financieros.

**Ubicación**: `apps/catalogos/management/commands/crear_mapeos_banco_agricola.py`

```bash
python manage.py crear_mapeos_banco_agricola
```

**Crea mapeos para**:
- **Razón Corriente**: Activo Corriente (1.1) / Pasivo Corriente (2.1)
- **Prueba Ácida**: (Activo Corriente - Inventarios) / Pasivo Corriente
- **Ratio de Endeudamiento**: Pasivo Total (2.3) / Patrimonio Total (3.4)
- **Cobertura de Intereses**: Utilidad Operativa (6.1) / Gastos Financieros (5.2)
- **ROE**: Utilidad Neta (6.4) / Patrimonio (3.4) × 100
- **ROA**: Utilidad Neta (6.4) / Activo Total (1.3) × 100

### 5. `crear_datos_completos_banco_agricola` ⭐ (RECOMENDADO)
Comando maestro que ejecuta todos los comandos anteriores en el orden correcto.

**Ubicación**: `apps/catalogos/management/commands/crear_datos_completos_banco_agricola.py`

```bash
python manage.py crear_datos_completos_banco_agricola
```

**Este comando ejecuta automáticamente**:
1. `crear_ratios_demo`
2. `crear_catalogo_banco_agricola`
3. `crear_estados_banco_agricola`
4. `crear_mapeos_banco_agricola`

## Orden de Ejecución

Si ejecutas los comandos individualmente, **debes seguir este orden**:

```bash
# 1. Primero los ratios financieros
python manage.py crear_ratios_demo

# 2. Luego el catálogo de cuentas
python manage.py crear_catalogo_banco_agricola

# 3. Después los estados financieros
python manage.py crear_estados_banco_agricola

# 4. Finalmente los mapeos
python manage.py crear_mapeos_banco_agricola
```

**O simplemente ejecuta**:
```bash
python manage.py crear_datos_completos_banco_agricola
```

## Comportamiento de los Comandos

### Manejo de Datos Existentes

- **Ratios financieros**: Se actualizan si ya existen (no se duplican)
- **Catálogo de cuentas**: Se elimina y reemplaza completamente
- **Estados financieros**: Se eliminan y reemplazan si ya existen para ese año
- **Mapeos**: Se eliminan y reemplazan completamente

### Validaciones

Los comandos validan:
- ✅ Que existan las dependencias necesarias antes de crear datos
- ✅ La ecuación contable en balances generales
- ✅ Que las cuentas mapeadas pertenezcan al catálogo correcto
- ✅ La integridad referencial entre modelos

### Mensajes de Salida

Los comandos usan colores para indicar el estado:
- 🟢 **Verde (SUCCESS)**: Operaciones exitosas
- 🟡 **Amarillo (WARNING)**: Advertencias (datos ya existentes)
- 🔴 **Rojo (ERROR)**: Errores críticos

## Verificación de Datos Creados

Después de ejecutar los comandos, puedes verificar los datos:

### Desde el shell de Django
```bash
python manage.py shell
```

```python
from apps.empresas.models import Empresa
from apps.catalogos.models import CatalogoCuenta, CuentaContable, MapeoCuentaRatio
from apps.estados.models import EstadoFinanciero

# Verificar empresa
banco = Empresa.objects.get(nombre='Banco Agrícola')
print(f"Empresa: {banco.nombre}")
print(f"Sector: {banco.sector.nombre}")

# Verificar catálogo
catalogo = banco.catalogo_cuenta
print(f"\nCuentas en catálogo: {catalogo.cuentas.count()}")

# Verificar estados financieros
estados = EstadoFinanciero.objects.filter(empresa=banco)
print(f"\nEstados financieros: {estados.count()}")
for estado in estados:
    print(f"  - {estado}")

# Verificar mapeos
mapeos = MapeoCuentaRatio.objects.filter(catalogo_cuenta=catalogo)
print(f"\nMapeos de ratios: {mapeos.count()}")
```

### Desde el admin de Django
Accede a `http://127.0.0.1:8000/admin/` y navega por:
- Empresas → Banco Agrícola
- Catálogos de Cuentas
- Estados Financieros
- Mapeos de Cuentas a Ratios

## Solución de Problemas

### Error: "Banco Agrícola no existe"
**Solución**: Ejecuta primero `crear_catalogo_banco_agricola`

### Error: "No hay ratios financieros"
**Solución**: Ejecuta primero `crear_ratios_demo`

### Error: "Catálogo no existe"
**Solución**: Ejecuta `crear_catalogo_banco_agricola` antes de crear estados o mapeos

### Error de integridad de base de datos
**Solución**: Elimina los datos manualmente desde el admin o shell y vuelve a ejecutar

## Archivos Relacionados

```
apps/
├── catalogos/
│   └── management/
│       └── commands/
│           ├── crear_ratios_demo.py
│           ├── crear_catalogo_banco_agricola.py
│           ├── crear_mapeos_banco_agricola.py
│           └── crear_datos_completos_banco_agricola.py
└── estados/
    └── management/
        └── commands/
            └── crear_estados_banco_agricola.py
```

## Notas Técnicas

### Transacciones Atómicas
Todos los comandos usan `transaction.atomic()` para garantizar que:
- Todos los datos se crean exitosamente, o
- Ningún dato se crea si hay un error (rollback automático)

### Datos Ficticios
Los montos de los estados financieros son **completamente ficticios** y generados para propósitos de demostración. Muestran crecimiento año tras año y mantienen las relaciones contables correctas.

### Escalabilidad
Los comandos están diseñados para ser:
- ✅ **Idempotentes**: Se pueden ejecutar múltiples veces sin problemas
- ✅ **Reversibles**: Puedes eliminar los datos y recrearlos
- ✅ **Extensibles**: Puedes agregar más años o empresas fácilmente

## Autor
Generado para el proyecto ProjectANF - Universidad de El Salvador
Fecha: 10 de noviembre de 2025
