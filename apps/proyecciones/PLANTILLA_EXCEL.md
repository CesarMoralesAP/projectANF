# Plantilla de Excel para Proyección de Ventas

## Estructura del Archivo

El archivo Excel debe tener **exactamente 3 columnas** en el siguiente orden:

| Columna | Nombre  | Tipo    | Descripción                    |
|---------|---------|---------|--------------------------------|
| 1       | Año     | Número  | Año del dato histórico (ej: 2023) |
| 2       | Mes     | Número  | Mes del dato histórico (1-12)  |
| 3       | Valor   | Decimal | Valor de ventas en USD         |

## Ejemplo de Datos

```
Año    Mes    Valor
2023   1      50000.00
2023   2      52000.00
2023   3      51500.00
2023   4      53000.00
2023   5      54500.00
2023   6      55000.00
2023   7      56000.00
2023   8      57500.00
2023   9      58000.00
2023   10     59000.00
2023   11     60000.00
2023   12     61000.00
```

## Notas Importantes

1. **Headers**: Los nombres de las columnas pueden ser cualquiera, el sistema solo toma las primeras 3 columnas
2. **Orden**: El orden de las filas no importa, el sistema las ordenará automáticamente
3. **Datos faltantes**: Las filas con valores vacíos o no numéricos serán ignoradas automáticamente
4. **Formato**: Puede ser .xlsx o .xls
5. **Mínimo de datos**: Se recomienda al menos 6 meses de datos históricos para proyecciones más precisas

## Generar Archivo en Excel

1. Abrir Microsoft Excel o LibreOffice Calc
2. Crear las 3 columnas (Año, Mes, Valor)
3. Ingresar los datos históricos
4. Guardar como `.xlsx` o `.xls`
5. Cargar el archivo en el sistema
