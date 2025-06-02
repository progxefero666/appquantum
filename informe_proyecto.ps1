# Obtener la ruta absoluta del directorio donde el script se ejecuta.
# Esto asegura que el script trabaje con rutas relativas a su propia ubicación,
# asumiendo que el script está en la raíz del proyecto.
$ScriptBaseDir = (Split-Path -Parent $MyInvocation.MyCommand.Definition)
Set-Location $ScriptBaseDir # Cambia la ubicación actual de PowerShell a esta carpeta.

# Nombre del archivo de salida
$OutputFileName = "ProjectSummary.txt"

# Eliminar el archivo de salida si ya existe para empezar limpio
if (Test-Path $OutputFileName) {
    Remove-Item $OutputFileName
}

# --- LIMPIEZA DE ARCHIVOS TEMPORALES DE PYTHON (como solicitaste) ---
Write-Host "Limpiando archivos temporales de Python (pycache, .pyc)..."
Get-ChildItem -Path . -Include __pycache__, *.pyc -Recurse -ErrorAction SilentlyContinue | Remove-Item -Force -Recurse -ErrorAction SilentlyContinue
Write-Host "Limpieza completada."
Write-Host "" # Línea en blanco para separación

# --- Extraer nombre del proyecto de pyproject.toml si está disponible ---
$projectName = "Proyecto Python" # Valor por defecto si no se encuentra el nombre
$pyprojectTomlPath = Join-Path $ScriptBaseDir "pyproject.toml"
if (Test-Path $pyprojectTomlPath) {
    try {
        # Lee el contenido del TOML y busca la línea 'name = "..."'
        $tomlContent = Get-Content $pyprojectTomlPath | Out-String
        if ($tomlContent -match 'name\s*=\s*"([^"]+)"') {
            $projectName = $Matches[1]
        }
    } catch {
        # En caso de error leyendo el TOML, se mantiene el nombre por defecto
        Write-Warning "No se pudo leer el nombre del proyecto de pyproject.toml."
    }
}

# Añadir una cabecera al archivo de resumen
Add-Content -Path $OutputFileName -Value "--- Resumen del Proyecto: $projectName ---"
Add-Content -Path $OutputFileName -Value "Generado el: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Add-Content -Path $OutputFileName -Value "" # Línea en blanco

# --- Sección 1: Contenido de archivos importantes ---

$ImportantFiles = @("pyproject.toml", "requirements.txt", "main.py")

foreach ($file in $ImportantFiles) {
    $filePath = Join-Path $ScriptBaseDir $file
    if (Test-Path $filePath) {
        Add-Content -Path $OutputFileName -Value "--- Contenido de: /$file ---"
        Get-Content -Path $filePath | Add-Content -Path $OutputFileName
        Add-Content -Path $OutputFileName -Value "" # Línea en blanco
        Add-Content -Path $OutputFileName -Value "" # Otra línea en blanco para separación
    } else {
        Add-Content -Path $OutputFileName -Value "--- El archivo: /$file NO ENCONTRADO ---"
        Add-Content -Path $OutputFileName -Value "" # Línea en blanco
        Add-Content -Path $OutputFileName -Value "" # Otra línea en blanco para separación
    }
}

# --- Sección 2: Estructura de directorios (con formato de árbol) ---

# Función auxiliar para generar el árbol de directorios recursivamente
function Get-TreeStructure {
    param (
        [string]$Path,
        [int]$Level = 0
    )
    process {
        # Ordenar directorios primero, luego archivos, ambos alfabéticamente
        $items = Get-ChildItem -LiteralPath $Path | Sort-Object { -not $_.PSIsContainer }, Name

        foreach ($item in $items) {
            $indentation = "  " * $Level # Dos espacios por nivel de indentación
            
            # Nombre a mostrar: solo el nombre del elemento, no la ruta completa
            $nameToShow = if ($item.PSIsContainer) { "$($item.Name)/" } else { $item.Name }

            Add-Content -Path $OutputFileName -Value "$indentation$nameToShow"

            # Si es un directorio, llamamos a la función recursivamente para sus contenidos
            if ($item.PSIsContainer) {
                Get-TreeStructure -Path $item.FullName -Level ($Level + 1)
            }
        }
    }
}

$TargetFolders = @("src", "public")

foreach ($folder in $TargetFolders) {
    $fullFolderPath = Join-Path $ScriptBaseDir $folder
    if (Test-Path $fullFolderPath -PathType Container) {
        Add-Content -Path $OutputFileName -Value "--- Estructura de Directorio: /$folder ---"
        # La función Get-TreeStructure ahora manejará la visualización recursiva desde la raíz del folder
        Get-TreeStructure -Path $fullFolderPath -Level 0 # Nivel inicial 0 para el contenido del folder
        Add-Content -Path $OutputFileName -Value "" # Línea en blanco
        Add-Content -Path $OutputFileName -Value "" # Otra línea en blanco para separación
    } else {
        Add-Content -Path $OutputFileName -Value "--- El directorio: /$folder NO ENCONTRADO ---"
        Add-Content -Path $OutputFileName -Value "" # Línea en blanco
        Add-Content -Path $OutputFileName -Value "" # Otra línea en blanco para separación
    }
}

Add-Content -Path $OutputFileName -Value "--- Fin del Resumen ---"

Write-Host "Resumen del proyecto guardado en '$OutputFileName'"