// Mathematical Tools Module JavaScript

let currentMatrix = null;
let currentGraph = null;
let currentTab = 'matrices';

// Switch between tabs
function switchTab(tab) {
    currentTab = tab;
    
    // Update tab styles
    document.getElementById('matrices-tab').classList.toggle('tab-active', tab === 'matrices');
    document.getElementById('graphs-tab').classList.toggle('tab-active', tab === 'graphs');
    
    // Show/hide sections
    document.getElementById('matrices-section').style.display = tab === 'matrices' ? 'block' : 'none';
    document.getElementById('graphs-section').style.display = tab === 'graphs' ? 'block' : 'none';
}

// ============= MATRICES SECTION =============

// Create matrix
async function createMatrix() {
    const type = document.getElementById('matrix-type').value;
    const size = parseInt(document.getElementById('matrix-size').value);
    
    showLoading();
    
    try {
        const response = await fetch('/api/math/matrix/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ matrix_type: type, size: size })
        });
        
        const data = await response.json();
        hideLoading();
        
        if (data.success) {
            currentMatrix = data.matrix;
            displayMatrix(data.matrix);
            displayMatrixProperties(data);
            enableMatrixOperations();
            showToast('Matriz creada correctamente', 'success');
        } else {
            showToast('Error al crear la matriz: ' + data.error, 'error');
        }
    } catch (error) {
        hideLoading();
        console.error('Error creating matrix:', error);
        showToast('Error de conexión', 'error');
    }
}

// Display matrix
function displayMatrix(matrix) {
    const display = document.getElementById('matrix-display');
    
    // Create HTML table for matrix
    let html = '<table class="mx-auto">';
    matrix.forEach(row => {
        html += '<tr>';
        row.forEach(value => {
            html += `<td class="px-2 py-1 text-center">${value.toFixed(3)}</td>`;
        });
        html += '</tr>';
    });
    html += '</table>';
    
    display.innerHTML = html;
}

// Display matrix properties
function displayMatrixProperties(data) {
    const props = document.getElementById('matrix-properties');
    props.innerHTML = `
        <p><strong>Tipo:</strong> ${data.type}</p>
        <p><strong>Tamaño:</strong> ${data.size} × ${data.size}</p>
        <p><strong>Elementos:</strong> ${data.size * data.size}</p>
    `;
}

// Enable matrix operations
function enableMatrixOperations() {
    document.querySelectorAll('button[onclick^="analyzeMatrix"]').forEach(btn => {
        btn.disabled = false;
        btn.classList.remove('btn-outline');
        btn.classList.add('btn-primary');
    });
}

// Analyze matrix
async function analyzeMatrix(operation) {
    if (!currentMatrix) {
        showToast('Primero crea una matriz', 'warning');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch('/api/math/matrix/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ matrix: currentMatrix, operation: operation })
        });
        
        const data = await response.json();
        hideLoading();
        
        if (data.success) {
            displayMatrixResults(operation, data.description);
            showToast('Análisis completado', 'success');
        } else {
            showToast('Error en el análisis: ' + data.error, 'error');
        }
    } catch (error) {
        hideLoading();
        console.error('Error analyzing matrix:', error);
        showToast('Error de conexión', 'error');
    }
}

// Display matrix results
function displayMatrixResults(operation, description) {
    const results = document.getElementById('matrix-results');
    const timestamp = new Date().toLocaleTimeString();
    
    results.innerHTML = `
        <div class="mb-3 p-2 bg-base-100 rounded">
            <div class="flex justify-between items-start mb-1">
                <h4 class="font-semibold text-primary">${getOperationTitle(operation)}</h4>
                <span class="text-xs opacity-50">${timestamp}</span>
            </div>
            <pre class="text-xs whitespace-pre-wrap">${description}</pre>
        </div>
    ` + results.innerHTML;
}

// Get operation title
function getOperationTitle(operation) {
    const titles = {
        'eigenvalues': 'Valores Propios',
        'svd': 'Descomposición SVD',
        'determinant': 'Determinante',
        'inverse': 'Matriz Inversa',
        'rank': 'Rango',
        'condition': 'Número de Condición',
        'trace': 'Traza',
        'norm': 'Norma'
    };
    return titles[operation] || operation;
}

// ============= GRAPHS SECTION =============

// Toggle probability field based on graph type
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('graph-type').addEventListener('change', function() {
        const probControl = document.getElementById('probability-control');
        probControl.style.display = this.value === 'random' ? 'block' : 'none';
    });
});

// Create graph
async function createGraph() {
    const type = document.getElementById('graph-type').value;
    const numNodes = parseInt(document.getElementById('num-nodes').value);
    const probability = parseFloat(document.getElementById('edge-probability').value);
    
    showLoading();
    
    try {
        const response = await fetch('/api/math/graph/create', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                graph_type: type, 
                num_nodes: numNodes,
                probability: probability 
            })
        });
        
        const data = await response.json();
        hideLoading();
        
        if (data.success) {
            currentGraph = data.adjacency_matrix;
            displayGraphProperties(data);
            displayAdjacencyMatrix(data.adjacency_matrix);
            document.querySelector('button[onclick="analyzeGraph()"]').disabled = false;
            showToast('Grafo creado correctamente', 'success');
        } else {
            showToast('Error al crear el grafo: ' + data.error, 'error');
        }
    } catch (error) {
        hideLoading();
        console.error('Error creating graph:', error);
        showToast('Error de conexión', 'error');
    }
}

// Display graph properties
function displayGraphProperties(data) {
    const props = document.getElementById('graph-properties');
    props.innerHTML = `
        <div class="stat bg-base-200 rounded p-2">
            <div class="stat-title text-xs">Nodos</div>
            <div class="stat-value text-lg">${data.num_nodes}</div>
        </div>
        <div class="stat bg-base-200 rounded p-2">
            <div class="stat-title text-xs">Aristas</div>
            <div class="stat-value text-lg">${data.num_edges}</div>
        </div>
        <div class="stat bg-base-200 rounded p-2">
            <div class="stat-title text-xs">Tipo</div>
            <div class="stat-value text-sm">${data.graph_type}</div>
        </div>
    `;
}

// Display adjacency matrix
function displayAdjacencyMatrix(matrix) {
    const display = document.getElementById('adjacency-matrix');
    
    if (matrix.length > 10) {
        display.innerHTML = '<p class="text-xs">Matriz muy grande para mostrar (>10x10)</p>';
        return;
    }
    
    let html = '<table class="text-xs mx-auto">';
    matrix.forEach(row => {
        html += '<tr>';
        row.forEach(value => {
            const cellClass = value === 1 ? 'bg-primary text-primary-content' : '';
            html += `<td class="px-1 py-0.5 text-center ${cellClass}">${value}</td>`;
        });
        html += '</tr>';
    });
    html += '</table>';
    
    display.innerHTML = html;
}

// Analyze graph
async function analyzeGraph() {
    if (!currentGraph) {
        showToast('Primero crea un grafo', 'warning');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch('/api/math/graph/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ adjacency_matrix: currentGraph })
        });
        
        const data = await response.json();
        hideLoading();
        
        if (data.success) {
            displayGraphAnalysis(data);
            if (data.visualization) {
                displayGraphVisualization(data.visualization);
            }
            showToast('Análisis completado', 'success');
        } else {
            showToast('Error en el análisis: ' + data.error, 'error');
        }
    } catch (error) {
        hideLoading();
        console.error('Error analyzing graph:', error);
        showToast('Error de conexión', 'error');
    }
}

// Display graph analysis
function displayGraphAnalysis(data) {
    const props = document.getElementById('graph-properties');
    
    // Add analysis results
    let analysisHtml = `
        <div class="divider">Análisis</div>
        <div class="space-y-1 text-sm">
            <p><strong>Densidad:</strong> ${data.properties.density.toFixed(3)}</p>
            <p><strong>Conectado:</strong> ${data.properties.is_connected ? 'Sí' : 'No'}</p>
            <p><strong>Grado promedio:</strong> ${data.properties.average_degree.toFixed(2)}</p>
    `;
    
    if (data.shortest_paths) {
        analysisHtml += `
            <p><strong>Diámetro:</strong> ${data.shortest_paths.diameter}</p>
            <p><strong>Distancia promedio:</strong> ${data.shortest_paths.average_distance.toFixed(3)}</p>
        `;
    }
    
    analysisHtml += '</div>';
    
    // Append to existing properties
    const existingContent = props.innerHTML;
    props.innerHTML = existingContent + analysisHtml;
}

// Display graph visualization
function displayGraphVisualization(imageBase64) {
    const viz = document.getElementById('graph-visualization');
    viz.innerHTML = `
        <img src="data:image/png;base64,${imageBase64}" 
             class="max-w-full h-auto rounded" 
             alt="Graph Visualization">
    `;
}

// ============= COMMON FUNCTIONS =============

// Show loading
function showLoading() {
    document.getElementById('loading-state').style.display = 'flex';
}

// Hide loading
function hideLoading() {
    document.getElementById('loading-state').style.display = 'none';
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