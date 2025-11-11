from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    """
    Comando maestro que ejecuta todos los comandos de demostración
    para Banco Agrícola en el orden correcto.
    """
    help = 'Crea todos los datos de demostración para Banco Agrícola (catálogo, estados, mapeos)'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS(
                '\n' + '='*70 +
                '\n🏦 CREACIÓN DE DATOS DEMO - BANCO AGRÍCOLA' +
                '\n' + '='*70 + '\n'
            )
        )
        
        comandos = [
            ('crear_ratios_demo', 'Creando ratios financieros predefinidos'),
            ('crear_catalogo_banco_agricola', 'Creando catálogo de cuentas de Banco Agrícola'),
            ('crear_estados_banco_agricola', 'Creando estados financieros de Banco Agrícola'),
            ('crear_mapeos_banco_agricola', 'Creando mapeos de ratios de Banco Agrícola'),
        ]
        
        for i, (comando, descripcion) in enumerate(comandos, 1):
            self.stdout.write(
                self.style.WARNING(
                    f'\n[{i}/{len(comandos)}] {descripcion}...'
                )
            )
            self.stdout.write(self.style.WARNING('-' * 70))
            
            try:
                call_command(comando)
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f'\n✗ Error ejecutando {comando}: {str(e)}'
                    )
                )
                return
        
        self.stdout.write(
            self.style.SUCCESS(
                '\n' + '='*70 +
                '\n✓ DATOS DE DEMOSTRACIÓN CREADOS EXITOSAMENTE' +
                '\n' + '='*70 +
                '\n\n📊 Resumen de datos creados:' +
                '\n  • Ratios financieros predefinidos (6 ratios)' +
                '\n  • Catálogo de cuentas de Banco Agrícola (~50 cuentas)' +
                '\n  • 3 Balances Generales (2022, 2023, 2024)' +
                '\n  • 3 Estados de Resultados (2022, 2023, 2024)' +
                '\n  • Mapeos de ratios financieros (~18 mapeos)' +
                '\n\n🎉 ¡Todo listo para usar el sistema!' +
                '\n' + '='*70 + '\n'
            )
        )
