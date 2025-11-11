# 🏦 Datos Demo - Banco Agrícola
## Resumen Ejecutivo de Datos Creados

### ✅ Estado: COMPLETADO EXITOSAMENTE

---

## 📊 Datos Creados

### 1. Empresa y Sector
- **Sector**: Bancario
- **Empresa**: Banco Agrícola

### 2. Catálogo de Cuentas (50 cuentas)

#### 🔵 ACTIVOS (12 cuentas)
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
```

#### 🔴 PASIVOS (12 cuentas)
```
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
```

#### 🟢 PATRIMONIO (5 cuentas)
```
3. Patrimonio
  3.1 Capital Social
  3.2 Resultados Acumulados
  3.3 Reservas
  3.4 Total Patrimonio
```

#### 🟡 INGRESOS (5 cuentas)
```
4. Ingresos
  4.1 Ingresos Financieros
    4.1.01 Intereses por Préstamos
    4.1.02 Comisiones por Servicios
  4.2 Otros Ingresos
  4.3 Total Ingresos
```

#### 🟠 GASTOS (11 cuentas)
```
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
```

#### 🟣 RESULTADOS (5 cuentas)
```
6. Resultados
  6.1 Utilidad Operativa
  6.2 Utilidad antes de Impuestos
  6.3 Impuesto a la Renta
  6.4 Utilidad Neta
```

---

### 3. Estados Financieros (6 estados)

#### 📋 Balances Generales (3 años)

| Año  | Total Activo  | Total Pasivo  | Total Patrimonio | Cuentas |
|------|---------------|---------------|------------------|---------|
| 2022 | $13,105,000   | $11,570,000   | $1,535,000       | 26      |
| 2023 | $14,950,000   | $13,155,000   | $1,795,000       | 26      |
| 2024 | $16,945,000   | $14,870,000   | $2,075,000       | 26      |

**✅ Ecuación Contable Validada**: `Activo = Pasivo + Patrimonio`

#### 📈 Estados de Resultados (3 años)

| Año  | Total Ingresos | Total Gastos | Utilidad Neta | Cuentas |
|------|----------------|--------------|---------------|---------|
| 2022 | $3,680,000     | $2,530,000   | $805,000      | 18      |
| 2023 | $4,180,000     | $2,900,000   | $896,000      | 18      |
| 2024 | $4,750,000     | $3,290,000   | $1,022,000    | 18      |

**Crecimiento de Utilidad Neta**:
- 2022 → 2023: +11.3%
- 2023 → 2024: +14.1%

---

### 4. Ratios Financieros (6 ratios con 13 mapeos)

#### 💧 Liquidez (2 ratios, 5 mapeos)

**Razón Corriente** = `Activo Corriente / Pasivo Corriente`
- ✓ Activo Corriente → 1.1
- ✓ Pasivo Corriente → 2.1

**Prueba Ácida** = `(Activo Corriente - Inventario) / Pasivo Corriente`
- ✓ Activo Corriente → 1.1
- ✓ Inventario → 1.1.04
- ✓ Pasivo Corriente → 2.1

#### 🔗 Endeudamiento (2 ratios, 4 mapeos)

**Ratio de Endeudamiento** = `Pasivo Total / Patrimonio Total`
- ✓ Pasivo Total → 2.3
- ✓ Patrimonio Total → 3.4

**Cobertura de Intereses** = `Utilidad Operativa / Gastos Financieros`
- ✓ Utilidad Operativa → 6.1
- ✓ Gastos Financieros → 5.2

#### 💰 Rentabilidad (2 ratios, 4 mapeos)

**ROE** = `(Utilidad Neta / Patrimonio) × 100`
- ✓ Utilidad Neta → 6.4
- ✓ Patrimonio → 3.4

**ROA** = `(Utilidad Neta / Activo Total) × 100`
- ✓ Utilidad Neta → 6.4
- ✓ Activo Total → 1.3

---

## 🎯 Casos de Uso Habilitados

Con estos datos puedes:

1. ✅ **Ver estados financieros** de 3 años consecutivos
2. ✅ **Calcular ratios financieros** automáticamente
3. ✅ **Comparar rendimiento** año tras año
4. ✅ **Analizar tendencias** de crecimiento
5. ✅ **Validar mapeos** de cuentas a ratios
6. ✅ **Probar exportación** a Excel
7. ✅ **Generar reportes** y análisis

---

## 📦 Comandos para Recrear

### Opción 1: Comando Maestro (Recomendado)
```bash
python manage.py crear_datos_completos_banco_agricola
```

### Opción 2: Comandos Individuales
```bash
python manage.py crear_ratios_demo
python manage.py crear_catalogo_banco_agricola
python manage.py crear_estados_banco_agricola
python manage.py crear_mapeos_banco_agricola
```

---

## 🔍 Verificación en Django Shell

```python
# Acceder al shell
python manage.py shell

# Verificar datos
from apps.empresas.models import Empresa
from apps.catalogos.models import CatalogoCuenta, MapeoCuentaRatio
from apps.estados.models import EstadoFinanciero

banco = Empresa.objects.get(nombre='Banco Agrícola')
print(f"✓ Empresa: {banco.nombre}")
print(f"✓ Catálogo: {banco.catalogo_cuenta.cuentas.count()} cuentas")
print(f"✓ Estados: {EstadoFinanciero.objects.filter(empresa=banco).count()}")
print(f"✓ Mapeos: {MapeoCuentaRatio.objects.filter(catalogo_cuenta=banco.catalogo_cuenta).count()}")
```

---

## 📁 Archivos Creados

```
apps/
├── catalogos/
│   └── management/
│       └── commands/
│           ├── crear_ratios_demo.py                          [EXISTENTE]
│           ├── crear_catalogo_banco_agricola.py              [NUEVO]
│           ├── crear_mapeos_banco_agricola.py                [NUEVO]
│           └── crear_datos_completos_banco_agricola.py       [NUEVO]
└── estados/
    └── management/                                            [NUEVO]
        ├── __init__.py                                        [NUEVO]
        └── commands/                                          [NUEVO]
            ├── __init__.py                                    [NUEVO]
            └── crear_estados_banco_agricola.py                [NUEVO]

Documentación:
├── DATOS_DEMO.md                                              [NUEVO]
└── RESUMEN_DATOS_DEMO.md                                      [NUEVO]
```

---

## ⚠️ Notas Importantes

1. **Datos Ficticios**: Todos los montos son inventados para demostración
2. **Ecuación Contable**: Todos los balances cumplen con `Activo = Pasivo + Patrimonio`
3. **Crecimiento Realista**: Los datos muestran crecimiento progresivo año tras año
4. **Idempotencia**: Puedes ejecutar los comandos múltiples veces sin problemas
5. **Transacciones Atómicas**: Si hay un error, nada se guarda (rollback automático)

---

## 🎉 Resultado Final

```
✓ 1 Sector creado
✓ 1 Empresa creada
✓ 1 Catálogo de cuentas creado
✓ 50 Cuentas contables creadas
✓ 6 Estados financieros creados
✓ 132 Items de estados financieros creados (44 por año × 3 años)
✓ 6 Ratios financieros configurados
✓ 13 Mapeos de ratios creados

TOTAL: ¡Sistema completo y funcional! 🚀
```

---

**Generado**: 10 de noviembre de 2025  
**Proyecto**: ProjectANF - Universidad de El Salvador  
**Empresa Demo**: Banco Agrícola
