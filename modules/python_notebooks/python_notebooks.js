// Python Notebooks Module JavaScript

let selectedNotebook = null;

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
    loadNotebookList();
    setupEditor();
});

// Load list of notebooks
async function loadNotebookList() {
    try {
        const response = await fetch('/api/notebooks/files');
        const data = await response.json();
        
        const notebookList = document.getElementById('notebook-list');
        
        if (data.success && data.files && data.files.length > 0) {
            notebookList.innerHTML = '';
            
            data.files.forEach(file => {
                const notebookItem = document.createElement('div');
                notebookItem.className = 'notebook-item p-2 rounded cursor-pointer hover:bg-base-200 transition-colors flex items-center gap-2 text-sm';
                notebookItem.innerHTML = `
                    <i class="ti ti-file-code text-sm"></i>
                    <span class="flex-1 truncate">${file}</span>
                `;
                
                notebookItem.onclick = () => selectNotebook(file, notebookItem);
                notebookList.appendChild(notebookItem);
            });
        } else {
            notebookList.innerHTML = `
                <div class="alert alert-warning alert-sm">
                    <i class="ti ti-alert-circle"></i>
                    <span>No se encontraron notebooks</span>
                </div>
            `;
        }
    } catch (error) {
        console.error('Error loading notebooks:', error);
        document.getElementById('notebook-list').innerHTML = `
            <div class="alert alert-error alert-sm">
                <i class="ti ti-alert-circle"></i>
                <span>Error al cargar notebooks</span>
            </div>
        `;
    }
}

// Select notebook
function selectNotebook(filename, element) {
    selectedNotebook = filename;
    
    // Update visual selection
    document.querySelectorAll('.notebook-item').forEach(item => {
        item.classList.remove('bg-primary', 'text-primary-content');
    });
    element.classList.add('bg-primary', 'text-primary-content');
    
    // Update info
    document.getElementById('notebook-info').innerHTML = `
        <p class="font-semibold">${filename}</p>
        <p class="text-xs">Listo para cargar</p>
    `;
    
    // Enable buttons
    document.getElementById('load-btn').disabled = false;
    document.getElementById('execute-btn').disabled = false;
    
    showToast(`Notebook seleccionado: ${filename}`);
}

// Load notebook
async function loadNotebook() {
    if (!selectedNotebook) return;
    
    try {
        const response = await fetch(`/api/notebooks/load/${selectedNotebook}`);
        const data = await response.json();
        
        if (data.success) {
            const editor = document.getElementById('code-editor');
            editor.value = data.content;
            updateEditorStats();
            showToast('Notebook cargado correctamente', 'success');
        } else {
            showToast('Error al cargar el notebook: ' + data.error, 'error');
        }
    } catch (error) {
        console.error('Error loading notebook:', error);
        showToast('Error de conexión al cargar el notebook', 'error');
    }
}

// Execute notebook
async function executeNotebook() {
    const code = document.getElementById('code-editor').value;
    
    if (!code.trim()) {
        showToast('El editor está vacío', 'warning');
        return;
    }
    
    showLoadingOverlay();
    
    // If we have a selected notebook, execute it. Otherwise, execute the editor content
    const endpoint = selectedNotebook ? 
        `/api/notebooks/execute/${selectedNotebook}` : 
        '/api/notebooks/execute/editor';
    
    try {
        const response = await fetch(endpoint, {
            method: selectedNotebook ? 'GET' : 'POST',
            headers: selectedNotebook ? {} : { 'Content-Type': 'application/json' },
            body: selectedNotebook ? undefined : JSON.stringify({ code: code })
        });
        
        const data = await response.json();
        hideLoadingOverlay();
        
        if (data.success) {
            // Show stdout output
            const output = document.getElementById('notebook-output');
            if (data.stdout) {
                output.innerHTML = data.stdout;
            } else {
                output.innerHTML = '<span class="text-success">✓ Código ejecutado sin salida</span>';
            }
            
            // Show visualization if any
            if (data.image) {
                document.getElementById('visualization-container').innerHTML = `
                    <img src="data:image/png;base64,${data.image}" 
                         class="max-w-full h-auto rounded shadow" 
                         alt="Notebook Visualization">
                `;
            }
            
            showToast('Código ejecutado correctamente', 'success');
        } else {
            const output = document.getElementById('notebook-output');
            output.innerHTML = `<span class="text-error">Error: ${data.error}</span>`;
            if (data.stdout) {
                output.innerHTML += '\n\n' + data.stdout;
            }
            showToast('Error al ejecutar el código', 'error');
        }
    } catch (error) {
        hideLoadingOverlay();
        console.error('Error executing notebook:', error);
        showToast('Error de conexión al ejecutar el código', 'error');
    }
}

// Setup editor
function setupEditor() {
    const editor = document.getElementById('code-editor');
    
    // Update stats on input
    editor.addEventListener('input', updateEditorStats);
    
    // Tab support
    editor.addEventListener('keydown', function(e) {
        if (e.key === 'Tab') {
            e.preventDefault();
            const start = this.selectionStart;
            const end = this.selectionEnd;
            this.value = this.value.substring(0, start) + '    ' + this.value.substring(end);
            this.selectionStart = this.selectionEnd = start + 4;
        }
    });
    
    // Initial stats
    updateEditorStats();
}

// Update editor statistics
function updateEditorStats() {
    const editor = document.getElementById('code-editor');
    const text = editor.value;
    
    const lines = text.split('\n').length;
    const chars = text.length;
    
    document.getElementById('line-count').textContent = `Líneas: ${lines}`;
    document.getElementById('char-count').textContent = `Caracteres: ${chars}`;
}

// Toggle editor theme
function toggleEditorTheme(checkbox) {
    const editor = document.getElementById('code-editor');
    const output = document.getElementById('notebook-output');
    
    if (checkbox.checked) {
        editor.classList.add('bg-base-900', 'text-green-400');
        editor.classList.remove('bg-base-200');
        output.classList.add('bg-base-900', 'text-green-400');
    } else {
        editor.classList.remove('bg-base-900', 'text-green-400');
        editor.classList.add('bg-base-200');
        output.classList.remove('bg-base-900', 'text-green-400');
    }
}

// Copy code
async function copyCode() {
    const code = document.getElementById('code-editor').value;
    
    if (!code) {
        showToast('No hay código para copiar', 'warning');
        return;
    }
    
    try {
        await navigator.clipboard.writeText(code);
        showToast('Código copiado al portapapeles', 'success');
    } catch (error) {
        console.error('Error copying code:', error);
        showToast('Error al copiar el código', 'error');
    }
}

// Format code (basic indentation fix)
function formatCode() {
    const editor = document.getElementById('code-editor');
    let code = editor.value;
    
    // Very basic formatting: ensure consistent indentation
    const lines = code.split('\n');
    let formattedLines = [];
    let indentLevel = 0;
    
    lines.forEach(line => {
        const trimmed = line.trim();
        
        // Decrease indent for these keywords
        if (trimmed.startsWith('elif') || trimmed.startsWith('else') || 
            trimmed.startsWith('except') || trimmed.startsWith('finally')) {
            if (indentLevel > 0) indentLevel--;
        }
        
        // Add line with current indent
        if (trimmed) {
            formattedLines.push('    '.repeat(indentLevel) + trimmed);
        } else {
            formattedLines.push('');
        }
        
        // Increase indent if line ends with :
        if (trimmed.endsWith(':')) {
            indentLevel++;
        }
        
        // Decrease indent after return, break, continue, pass
        if (trimmed === 'return' || trimmed === 'break' || 
            trimmed === 'continue' || trimmed === 'pass') {
            if (indentLevel > 0) indentLevel--;
        }
    });
    
    editor.value = formattedLines.join('\n');
    updateEditorStats();
    showToast('Código formateado', 'success');
}

// Clear output
function clearOutput() {
    document.getElementById('notebook-output').innerHTML = '<span class="opacity-50">La salida aparecerá aquí...</span>';
    document.getElementById('visualization-container').innerHTML = `
        <div class="text-center">
            <i class="ti ti-chart-line text-4xl text-base-300 mb-2"></i>
            <p class="text-sm text-base-content/60">
                Las visualizaciones aparecerán aquí
            </p>
        </div>
    `;
    showToast('Salida limpiada', 'info');
}

// Show loading overlay
function showLoadingOverlay() {
    document.getElementById('loading-overlay').style.display = 'flex';
}

// Hide loading overlay
function hideLoadingOverlay() {
    document.getElementById('loading-overlay').style.display = 'none';
}

// Show toast notification
function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toast-container');
    const toastMessage = document.getElementById('toast-message');
    const alertDiv = toastContainer.querySelector('.alert');
    
    toastMessage.textContent = message;
    alertDiv.className = `alert alert-${type}`;
    
    toastContainer.style.display = 'block';
    
    setTimeout(() => {
        toastContainer.style.display = 'none';
    }, 3000);
} 