# Instrucciones para el Proyecto: appquantum

Este archivo es un recordatorio para actualizar el repositorio Git local y sincronizarlo con el repositorio remoto en GitHub para el proyecto `appquantum`.

## 1. Recordatorio: Gestión de Credenciales de Git en Windows

*   **Usuario de GitHub Asociado:** `progxefero666`
*   **Correo Electrónico Asociado:** `correoxefero@gmail.com`
*   Git en Windows, a través del **Administrador de Credenciales de Windows** (o Git Credential Manager Core), debería gestionar tus credenciales automáticamente después del primer push/pull exitoso.
*   Si se solicitan credenciales inesperadamente, verifica el Administrador de Credenciales o considera usar/renovar un Personal Access Token (PAT).

## 2. Detalles del Repositorio `appquantum`

*   **URL del Repositorio en GitHub:** `https://github.com/progxefero666/appquantum`
*   **Rama Principal Designada:** `main`
*   **Ruta Local del Proyecto (esperada):** `C:\python\apps\appquantum`

## 3. Comandos para Actualizar el Repositorio

Los siguientes comandos asumen que estás en la raíz de la carpeta de tu proyecto `appquantum` (`C:\python\apps\appquantum`) en la terminal y que el repositorio ya está inicializado y conectado al remoto.

```bash
# 0. (Opcional, si necesitas cambiar la configuración de Git solo para este repo)
# git config user.name "progxefero666"
# git config user.email "correoxefero@gmail.com"

# 1. Verifica el estado de tus archivos y la rama actual
# (Asegúrate de estar en la rama 'main' o en la rama que quieres actualizar)
git status
# git branch (para ver la rama actual y otras)
# git checkout main (si necesitas cambiar a la rama 'main')

# 2. Revisa si hay cambios remotos que necesites incorporar antes de hacer push (opcional pero recomendado)
# git pull origin main

# 3. Añade los archivos modificados/nuevos al staging area
# Para añadir todos los cambios:
git add .
# O para añadir archivos específicos:
# git add ruta/al/archivo1.py ruta/al/archivo2.py

# 4. Realiza el commit con un mensaje descriptivo
git commit -m "Tu mensaje descriptivo sobre los cambios"

# 5. Sube los cambios a GitHub (a la rama 'main')
git push origin main
# Si la rama upstream ya está configurada, 'git push' podría ser suficiente.
```

## Pasos a Seguir Cuando Abras la Carpeta del Proyecto `appquantum`:

1.  Abre una terminal en la ruta local del proyecto: `C:\python\apps\appquantum`.
2.  Verifica el estado actual de tu repositorio con `git status` para ver si hay cambios sin confirmar.
3.  Si has realizado cambios y quieres subirlos, sigue los comandos de la sección 3 (principalmente `git add .`, `git commit -m "mensaje"`, y `git push origin main`).
4.  Es buena práctica hacer `git pull origin main` antes de empezar a trabajar o antes de hacer un push, para asegurarte de tener la última versión del repositorio remoto y evitar conflictos. 