# 📚 Guía de Configuración para Nuevos Proyectos Git/GitHub

> Esta guía te ayudará a configurar tu entorno una sola vez para que todos tus futuros proyectos sean más fáciles de subir a GitHub.

## 🔧 Configuraciones Globales de Git (Hacer UNA SOLA VEZ)

### 1. Configurar tu identidad global
```bash
git config --global user.name "progxefero666"
git config --global user.email "correoxefero@gmail.com"
```

### 2. Usar 'main' como rama predeterminada
Para alinearse con el estándar actual de GitHub:
```bash
git config --global init.defaultBranch main
```

### 3. Configurar el manejo de finales de línea (Windows)
Evita los warnings de CRLF en Windows:
```bash
git config --global core.autocrlf true
```

### 4. Evitar el problema de "dubious ownership"
```bash
git config --global --add safe.directory *
```

### 5. Configurar un editor predeterminado (opcional)
```bash
# Para Visual Studio Code
git config --global core.editor "code --wait"

# Para Notepad++
git config --global core.editor "notepad++ -multiInst -notabbar -nosession -noPlugin"

# Para Notepad (Windows)
git config --global core.editor "notepad"
```

### 6. Configurar gestor de credenciales
Para no tener que escribir usuario/contraseña constantemente:
```bash
git config --global credential.helper manager-core
```

## 📝 Crear un .gitignore Global

### Paso 1: Crear el archivo
Crea un archivo llamado `.gitignore_global` en tu carpeta de usuario (`C:\Users\TuUsuario\`) con el siguiente contenido:

```gitignore
# ===== WINDOWS =====
Thumbs.db
ehthumbs.db
Desktop.ini
$RECYCLE.BIN/
*.cab
*.msi
*.msm
*.msp
*.lnk

# ===== MACOS =====
.DS_Store
.AppleDouble
.LSOverride
._*

# ===== LINUX =====
*~
.fuse_hidden*
.directory
.Trash-*

# ===== PYTHON =====
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
.env
*.egg-info/
pip-log.txt
pip-delete-this-directory.txt
.pytest_cache/
.coverage
htmlcov/

# ===== NODE.JS =====
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# ===== IDEs y EDITORES =====
# Visual Studio Code
.vscode/
*.code-workspace

# JetBrains (PyCharm, IntelliJ, etc.)
.idea/
*.iml
*.iws
*.ipr

# Sublime Text
*.sublime-project
*.sublime-workspace

# Vim
*.swp
*.swo
*~

# ===== OTROS =====
*.log
logs/
*.tmp
*.temp
.cache/
```

### Paso 2: Configurar Git para usar este archivo
```bash
git config --global core.excludesfile ~/.gitignore_global
```

## 🚀 Flujos de Trabajo para Nuevos Proyectos

### 📌 Opción A: Crear primero en local
```bash
# 1. En tu carpeta del proyecto
git init

# 2. Crear un README básico
echo "# Nombre de Mi Proyecto" > README.md

# 3. Agregar archivos
git add .
git commit -m "Initial commit"

# 4. Crear repo en GitHub (SIN PLANTILLA) y luego:
git remote add origin https://github.com/progxefero666/nombre-proyecto.git
git push -u origin main
```

### 📌 Opción B: Crear primero en GitHub (RECOMENDADO)
1. Crear repositorio en GitHub **SIN PLANTILLA** ⚠️
2. En tu terminal:
```bash
# Clonar el repositorio vacío
git clone https://github.com/progxefero666/nombre-proyecto.git
cd nombre-proyecto

# Agregar tus archivos
# (copiar archivos del proyecto aquí)

# Subir cambios
git add .
git commit -m "Initial commit"
git push
```

### 📌 Opción C: Usar GitHub CLI (LA MÁS SIMPLE)

#### Instalación de GitHub CLI
```bash
# Windows (con Chocolatey)
choco install gh

# Windows (con Scoop)
scoop install gh

# O descargar desde: https://cli.github.com/
```

#### Uso
```bash
# Autenticarse (solo la primera vez)
gh auth login

# Desde tu carpeta del proyecto
gh repo create nombre-proyecto --public --source=. --push
```

## 💡 Tips y Mejores Prácticas

### 1. Plantilla de .gitignore para proyectos Python/Flask
Crea un archivo `python_gitignore_template.txt` que puedas copiar a nuevos proyectos:
```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
dist/
*.egg-info/
.installed.cfg
*.egg

# Flask
instance/
.webassets-cache

# Environments
.env
.env.local
.env.*.local

# IDEs
.vscode/
.idea/
*.swp
*.swo

# Testing
.pytest_cache/
.coverage
htmlcov/

# Logs
*.log
logs/

# OS
.DS_Store
Thumbs.db
```

### 2. Estructura básica para nuevos proyectos
```
mi-proyecto/
├── README.md
├── .gitignore
├── requirements.txt (para Python)
├── LICENSE (opcional)
└── src/
    └── (tu código aquí)
```

### 3. Comandos Git más comunes
```bash
# Ver estado
git status

# Agregar cambios
git add .                    # Todos los archivos
git add archivo.py          # Archivo específico

# Hacer commit
git commit -m "Descripción clara del cambio"

# Subir cambios
git push

# Actualizar desde remoto
git pull

# Ver historial
git log --oneline

# Crear rama
git checkout -b nueva-rama

# Cambiar de rama
git checkout main
```

## 🔍 Verificar tu configuración
Para ver toda tu configuración actual de Git:
```bash
git config --list
```

Para ver solo la configuración global:
```bash
git config --global --list
```

## ⚠️ Solución de Problemas Comunes

### Error: "fatal: not a git repository"
```bash
git init
```

### Error: "fatal: remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/usuario/repo.git
```

### Error: "rejected - non-fast-forward"
```bash
git pull origin main --rebase
git push
```

### Cambiar URL del repositorio remoto
```bash
git remote set-url origin https://github.com/nuevo-usuario/nuevo-repo.git
```

## 📅 Checklist para Nuevo Proyecto

- [ ] Crear carpeta del proyecto
- [ ] Copiar .gitignore apropiado
- [ ] Crear README.md básico
- [ ] Inicializar git (`git init`) o clonar repo vacío
- [ ] Hacer primer commit
- [ ] Conectar con GitHub
- [ ] Push inicial
- [ ] Verificar en GitHub que todo esté correcto

---

💡 **Recuerda**: Con estas configuraciones hechas UNA VEZ, crear y subir nuevos proyectos será tan simple como 3-4 comandos. ¡No más problemas de configuración!

📌 **Nota**: Guarda este archivo en un lugar accesible para consultarlo cuando crees nuevos proyectos. 