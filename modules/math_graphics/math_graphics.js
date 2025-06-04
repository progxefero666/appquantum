// Math Graphics Module JavaScript

let selectedFile = null;
let currentCode = '';

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
    loadFileList();
});

// Load list of available graphics files
async function loadFileList() {
    try {
        const response = await fetch('/api/graphics/files');
        const data = await response.json();
        
        const fileListDiv = document.getElementById('file-list');
        
        if (data.success && data.files && data.files.length > 0) {
            fileListDiv.innerHTML = '';
            
            data.files.forEach(file => {
                const fileItem = document.createElement('div');
                fileItem.className = 'file-item p-3 rounded-lg cursor-pointer hover:bg-base-200 transition-colors flex items-center gap-3';
                fileItem.innerHTML = `
                    <i class="ti ti-file-code text-lg"></i>
                    <span class="flex-1">${file}</span>
                    <i class="ti ti-chevron-right text-sm opacity-50"></i>
                `;
                
                fileItem.onclick = () => selectFile(file, fileItem);
                fileListDiv.appendChild(fileItem);
            });
        } else {
            fileListDiv.innerHTML = `
                <div class="alert alert-warning">
                    <i class="ti ti-alert-circle"></i>
                    <span>No se encontraron scripts en la carpeta public/graphs/</span>
                </div>
            `;
        }
    } catch (error) {
        console.error('Error loading files:', error);
        document.getElementById('file-list').innerHTML = `
            <div class="alert alert-error">
                <i class="ti ti-alert-circle"></i>
                <span>Error al cargar los archivos</span>
            </div>
        `;
    }
}

// Select a file
function selectFile(filename, element) {
    selectedFile = filename;
    
    // Update visual selection
    document.querySelectorAll('.file-item').forEach(item => {
        item.classList.remove('bg-primary', 'text-primary-content');
    });
    element.classList.add('bg-primary', 'text-primary-content');
    
    // Enable buttons
    document.getElementById('load-btn').disabled = false;
    document.getElementById('execute-btn').disabled = false;
    
    // Show notification
    showToast(`Archivo seleccionado: ${filename}`);
}

// Load graphics code
async function loadGraphicsCode() {
    if (!selectedFile) return;
    
    try {
        const response = await fetch(`/api/graphics/load/${selectedFile}`);
        const data = await response.json();
        
        if (data.success) {
            currentCode = data.content;
            
            // Display code with basic syntax highlighting
            const codeDisplay = document.getElementById('code-display');
            codeDisplay.innerHTML = highlightPython(data.content);
            
            showToast('Código cargado correctamente');
        } else {
            showError('Error al cargar el código: ' + data.error);
        }
    } catch (error) {
        console.error('Error loading code:', error);
        showError('Error de conexión al cargar el código');
    }
}

// Execute graphics script
async function executeGraphics() {
    if (!selectedFile) return;
    
    showLoading();
    
    try {
        const response = await fetch(`/api/graphics/execute/${selectedFile}`);
        const data = await response.json();
        
        if (data.success && data.image) {
            showVisualization(data.image);
            showToast('Script ejecutado correctamente');
        } else {
            showError(data.error || 'Error al ejecutar el script');
        }
    } catch (error) {
        console.error('Error executing graphics:', error);
        showError('Error de conexión al ejecutar el script');
    }
}

// Copy code to clipboard
async function copyCode() {
    if (!currentCode) {
        showToast('No hay código para copiar', 'warning');
        return;
    }
    
    try {
        await navigator.clipboard.writeText(currentCode);
        showToast('Código copiado al portapapeles', 'success');
    } catch (error) {
        console.error('Error copying code:', error);
        showToast('Error al copiar el código', 'error');
    }
}

// Show loading state
function showLoading() {
    document.getElementById('visualization-container').style.display = 'none';
    document.getElementById('loading-state').style.display = 'flex';
    document.getElementById('error-state').style.display = 'none';
}

// Show visualization
function showVisualization(imageBase64) {
    const container = document.getElementById('visualization-container');
    container.innerHTML = `
        <img src="data:image/png;base64,${imageBase64}" 
             class="max-w-full h-auto rounded-lg shadow-lg" 
             alt="Visualization">
    `;
    
    container.style.display = 'block';
    document.getElementById('loading-state').style.display = 'none';
    document.getElementById('error-state').style.display = 'none';
}

// Show error
function showError(message) {
    document.getElementById('error-message').textContent = message;
    document.getElementById('error-state').style.display = 'block';
    document.getElementById('loading-state').style.display = 'none';
    document.getElementById('visualization-container').style.display = 'none';
}

// Show toast notification
function showToast(message, type = 'success') {
    const toastContainer = document.getElementById('toast-container');
    const toastMessage = document.getElementById('toast-message');
    const alertDiv = toastContainer.querySelector('.alert');
    
    // Update message
    toastMessage.textContent = message;
    
    // Update alert class based on type
    alertDiv.className = `alert alert-${type}`;
    
    // Update icon based on type
    const icon = alertDiv.querySelector('i');
    switch(type) {
        case 'success':
            icon.className = 'ti ti-check';
            break;
        case 'warning':
            icon.className = 'ti ti-alert-triangle';
            break;
        case 'error':
            icon.className = 'ti ti-x';
            break;
        default:
            icon.className = 'ti ti-info-circle';
    }
    
    // Show toast
    toastContainer.style.display = 'block';
    
    // Hide after 3 seconds
    setTimeout(() => {
        toastContainer.style.display = 'none';
    }, 3000);
}

// Basic Python syntax highlighting
function highlightPython(code) {
    // This is a simple highlighting function
    // For production, consider using a library like Prism.js or highlight.js
    
    const keywords = [
        'import', 'from', 'def', 'class', 'if', 'else', 'elif', 'for', 'while',
        'try', 'except', 'finally', 'with', 'as', 'return', 'yield', 'lambda',
        'True', 'False', 'None', 'and', 'or', 'not', 'in', 'is', 'break',
        'continue', 'pass', 'raise', 'assert', 'del', 'global', 'nonlocal'
    ];
    
    const builtins = [
        'print', 'len', 'range', 'str', 'int', 'float', 'list', 'dict', 'set',
        'tuple', 'bool', 'type', 'isinstance', 'hasattr', 'getattr', 'setattr',
        'delattr', 'open', 'close', 'read', 'write', 'min', 'max', 'sum', 'abs'
    ];
    
    // Escape HTML
    let highlighted = code
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');
    
    // Highlight strings
    highlighted = highlighted.replace(/(["'])((?:\\.|(?!\1).)*?)\1/g, 
        '<span class="text-success">$1$2$1</span>');
    
    // Highlight comments
    highlighted = highlighted.replace(/(#.*)$/gm, 
        '<span class="text-base-content/50 italic">$1</span>');
    
    // Highlight keywords
    keywords.forEach(keyword => {
        const regex = new RegExp(`\\b${keyword}\\b`, 'g');
        highlighted = highlighted.replace(regex, 
            `<span class="text-primary font-semibold">${keyword}</span>`);
    });
    
    // Highlight built-in functions
    builtins.forEach(builtin => {
        const regex = new RegExp(`\\b${builtin}\\b`, 'g');
        highlighted = highlighted.replace(regex, 
            `<span class="text-secondary">${builtin}</span>`);
    });
    
    // Highlight numbers
    highlighted = highlighted.replace(/\b(\d+\.?\d*)\b/g, 
        '<span class="text-info">$1</span>');
    
    return highlighted;
} 