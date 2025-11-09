from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    """
    Comando para crear usuarios de demostración.
    """
    help = 'Crea usuarios de demostración (admin y usuario regular)'

    def handle(self, *args, **options):
        # Crear usuario admin
        admin_email = 'admin@sistema.com'
        admin_password = 'admin123'
        
        if not User.objects.filter(email=admin_email).exists():
            admin_user = User.objects.create_user(
                username=admin_email,
                email=admin_email,
                password=admin_password,
                is_staff=True,
                is_superuser=True,
                first_name='Administrador',
                last_name='Sistema'
            )
            self.stdout.write(
                self.style.SUCCESS(f'✓ Usuario admin creado: {admin_email} / {admin_password}')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'⚠ Usuario admin ya existe: {admin_email}')
            )

        # Crear usuario regular
        usuario_email = 'usuario@sistema.com'
        usuario_password = 'user123'
        
        if not User.objects.filter(email=usuario_email).exists():
            usuario = User.objects.create_user(
                username=usuario_email,
                email=usuario_email,
                password=usuario_password,
                is_staff=False,
                is_superuser=False,
                first_name='Usuario',
                last_name='Demo'
            )
            self.stdout.write(
                self.style.SUCCESS(f'✓ Usuario demo creado: {usuario_email} / {usuario_password}')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'⚠ Usuario demo ya existe: {usuario_email}')
            )

        self.stdout.write(
            self.style.SUCCESS('\n✓ Usuarios de demostración listos para usar.')
        )

