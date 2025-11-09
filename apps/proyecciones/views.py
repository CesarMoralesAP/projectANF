import pandas as pd
import numpy as np
from django.shortcuts import render, redirect
from django.contrib import messages
from apps.estados.models import Empresa
from apps.proyecciones.models import ProyeccionVenta

# =====================================
# CARGAR ARCHIVO Y GENERAR PROYECCIÓN
# =====================================

def cargar_proyeccion(request):
    if request.method == 'POST':
        empresa_id = request.POST.get('empresa')
        metodo = request.POST.get('metodo')
        archivo = request.FILES.get('archivo')

        if not empresa_id or not metodo or not archivo:
            messages.error(request, "Por favor seleccione una empresa, método y archivo Excel.")
            return redirect('cargar_proyeccion')

        try:
            empresa = Empresa.objects.get(id=empresa_id)

            # Leer archivo Excel (espera columnas Año, Mes, Valor)
            df = pd.read_excel(archivo)
            if df.shape[1] < 3:
                messages.error(request, "El archivo debe tener las columnas: Año, Mes y Valor.")
                return redirect('cargar_proyeccion')

            # Tomar solo las primeras tres columnas y renombrarlas
            df = df.iloc[:, :3]
            df.columns = ['Año', 'Mes', 'Valor']
            df = df.dropna()

            # Convertir a tipos correctos
            df['Valor'] = pd.to_numeric(df['Valor'], errors='coerce')
            df = df.dropna(subset=['Valor'])

            # Datos históricos
            valores_hist = df['Valor'].tolist()
            meses_hist = [f"{m} {a}" for a, m in zip(df['Año'], df['Mes'])]

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

            elif metodo == 'Incremento Porcentual':
                incremento = ((valores_hist[-1] - valores_hist[0]) / valores_hist[0]) / len(valores_hist)
                valores_proj = [valores_hist[-1] * (1 + incremento) ** i for i in range(1, 13)]
                meses_proj = [f"Mes {len(x) + i}" for i in range(1, 13)]

            elif metodo == 'Incremento Absoluto':
                incremento = (valores_hist[-1] - valores_hist[0]) / len(valores_hist)
                valores_proj = [valores_hist[-1] + incremento * i for i in range(1, 13)]
                meses_proj = [f"Mes {len(x) + i}" for i in range(1, 13)]

            else:
                messages.error(request, "Método de proyección no reconocido.")
                return redirect('cargar_proyeccion')

            # ==========================
            # GUARDAR EN BASE DE DATOS
            # ==========================
            for mes, valor in zip(meses_proj, valores_proj):
                ProyeccionVenta.objects.create(
                    empresa=empresa,
                    anio=anio_proj,
                    mes=int(mes.split()[-1]),
                    metodo=metodo,
                    valor_proyectado=valor
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
            return redirect('cargar_proyeccion')

    # Si es GET, mostrar formulario
    empresas = Empresa.objects.all()
    return render(request, 'proyecciones/proyeccion_form.html', {'empresas': empresas})
