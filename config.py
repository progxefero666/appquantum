import os

# Obtener la ruta absoluta del directorio raíz del proyecto
# Esto asume que config.py está en la raíz del proyecto.
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# --- RUTAS BASE PARA EL CONTENIDO DEL USUARIO ---
# Modifica estas rutas según sea necesario para tu entorno.

# Opción 1: Ruta relativa dentro del proyecto (para desarrollo inicial y creación de carpetas)
# Usaremos 'data' como la carpeta contenedora dentro del proyecto.
APP_DATA_RELATIVE_PATH = 'data'
APP_DATA_DIR = os.path.join(PROJECT_ROOT, APP_DATA_RELATIVE_PATH)

# Derivamos las otras rutas de APP_DATA_DIR
CIRCUITS_BASE_DIR = os.path.join(APP_DATA_DIR, 'circuits')
GRAPHS_BASE_DIR = os.path.join(APP_DATA_DIR, 'graphs')
NOTEBOOKS_BASE_DIR = os.path.join(APP_DATA_DIR, 'notebooks')
DATASETS_BASE_DIR = os.path.join(APP_DATA_DIR, 'datasets')

# Opción 2: Ejemplo de rutas absolutas (para ilustrar cómo se cambiaría)
# Si descomentas estas, asegúrate de que las carpetas existan o créalas.
#
# Para Windows (ejemplo que me diste, usando barras invertidas escapadas o raw strings):
# APP_DATA_DIR_WIN_EXAMPLE = r'C:\python\apps\appquantum\data' 
# o APP_DATA_DIR_WIN_EXAMPLE = 'C:/python/apps/appquantum/data' # Python maneja bien / en Windows
#
# CIRCUITS_BASE_DIR_WIN_EXAMPLE = os.path.join(APP_DATA_DIR_WIN_EXAMPLE, 'circuits')
# GRAPHS_BASE_DIR_WIN_EXAMPLE = os.path.join(APP_DATA_DIR_WIN_EXAMPLE, 'graphs')
# NOTEBOOKS_BASE_DIR_WIN_EXAMPLE = os.path.join(APP_DATA_DIR_WIN_EXAMPLE, 'notebooks')
# DATASETS_BASE_DIR_WIN_EXAMPLE = os.path.join(APP_DATA_DIR_WIN_EXAMPLE, 'datasets')
#
# Para Linux/macOS:
# APP_DATA_DIR_LINUX_EXAMPLE = '/srv/appquantum_data'
# CIRCUITS_BASE_DIR_LINUX_EXAMPLE = os.path.join(APP_DATA_DIR_LINUX_EXAMPLE, 'circuits')
# etc.


# --- Asegurarse de que los directorios base (para la Opción 1) existan ---
# Esta lógica creará las carpetas si no existen cuando se importa config.py por primera vez.
def ensure_directories():
    print(f"Asegurando directorios bajo: {APP_DATA_DIR}")
    for dir_path in [APP_DATA_DIR, CIRCUITS_BASE_DIR, GRAPHS_BASE_DIR, NOTEBOOKS_BASE_DIR, DATASETS_BASE_DIR]:
        if not os.path.exists(dir_path):
            try:
                os.makedirs(dir_path)
                print(f"Directorio creado: {dir_path}")
            except OSError as e:
                print(f"Error al crear directorio {dir_path}: {e}")
        else:
            print(f"Directorio ya existe: {dir_path}")

# Llamamos a la función para asegurar los directorios al cargar este módulo de configuración.
# Esto es conveniente para el desarrollo. En producción, podrías manejar la creación de directorios
# como parte de tu script de despliegue.
ensure_directories()

print(f"Configuración de rutas cargada. Usando APP_DATA_DIR: {APP_DATA_DIR}") 