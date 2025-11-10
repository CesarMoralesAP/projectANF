from django.core.management.base import BaseCommand
from apps.empresas.models import Sector, Empresa


class Command(BaseCommand):
    """
    Comando para crear datos de demostración (sectores y empresas).
    """
    help = 'Crea sectores y empresas de demostración'

    def handle(self, *args, **options):
        # Crear sectores
        sectores_data = [
            {'nombre': 'Mineria'},
            {'nombre': 'Bancario'},
            {'nombre': 'Comercio'},
            {'nombre': 'Servicios'},
        ]
        
        for sector_data in sectores_data:
            sector, created = Sector.objects.get_or_create(
                nombre=sector_data['nombre']
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Sector creado: {sector.nombre}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'⚠ Sector ya existe: {sector.nombre}')
                )

        # Crear empresa de ejemplo
        try:
            sector_mineria = Sector.objects.get(nombre='Mineria')
            empresa, created = Empresa.objects.get_or_create(
                nombre='Banco agrícola',
                defaults={
                    'sector': sector_mineria,
                }
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Empresa creada: {empresa.nombre}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'⚠ Empresa ya existe: {empresa.nombre}')
                )
        except Sector.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('✗ No se encontró el sector Mineria')
            )

        self.stdout.write(
            self.style.SUCCESS('\n✓ Datos de demostración listos.')
        )

