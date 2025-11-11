"""
Comando de gestión para actualizar los promedios generales de todos los ratios.
Este comando recalcula los promedios basándose en todos los valores calculados existentes.
"""
from django.core.management.base import BaseCommand
from django.db.models import Avg
from decimal import Decimal

from apps.catalogos.models import RatioFinanciero
from apps.analisis.models import ValorRatioCalculado


class Command(BaseCommand):
    help = 'Actualiza los promedios generales de todos los ratios financieros'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write(self.style.SUCCESS('ACTUALIZACIÓN DE PROMEDIOS GENERALES'))
        self.stdout.write(self.style.SUCCESS('='*60))
        
        ratios = RatioFinanciero.objects.all()
        actualizados = 0
        sin_datos = 0
        
        for ratio in ratios:
            # Obtener todos los valores calculados de este ratio
            valores = ValorRatioCalculado.objects.filter(
                ratio=ratio,
                valor_calculado__isnull=False
            )
            
            if valores.exists():
                # Calcular promedio
                promedio = valores.aggregate(Avg('valor_calculado'))['valor_calculado__avg']
                
                if promedio is not None:
                    promedio_anterior = ratio.promedio_general
                    ratio.promedio_general = round(Decimal(str(promedio)), 4)
                    ratio.save(update_fields=['promedio_general', 'actualizado_en'])
                    
                    actualizados += 1
                    
                    cambio = ""
                    if promedio_anterior:
                        diferencia = ratio.promedio_general - promedio_anterior
                        if diferencia > 0:
                            cambio = f" (↑ +{diferencia:.4f})"
                        elif diferencia < 0:
                            cambio = f" (↓ {diferencia:.4f})"
                        else:
                            cambio = " (sin cambio)"
                    else:
                        cambio = " (nuevo)"
                    
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'✅ {ratio.nombre}: {ratio.promedio_general}{cambio}'
                        )
                    )
                    self.stdout.write(f'   Basado en {valores.count()} valores calculados')
            else:
                sin_datos += 1
                self.stdout.write(
                    self.style.WARNING(
                        f'⚠️  {ratio.nombre}: Sin valores calculados'
                    )
                )
        
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write(self.style.SUCCESS(f'Ratios actualizados: {actualizados}'))
        self.stdout.write(self.style.WARNING(f'Ratios sin datos: {sin_datos}'))
        self.stdout.write(self.style.SUCCESS('='*60))
