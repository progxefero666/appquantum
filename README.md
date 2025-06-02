# 🚀 AppQuantum - Aplicación de Aprendizaje Científico

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 Descripción

AppQuantum es una aplicación educativa interactiva desarrollada con Flask que integra múltiples herramientas científicas para el aprendizaje de química, física cuántica, matemáticas y programación. La aplicación ofrece visualizaciones interactivas, simulaciones cuánticas y análisis de datos científicos.

## ✨ Características Principales

### 🧪 Módulo de Química
- Tabla periódica interactiva con información detallada de elementos
- Visualización de estructuras moleculares
- Gráficos de orbitales atómicos
- Base de datos SQLite con propiedades químicas

### ⚛️ Módulo de Circuitos Cuánticos
- Creación y visualización de circuitos cuánticos usando Qiskit
- Simulación de estados cuánticos
- Generación de estados de Bell
- Visualización de esferas de Bloch

### 📊 Herramientas Matemáticas
- Operaciones con matrices
- Teoría de grafos
- Análisis de datos con Pandas
- Visualizaciones matemáticas con matplotlib

### 🎨 Módulo de Gráficos
- Visualizaciones 3D interactivas
- Gráficos de funciones matemáticas
- Representaciones de datos científicos
- Exportación de gráficos en múltiples formatos

### 📈 Análisis de Datos
- Datasets científicos precargados
- Herramientas de análisis estadístico
- Visualización de datos experimentales
- Procesamiento de datos con Pandas

## 🛠️ Requisitos del Sistema

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Sistema operativo: Windows, macOS o Linux

## 📦 Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/progxefero666/appquantum.git
cd appquantum
```

2. **Crear un entorno virtual**
```bash
python -m venv venv
```

3. **Activar el entorno virtual**

Windows:
```bash
.\venv\Scripts\activate
```

macOS/Linux:
```bash
source venv/bin/activate
```

4. **Instalar las dependencias**
```bash
pip install -r requirements.txt
```

## 🚀 Uso

1. **Iniciar la aplicación Flask**
```bash
python app.py
```

2. **Abrir el navegador**
   - Navegar a: `http://localhost:5000`

3. **Explorar los módulos**
   - Seleccionar cualquier módulo desde la interfaz principal
   - Interactuar con las herramientas y visualizaciones

## 📁 Estructura del Proyecto

```
appquantum/
├── app.py                  # Aplicación Flask principal
├── main.py                 # Punto de entrada alternativo
├── requirements.txt        # Dependencias del proyecto
├── config.py              # Configuración de la aplicación
│
├── src/                   # Código fuente principal
│   ├── chemical/          # Módulos de química
│   ├── quantum/           # Módulos cuánticos
│   ├── math/              # Herramientas matemáticas
│   ├── physics/           # Módulos de física
│   ├── database/          # Gestión de base de datos
│   ├── modules/           # Módulos de la aplicación
│   └── utils/             # Utilidades generales
│
├── public/                # Archivos públicos
│   ├── circuits/          # Circuitos cuánticos
│   └── graphs/            # Scripts de gráficos
│
├── data/                  # Datos de la aplicación
│   ├── datasets/          # Conjuntos de datos científicos
│   ├── circuits/          # Definiciones de circuitos
│   └── elements.db        # Base de datos de elementos
│
├── templates/             # Plantillas HTML
└── static/                # Archivos estáticos (CSS, JS)
```

## 🔧 Configuración

La aplicación se puede configurar modificando el archivo `config.py`:

```python
# Configuración del servidor
HOST = 'localhost'
PORT = 5000
DEBUG = True

# Rutas de datos
DATA_DIR = 'data'
PUBLIC_DIR = 'public'
```

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Para contribuir:

1. Fork el proyecto
2. Crea una rama para tu característica (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 🐛 Reporte de Errores

Si encuentras algún error, por favor abre un issue en GitHub incluyendo:
- Descripción del error
- Pasos para reproducirlo
- Sistema operativo y versión de Python
- Mensajes de error relevantes

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## 👨‍💻 Autor

**progxefero666**
- GitHub: [@progxefero666](https://github.com/progxefero666)
- Email: correoxefero@gmail.com

## 🙏 Agradecimientos

- [Qiskit](https://qiskit.org/) por las herramientas de computación cuántica
- [Flask](https://flask.palletsprojects.com/) por el framework web
- [matplotlib](https://matplotlib.org/) por las capacidades de visualización
- La comunidad de código abierto por las increíbles bibliotecas utilizadas

---

⭐ Si te gusta este proyecto, ¡no olvides darle una estrella en GitHub! ⭐ 