from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = 'Crea los roles (grupos) del sistema con sus permisos correspondientes'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Creando roles y asignando permisos...'))
        
        # ============================================
        # GRUPO 1: ADMINISTRADOR (Acceso total)
        # ============================================
        admin_group, created = Group.objects.get_or_create(name='Administrador')
        
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Grupo "Administrador" creado'))
        else:
            self.stdout.write(self.style.WARNING('○ Grupo "Administrador" ya existía'))
        
        # Asignar TODOS los permisos al administrador
        all_permissions = Permission.objects.all()
        admin_group.permissions.set(all_permissions)
        self.stdout.write(self.style.SUCCESS(f'  → Asignados {all_permissions.count()} permisos'))
        
        
        # ============================================
        # GRUPO 2: GERENTE DE ADMINISTRACIÓN
        # (Todos los permisos EXCEPTO delete)
        # ============================================
        gerente_group, created = Group.objects.get_or_create(name='Gerente de Administración')
        
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Grupo "Gerente de Administración" creado'))
        else:
            self.stdout.write(self.style.WARNING('○ Grupo "Gerente de Administración" ya existía'))
        
        # Obtener todos los permisos EXCEPTO los de eliminar (delete)
        permisos_gerente = Permission.objects.exclude(codename__startswith='delete_')
        gerente_group.permissions.set(permisos_gerente)
        self.stdout.write(self.style.SUCCESS(f'  → Asignados {permisos_gerente.count()} permisos (sin delete)'))
        
        
        # ============================================
        # RESUMEN
        # ============================================
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('RESUMEN DE ROLES CREADOS:'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(f'')
        self.stdout.write(f'📋 Administrador:')
        self.stdout.write(f'   - Permisos totales: {admin_group.permissions.count()}')
        self.stdout.write(f'   - Puede: Ver, Crear, Editar y ELIMINAR')
        self.stdout.write(f'')
        self.stdout.write(f'📋 Gerente de Administración:')
        self.stdout.write(f'   - Permisos totales: {gerente_group.permissions.count()}')
        self.stdout.write(f'   - Puede: Ver, Crear y Editar')
        self.stdout.write(f'   - NO puede: Eliminar')
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('✅ Roles configurados correctamente'))
