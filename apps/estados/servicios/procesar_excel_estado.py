import openpyxl
from decimal import Decimal, InvalidOperation
from apps.estados.models import EstadoFinanciero, ItemEstadoFinanciero, TipoEstadoFinanciero
from apps.empresas.models import Empresa
from apps.catalogos.models import CatalogoCuenta, CuentaContable, TipoCuenta
from django.db import transaction


def procesar_excel_estado(archivo, empresa, año, tipo_estado):
    """
    Procesa un archivo Excel y crea/actualiza un estado financiero.
    
    Args:
        archivo: Archivo Excel cargado
        empresa: Instancia de Empresa
        año: Año del estado financiero
        tipo_estado: TipoEstadoFinanciero (BALANCE_GENERAL o ESTADO_RESULTADOS)
    
    Returns:
        tuple: (éxito: bool, errores: list, items_procesados: int)
    """
    errores = []
    items_procesados = 0
    éxito = False
    
    try:
        wb = openpyxl.load_workbook(archivo)
        ws = wb.active
        
        # Validar encabezados
        headers = [cell.value for cell in ws[1]]
        headers_esperados = ['Código de la cuenta', 'Nombre de la cuenta', 'Tipo de cuenta', 'Monto']
        
        if headers != headers_esperados:
            errores.append(
                f'Los encabezados no coinciden. Se esperaban: {", ".join(headers_esperados)}'
            )
            return False, errores, 0
        
        # Obtener o crear catálogo de cuentas
        try:
            catalogo = CatalogoCuenta.objects.get(empresa=empresa)
        except CatalogoCuenta.DoesNotExist:
            errores.append(f'La empresa "{empresa.nombre}" no tiene un catálogo de cuentas configurado.')
            return False, errores, 0
        
        # Validar tipos de cuenta según el tipo de estado
        if tipo_estado == TipoEstadoFinanciero.BALANCE_GENERAL:
            tipos_permitidos = [TipoCuenta.ACTIVO, TipoCuenta.PASIVO, TipoCuenta.PATRIMONIO]
        elif tipo_estado == TipoEstadoFinanciero.ESTADO_RESULTADOS:
            tipos_permitidos = [TipoCuenta.INGRESO, TipoCuenta.GASTO, TipoCuenta.RESULTADO]
        else:
            errores.append(f'Tipo de estado financiero no válido: {tipo_estado}')
            return False, errores, 0
        
        # Procesar con transacción atómica
        with transaction.atomic():
            # Obtener o crear estado financiero
            estado_financiero, creado = EstadoFinanciero.objects.get_or_create(
                empresa=empresa,
                año=año,
                tipo=tipo_estado,
                defaults={}
            )
            
            # Si ya existía, eliminar items existentes para reemplazarlos
            if not creado:
                ItemEstadoFinanciero.objects.filter(estado_financiero=estado_financiero).delete()
            
            # Procesar filas (empezar desde la fila 2, ya que la 1 son los encabezados)
            for row_num, row in enumerate(ws.iter_rows(min_row=2, values_only=True), start=2):
                # Saltar filas vacías
                if not any(row):
                    continue
                
                codigo = str(row[0]).strip() if row[0] else None
                nombre = str(row[1]).strip() if row[1] else None
                tipo_cuenta_str = str(row[2]).strip() if row[2] else None
                monto_str = row[3] if row[3] is not None else None
                
                # Validar campos requeridos
                if not codigo:
                    errores.append(f'Fila {row_num}: Falta el código de la cuenta')
                    continue
                
                if not nombre:
                    errores.append(f'Fila {row_num}: Falta el nombre de la cuenta')
                    continue
                
                # Validar que la cuenta existe en el catálogo
                try:
                    cuenta = CuentaContable.objects.get(
                        catalogo=catalogo,
                        codigo=codigo
                    )
                except CuentaContable.DoesNotExist:
                    errores.append(
                        f'Fila {row_num}: La cuenta con código "{codigo}" no existe en el catálogo de la empresa.'
                    )
                    continue
                
                # Validar que el tipo de cuenta coincide
                if cuenta.tipo != tipo_cuenta_str:
                    errores.append(
                        f'Fila {row_num}: El tipo de cuenta no coincide. '
                        f'Esperado: {tipo_cuenta_str}, Encontrado: {cuenta.get_tipo_display()}'
                    )
                    continue
                
                # Validar que el tipo de cuenta es permitido para este estado
                if cuenta.tipo not in tipos_permitidos:
                    errores.append(
                        f'Fila {row_num}: La cuenta "{codigo}" de tipo "{cuenta.get_tipo_display()}" '
                        f'no es válida para un {estado_financiero.get_tipo_display()}.'
                    )
                    continue
                
                # Validar y convertir monto
                if monto_str is None:
                    monto = Decimal('0.00')
                else:
                    try:
                        # Convertir a Decimal
                        if isinstance(monto_str, (int, float)):
                            monto = Decimal(str(monto_str))
                        elif isinstance(monto_str, str):
                            # Limpiar el string (remover espacios, comas como separadores de miles)
                            monto_str_limpio = monto_str.strip().replace(',', '')
                            monto = Decimal(monto_str_limpio)
                        else:
                            monto = Decimal('0.00')
                    except (InvalidOperation, ValueError):
                        errores.append(
                            f'Fila {row_num}: El monto "{monto_str}" no es un número válido.'
                        )
                        continue
                
                # Crear item del estado financiero
                try:
                    ItemEstadoFinanciero.objects.create(
                        estado_financiero=estado_financiero,
                        cuenta_contable=cuenta,
                        monto=monto
                    )
                    items_procesados += 1
                except Exception as e:
                    errores.append(f'Fila {row_num}: Error al crear item - {str(e)}')
            
            éxito = len(errores) == 0
    
    except Exception as e:
        errores.append(f'Error al procesar el archivo: {str(e)}')
        éxito = False
    
    return éxito, errores, items_procesados

