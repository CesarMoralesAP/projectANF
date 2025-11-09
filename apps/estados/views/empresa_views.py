from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from apps.estados.models import Empresa, Sector, Catalogo, Cuenta
from apps.estados.forms.empresa_forms import EmpresaForm
import openpyxl

# Listar empresas
def listar_empresas(request):
    empresas = Empresa.objects.all()
    return render(request, 'estados/empresas_list.html', {'empresas': empresas})

# Crear empresa
def crear_empresa(request):
    if request.method == 'POST':
        form = EmpresaForm(request.POST, request.FILES)
        if form.is_valid():
            empresa = form.save()

            # Procesar archivo Excel si fue subido
            catalogo_excel = request.FILES.get('catalogo_excel')
            if catalogo_excel:
                # Crear registro de catálogo vinculado a la empresa
                catalogo = Catalogo.objects.create(empresa=empresa)

                # Cargar el archivo Excel
                wb = openpyxl.load_workbook(catalogo_excel)
                hoja = wb.active  

                for fila in hoja.iter_rows(min_row=2, values_only=True):
                    codigo, nombre, tipo = fila
                    if codigo and nombre:
                        Cuenta.objects.create(
                            catalogo=catalogo,
                            codigo=str(codigo),
                            nombre=str(nombre),
                            tipo=str(tipo) if tipo else 'N/A'
                        )

                messages.success(request, "Empresa y catálogo creados correctamente.")
            else:
                messages.success(request, "Empresa creada sin catálogo.")

            return redirect('listar_empresas')
    else:
        form = EmpresaForm()

    return render(request, 'estados/empresa_form.html', {'form': form, 'accion': 'Crear'})

# Editar empresa
def editar_empresa(request, id):
    empresa = get_object_or_404(Empresa, id=id)
    catalogo_existente = Catalogo.objects.filter(empresa=empresa).exists()
    if request.method == 'POST':
        form = EmpresaForm(request.POST, instance=empresa)
        if form.is_valid():
            form.save()
            messages.success(request, "Empresa actualizada correctamente.")
            return redirect('listar_empresas')
    else:
        form = EmpresaForm(instance=empresa)
    return render(request, 'estados/empresa_form.html', {
        'form': form,
        'editando': True,
        'catalogo_existente': catalogo_existente
    })

# Eliminar empresa
def eliminar_empresa(request, pk):
    empresa = get_object_or_404(Empresa, pk=pk)
    if request.method == 'POST':
        empresa.delete()
        messages.success(request, "Empresa eliminada correctamente.")
        return redirect('listar_empresas')
    return render(request, 'estados/empresa_confirm_delete.html', {'empresa': empresa})