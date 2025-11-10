from django.core.management.base import BaseCommand
from apps.catalogos.models import RatioFinanciero, ComponenteRatio


class Command(BaseCommand):
    """
    Comando para crear ratios financieros de ejemplo con sus componentes.
    """
    help = 'Crea ratios financieros de ejemplo con sus componentes'

    def handle(self, *args, **options):
        # Ratios de Liquidez
        ratios_liquidez = [
            {
                'nombre': 'Razón Corriente',
                'formula_display': 'Activo Corriente / Pasivo Corriente',
                'componentes': ['Activo Corriente', 'Pasivo Corriente']
            },
            {
                'nombre': 'Prueba Ácida',
                'formula_display': '(Activo Corriente - Inventario) / Pasivo Corriente',
                'componentes': ['Activo Corriente', 'Inventario', 'Pasivo Corriente']
            },
        ]
        
        # Ratios de Endeudamiento
        ratios_endeudamiento = [
            {
                'nombre': 'Ratio de Endeudamiento',
                'formula_display': 'Pasivo Total / Patrimonio Total',
                'componentes': ['Pasivo Total', 'Patrimonio Total']
            },
            {
                'nombre': 'Cobertura de Intereses',
                'formula_display': 'Utilidad Operativa / Gastos Financieros',
                'componentes': ['Utilidad Operativa', 'Gastos Financieros']
            },
        ]
        
        # Ratios de Rentabilidad
        ratios_rentabilidad = [
            {
                'nombre': 'ROE',
                'formula_display': '(Utilidad Neta / Patrimonio) × 100',
                'componentes': ['Utilidad Neta', 'Patrimonio']
            },
            {
                'nombre': 'ROA',
                'formula_display': '(Utilidad Neta / Activo Total) × 100',
                'componentes': ['Utilidad Neta', 'Activo Total']
            },
        ]
        
        # Crear ratios
        categorias = {
            'Liquidez': ratios_liquidez,
            'Endeudamiento': ratios_endeudamiento,
            'Rentabilidad': ratios_rentabilidad,
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

