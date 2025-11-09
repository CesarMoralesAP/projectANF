import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from apps.estados.models import Sector

# === CREAR SECTOR ===
def crear_sector(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()

        nombres = request.POST.getlist('ratio_name[]')
        valores = request.POST.getlist('ratio_value[]')

        try:
            data = {nombres[i]: float(valores[i]) for i in range(len(nombres)) if nombres[i].strip() != ""}
        except ValueError:
            messages.error(request, "Verifica que todos los valores sean numéricos válidos.")
            return redirect('crear_sector')

        Sector.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            valor_referencia=json.dumps(data)
        )
        messages.success(request, "Sector registrado correctamente.")
        return redirect('listar_sectores')

    return render(request, 'estados/sector_form.html')


# === EDITAR SECTOR ===
def editar_sector(request, pk):
    sector = get_object_or_404(Sector, pk=pk)

    if request.method == 'POST':
        sector.nombre = request.POST.get('nombre', '').strip()
        sector.descripcion = request.POST.get('descripcion', '').strip()

        nombres = request.POST.getlist('ratio_name[]')
        valores = request.POST.getlist('ratio_value[]')

        try:
            data = {nombres[i]: float(valores[i]) for i in range(len(nombres)) if nombres[i].strip() != ""}
        except ValueError:
            messages.error(request, "Verifica que todos los valores sean numéricos válidos.")
            return redirect('editar_sector', pk=pk)

        sector.valor_referencia = json.dumps(data)
        sector.save()
        messages.success(request, "Sector actualizado correctamente.")
        return redirect('listar_sectores')

    # Cargar ratios ya guardados
    ratios = []
    if sector.valor_referencia:
        try:
            parsed = json.loads(sector.valor_referencia)
            if isinstance(parsed, dict):
                ratios = [(k, v) for k, v in parsed.items()]
        except Exception as e:
            print("Error al parsear JSON:", e)
            ratios = []

    context = {
        'sector': sector,
        'ratios': ratios,
    }
    return render(request, 'estados/sector_form.html', context)


# === LISTAR SECTORES ===
def listar_sectores(request):
    sectores = Sector.objects.all()
    return render(request, 'estados/sectores_list.html', {'sectores': sectores})


# === ELIMINAR SECTOR ===
def eliminar_sector(request, pk):
    sector = get_object_or_404(Sector, pk=pk)
    sector.delete()
    messages.success(request, "Sector eliminado correctamente.")
    return redirect('listar_sectores')
