// Pandas Analytics Module JavaScript

let currentDataset = null;

// Load dataset
async function loadDataset() {
    const selector = document.getElementById('dataset-selector');
    const dataset = selector.value;
    
    if (!dataset) {
        resetUI();
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch(`/api/pandas/load/${dataset}`);
        const data = await response.json();
        
        hideLoading();
        
        if (data.success) {
            currentDataset = dataset;
            
            // Show data preview
            document.getElementById('data-preview').innerHTML = data.preview;
            
            // Enable analysis buttons
            document.querySelectorAll('button[onclick^="analyzeData"]').forEach(btn => {
                btn.disabled = false;
                btn.classList.add('btn-primary');
                btn.classList.remove('btn-outline');
            });
            
            // Update dataset info
            document.getElementById('dataset-info').innerHTML = `
                <p class="font-semibold">${dataset.charAt(0).toUpperCase() + dataset.slice(1)} Dataset</p>
                <p class="text-xs">Datos cargados correctamente</p>
            `;
            
            // Basic summary
            updateDataSummary();
            
            showToast(`Dataset ${dataset} cargado correctamente`, 'success');
        } else {
            showError('Error al cargar el dataset: ' + data.error);
        }
    } catch (error) {
        hideLoading();
        console.error('Error loading dataset:', error);
        showError('Error de conexión al cargar el dataset');
    }
}

// Analyze data
async function analyzeData(analysisType) {
    if (!currentDataset) {
        showToast('Por favor selecciona un dataset primero', 'warning');
        return;
    }
    
    showLoading();
    
    // Highlight selected analysis button
    document.querySelectorAll('button[onclick^="analyzeData"]').forEach(btn => {
        btn.classList.remove('btn-accent');
    });
    event.target.classList.add('btn-accent');
    
    try {
        const response = await fetch(`/api/pandas/analyze/${currentDataset}/${analysisType}`);
        const data = await response.json();
        
        hideLoading();
        
        if (data.success) {
            // Show visualization
            if (data.plot_image) {
                document.getElementById('visualization-container').innerHTML = `
                    <img src="data:image/png;base64,${data.plot_image}" 
                         class="max-w-full h-auto rounded shadow" 
                         alt="${analysisType} visualization">
                `;
            }
            
            // Show analysis info
            document.getElementById('analysis-info').innerHTML = `
                <div>
                    <p class="font-semibold mb-1">${data.info_text}</p>
                    ${data.summary ? `<pre class="text-xs opacity-80 mt-2">${data.summary}</pre>` : ''}
                </div>
            `;
            
            showToast('Análisis completado', 'success');
        } else {
            showError('Error al realizar el análisis: ' + data.error);
        }
    } catch (error) {
        hideLoading();
        console.error('Error analyzing data:', error);
        showError('Error de conexión al realizar el análisis');
    }
}

// Update data summary
function updateDataSummary() {
    const preview = document.getElementById('data-preview');
    const table = preview.querySelector('table');
    
    if (table) {
        const rows = table.querySelectorAll('tr').length - 1; // Minus header
        const cols = table.querySelector('tr').querySelectorAll('th').length;
        
        document.getElementById('data-summary').innerHTML = `
            <p class="text-xs">
                <strong>Filas:</strong> ${rows} (mostrando primeras 5)<br>
                <strong>Columnas:</strong> ${cols}<br>
                <strong>Tipo:</strong> Tabla de datos estructurados
            </p>
        `;
    }
}

// Reset UI
function resetUI() {
    currentDataset = null;
    
    // Reset preview
    document.getElementById('data-preview').innerHTML = `
        <div class="text-center py-8">
            <i class="ti ti-table text-4xl text-base-300 mb-2"></i>
            <p class="text-sm text-base-content/60">
                Los datos se mostrarán aquí
            </p>
        </div>
    `;
    
    // Reset visualization
    document.getElementById('visualization-container').innerHTML = `
        <div class="text-center">
            <i class="ti ti-chart-dots text-5xl text-base-300 mb-3"></i>
            <p class="text-base-content/60">
                Selecciona un dataset y tipo de análisis
            </p>
        </div>
    `;
    
    // Disable buttons
    document.querySelectorAll('button[onclick^="analyzeData"]').forEach(btn => {
        btn.disabled = true;
        btn.classList.remove('btn-primary', 'btn-accent');
        btn.classList.add('btn-outline');
    });
    
    // Reset info
    document.getElementById('dataset-info').innerHTML = `
        <p>Selecciona un dataset para comenzar</p>
    `;
    
    document.getElementById('data-summary').innerHTML = `
        <p class="text-xs opacity-70">Información del dataset aparecerá aquí</p>
    `;
    
    document.getElementById('analysis-info').innerHTML = `
        <p class="opacity-70">La información del análisis aparecerá aquí</p>
    `;
}

// Show loading
function showLoading() {
    document.getElementById('visualization-container').style.display = 'none';
    document.getElementById('loading-state').style.display = 'flex';
}

// Hide loading
function hideLoading() {
    document.getElementById('loading-state').style.display = 'none';
    document.getElementById('visualization-container').style.display = 'flex';
}

// Show error
function showError(message) {
    document.getElementById('visualization-container').innerHTML = `
        <div class="alert alert-error">
            <i class="ti ti-alert-circle"></i>
            <span>${message}</span>
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
    
    // Update alert class
    alertDiv.className = `alert alert-${type}`;
    
    // Show toast
    toastContainer.style.display = 'block';
    
    // Hide after 3 seconds
    setTimeout(() => {
        toastContainer.style.display = 'none';
    }, 3000);
} 