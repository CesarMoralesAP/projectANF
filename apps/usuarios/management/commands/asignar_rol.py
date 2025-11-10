from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()


class Command(BaseCommand):
    help = 'Asigna un usuario a un grupo específico (rol)'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Nombre de usuario')
        parser.add_argument('rol', type=str, help='Rol a asignar: "admin" o "gerente"')

    def handle(self, *args, **options):
        username = options['username']
        rol = options['rol'].lower()
        
        # Validar rol
        if rol not in ['admin', 'gerente', 'administrador']:
            self.stdout.write(
                self.style.ERROR('❌ Rol inválido. Use "admin" o "gerente"')
            )
            return
        
        # Obtener usuario
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'❌ Usuario "{username}" no existe')
            )
            return
        
        # Determinar el nombre del grupo
        if rol in ['admin', 'administrador']:
            grupo_nombre = 'Administrador'
        else:
            grupo_nombre = 'Gerente de Administración'
        
        # Obtener grupo
        try:
            grupo = Group.objects.get(name=grupo_nombre)
        except Group.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(
                    f'❌ El grupo "{grupo_nombre}" no existe. '
                    'Ejecuta: python manage.py crear_roles'
                )
            )
            return
        
        # Limpiar grupos anteriores y asignar el nuevo
        user.groups.clear()
        user.groups.add(grupo)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'✅ Usuario "{username}" asignado al grupo "{grupo_nombre}"'
            )
        )
        
        # Mostrar permisos
        permisos = user.get_all_permissions()
        self.stdout.write(f'📋 Permisos totales: {len(permisos)}')
