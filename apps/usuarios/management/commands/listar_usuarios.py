from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Lista todos los usuarios con sus roles asignados'

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(self.style.SUCCESS('👥 USUARIOS DEL SISTEMA'))
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write('')
        
        if users:
            for user in users:
                grupos = list(user.groups.values_list('name', flat=True))
                grupos_str = ', '.join(grupos) if grupos else 'Sin grupo asignado'
                
                self.stdout.write(f'📧 Usuario: {user.username}')
                self.stdout.write(f'   Email: {user.email or "No configurado"}')
                self.stdout.write(f'   Superuser: {"✅ Sí" if user.is_superuser else "❌ No"}')
                self.stdout.write(f'   Grupos: {grupos_str}')
                self.stdout.write('')
        else:
            self.stdout.write(self.style.WARNING('⚠️  No hay usuarios creados'))
            self.stdout.write('')
            self.stdout.write('Crea un superusuario con:')
            self.stdout.write('  python manage.py createsuperuser')
        
        self.stdout.write(self.style.SUCCESS('=' * 70))
