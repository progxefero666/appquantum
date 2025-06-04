// Periodic Elements Module JavaScript

let allElements = [];
let filteredElements = [];
let selectedElement = null;

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
    loadElements();
});

// Load all elements from API
async function loadElements() {
    try {
        const response = await fetch('/api/elements/all');
        const data = await response.json();
        
        if (data.success) {
            allElements = data.elements;
            displayElements(allElements);
            updateStatistics();
        } else {
            showError('Error al cargar los elementos');
        }
    } catch (error) {
        console.error('Error loading elements:', error);
        showError('Error de conexión al cargar elementos');
    }
}

// Display elements in the grid
function displayElements(elements) {
    const grid = document.getElementById('elements-grid');
    const count = document.getElementById('element-count');
    
    filteredElements = elements;
    count.textContent = elements.length;
    
    if (elements.length === 0) {
        grid.innerHTML = `
            <div class="alert alert-warning">
                <i class="ti ti-alert-circle"></i>
                <span>No se encontraron elementos con los filtros aplicados</span>
            </div>
        `;
        return;
    }
    
    grid.innerHTML = '';
    
    elements.forEach(element => {
        const elementCard = createElementCard(element);
        grid.appendChild(elementCard);
    });
}

// Create element card
function createElementCard(element) {
    const card = document.createElement('div');
    const categoryClass = getCategoryClass(element.category);
    
    card.className = `element-card p-3 rounded-lg cursor-pointer hover:shadow-lg transition-all 
                      flex items-center gap-3 bg-base-200 hover:bg-base-300`;
    
    card.innerHTML = `
        <div class="flex-none">
            <div class="w-12 h-12 rounded-lg ${categoryClass} flex items-center justify-center text-white font-bold">
                ${element.symbol}
            </div>
        </div>
        <div class="flex-1">
            <div class="font-semibold">${element.name}</div>
            <div class="text-sm opacity-70">N° ${element.atomic_number} • ${element.category || 'Unknown'}</div>
        </div>
        <i class="ti ti-chevron-right opacity-50"></i>
    `;
    
    card.onclick = () => selectElement(element);
    
    return card;
}

// Get category CSS class
function getCategoryClass(category) {
    const categoryMap = {
        'alkali metal': 'element-alkali',
        'alkaline earth metal': 'element-alkaline',
        'transition metal': 'element-transition',
        'metalloid': 'element-metalloid',
        'nonmetal': 'element-nonmetal',
        'halogen': 'element-halogen',
        'noble gas': 'element-noble',
        'lanthanide': 'element-lanthanide',
        'actinide': 'element-actinide'
    };
    
    return categoryMap[category] || 'bg-gray-500';
}

// Select an element
function selectElement(element) {
    selectedElement = element;
    
    // Update visual selection
    document.querySelectorAll('.element-card').forEach(card => {
        card.classList.remove('ring-2', 'ring-primary');
    });
    event.currentTarget.classList.add('ring-2', 'ring-primary');
    
    // Show element details
    showElementDetails(element);
    
    // Enable visualization button
    document.getElementById('visualize-btn').disabled = false;
}

// Show element details
function showElementDetails(element) {
    const detailsDiv = document.getElementById('element-details');
    
    detailsDiv.innerHTML = `
        <!-- Element Header -->
        <div class="text-center mb-6">
            <div class="text-6xl font-bold mb-2 ${getCategoryClass(element.category)} 
                        text-white w-24 h-24 rounded-2xl mx-auto flex items-center justify-center">
                ${element.symbol}
            </div>
            <h3 class="text-2xl font-bold">${element.name}</h3>
            <p class="text-sm opacity-70">${element.category || 'Unknown Category'}</p>
        </div>
        
        <!-- Basic Properties -->
        <div class="space-y-2">
            <div class="flex justify-between py-2 border-b border-base-300">
                <span class="font-semibold">Número Atómico:</span>
                <span>${element.atomic_number}</span>
            </div>
            <div class="flex justify-between py-2 border-b border-base-300">
                <span class="font-semibold">Peso Atómico:</span>
                <span>${element.atomic_weight || 'N/A'}</span>
            </div>
            <div class="flex justify-between py-2 border-b border-base-300">
                <span class="font-semibold">Período:</span>
                <span>${element.period || 'N/A'}</span>
            </div>
            <div class="flex justify-between py-2 border-b border-base-300">
                <span class="font-semibold">Grupo:</span>
                <span>${element.group || 'N/A'}</span>
            </div>
        </div>
        
        <!-- Physical Properties -->
        <div class="mt-6">
            <h4 class="font-bold mb-3">Propiedades Físicas</h4>
            <div class="space-y-2">
                ${element.melting_point ? `
                <div class="flex justify-between py-2 border-b border-base-300">
                    <span class="text-sm">Punto de Fusión:</span>
                    <span class="text-sm">${element.melting_point} K</span>
                </div>` : ''}
                ${element.boiling_point ? `
                <div class="flex justify-between py-2 border-b border-base-300">
                    <span class="text-sm">Punto de Ebullición:</span>
                    <span class="text-sm">${element.boiling_point} K</span>
                </div>` : ''}
                ${element.density ? `
                <div class="flex justify-between py-2 border-b border-base-300">
                    <span class="text-sm">Densidad:</span>
                    <span class="text-sm">${element.density} g/cm³</span>
                </div>` : ''}
            </div>
        </div>
        
        <!-- Electron Configuration -->
        ${element.electron_configuration ? `
        <div class="mt-6">
            <h4 class="font-bold mb-3">Configuración Electrónica</h4>
            <div class="text-sm font-mono bg-base-200 p-3 rounded-lg">
                ${element.electron_configuration}
            </div>
        </div>` : ''}
        
        <!-- More Info Button -->
        <button class="btn btn-sm btn-ghost mt-4" onclick="showMoreInfo()">
            <i class="ti ti-info-circle"></i>
            Más Información
        </button>
    `;
}

// Filter elements
function filterElements() {
    const searchTerm = document.getElementById('search-input').value.toLowerCase();
    const category = document.getElementById('category-filter').value;
    const period = document.getElementById('period-filter').value;
    
    const filtered = allElements.filter(element => {
        // Search filter
        const matchesSearch = searchTerm === '' || 
            element.name.toLowerCase().includes(searchTerm) ||
            element.symbol.toLowerCase().includes(searchTerm);
        
        // Category filter
        const matchesCategory = category === '' || element.category === category;
        
        // Period filter
        const matchesPeriod = period === '' || element.period == period;
        
        return matchesSearch && matchesCategory && matchesPeriod;
    });
    
    displayElements(filtered);
}

// Clear search
function clearSearch() {
    document.getElementById('search-input').value = '';
    filterElements();
}

// Visualize element
async function visualizeElement() {
    if (!selectedElement) return;
    
    showLoading();
    
    try {
        const response = await fetch(`/api/elements/visualize/${selectedElement.atomic_number}`);
        const data = await response.json();
        
        if (data.success) {
            showVisualization(data.visualization);
        } else {
            showError(data.error || 'Error al generar visualización');
        }
    } catch (error) {
        console.error('Error visualizing element:', error);
        showError('Error de conexión al generar visualización');
    }
}

// Show more info in modal
function showMoreInfo() {
    if (!selectedElement) return;
    
    const modal = document.getElementById('info-modal');
    const modalTitle = document.getElementById('modal-title');
    const modalContent = document.getElementById('modal-content');
    
    modalTitle.textContent = `${selectedElement.name} (${selectedElement.symbol})`;
    
    modalContent.innerHTML = `
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
                <h4 class="font-bold mb-3">Propiedades Completas</h4>
                <div class="space-y-2 text-sm">
                    ${Object.entries(selectedElement).map(([key, value]) => {
                        if (value && key !== 'id') {
                            const label = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
                            return `
                                <div class="flex justify-between py-1">
                                    <span class="font-semibold">${label}:</span>
                                    <span>${value}</span>
                                </div>
                            `;
                        }
                        return '';
                    }).join('')}
                </div>
            </div>
            
            <div>
                <h4 class="font-bold mb-3">Información Adicional</h4>
                <div class="space-y-3">
                    <div class="alert alert-info">
                        <i class="ti ti-info-circle"></i>
                        <span>Usa el botón "Generar Visualización Completa" para ver gráficos detallados de este elemento.</span>
                    </div>
                    
                    ${selectedElement.discovery_year ? `
                    <div class="stat bg-base-200 rounded-lg">
                        <div class="stat-title">Año de Descubrimiento</div>
                        <div class="stat-value text-primary">${selectedElement.discovery_year}</div>
                    </div>` : ''}
                </div>
            </div>
        </div>
    `;
    
    modal.showModal();
}

// Update statistics
function updateStatistics() {
    let discoveredCount = 0;
    let syntheticCount = 0;
    
    allElements.forEach(element => {
        if (element.discovery_year) discoveredCount++;
        // Assuming elements with atomic number > 92 are synthetic
        if (element.atomic_number > 92) syntheticCount++;
    });
    
    document.getElementById('discovered-count').textContent = discoveredCount;
    document.getElementById('synthetic-count').textContent = syntheticCount;
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
             alt="Element Visualization">
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