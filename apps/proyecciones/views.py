import pandas as pd
import numpy as np
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from apps.empresas.models import Empresa
from .models import ProyeccionVenta, Ventas


class ProyeccionVentasView(LoginRequiredMixin, TemplateView):
    """
    Vista para cargar archivo Excel y generar proyección de ventas.
    """
    template_name = 'proyecciones/proyeccion_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['empresas'] = Empresa.objects.all().select_related('sector')
        return context


@method_decorator(require_http_methods(["POST"]), name='dispatch')
class GenerarProyeccionView(LoginRequiredMixin, View):
    """
    Vista para procesar el archivo Excel y generar proyecciones.
    """

    def post(self, request):
        empresa_id = request.POST.get('empresa')
        metodo = request.POST.get('metodo')
        archivo = request.FILES.get('archivo')

        # Validaciones básicas
        if not empresa_id or not metodo or not archivo:
            messages.error(request, "Por favor seleccione una empresa, método y archivo Excel.")
            return redirect('proyecciones:proyeccion_ventas')

        try:
            empresa = Empresa.objects.get(id=empresa_id)

            # Leer archivo Excel (espera columnas Año, Mes, Valor)
            df = pd.read_excel(archivo)
            if df.shape[1] < 3:
                messages.error(request, "El archivo debe tener las columnas: Año, Mes y Valor.")
                return redirect('proyecciones:proyeccion_ventas')

            # Tomar solo las primeras tres columnas y renombrarlas
            df = df.iloc[:, :3]
            df.columns = ['Año', 'Mes', 'Valor']
            df = df.dropna()

            # Convertir a tipos correctos
            df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce')
            df = df.dropna(subset=['Valor'])

            # ==========================
            # GUARDAR DATOS HISTÓRICOS EN BD
            # ==========================
            # Eliminar todos los datos históricos de ventas de esta empresa
            Ventas.objects.filter(empresa=empresa).delete()
            
            # Guardar los nuevos datos
            for _, row in df.iterrows():
                anio = int(row['Año'])
                mes = int(row['Mes'])
                valor = round(float(row['Valor']), 2)
                
                Ventas.objects.create(
                    empresa=empresa,
                    anio=anio,
                    mes=mes,
                    valor=valor
                )

            # Datos históricos
            valores_hist = df['Valor'].tolist()
            meses_hist = [f"{int(m)} {int(a)}" for a, m in zip(df['Año'], df['Mes'])]

            # Ejes para cálculo
            x = np.arange(1, len(valores_hist) + 1)
            y = np.array(valores_hist)

            # ==========================
            # CÁLCULO DE PROYECCIONES
            # ==========================
            meses_proj = []
            valores_proj = []
            ecuacion = None
            anio_proj = int(df['Año'].max()) + 1  # siguiente año a proyectar
            
            if metodo == 'Minimos Cuadrados':
                # Ajuste lineal: y = a + bx
                b, a = np.polyfit(x, y, 1)
                signo = "-" if a < 0 else "+"
                ecuacion = f"y = {b:.4f}x {signo} {abs(a):.4f}"
            
                x_proj = np.arange(len(x) + 1, len(x) + 13)
                valores_proj = a + b * x_proj
                meses_proj = [f"Mes {i - len(x)}" for i in x_proj]
            
            elif metodo == 'Incremento Absoluto':
                # Promedio de diferencias absolutas entre meses consecutivos
                incrementos = np.diff(y)
                promedio_absoluto = np.mean(incrementos)
            
                ultimo_valor = y[-1]
                valores_proj = []
                for i in range(12):
                    nuevo_valor = ultimo_valor + promedio_absoluto
                    valores_proj.append(nuevo_valor)
                    ultimo_valor = nuevo_valor
            
                meses_proj = [f"Mes {i+1}" for i in range(12)]
            
            elif metodo == 'Incremento Porcentual':
                # Promedio de variaciones porcentuales mes a mes
                variaciones = np.diff(y) / y[:-1]
                promedio_porcentual = np.mean(variaciones)
            
                ultimo_valor = y[-1]
                valores_proj = []
                for i in range(12):
                    nuevo_valor = ultimo_valor * (1 + promedio_porcentual)
                    valores_proj.append(nuevo_valor)
                    ultimo_valor = nuevo_valor
            
                meses_proj = [f"Mes {i+1}" for i in range(12)]
            
            else:
                messages.error(request, "Método de proyección no reconocido.")
                return redirect('cargar_proyeccion')
            
            # ==========================
            # GUARDAR EN BASE DE DATOS
            # ==========================
            for mes, valor in zip(meses_proj, valores_proj):
                mes_numero = int(mes.split()[-1])
                # Convertir y redondear a 2 decimales para decimal(15,2)
                valor_redondeado = round(float(valor), 2)
                ProyeccionVenta.objects.create(
                    empresa=empresa,
                    anio=anio_proj,
                    mes=mes_numero,
                    metodo=metodo,
                    valor_proyectado=valor_redondeado
                )

            # Empaquetar datos para tabla y gráfico
            proyecciones_tabla = list(zip(meses_proj, valores_proj))

            context = {
                'empresa': empresa,
                'anio': anio_proj,
                'metodo': metodo,
                'meses_hist': meses_hist,
                'valores_hist': valores_hist,
                'meses_proj': meses_proj,
                'valores_proj': list(map(float, valores_proj)),
                'ecuacion': ecuacion,
                'proyecciones_tabla': proyecciones_tabla,
            }

            messages.success(request, f"Proyección generada exitosamente para el año {anio_proj} con el método {metodo}.")
            return render(request, 'proyecciones/proyeccion_resultados.html', context)

        except Exception as e:
            messages.error(request, f"Error procesando el archivo: {str(e)}")
            return redirect('proyecciones:proyeccion_ventas')
