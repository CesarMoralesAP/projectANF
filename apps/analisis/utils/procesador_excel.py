"""
Procesador de archivos Excel para proyecciones financieras.
"""
import pandas as pd
from typing import Dict, List, Any


# Configuración de columnas y hojas del Excel
CONFIGURACION_EXCEL = {
    'VALOR_INCREMENTAL': {
        'hoja': 'valor incremental',
        'columna_periodo': 'Mes',
        'columna_valor': 'Venta',
    },
    'VALOR_ABSOLUTO': {
        'hoja': 'valor absoluto',
        'columna_periodo': 'Mes',
        'columna_valor': 'Venta',
    },
    'MINIMOS_CUADRADOS': {
        'hoja': 'minimos cuadrados',
        'columna_periodo': 'Mes',
        'columna_valor': 'Venta',
    }
}


def procesar_excel_proyeccion(archivo_path: str) -> Dict[str, Any]:
    """
    Procesa archivo Excel con proyecciones financieras.
    
    Lee tres hojas:
    - 'valor incremental': Método de valor incremental/porcentual
    - 'valor absoluto': Método de valor absoluto
    - 'minimos cuadrados': Método de mínimos cuadrados (opcional)
    
    Args:
        archivo_path: Ruta al archivo Excel subido
    
    Returns:
        dict: {
            'valor_incremental': {'periodos': [...], 'valores': [...]},
            'valor_absoluto': {'periodos': [...], 'valores': [...]},
            'minimos_cuadrados': {'periodos': [...], 'valores': [...]} (opcional)
        }
    
    Raises:
        ValueError: Si hay error al procesar el archivo
    """
    try:
        resultado = {}
        
        # Procesar método de Valor Incremental
        resultado['valor_incremental'] = _procesar_hoja(
            archivo_path,
            CONFIGURACION_EXCEL['VALOR_INCREMENTAL']
        )
        
        # Procesar método de Valor Absoluto
        resultado['valor_absoluto'] = _procesar_hoja(
            archivo_path,
            CONFIGURACION_EXCEL['VALOR_ABSOLUTO']
        )
        
        # Procesar método de Mínimos Cuadrados (opcional)
        try:
            resultado['minimos_cuadrados'] = _procesar_hoja(
                archivo_path,
                CONFIGURACION_EXCEL['MINIMOS_CUADRADOS']
            )
        except (KeyError, ValueError):
            # Si no existe la hoja, no es error crítico
            resultado['minimos_cuadrados'] = None
        
        return resultado
    
    except Exception as e:
        raise ValueError(f'Error al procesar archivo Excel: {str(e)}')


def _procesar_hoja(archivo_path: str, config: Dict[str, str]) -> Dict[str, List]:
    """
    Procesa una hoja específica del Excel.
    
    Args:
        archivo_path: Ruta al archivo Excel
        config: Configuración con nombre de hoja y columnas
    
    Returns:
        dict: {'periodos': [...], 'valores': [...]}
    """
    try:
        # Leer hoja específica
        df = pd.read_excel(
            archivo_path,
            sheet_name=config['hoja']
        )
        
        # Obtener nombres de columnas
        col_periodo = config['columna_periodo']
        col_valor = config['columna_valor']
        
        # Validar que las columnas existan
        if col_periodo not in df.columns:
            raise ValueError(
                f"No se encontró la columna '{col_periodo}' en la hoja '{config['hoja']}'"
            )
        if col_valor not in df.columns:
            raise ValueError(
                f"No se encontró la columna '{col_valor}' en la hoja '{config['hoja']}'"
            )
        
        # Extraer y limpiar datos
        periodos = df[col_periodo].dropna().astype(str).tolist()
        valores = df[col_valor].dropna().astype(float).tolist()
        
        # Asegurar que ambas listas tengan la misma longitud
        min_length = min(len(periodos), len(valores))
        periodos = periodos[:min_length]
        valores = valores[:min_length]
        
        return {
            'periodos': periodos,
            'valores': valores,
            'total_registros': min_length
        }
    
    except KeyError as e:
        raise ValueError(
            f"Hoja '{config['hoja']}' no encontrada en el archivo Excel"
        )
    except Exception as e:
        raise ValueError(f"Error al procesar hoja '{config['hoja']}': {str(e)}")


def validar_estructura_excel(archivo_path: str) -> tuple[bool, str]:
    """
    Valida que el archivo Excel tenga la estructura esperada.
    
    Args:
        archivo_path: Ruta al archivo Excel
    
    Returns:
        tuple: (es_valido: bool, mensaje: str)
    """
    try:
        # Leer todas las hojas
        excel_file = pd.ExcelFile(archivo_path)
        hojas_disponibles = excel_file.sheet_names
        
        # Verificar hojas requeridas
        hojas_requeridas = ['valor incremental', 'valor absoluto']
        hojas_faltantes = [h for h in hojas_requeridas if h not in hojas_disponibles]
        
        if hojas_faltantes:
            return False, f"Faltan las hojas: {', '.join(hojas_faltantes)}"
        
        # Verificar columnas en cada hoja
        for tipo_metodo, config in CONFIGURACION_EXCEL.items():
            df = pd.read_excel(archivo_path, sheet_name=config['hoja'])
            
            if config['columna_periodo'] not in df.columns:
                return False, f"Falta columna '{config['columna_periodo']}' en hoja '{config['hoja']}'"
            
            if config['columna_valor'] not in df.columns:
                return False, f"Falta columna '{config['columna_valor']}' en hoja '{config['hoja']}'"
        
        return True, "Estructura válida"
    
    except Exception as e:
        return False, f"Error al validar archivo: {str(e)}"
