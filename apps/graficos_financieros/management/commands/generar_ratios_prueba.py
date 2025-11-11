"""
Comando para generar datos de prueba de ratios financieros.
Crea registros en las tablas ratio_financiero y valor_ratio_calculado.

Uso:
    python manage.py generar_ratios_prueba
    python manage.py generar_ratios_prueba --empresas 1 2 3
    python manage.py generar_ratios_prueba --anios 2020 2021 2022 2023 2024
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.graficos_financieros.models import RatioFinanciero, ValorRatioCalculado
from apps.empresas.models import Empresa
import random


class Command(BaseCommand):
    help = 'Genera datos de prueba para ratios financieros'

    def add_arguments(self, parser):
        parser.add_argument(
            '--empresas',
            nargs='+',
            type=int,
            help='IDs específicos de empresas (por defecto: todas)',
        )
        parser.add_argument(
            '--anios',
            nargs='+',
            type=int,
            default=[2022, 2023, 2024],
            help='Años para generar datos (por defecto: 2022, 2023, 2024)',
        )
        parser.add_argument(
            '--limpiar',
            action='store_true',
            help='Eliminar datos existentes antes de generar nuevos',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n=== GENERADOR DE DATOS DE RATIOS FINANCIEROS ===\n'))

        # Limpiar datos existentes si se solicita
        if options['limpiar']:
            self.stdout.write(self.style.WARNING('[!] Limpiando datos existentes...'))
            ValorRatioCalculado.objects.all().delete()
            RatioFinanciero.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('[OK] Datos limpiados'))

        # Crear o verificar ratios
        self.stdout.write('\n[*] Creando/verificando catalogo de ratios...')
        ratios_data = [
            {
                'nombre': 'Razón Corriente',
                'formula_display': 'Activo Corriente / Pasivo Corriente',
                'categoria': 'Liquidez',
                'promedio_general': 0.2561,
            },
            {
                'nombre': 'Prueba Ácida',
                'formula_display': '(Activo Corriente - Inventario) / Pasivo Corriente',
                'categoria': 'Liquidez',
                'promedio_general': 0.2358,
            },
            {
                'nombre': 'Ratio de Endeudamiento',
                'formula_display': 'Pasivo Total / Patrimonio Total',
                'categoria': 'Endeudamiento',
                'promedio_general': 7.8901,
            },
            {
                'nombre': 'Cobertura de Intereses',
                'formula_display': 'Utilidad Operativa / Gastos Financieros',
                'categoria': 'Endeudamiento',
                'promedio_general': 0.3808,
            },
            {
                'nombre': 'ROE',
                'formula_display': '(Utilidad Neta / Patrimonio) × 100',
                'categoria': 'Rentabilidad',
                'promedio_general': 1.9092,
            },
            {
                'nombre': 'ROA',
                'formula_display': '(Utilidad Neta / Activo Total) × 100',
                'categoria': 'Rentabilidad',
                'promedio_general': 16.9236,
            },
        ]

        ratios_creados = []
        for ratio_data in ratios_data:
            ratio, created = RatioFinanciero.objects.get_or_create(
                nombre=ratio_data['nombre'],
                defaults=ratio_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'  [+] Creado: {ratio.nombre}'))
            else:
                self.stdout.write(f'  [-] Existente: {ratio.nombre}')
            ratios_creados.append(ratio)

        # Obtener empresas
        if options['empresas']:
            empresas = Empresa.objects.filter(id__in=options['empresas'])
        else:
            empresas = Empresa.objects.all()

        if not empresas.exists():
            self.stdout.write(self.style.ERROR('\n[X] No se encontraron empresas'))
            return

        self.stdout.write(f'\n[*] Empresas seleccionadas: {empresas.count()}')
        for empresa in empresas:
            self.stdout.write(f'  - {empresa.nombre} (Sector: {empresa.sector.nombre})')

        # Años a generar
        anios = options['anios']
        self.stdout.write(f'\n[*] Anios: {", ".join(map(str, anios))}')

        # Generar valores calculados
        self.stdout.write('\n[*] Generando valores calculados...\n')
        total_generados = 0

        for empresa in empresas:
            self.stdout.write(f'\n  [*] {empresa.nombre}:')
            
            for ratio in ratios_creados:
                # Generar valores realistas con tendencia
                base_value = float(ratio.promedio_general or 1.0)
                
                for i, anio in enumerate(anios):
                    # Generar valor con variación realista
                    # Tendencia: mejora gradual con algo de volatilidad
                    tendencia = 1 + (i * 0.05)  # Mejora del 5% por año
                    variacion = random.uniform(0.90, 1.10)  # ±10% de variación
                    valor = round(base_value * tendencia * variacion, 4)
                    
                    # Crear o actualizar valor
                    valor_obj, created = ValorRatioCalculado.objects.update_or_create(
                        empresa=empresa,
                        ratio=ratio,
                        año=anio,
                        defaults={
                            'valor_calculado': valor,
                            'usuario_calculo_id': 1,  # Usuario admin por defecto
                            'fecha_calculo': timezone.now(),
                        }
                    )
                    
                    if created:
                        total_generados += 1
                        accion = '[+]'
                    else:
                        accion = '[U]'
                    
                    self.stdout.write(
                        f'    {accion} {ratio.nombre[:25]:25} | {anio}: {valor:8.2f}'
                    )

        # Resumen final
        self.stdout.write(self.style.SUCCESS(f'\n\n[OK] PROCESO COMPLETADO'))
        self.stdout.write(self.style.SUCCESS(f'   Ratios en catalogo: {len(ratios_creados)}'))
        self.stdout.write(self.style.SUCCESS(f'   Empresas procesadas: {empresas.count()}'))
        self.stdout.write(self.style.SUCCESS(f'   Anios generados: {len(anios)}'))
        self.stdout.write(self.style.SUCCESS(f'   Total valores generados: {total_generados}'))
        self.stdout.write(self.style.SUCCESS(f'   Total registros: {ValorRatioCalculado.objects.count()}\n'))
