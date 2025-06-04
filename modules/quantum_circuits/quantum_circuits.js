// Quantum Circuits Module JavaScript

let selectedFile = null;
let currentCode = '';

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
    loadFileList();
});

// Load list of circuit files
async function loadFileList() {
    try {
        const response = await fetch('/api/circuits/files');
        const data = await response.json();
        
        const fileListDiv = document.getElementById('file-list');
        
        if (data.success && data.files && data.files.length > 0) {
            fileListDiv.innerHTML = '';
            
            data.files.forEach(file => {
                const fileItem = document.createElement('div');
                fileItem.className = 'file-item p-2 rounded cursor-pointer hover:bg-base-200 transition-colors flex items-center gap-2 text-sm';
                fileItem.innerHTML = `
                    <i class="ti ti-file-code text-sm"></i>
                    <span class="flex-1 truncate">${file}</span>
                `;
                
                fileItem.onclick = () => selectFile(file, fileItem);
                fileListDiv.appendChild(fileItem);
            });
        } else {
            fileListDiv.innerHTML = `
                <div class="alert alert-warning alert-sm">
                    <i class="ti ti-alert-circle"></i>
                    <span>No se encontraron circuitos</span>
                </div>
            `;
        }
    } catch (error) {
        console.error('Error loading files:', error);
        document.getElementById('file-list').innerHTML = `
            <div class="alert alert-error alert-sm">
                <i class="ti ti-alert-circle"></i>
                <span>Error al cargar archivos</span>
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
    
    // Update file info
    document.getElementById('file-info').innerHTML = `
        <p class="font-semibold">${filename}</p>
        <p class="text-xs opacity-70">Listo para cargar</p>
    `;
    
    // Enable buttons
    document.getElementById('load-btn').disabled = false;
    document.getElementById('execute-btn').disabled = false;
    
    showToast(`Circuito seleccionado: ${filename}`);
}

// Load circuit code
async function loadCircuitCode() {
    if (!selectedFile) return;
    
    try {
        const response = await fetch(`/api/circuits/load/${selectedFile}`);
        const data = await response.json();
        
        if (data.success) {
            currentCode = data.content;
            document.getElementById('code-display').innerHTML = data.formatted_content || highlightPython(data.content);
            showToast('Código cargado correctamente');
        } else {
            showError('Error al cargar el código');
        }
    } catch (error) {
        console.error('Error loading code:', error);
        showError('Error de conexión al cargar el código');
    }
}

// Execute circuit
async function executeCircuit() {
    if (!selectedFile) return;
    
    showLoadingOverlay();
    
    try {
        const response = await fetch(`/api/circuits/execute/${selectedFile}`);
        const data = await response.json();
        
        hideLoadingOverlay();
        
        if (data.success) {
            // Show circuit info
            document.getElementById('circuit-info').innerHTML = `
                <p class="text-sm font-semibold mb-1">${data.circuit_info}</p>
                <p class="text-xs opacity-70">Circuito ejecutado exitosamente</p>
            `;
            
            // Show circuit diagram
            if (data.circuit_image) {
                document.getElementById('circuit-diagram').innerHTML = `
                    <img src="data:image/png;base64,${data.circuit_image}" 
                         class="max-w-full h-auto" 
                         alt="Circuit Diagram">
                `;
            }
            
            // Show results
            if (data.result_image || data.result_text) {
                const resultsContainer = document.getElementById('results-container');
                resultsContainer.innerHTML = '';
                
                if (data.result_image) {
                    resultsContainer.innerHTML = `
                        <img src="data:image/png;base64,${data.result_image}" 
                             class="max-w-full h-auto rounded" 
                             alt="Measurement Results">
                    `;
                }
                
                if (data.result_text) {
                    document.getElementById('results-text').style.display = 'block';
                    document.getElementById('results-text').textContent = data.result_text;
                }
            } else {
                document.getElementById('results-container').innerHTML = `
                    <div class="text-center py-4">
                        <i class="ti ti-info-circle text-3xl text-warning mb-2"></i>
                        <p class="text-sm">Este circuito no tiene mediciones</p>
                    </div>
                `;
            }
            
            showToast('Circuito ejecutado correctamente', 'success');
        } else {
            showError(data.error || 'Error al ejecutar el circuito');
        }
    } catch (error) {
        hideLoadingOverlay();
        console.error('Error executing circuit:', error);
        showError('Error de conexión al ejecutar el circuito');
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

// Show loading overlay
function showLoadingOverlay() {
    document.getElementById('loading-overlay').style.display = 'flex';
}

// Hide loading overlay
function hideLoadingOverlay() {
    document.getElementById('loading-overlay').style.display = 'none';
}

// Show error
function showError(message) {
    // Update circuit info with error
    document.getElementById('circuit-info').innerHTML = `
        <div class="text-error">
            <i class="ti ti-alert-circle"></i>
            <span class="text-sm ml-1">${message}</span>
        </div>
    `;
    
    showToast(message, 'error');
}

// Show toast notification
function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toast-container');
    const toastMessage = document.getElementById('toast-message');
    const alertDiv = toastContainer.querySelector('.alert');
    
    // Update message
    toastMessage.textContent = message;
    
    // Update alert class based on type
    alertDiv.className = `alert alert-${type}`;
    
    // Show toast
    toastContainer.style.display = 'block';
    
    // Hide after 3 seconds
    setTimeout(() => {
        toastContainer.style.display = 'none';
    }, 3000);
}

// Basic Python syntax highlighting (simplified)
function highlightPython(code) {
    const keywords = [
        'import', 'from', 'def', 'class', 'if', 'else', 'elif', 'for', 'while',
        'try', 'except', 'finally', 'with', 'as', 'return', 'yield', 'lambda',
        'True', 'False', 'None', 'and', 'or', 'not', 'in', 'is'
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
    
    // Highlight numbers
    highlighted = highlighted.replace(/\b(\d+\.?\d*)\b/g, 
        '<span class="text-info">$1</span>');
    
    return highlighted;
} 