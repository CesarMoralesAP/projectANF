from django import template
from decimal import Decimal

register = template.Library()


@register.filter
def monto_input(monto):
    """
    Formatea un monto para usar en inputs HTML type="number".
    Siempre usa punto como separador decimal, independiente del locale.
    """
    if monto is None:
        return "0.00"
    
    # Convertir a Decimal para precisión
    try:
        monto_decimal = Decimal(str(monto))
        # Quantize para asegurar 2 decimales
        monto_decimal = monto_decimal.quantize(Decimal('0.01'))
        
        # Obtener signo
        signo = '-' if monto_decimal < 0 else ''
        monto_abs = abs(monto_decimal)
        
        # Convertir a int para parte entera y decimal
        parte_entera = int(monto_abs)
        parte_decimal_int = int((monto_abs - parte_entera) * 100)
        
        # Construir string manualmente con punto decimal
        monto_str = f"{signo}{parte_entera}.{parte_decimal_int:02d}"
        
        return monto_str
    except (ValueError, TypeError):
        return "0.00"

