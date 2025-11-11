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

## Configuración de la Base de Datos

Este proyecto utiliza MySQL como motor de base de datos. Los siguientes pasos te guiarán para configurar tu base de datos local importando un backup existente.

### Prerrequisitos

Asegúrate de tener instalado el software de MySQL necesario.

1. **MySQL Community Server:**
    * **Versión Requerida:** 8.4.x LTS
    * **Descarga:** [MySQL Community Server 8.4 LTS](https://dev.mysql.com/downloads/mysql/)
    * Durante la instalación, se te pedirá que establezcas una contraseña para el usuario **`root`**. **Guarda esta contraseña**, es muy importante.
2. **MySQL Workbench:**
    * **Versión Requerida:** 8.0.x o superior
    * **Descarga:** [MySQL Workbench](https://dev.mysql.com/downloads/workbench/)

### Paso 1: Importar la Base de Datos desde el Backup

En lugar de crear la base de datos manualmente, la restauraremos desde un archivo de backup (`.sql`) usando MySQL Workbench.

1. Abre **MySQL Workbench** y conéctate a tu servidor de base de datos local usando el usuario `root` y la contraseña que estableciste durante la instalación.
2. Navega al menú superior y selecciona **`Server`** -> **`Data Import`**.
3. En la pantalla de "Import from Disk", selecciona la opción **`Import from Self-Contained File`**.
4. Busca y selecciona el archivo de backup **`projectanf_backup.sql`** (debe estar ubicado en la raíz del proyecto o en una carpeta designada).
5. En la sección **`Default Target Schema`**, deja que el script cree la base de datos automáticamente. Si el backup no contiene la instrucción `CREATE DATABASE`, selecciona "New" y crea un schema llamado `projectanf`.
6. Haz clic en el botón **`Start Import`** en la esquina inferior derecha para comenzar el proceso de restauración.

### Paso 2: Configurar las Variables de Entorno (Conexión Root)

Para simplificar la configuración de desarrollo local, nos conectaremos directamente con el usuario `root`.

1. **Crea un archivo `.env`** en la raíz de tu proyecto (a la misma altura que `manage.py`).
2. **Añade las credenciales** de tu usuario `root` al archivo `.env`. Reemplaza `tu_contraseña_de_root` con la contraseña real.

```ini
# Archivo: .env
# Variables de entorno para la configuración de la base de datos (desarrollo)

DB_NAME=projectanf
DB_USER=root
DB_PASSWORD=tu_contraseña_de_root
DB_HOST=127.0.0.1
DB_PORT=3306
```


### Paso 3: Conectar Django a la Base de Datos

1. **Actualiza la configuración de `DATABASES`** para usar estas variables:

```python
# En core/settings.py

DATABASES = {
    'default': {
        'ENGINE': 'mysql.connector.django',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
```

### Paso 4: Verificar Sincronización y Crear Administrador

1. **Verifica el estado de las migraciones:**
Como la base de datos fue importada, es probable que las tablas ya existan. Ejecuta `migrate` para asegurar que Django esté sincronizado.

```bash
python manage.py migrate
```

Si ves el mensaje "No migrations to apply", significa que todo está correcto.
2. **Crea un superusuario** para acceder al panel de administración de Django:

```bash
python manage.py createsuperuser
```

Sigue las instrucciones en pantalla para crear tu cuenta de administrador personal. 

O puedes crear datos de prueba iniciales con los comandos:

```bash
python manage.py crear_usuarios_demo
python manage.py crear_datos_demo
```

## Configuración Inicial del Proyecto

Si estás configurando el proyecto desde cero (sin un backup de base de datos), sigue estos pasos para inicializar la estructura de la base de datos y poblarla con datos de prueba.

### 1. Crear las Migraciones

Primero, asegúrate de que tu entorno virtual esté activado y que hayas configurado correctamente el archivo `.env` con las credenciales de tu base de datos MySQL.

```powershell
# Asegúrate de que el entorno virtual esté activado
venv\Scripts\Activate.ps1
```

Luego, crea todas las migraciones necesarias para las apps del proyecto:

```bash
# Crear las migraciones para todas las apps
python manage.py makemigrations
```

### 2. Aplicar las Migraciones

Aplica las migraciones para crear todas las tablas en la base de datos:

```bash
# Aplicar todas las migraciones
python manage.py migrate
```

Este comando creará todas las tablas necesarias según los modelos definidos en las apps: `empresas`, `catalogos`, `estados`, `parametros`, `analisis`, `graficas`, `proyecciones` y `usuarios`.

### 3. Crear Datos de Prueba

Una vez que la estructura de la base de datos esté lista, tienes varias opciones para poblarla con datos de ejemplo:

#### Opción A: Crear Datos Completos Automáticamente (Recomendado)

Este comando maestro ejecuta todos los subcomandos necesarios para crear un sistema completamente funcional con 2 bancos de ejemplo:

```bash
# Comando maestro que crea TODO (usuarios, sectores, empresas, ratios, catálogos, estados, mapeos)
python manage.py crear_todos_los_bancos_demo
```

Este comando creará:
- ✅ Usuarios de prueba (admin y usuario regular)
- ✅ Sectores económicos y empresas
- ✅ 6 Ratios financieros predefinidos (Liquidez, Endeudamiento, Rentabilidad)
- ✅ **Banco Agrícola**: Catálogo completo, 6 estados financieros (2022-2024), mapeos de ratios
- ✅ **Banco Atlántida**: Catálogo completo, 6 estados financieros (2022-2024), mapeos de ratios
