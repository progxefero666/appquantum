// Quantum Waves Module JavaScript

// Update label functions for sliders
function updateFrequencyLabel() {
    const value = document.getElementById('wave-frequency').value;
    document.getElementById('freq-value').textContent = parseFloat(value).toFixed(1);
}

function updateAmplitudeLabel() {
    const value = document.getElementById('wave-amplitude').value;
    document.getElementById('amp-value').textContent = parseFloat(value).toFixed(1);
}

function updatePhaseLabel() {
    const value = document.getElementById('wave-phase').value;
    document.getElementById('phase-value').textContent = parseFloat(value).toFixed(1) + 'π';
}

// Generate wave function
async function generateWave() {
    // Get parameters
    const frequency = parseFloat(document.getElementById('wave-frequency').value);
    const amplitude = parseFloat(document.getElementById('wave-amplitude').value);
    const phase = parseFloat(document.getElementById('wave-phase').value);
    const waveType = document.getElementById('wave-type').value;

    // Show loading state
    showLoading();

    try {
        // Prepare data for API
        const data = {
            frequency: frequency,
            amplitude: amplitude,
            phase: phase,
            wave_type: waveType
        };

        // Call API
        const response = await fetch('/api/waves/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        const result = await response.json();

        if (result.success) {
            // Show visualization
            showVisualization(result.plot_image);
            
            // Show wave info
            showWaveInfo(result.info_text);
        } else {
            showError(result.error || 'Error al generar la onda');
        }
    } catch (error) {
        console.error('Error:', error);
        showError('Error de conexión con el servidor');
    }
}

// Clear visualization
function clearWaveVisualization() {
    const vizContainer = document.getElementById('wave-visualization');
    vizContainer.innerHTML = `
        <div class="text-center">
            <i class="ti ti-wave-sine text-6xl text-base-300 mb-4"></i>
            <p class="text-base-content/60">
                Ajusta los parámetros y presiona "Generar Onda" para ver la visualización
            </p>
        </div>
    `;
    
    // Hide info card
    document.getElementById('wave-info-card').style.display = 'none';
    
    // Hide error if visible
    document.getElementById('error-state').style.display = 'none';
}

// Show loading state
function showLoading() {
    document.getElementById('wave-visualization').style.display = 'none';
    document.getElementById('loading-state').style.display = 'flex';
    document.getElementById('error-state').style.display = 'none';
}

// Show visualization
function showVisualization(imageBase64) {
    const vizContainer = document.getElementById('wave-visualization');
    vizContainer.innerHTML = `<img src="data:image/png;base64,${imageBase64}" class="w-full h-auto rounded-lg shadow-lg" alt="Wave Visualization">`;
    
    // Show visualization, hide loading
    vizContainer.style.display = 'block';
    document.getElementById('loading-state').style.display = 'none';
}

// Show wave information
function showWaveInfo(infoText) {
    const infoCard = document.getElementById('wave-info-card');
    const infoContent = document.getElementById('wave-info');
    
    // Format the info text with proper HTML
    const formattedInfo = infoText.split('\n').map(line => {
        if (line.includes(':')) {
            const [label, value] = line.split(':');
            return `<div class="flex justify-between py-1">
                        <span class="font-semibold">${label}:</span>
                        <span class="text-right">${value}</span>
                    </div>`;
        }
        return `<div class="py-1">${line}</div>`;
    }).join('');
    
    infoContent.innerHTML = formattedInfo;
    infoCard.style.display = 'block';
}

// Show error
function showError(message) {
    document.getElementById('error-message').textContent = message;
    document.getElementById('error-state').style.display = 'block';
    document.getElementById('loading-state').style.display = 'none';
    document.getElementById('wave-visualization').style.display = 'none';
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    // Set initial label values
    updateFrequencyLabel();
    updateAmplitudeLabel();
    updatePhaseLabel();
    
    // Add enter key support for generating waves
    document.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            generateWave();
        }
    });
}); 