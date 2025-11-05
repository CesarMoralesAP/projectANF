# PROJECTANF: Analisis de estados financieros

Una aplicación web desarrollada con Django para el procesamiento de estados financieros. Esta herramienta permite a los usuarios gestionar catálogos de cuentas, ingresar balances y estados de resultados para períodos específicos y generar automáticamente reportes sobre ratios financieros y graficos de comparación.

## Tabla de Contenidos

- [Instalación](#instalaci%C3%B3n)
- [Configuración de la Base de Datos](#configuraci%C3%B3n-de-la-base-de-datos)
- [Uso](#uso)
- [Ejecutar Pruebas](#ejecutar-pruebas)


## Instalación

Sigue estos pasos para configurar el entorno de desarrollo en tu máquina local.

### Prerrequisitos

Asegúrate de tener instalado el siguiente software:

* [Python](https://www.python.org/downloads/) (se recomienda la versión 3.10 o superior)
* [VSCode](https://code.visualstudio.com/)
* [Git](https://git-scm.com/downloads/)


### Pasos para la Configuración Local

1. **Clona el repositorio:**
Abre tu terminal, navega al directorio donde quieras guardar el proyecto y clona el repositorio.

```bash
git clone https://github.com/CesarMoralesAP/projectANF.git
cd projectANF
```

2. **Crea y activa un entorno virtual:**
Se utiliza un entorno virtual para aislar las dependencias del proyecto y evitar conflictos con otros proyectos.

```bash
# Crear la carpeta del entorno virtual llamada 'venv'
python -m venv venv
```

Ahora, activa el entorno:
    * **Windows (PowerShell):**

```powershell
# Nota: Si recibes un error de política de ejecución, ejecuta primero este comando:
# Set-ExecutionPolicy Unrestricted -Scope Process
venv\Scripts\Activate.ps1
```

Tu línea de comandos ahora debería mostrar `(venv)` al principio.
3. **Instala las dependencias del proyecto:**
Todos los paquetes de Python necesarios están listados en el archivo `requirements.txt`. Usa `pip` para instalarlos.

```bash
# Asegúrate de que tu entorno virtual esté activado
python -m pip install -r requirements.txt
```

*Este comando lee el archivo `requirements.txt` e instala las versiones específicas de Django y otras librerías necesarias.*
4. **Verifica la instalación (Opcional):**
Puedes confirmar que `pip` y `Django` se instalaron correctamente dentro de tu entorno virtual.

```bash
# Verifica la versión de pip (debería apuntar a la carpeta 'venv')
python -m pip --version

# Verifica la versión de Django instalada
django-admin --version
```

5. **Ejecuta el servidor de desarrollo:**
Una vez instaladas las dependencias, puedes iniciar el servidor de desarrollo de Django.

```bash
python manage.py runserver
```

6. **Accede a la aplicación:**
El servidor se iniciará en `http://127.0.0.1:8000`. Abre esta URL en tu navegador web y deberías ver la página de bienvenida de Django, confirmando que la instalación fue exitosa.
