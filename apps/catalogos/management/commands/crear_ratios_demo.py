from django.core.management.base import BaseCommand
from django.db import transaction
from apps.catalogos.models import RatioFinanciero, ComponenteRatio


class Command(BaseCommand):
    """
    Comando para crear ratios financieros de ejemplo con sus componentes.
    """
    help = 'Crea ratios financieros de ejemplo con sus componentes'

    def handle(self, *args, **options):
        # Lista de ratios que deben existir (los demás se eliminarán)
        ratios_validos = [
            'Razón Corriente',
            'Prueba Ácida',
            'Ratio de Endeudamiento Total',
            'Ratio de Autonomía Financiera',
            'ROA',
            'ROE',
            'Margen Neto',
            'Margen de Interés Neto (NIM)',
            'Margen Operativo',
            'Ratio de Eficiencia',
        ]
        
        # Eliminar ratios que no están en la lista válida
        ratios_obsoletos = RatioFinanciero.objects.exclude(nombre__in=ratios_validos)
        if ratios_obsoletos.exists():
            count = ratios_obsoletos.count()
            nombres_eliminados = list(ratios_obsoletos.values_list('nombre', flat=True))
            ratios_obsoletos.delete()
            self.stdout.write(
                self.style.WARNING(
                    f'\n⚠ {count} ratio(s) obsoleto(s) eliminado(s): {", ".join(nombres_eliminados)}\n'
                )
            )
        
        # Ratios de Liquidez
        ratios_liquidez = [
            {
                'nombre': 'Razón Corriente',
                'formula_display': 'Activo Corriente / Pasivo Corriente',
                'componentes': ['Activo Corriente', 'Pasivo Corriente']
            },
            {
                'nombre': 'Prueba Ácida',
                'formula_display': '(Activo Corriente - Inventarios) / Pasivo Corriente',
                'componentes': ['Activo Corriente', 'Inventarios', 'Pasivo Corriente']
            },
        ]
        
        # Ratios de Endeudamiento
        ratios_endeudamiento = [
            {
                'nombre': 'Ratio de Endeudamiento Total',
                'formula_display': 'Pasivo Total / Activo Total',
                'componentes': ['Pasivo Total', 'Activo Total']
            },
            {
                'nombre': 'Ratio de Autonomía Financiera',
                'formula_display': 'Patrimonio Neto / Activo Total',
                'componentes': ['Patrimonio Neto', 'Activo Total']
            },
        ]
        
        # Ratios de Rentabilidad
        ratios_rentabilidad = [
            {
                'nombre': 'ROA',
                'formula_display': 'Utilidad Neta / Activo Total Promedio',
                'componentes': ['Utilidad Neta', 'Activo Total Promedio']
            },
            {
                'nombre': 'ROE',
                'formula_display': 'Utilidad Neta / Patrimonio Neto Promedio',
                'componentes': ['Utilidad Neta', 'Patrimonio Neto Promedio']
            },
            {
                'nombre': 'Margen Neto',
                'formula_display': 'Utilidad Neta / Ingresos Financieros Netos',
                'componentes': ['Utilidad Neta', 'Ingresos Financieros Netos']
            },
            {
                'nombre': 'Margen de Interés Neto (NIM)',
                'formula_display': '(Ingresos Financieros - Gastos Financieros) / Activos Productivos Promedio',
                'componentes': ['Ingresos Financieros', 'Gastos Financieros', 'Activos Productivos Promedio']
            },
            {
                'nombre': 'Margen Operativo',
                'formula_display': 'Resultado Operativo / Ingresos de Operación',
                'componentes': ['Resultado Operativo', 'Ingresos de Operación']
            },
        ]
        
        # Ratios de Eficiencia
        ratios_eficiencia = [
            {
                'nombre': 'Ratio de Eficiencia',
                'formula_display': 'Gastos Operativos / Margen Bruto',
                'componentes': ['Gastos Operativos', 'Margen Bruto']
            },
        ]
        
        # Crear ratios
        categorias = {
            'Liquidez': ratios_liquidez,
            'Endeudamiento': ratios_endeudamiento,
            'Rentabilidad': ratios_rentabilidad,
            'Eficiencia': ratios_eficiencia,
        }
        
        total_ratios = 0
        total_componentes = 0
        
        for categoria, ratios in categorias.items():
            self.stdout.write(self.style.SUCCESS(f'\n📊 Creando ratios de {categoria}...'))
            
            for ratio_data in ratios:
                # Crear o obtener el ratio
                ratio, created = RatioFinanciero.objects.get_or_create(
                    nombre=ratio_data['nombre'],
                    defaults={
                        'formula_display': ratio_data['formula_display'],
                        'categoria': categoria
                    }
                )
                
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(f'  ✓ Ratio creado: {ratio.nombre}')
                    )
                    total_ratios += 1
                else:
                    # Actualizar fórmula y categoría si cambian
                    ratio.formula_display = ratio_data['formula_display']
                    ratio.categoria = categoria
                    ratio.save()
                    self.stdout.write(
                        self.style.WARNING(f'  ⚠ Ratio ya existe: {ratio.nombre}')
                    )
                    
                    # Eliminar componentes obsoletos que ya no están en la definición actual
                    componentes_actuales = ratio_data['componentes']
                    componentes_obsoletos = ComponenteRatio.objects.filter(
                        ratio_financiero=ratio
                    ).exclude(nombre_componente__in=componentes_actuales)
                    
                    if componentes_obsoletos.exists():
                        count_comp = componentes_obsoletos.count()
                        nombres_comp = list(componentes_obsoletos.values_list('nombre_componente', flat=True))
                        componentes_obsoletos.delete()
                        self.stdout.write(
                            self.style.WARNING(
                                f'    ⚠ Eliminados {count_comp} componente(s) obsoleto(s): {", ".join(nombres_comp)}'
                            )
                        )
                
                # Crear componentes del ratio
                for orden, nombre_componente in enumerate(ratio_data['componentes'], start=1):
                    componente, created = ComponenteRatio.objects.get_or_create(
                        ratio_financiero=ratio,
                        nombre_componente=nombre_componente,
                        defaults={}
                    )
                    
                    if created:
                        self.stdout.write(
                            self.style.SUCCESS(f'    ✓ Componente creado: {nombre_componente}')
                        )
                        total_componentes += 1
                    else:
                        self.stdout.write(
                            self.style.WARNING(f'    ⚠ Componente ya existe: {nombre_componente}')
                        )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✓ Ratios financieros creados: {total_ratios} ratios, {total_componentes} componentes'
            )
        )

