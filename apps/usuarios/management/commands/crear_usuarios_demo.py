from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction

User = get_user_model()


class Command(BaseCommand):
    """
    Comando para crear usuarios de demostración.
    """
    help = 'Crea usuarios de demostración (admin y usuario regular)'

    def handle(self, *args, **options):
        try:
            # Verificar conexión a la base de datos
            self.stdout.write('Verificando conexión a la base de datos...')
            User.objects.all().count()  # Test de conexión
            self.stdout.write(self.style.SUCCESS('✓ Conexión a la base de datos OK'))
            
            # Crear usuario admin
            admin_email = 'admin@sistema.com'
            admin_password = 'admin123'
            
            self.stdout.write(f'\nCreando usuario admin: {admin_email}')
            
            if User.objects.filter(email=admin_email).exists():
                self.stdout.write(
                    self.style.WARNING(f'⚠ Usuario admin ya existe: {admin_email}')
                )
            else:
                with transaction.atomic():
                    admin_user = User.objects.create_user(
                        username=admin_email,
                        email=admin_email,
                        password=admin_password,
                        is_staff=True,
                        is_superuser=True,
                        first_name='Administrador',
                        last_name='Sistema'
                    )
                    # Verificar que se creó correctamente
                    if admin_user.pk:
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'✓ Usuario admin creado exitosamente: {admin_email} / {admin_password}'
                            )
                        )
                        self.stdout.write(f'  ID: {admin_user.pk}, Username: {admin_user.username}')
                    else:
                        self.stdout.write(
                            self.style.ERROR('✗ Error: Usuario admin no se guardó correctamente')
                        )

            # Crear usuario regular
            usuario_email = 'usuario@sistema.com'
            usuario_password = 'user123'
            
            self.stdout.write(f'\nCreando usuario regular: {usuario_email}')
            
            if User.objects.filter(email=usuario_email).exists():
                self.stdout.write(
                    self.style.WARNING(f'⚠ Usuario demo ya existe: {usuario_email}')
                )
            else:
                with transaction.atomic():
                    usuario = User.objects.create_user(
                        username=usuario_email,
                        email=usuario_email,
                        password=usuario_password,
                        is_staff=False,
                        is_superuser=False,
                        first_name='Usuario',
                        last_name='Demo'
                    )
                    # Verificar que se creó correctamente
                    if usuario.pk:
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'✓ Usuario demo creado exitosamente: {usuario_email} / {usuario_password}'
                            )
                        )
                        self.stdout.write(f'  ID: {usuario.pk}, Username: {usuario.username}')
                    else:
                        self.stdout.write(
                            self.style.ERROR('✗ Error: Usuario demo no se guardó correctamente')
                        )

            # Verificación final
            total_usuarios = User.objects.count()
            self.stdout.write(
                self.style.SUCCESS(f'\n✓ Proceso completado. Total de usuarios en BD: {total_usuarios}')
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'\n✗ Error al crear usuarios: {str(e)}')
            )
            import traceback
            self.stdout.write(self.style.ERROR(traceback.format_exc()))
            raise

