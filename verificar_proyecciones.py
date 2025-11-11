#!/usr/bin/env python
"""
Script de verificación de la implementación del módulo de proyecciones.
Ejecutar: python verificar_proyecciones.py
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.conf import settings
from apps.proyecciones.models import Ventas, ProyeccionVenta


def verificar_implementacion():
    """
    Verificar que todos los componentes del módulo estén correctamente implementados.
    """
    print("🔍 Verificando implementación del módulo de proyecciones...\n")
    
    errores = []
    warnings = []
    
    # 1. Verificar que la app esté instalada
    print("✓ Verificando apps instaladas...")
    if 'apps.proyecciones' in settings.INSTALLED_APPS:
        print("  ✓ App 'apps.proyecciones' instalada")
    else:
        errores.append("❌ App 'apps.proyecciones' NO está en INSTALLED_APPS")
    
    # 2. Verificar modelos
    print("\n✓ Verificando modelos...")
    try:
        # Verificar que los modelos existen
        ventas_count = Ventas.objects.count()
        proyeccion_count = ProyeccionVenta.objects.count()
        print(f"  ✓ Modelo Ventas accesible ({ventas_count} registros)")
        print(f"  ✓ Modelo ProyeccionVenta accesible ({proyeccion_count} registros)")
    except Exception as e:
        errores.append(f"❌ Error con modelos: {str(e)}")
    
    # 3. Verificar templates
    print("\n✓ Verificando templates...")
    templates_dir = os.path.join('templates', 'proyecciones')
    if os.path.exists(templates_dir):
        print(f"  ✓ Directorio de templates existe: {templates_dir}")
        
        template_files = ['proyeccion_form.html', 'proyeccion_resultados.html']
        for template in template_files:
            template_path = os.path.join(templates_dir, template)
            if os.path.exists(template_path):
                print(f"  ✓ Template existe: {template}")
            else:
                errores.append(f"❌ Template NO existe: {template}")
    else:
        errores.append(f"❌ Directorio de templates NO existe: {templates_dir}")
    
    # 4. Verificar archivos de la app
    print("\n✓ Verificando archivos de la app...")
    app_dir = os.path.join('apps', 'proyecciones')
    app_files = ['models.py', 'views.py', 'urls.py', 'admin.py', 'tests.py']
    for file in app_files:
        file_path = os.path.join(app_dir, file)
        if os.path.exists(file_path):
            print(f"  ✓ Archivo existe: {file}")
        else:
            errores.append(f"❌ Archivo NO existe: {file}")
    
    # 5. Verificar URLs
    print("\n✓ Verificando configuración de URLs...")
    try:
        from apps.proyecciones.urls import urlpatterns as proyecciones_urls
        print(f"  ✓ URLs de proyecciones configuradas ({len(proyecciones_urls)} rutas)")
    except ImportError as e:
        errores.append(f"❌ Error importando URLs: {str(e)}")
    
    # 6. Verificar vistas
    print("\n✓ Verificando vistas...")
    try:
        from apps.proyecciones.views import ProyeccionVentasView, GenerarProyeccionView
        print("  ✓ ProyeccionVentasView importada")
        print("  ✓ GenerarProyeccionView importada")
    except ImportError as e:
        errores.append(f"❌ Error importando vistas: {str(e)}")
    
    # 7. Verificar dependencias
    print("\n✓ Verificando dependencias...")
    try:
        import pandas
        print(f"  ✓ pandas instalado (v{pandas.__version__})")
    except ImportError:
        errores.append("❌ pandas NO está instalado")
    
    try:
        import numpy
        print(f"  ✓ numpy instalado (v{numpy.__version__})")
    except ImportError:
        errores.append("❌ numpy NO está instalado")
    
    try:
        import openpyxl
        print(f"  ✓ openpyxl instalado (v{openpyxl.__version__})")
    except ImportError:
        errores.append("❌ openpyxl NO está instalado")
    
    # 8. Verificar documentación
    print("\n✓ Verificando documentación...")
    doc_files = [
        'apps/proyecciones/README.md',
        'apps/proyecciones/PLANTILLA_EXCEL.md',
        'IMPLEMENTACION_PROYECCIONES.md'
    ]
    for doc in doc_files:
        if os.path.exists(doc):
            print(f"  ✓ Documentación existe: {doc}")
        else:
            warnings.append(f"⚠ Documentación NO existe: {doc}")
    
    # Resumen
    print("\n" + "="*60)
    print("📊 RESUMEN DE VERIFICACIÓN")
    print("="*60)
    
    if errores:
        print(f"\n❌ Se encontraron {len(errores)} errores:")
        for error in errores:
            print(f"  {error}")
    else:
        print("\n✓ ¡No se encontraron errores!")
    
    if warnings:
        print(f"\n⚠ Se encontraron {len(warnings)} advertencias:")
        for warning in warnings:
            print(f"  {warning}")
    
    if not errores and not warnings:
        print("\n🎉 ¡Implementación completada exitosamente!")
        print("\n📝 Próximos pasos:")
        print("  1. Ejecutar: python manage.py runserver")
        print("  2. Acceder a: http://127.0.0.1:8000/proyecciones/")
        print("  3. Generar plantilla: python generar_plantilla_ejemplo.py")
        print("  4. Probar con datos de ejemplo")
    
    print("\n" + "="*60)
    
    return len(errores) == 0


if __name__ == '__main__':
    try:
        exito = verificar_implementacion()
        sys.exit(0 if exito else 1)
    except Exception as e:
        print(f"\n❌ Error crítico durante la verificación: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
