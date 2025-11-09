from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    """
    Comando para actualizar el usuario admin con el nombre Kevin.
    """
    help = 'Actualiza el usuario admin con nombre Kevin'

    def handle(self, *args, **options):
        try:
            admin_user = User.objects.get(email='admin@sistema.com')
            admin_user.first_name = 'Kevin'
            admin_user.last_name = ''  # Limpiar apellido para mostrar solo "Kevin"
            admin_user.save()
            self.stdout.write(
                self.style.SUCCESS(f'✓ Usuario admin actualizado: {admin_user.get_full_name()} • Administrador')
            )
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('✗ Usuario admin no encontrado')
            )

