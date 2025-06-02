# AppSpyder - Plataforma de Aprendizaje Científico

AppSpyder es una aplicación web modular construida con Flask (Python) y JavaScript, diseñada para el aprendizaje interactivo y la visualización en diversas áreas científicas. Permite a los usuarios explorar conceptos a través de módulos especializados que ofrecen funcionalidades como ejecución de scripts, visualización de datos y herramientas matemáticas interactivas.

## Características Principales

*   **Interfaz Modular:** La aplicación se organiza en módulos, cada uno enfocado en un área científica o herramienta específica.
*   **Backend en Flask:** Gestiona la lógica de negocio, ejecución de código, análisis de datos y servicio de la API.
*   **Frontend Interactivo:** Construido con HTML, CSS y JavaScript vainilla, permite a los usuarios interactuar con los módulos y visualizar resultados.
*   **Visualización Dinámica:** Uso extensivo de Matplotlib, Seaborn, Qiskit y NetworkX para generar gráficos y diagramas en tiempo real.

## Sistema de Ventanas (Interfaz de Usuario)

La interfaz de usuario principal se divide en varias secciones:

1.  **Cabecera:**
    *   Título de la aplicación.
    *   Botones de selección de módulos: Permiten cambiar entre los diferentes módulos disponibles.

2.  **Contenedor Principal (dividido en dos paneles):**
    *   **Panel Izquierdo:**
        *   Controles específicos del módulo activo (por ejemplo, selectores de archivos, campos de entrada para parámetros, botones de acción como "Cargar", "Ejecutar", "Generar").
        *   Visualización de código fuente de scripts (si aplica).
        *   Previsualización de datos o estructuras (como matrices o grafos generados).
    *   **Panel Derecho (Panel de Resultados):**
        *   Muestra los resultados de las operaciones ejecutadas en el módulo activo.
        *   Esto puede incluir imágenes (gráficos, diagramas), texto (sumarios, logs, errores) o tablas.

## Módulos Implementados

### 1. Quantum Circuits (Circuitos Cuánticos) 🔬
*   **Descripción:** Permite cargar, visualizar y ejecutar scripts de Python que definen circuitos cuánticos utilizando Qiskit.
*   **Carga de Datos/Scripts:**
    *   Los scripts `.py` se almacenan en el directorio `public/circuits/`.
    *   El frontend lista los archivos disponibles mediante una llamada a la API (`/api/circuits/files`).
    *   El contenido del script seleccionado se carga y muestra (`/api/circuits/load/<filename>`).
*   **Funcionalidad:**
    *   Muestra el código fuente del script.
    *   Ejecuta el circuito (`/api/circuits/execute/<filename>`).
    *   Visualiza el diagrama del circuito (usando `qiskit.visualization.circuit_drawer` y `matplotlib`).
    *   Si el circuito tiene mediciones, simula la ejecución (usando `qiskit-aer`) y muestra un histograma de resultados y probabilidades.

### 2. Math Graphics (Gráficos Matemáticos) 📊
*   **Descripción:** Ejecuta scripts de Python que generan visualizaciones utilizando Matplotlib (y otras bibliotecas compatibles como Qiskit para esferas de Bloch).
*   **Carga de Datos/Scripts:**
    *   Los scripts `.py` se almacenan en el directorio `public/graphs/`.
    *   El frontend lista los archivos disponibles (`/api/graphics/files`).
    *   El contenido del script seleccionado se carga y muestra (`/api/graphics/load/<filename>`).
*   **Funcionalidad:**
    *   Ejecuta el script (`/api/graphics/execute/<filename>`).
    *   El backend (a través de `FileLoader`) intenta capturar la figura de Matplotlib generada por el script.
    *   La figura se envía como una imagen base64 al frontend para su visualización.

### 3. Periodic Elements (Elementos Periódicos) ⚛️
*   **Descripción:** Muestra información y visualizaciones de los elementos de la tabla periódica.
*   **Carga de Datos/Scripts:**
    *   Los datos de los elementos se cargan desde una base de datos (gestionada por `DatabaseManager`, probablemente un archivo JSON o similar).
    *   API endpoints: `/api/elements/all` para obtener todos los elementos y `/api/elements/search` para filtrar.
*   **Funcionalidad:**
    *   Permite buscar y filtrar elementos.
    *   Muestra detalles del elemento seleccionado.
    *   Genera una visualización completa del elemento (`/api/elements/visualize/<atomic_number>`) incluyendo:
        *   Gráfico de propiedades.
        *   Posición en la tabla periódica.
        *   Clasificación y configuración electrónica.
        *   Diagrama de estructura Bohr (simplificado).

### 4. Quantum Waves (Ondas Cuánticas) 🌊
*   **Descripción:** Permite generar y visualizar diferentes tipos de ondas cuánticas (seno, coseno, cuadrada, probabilidad) y sus propiedades.
*   **Carga de Datos/Scripts:** No carga scripts externos, los parámetros se definen en la UI.
*   **Funcionalidad:**
    *   Los usuarios definen parámetros como frecuencia, amplitud, fase y tipo de onda.
    *   El backend (`/api/waves/generate`) calcula la onda, su espectro de frecuencia, trayectoria en el espacio de fases y distribución de energía.
    *   Genera una figura Matplotlib con estas visualizaciones y la envía como imagen base64.
    *   Devuelve un resumen de las propiedades de la onda.

### 5. Data Analysis (Análisis de Datos con Pandas) 📈
*   **Descripción:** Permite cargar datasets de ejemplo y realizar análisis básicos y visualizaciones utilizando Pandas y Matplotlib/Seaborn.
*   **Carga de Datos/Scripts:**
    *   Los datasets se generan en el backend (`/api/pandas/load/<dataset_name>`) o podrían cargarse desde archivos en el futuro.
    *   Datasets de ejemplo: `sample_data`, `sales_data`, `scientific_data`.
*   **Funcionalidad:**
    *   Muestra una previsualización del dataset cargado (primeras filas, tipos de datos).
    *   Permite realizar diferentes tipos de análisis (`/api/pandas/analyze/<dataset>/<analysis_type>`) como:
        *   Resumen estadístico (`describe`).
        *   Matriz de correlación.
        *   Histogramas.
        *   Gráficos de dispersión.
        *   Diagramas de caja (Box plots).
    *   Los resultados gráficos se envían como imágenes base64.

### 6. Mathematical Tools (Herramientas Matemáticas) 🧮
*   **Descripción:** Proporciona herramientas para operaciones con matrices y teoría de grafos.
*   **Carga de Datos/Scripts:** Los datos (matrices, especificaciones de grafos) se generan o introducen a través de la UI.
*   **Funcionalidad:**
    *   **Operaciones con Matrices:**
        *   Creación de matrices (aleatorias, identidad, etc.) (`/api/math/matrix/create`).
        *   Análisis de matrices (eigenvalores, SVD, determinante, inversa, rango, etc.) (`/api/math/matrix/analyze`).
        *   Las matrices y resultados se muestran en formato textual/tabular.
    *   **Teoría de Grafos:**
        *   Creación de grafos (aleatorios, completos, ciclos, etc.) (`/api/math/graph/create`).
        *   Análisis de grafos (número de nodos/aristas, densidad, conectividad, diámetro, etc.) (`/api/math/graph/analyze`).
        *   Se genera una visualización del grafo usando NetworkX y Matplotlib, enviada como imagen base64.

## Estructura del Proyecto (Simplificada)

```
appquantum/
├── app.py                    # Archivo principal de la aplicación Flask (backend)
├── requirements.txt          # Dependencias de Python
├── README.md                 # Este archivo
├── public/                   # Archivos estáticos accesibles públicamente
│   ├── circuits/             # Scripts de circuitos cuánticos (.py)
│   └── graphs/               # Scripts de gráficos matemáticos (.py)
├── src/                      # Código fuente modularizado
│   ├── database/
│   │   └── db_manager.py     # Gestor de base de datos (para elementos, etc.)
│   ├── utils/
│   │   └── file_loader.py    # Utilidad para cargar y ejecutar scripts Python
│   │   └── module_manager.py # (Si existe, para configuración de módulos)
│   ├── chemical/
│   │   └── chemicalgraphs/
│   │       └── atomic_graphs.py # Lógica para gráficos atómicos
│   ├── quantum/
│   │   └── graph_circuit.py  # Lógica para dibujar circuitos Qiskit
│   └── ui/                     # (Potencialmente para clases de UI si se expande)
│       └── base_module.py    # (Ejemplo de clase base para módulos)
│       └── main_window.py    # (Podría ser de una versión anterior de escritorio)
├── templates/
│   └── index.html            # Archivo HTML principal (frontend)
└── static/                   # Archivos CSS, JS cliente, imágenes (si se separan de public)
    └── (css, js, images)
```

## Próximos Pasos / Mejoras Potenciales
*   Expandir la documentación de la API.
*   Añadir más tipos de análisis y visualizaciones.
*   Implementar carga de archivos por el usuario.
*   Mejorar la gestión de errores y feedback al usuario.
*   Añadir pruebas unitarias e integración.

---
Este `README.md` es un punto de partida. Te animo a que lo revises, corrijas y añadas cualquier detalle que consideres importante. 