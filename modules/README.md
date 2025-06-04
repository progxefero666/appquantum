# Estructura de Módulos - AppQuantum

## Descripción

Esta carpeta contiene todos los módulos de la aplicación AppQuantum. Cada módulo está autocontenido en su propia carpeta con sus archivos HTML y JavaScript.

## Estructura

```
modules/
├── mathematical_tools/
│   ├── mathematical_tools.html
│   └── mathematical_tools.js
├── math_graphics/
│   ├── math_graphics.html
│   └── math_graphics.js
├── pandas_analytics/
│   ├── pandas_analytics.html
│   └── pandas_analytics.js
├── periodic_elements/
│   ├── periodic_elements.html
│   └── periodic_elements.js
├── python_notebooks/
│   ├── python_notebooks.html
│   └── python_notebooks.js
├── quantum_circuits/
│   ├── quantum_circuits.html
│   └── quantum_circuits.js
└── quantum_waves/
    ├── quantum_waves.html
    └── quantum_waves.js
```

## Módulos Disponibles

1. **Mathematical Tools** - Herramientas matemáticas (matrices y grafos)
2. **Math Graphics** - Visualización de gráficos matemáticos
3. **Pandas Analytics** - Análisis de datos con Pandas
4. **Periodic Elements** - Tabla periódica y análisis de elementos
5. **Python Notebooks** - Editor y ejecutor de código Python
6. **Quantum Circuits** - Visualización de circuitos cuánticos
7. **Quantum Waves** - Generación y análisis de ondas cuánticas

## Uso

Las rutas de los módulos están configuradas en `app.py` y son accesibles vía:
- `/mathematical-tools`
- `/math-graphics`
- `/pandas-analytics`
- `/periodic-elements`
- `/python-notebooks`
- `/quantum-circuits`
- `/quantum-waves`

## Desarrollo

Para añadir un nuevo módulo:
1. Crear una carpeta en `modules/nombre_modulo/`
2. Añadir `nombre_modulo.html` y `nombre_modulo.js`
3. Actualizar las rutas en `app.py`
4. Añadir la ruta del template en la configuración del loader de Flask 