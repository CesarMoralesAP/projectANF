from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    """
    Comando maestro que ejecuta todos los comandos de demostración
    para AMBOS bancos (Agrícola y Atlántida) en el orden correcto.
    """
    help = 'Crea todos los datos de demostración para Banco Agrícola y Banco Atlántida'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS(
                '\n' + '='*80 +
                '\n🏦 CREACIÓN DE DATOS DEMO - TODOS LOS BANCOS' +
                '\n' + '='*80 + '\n'
            )
        )
        
        # Primero crear los ratios financieros (solo una vez para todos)
        self.stdout.write(
            self.style.WARNING(
                f'\n[1/3] Creando ratios financieros predefinidos...'
            )
        )
        self.stdout.write(self.style.WARNING('-' * 80))
        
        try:
            call_command('crear_ratios_demo')
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f'\n✗ Error ejecutando crear_ratios_demo: {str(e)}'
                )
            )
            return
        
        # Crear datos de Banco Agrícola
        self.stdout.write(
            self.style.WARNING(
                f'\n[2/3] Creando datos completos de Banco Agrícola...'
            )
        )
        self.stdout.write(self.style.WARNING('-' * 80))
        
        comandos_agricola = [
            ('crear_catalogo_banco_agricola', 'Catálogo de Banco Agrícola'),
            ('crear_estados_banco_agricola', 'Estados financieros de Banco Agrícola'),
            ('crear_mapeos_banco_agricola', 'Mapeos de ratios de Banco Agrícola'),
        ]
        
        for comando, descripcion in comandos_agricola:
            self.stdout.write(self.style.SUCCESS(f'\n  → {descripcion}...'))
            try:
                call_command(comando)
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f'  ✗ Error ejecutando {comando}: {str(e)}'
                    )
                )
                return
        
        # Crear datos de Banco Atlántida
        self.stdout.write(
            self.style.WARNING(
                f'\n[3/3] Creando datos completos de Banco Atlántida...'
            )
        )
        self.stdout.write(self.style.WARNING('-' * 80))
        
        comandos_atlantida = [
            ('crear_catalogo_banco_atlantida', 'Catálogo de Banco Atlántida'),
            ('crear_estados_banco_atlantida', 'Estados financieros de Banco Atlántida'),
            ('crear_mapeos_banco_atlantida', 'Mapeos de ratios de Banco Atlántida'),
        ]
        
        for comando, descripcion in comandos_atlantida:
            self.stdout.write(self.style.SUCCESS(f'\n  → {descripcion}...'))
            try:
                call_command(comando)
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(
                        f'  ✗ Error ejecutando {comando}: {str(e)}'
                    )
                )
                return
        
        # Resumen final
        self.stdout.write(
            self.style.SUCCESS(
                '\n' + '='*80 +
                '\n✓ DATOS DE DEMOSTRACIÓN CREADOS EXITOSAMENTE' +
                '\n' + '='*80 +
                '\n\n📊 Resumen de datos creados:' +
                '\n' +
                '\n🏦 BANCO AGRÍCOLA:' +
                '\n  • Catálogo con ~50 cuentas contables' +
                '\n  • 3 Balances Generales (2022, 2023, 2024)' +
                '\n  • 3 Estados de Resultados (2022, 2023, 2024)' +
                '\n  • 13 Mapeos de ratios financieros' +
                '\n' +
                '\n🏦 BANCO ATLÁNTIDA:' +
                '\n  • Catálogo con ~50 cuentas contables' +
                '\n  • 3 Balances Generales (2022, 2023, 2024)' +
                '\n  • 3 Estados de Resultados (2022, 2023, 2024)' +
                '\n  • 13 Mapeos de ratios financieros' +
                '\n' +
                '\n📈 RATIOS FINANCIEROS (compartidos):' +
                '\n  • 6 Ratios predefinidos (Liquidez, Endeudamiento, Rentabilidad)' +
                '\n' +
                '\n🎉 ¡Sistema completo con 2 bancos listos para comparación!' +
                '\n' + '='*80 + '\n'
            )
        )
