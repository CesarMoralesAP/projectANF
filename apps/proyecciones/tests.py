from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.empresas.models import Empresa, Sector
from .models import Ventas, ProyeccionVenta

User = get_user_model()


class VentasModelTest(TestCase):
    """
    Tests para el modelo Ventas.
    """

    def setUp(self):
        # Crear sector
        self.sector = Sector.objects.create(
            nombre='Sector Test',
            descripcion='Descripción test'
        )
        
        # Crear empresa
        self.empresa = Empresa.objects.create(
            nombre='Empresa Test',
            sector=self.sector
        )

    def test_crear_venta(self):
        """Verificar que se puede crear una venta."""
        venta = Ventas.objects.create(
            empresa=self.empresa,
            anio=2023,
            mes=1,
            valor=50000.00
        )
        self.assertEqual(venta.empresa, self.empresa)
        self.assertEqual(venta.anio, 2023)
        self.assertEqual(venta.mes, 1)
        self.assertEqual(venta.valor, 50000.00)

    def test_str_venta(self):
        """Verificar el método __str__ de Ventas."""
        venta = Ventas.objects.create(
            empresa=self.empresa,
            anio=2023,
            mes=1,
            valor=50000.00
        )
        expected = f"{self.empresa} - 1/2023: 50000.00"
        self.assertEqual(str(venta), expected)

    def test_unique_together(self):
        """Verificar que no se pueden crear ventas duplicadas para la misma empresa/año/mes."""
        Ventas.objects.create(
            empresa=self.empresa,
            anio=2023,
            mes=1,
            valor=50000.00
        )
        
        # Intentar crear otra venta con los mismos datos debe fallar
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Ventas.objects.create(
                empresa=self.empresa,
                anio=2023,
                mes=1,
                valor=60000.00
            )


class ProyeccionVentaModelTest(TestCase):
    """
    Tests para el modelo ProyeccionVenta.
    """

    def setUp(self):
        # Crear sector
        self.sector = Sector.objects.create(
            nombre='Sector Test',
            descripcion='Descripción test'
        )
        
        # Crear empresa
        self.empresa = Empresa.objects.create(
            nombre='Empresa Test',
            sector=self.sector
        )

    def test_crear_proyeccion(self):
        """Verificar que se puede crear una proyección."""
        proyeccion = ProyeccionVenta.objects.create(
            empresa=self.empresa,
            anio=2024,
            mes=1,
            metodo='Minimos Cuadrados',
            valor_proyectado=55000.00
        )
        self.assertEqual(proyeccion.empresa, self.empresa)
        self.assertEqual(proyeccion.anio, 2024)
        self.assertEqual(proyeccion.mes, 1)
        self.assertEqual(proyeccion.metodo, 'Minimos Cuadrados')
        self.assertEqual(proyeccion.valor_proyectado, 55000.00)

    def test_str_proyeccion(self):
        """Verificar el método __str__ de ProyeccionVenta."""
        proyeccion = ProyeccionVenta.objects.create(
            empresa=self.empresa,
            anio=2024,
            mes=1,
            metodo='Minimos Cuadrados',
            valor_proyectado=55000.00
        )
        expected = f"{self.empresa} - Minimos Cuadrados (1/2024)"
        self.assertEqual(str(proyeccion), expected)


class ProyeccionViewsTest(TestCase):
    """
    Tests para las vistas del módulo de proyecciones.
    """

    def setUp(self):
        # Crear usuario
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Crear sector
        self.sector = Sector.objects.create(
            nombre='Sector Test',
            descripcion='Descripción test'
        )
        
        # Crear empresa
        self.empresa = Empresa.objects.create(
            nombre='Empresa Test',
            sector=self.sector
        )

    def test_proyeccion_form_requiere_login(self):
        """Verificar que la vista del formulario requiere login."""
        response = self.client.get('/proyecciones/')
        # Debe redirigir al login
        self.assertEqual(response.status_code, 302)
        self.assertIn('/usuarios/login/', response.url)

    def test_proyeccion_form_con_login(self):
        """Verificar que un usuario logueado puede acceder al formulario."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/proyecciones/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'proyecciones/proyeccion_form.html')
        self.assertIn('empresas', response.context)

    def test_generar_proyeccion_requiere_login(self):
        """Verificar que la generación de proyección requiere login."""
        response = self.client.post('/proyecciones/generar/')
        # Debe redirigir al login
        self.assertEqual(response.status_code, 302)
        self.assertIn('/usuarios/login/', response.url)
