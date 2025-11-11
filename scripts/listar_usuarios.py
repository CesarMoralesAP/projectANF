import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User

users = User.objects.all()
print('👥 Usuarios existentes:')
if users:
    for u in users:
        grupos = ', '.join([g.name for g in u.groups.all()]) if u.groups.exists() else 'Sin grupo'
        print(f'  - {u.username} | Superuser: {u.is_superuser} | Grupos: {grupos}')
else:
    print('  ⚠️  No hay usuarios creados')
