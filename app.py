# app.py
"""
Web version of AppSpyder application.
A modular web application for scientific learning and visualization.
"""

import os
import sys
import json
import base64
import io
import traceback
import time
from flask import Flask, render_template, request, jsonify, send_file
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import scipy.linalg
import networkx as nx
from fpdf import FPDF # Importar FPDF

try:
    from pygments import highlight
    from pygments.lexers import PythonLexer
    from pygments.formatters import HtmlFormatter
    PYGMENTS_AVAILABLE = True
except ImportError:
    PYGMENTS_AVAILABLE = False

# Importar configuración de rutas
from config import CIRCUITS_BASE_DIR, GRAPHS_BASE_DIR, NOTEBOOKS_BASE_DIR, DATASETS_BASE_DIR

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.database.db_manager import DatabaseManager
from src.utils.file_loader import FileLoader
from src.chemical.chemicalgraphs.atomic_graphs import AtomicGraphs
from src.quantum.graph_circuit import generate_circuit_diagram_figure
import pandas as pd
import numpy as np
import seaborn as sns

app = Flask(__name__, static_folder='static', static_url_path='/static')

# Initialize database
db_manager = DatabaseManager()
file_loader = FileLoader()

def format_python_code(code):
    """Format Python code with basic syntax highlighting."""
    import html
    import re
    
    # Escape HTML first
    escaped_code = html.escape(code)
    
    # Very simple highlighting - only keywords and comments to avoid conflicts
    keywords = ['def', 'class', 'if', 'else', 'for', 'while', 'try', 'except', 
                'import', 'from', 'return', 'True', 'False', 'None']
    
    # Apply highlighting only for keywords and comments
    lines = escaped_code.split('\n')
    formatted_lines = []
    
    for line in lines:
        # Check if line is a comment
        if line.strip().startswith('#'):
            formatted_line = f'<span style="color: #808080; font-style: italic;">{line}</span>'
        else:
            formatted_line = line
            # Only highlight basic keywords
            for keyword in keywords:
                pattern = r'\b' + re.escape(keyword) + r'\b'
                replacement = f'<span style="color: #0000ff; font-weight: bold;">{keyword}</span>'
                formatted_line = re.sub(pattern, replacement, formatted_line)
            
        formatted_lines.append(formatted_line)
    
    formatted_code = '\n'.join(formatted_lines)
    return f'<pre style="background-color: #f8f9fa; padding: 15px; border-radius: 4px; overflow-x: auto; font-family: Consolas, Monaco, monospace; line-height: 1.4;">{formatted_code}</pre>'

@app.route('/')
def index():
    """Main page with module selection."""
    return render_template('index.html', last_updated=time.time())

@app.route('/api/circuits/files')
def get_circuit_files():
    """Get list of available circuit files."""
    circuits_dir = CIRCUITS_BASE_DIR
    files = []
    print(f"[DEBUG] Attempting to list files from: {os.path.abspath(circuits_dir)}")
    
    if os.path.exists(circuits_dir):
        print(f"[DEBUG] Directory {circuits_dir} exists.")
        try:
            for file_name in os.listdir(circuits_dir):
                print(f"[DEBUG] Found file/dir: {file_name}")
                if file_name.endswith('.py'):
                    print(f"[DEBUG] Adding .py file: {file_name}")
                    files.append(file_name)
            
            if not files:
                print("[DEBUG] No .py files found in the directory.")
            
            print(f"[DEBUG] Returning files: {files}")
            return jsonify({'success': True, 'files': files})
        except Exception as e:
            print(f"[DEBUG] Error during listing files: {str(e)}")
            return jsonify({'success': False, 'error': f'Error listing files: {str(e)}'})
    else:
        print(f"[DEBUG] Directory {circuits_dir} does NOT exist.")
        try:
            os.makedirs(circuits_dir)
            print(f"[DEBUG] Created directory {circuits_dir} as it was missing.")
            return jsonify({'success': True, 'files': []})
        except Exception as e_create:
            print(f"[DEBUG] Failed to create directory {circuits_dir}: {e_create}")
            return jsonify({'success': False, 'error': f'Circuits directory not found and could not be created at {circuits_dir}'})

@app.route('/api/circuits/load/<filename>')
def load_circuit_file(filename):
    """Load circuit file content."""
    file_path = os.path.join(CIRCUITS_BASE_DIR, filename)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Format with syntax highlighting
        formatted_content = format_python_code(content)
        
        return jsonify({
            'success': True, 
            'content': content,
            'formatted_content': formatted_content
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/circuits/execute/<filename>')
def execute_circuit(filename):
    """Execute circuit file and return results."""
    file_path = os.path.join(CIRCUITS_BASE_DIR, filename)
    
    try:
        # Load and execute the circuit
        circuit_data = file_loader.load_circuit_file(file_path)
        circuit = circuit_data['circuit']
        
        # Create circuit diagram using the dedicated function
        fig = generate_circuit_diagram_figure(circuit)

        circuit_img = None
        if fig:
            try:
                # Convert to base64
                img_buffer = io.BytesIO()
                fig.savefig(img_buffer, format='png', bbox_inches='tight', dpi=100)
                img_buffer.seek(0)
                circuit_img = base64.b64encode(img_buffer.getvalue()).decode()
                print("[DEBUG-CIRCUIT] Circuit image generated successfully from fig.")
            except Exception as e_fig_to_base64:
                print(f"[DEBUG-CIRCUIT] Error converting figure to base64: {e_fig_to_base64}")
                print(traceback.format_exc())
                # Si la conversión de la figura falla, es un problema, no deberíamos continuar con una imagen vacía.
                # Podríamos intentar generar una imagen de error aquí si es necesario.
                # Por ahora, dejaremos circuit_img como None y el frontend no la mostrará.
        else:
            # Esto sucedería si generate_circuit_diagram_figure devuelve None o una figura de error
            # que no queremos procesar como una imagen de circuito válida.
            # O si devuelve una figura que ya es un error (como en tu código de graph_circuit.py)
            # Necesitamos manejar esto con más gracia si la figura de error de generate_circuit_diagram_figure
            # ya es una imagen que queremos mostrar.
            # Por simplicidad ahora, si fig es None o ya es una fig de error, no intentamos convertirla.
            # La lógica de generate_circuit_diagram_figure ya imprime errores.
            print("[DEBUG-CIRCUIT] generate_circuit_diagram_figure did not return a valid figure for direct conversion.")
            # Si generate_circuit_diagram_figure devuelve una figura de error pre-renderizada,
            # podríamos intentar convertirla aquí también. Pero el código original ya hace un fallback.
            # Vamos a intentar generar una imagen de texto como fallback si fig es None.
            if fig is None: # Solo si es None, si es una figura de error, ya se manejo.
                fallback_fig = Figure(figsize=(12, 6), dpi=100)
                ax_fallback = fallback_fig.add_subplot(111)
                ax_fallback.text(0.5, 0.5, str(circuit), transform=ax_fallback.transAxes, 
                       fontsize=10, ha='center', va='center', fontfamily='monospace')
                ax_fallback.set_title("Circuit Text Representation (Fallback)", fontsize=14)
                ax_fallback.axis('off')
                img_buffer = io.BytesIO()
                fallback_fig.savefig(img_buffer, format='png', bbox_inches='tight', dpi=100)
                img_buffer.seek(0)
                circuit_img = base64.b64encode(img_buffer.getvalue()).decode()
                print("[DEBUG-CIRCUIT] Fallback text representation image generated.")

        # Execute circuit if it has measurements
        result_img = None
        result_text = ""
        
        if circuit.num_clbits > 0:
            try:
                from qiskit import transpile
                from qiskit_aer import AerSimulator
                
                simulator = AerSimulator()
                transpiled_circuit = transpile(circuit, simulator)
                job = simulator.run(transpiled_circuit, shots=1024)
                result = job.result()
                counts = result.get_counts()
                
                # Create histogram
                result_fig = Figure(figsize=(10, 6), dpi=100)
                result_ax = result_fig.add_subplot(111)
                
                states = list(counts.keys())
                values = list(counts.values())
                
                bars = result_ax.bar(states, values, color='skyblue', edgecolor='navy', alpha=0.7)
                result_ax.set_xlabel('Measurement States', fontsize=12)
                result_ax.set_ylabel('Counts', fontsize=12)
                result_ax.set_title('Measurement Results', fontsize=14, fontweight='bold')
                result_ax.grid(True, alpha=0.3)
                
                # Add value labels on bars
                for bar, value in zip(bars, values):
                    height = bar.get_height()
                    result_ax.text(bar.get_x() + bar.get_width()/2., height + 0.01*max(values),
                                 f'{value}', ha='center', va='bottom', fontweight='bold')
                
                result_fig.tight_layout()
                
                # Convert to base64
                result_buffer = io.BytesIO()
                result_fig.savefig(result_buffer, format='png', bbox_inches='tight', dpi=100)
                result_buffer.seek(0)
                result_img = base64.b64encode(result_buffer.getvalue()).decode()
                
                # Create text summary
                total_shots = sum(values)
                result_text = f"Total shots: {total_shots}\nMeasurement probabilities:\n"
                for state, count in counts.items():
                    probability = count / total_shots
                    result_text += f"  |{state}⟩: {count}/{total_shots} ({probability:.3f})\n"
                    
            except Exception as e:
                result_text = f"Execution error: {str(e)}"
        
        plt.close('all')  # Clean up
        
        return jsonify({
            'success': True,
            'circuit_info': f"Circuit: {circuit.num_qubits} qubits, {circuit.num_clbits} classical bits",
            'circuit_image': circuit_img,
            'result_image': result_img,
            'result_text': result_text
        })
        
    except Exception as e:
        print(f"[ERROR] execute_circuit failed for {filename}: {e}")
        print(traceback.format_exc())
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/graphics/files')
def get_graphics_files():
    """Get list of available graphics files."""
    graphics_dir = GRAPHS_BASE_DIR
    files = []
    print(f"[DEBUG-GFX] Attempting to list files from: {os.path.abspath(graphics_dir)}")
    
    if os.path.exists(graphics_dir):
        print(f"[DEBUG-GFX] Directory {graphics_dir} exists.")
        try:
            for file_name in os.listdir(graphics_dir):
                print(f"[DEBUG-GFX] Found file/dir: {file_name}")
                if file_name.endswith('.py'):
                    print(f"[DEBUG-GFX] Adding .py file: {file_name}")
                    files.append(file_name)
            
            if not files:
                print("[DEBUG-GFX] No .py files found in the directory.")
            
            print(f"[DEBUG-GFX] Returning files: {files}")
            return jsonify({'success': True, 'files': files})
        except Exception as e:
            print(f"[DEBUG-GFX] Error during listing files: {str(e)}")
            return jsonify({'success': False, 'error': f'Error listing graphics files: {str(e)}'})
    else:
        print(f"[DEBUG-GFX] Directory {graphics_dir} does NOT exist.")
        try:
            os.makedirs(graphics_dir)
            print(f"[DEBUG-GFX] Created graphics directory {graphics_dir} as it was missing.")
            return jsonify({'success': True, 'files': []})
        except Exception as e_create:
            print(f"[DEBUG-GFX] Failed to create graphics directory {graphics_dir}: {e_create}")
            return jsonify({'success': False, 'error': f'Graphics directory not found and could not be created at {graphics_dir}'})

@app.route('/api/graphics/load/<filename>')
def load_graphics_file(filename):
    """Load graphics file content."""
    file_path = os.path.join(GRAPHS_BASE_DIR, filename)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        # No formatear con Pygments aquí, solo devolver el contenido crudo.
        # El formateo se haría en el frontend si es necesario, o si Pygments se aplica a scripts Python.
        return jsonify({'success': True, 'content': content})
    except FileNotFoundError:
        app.logger.error(f"Graphics file not found: {file_path}")
        return jsonify({'success': False, 'error': 'Graphics file not found'}), 404
    except Exception as e:
        app.logger.error(f"Error loading graphics file {filename}: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/graphics/execute/<filename>', methods=['GET'])
def execute_graphics(filename):
    """Execute graphics file and return plot image."""
    file_path = os.path.join(GRAPHS_BASE_DIR, filename)
    app.logger.info(f"Executing graphics script: {file_path}")

    if not os.path.exists(file_path):
        app.logger.error(f"Graphics file not found for execution: {file_path}")
        return jsonify({'success': False, 'error': 'Graphics file not found'}), 404

    try:
        # Usar FileLoader para ejecutar el script y obtener la figura
        loader_instance = FileLoader() # Asumiendo que FileLoader no necesita __init__ args
        result = loader_instance.load_graphics_file(file_path) # Reutilizamos la lógica de carga y ejecución
        
        if result and isinstance(result.get('figure'), Figure):
            fig = result['figure']
            img_buffer = io.BytesIO()
            fig.savefig(img_buffer, format='png', bbox_inches='tight')
            img_buffer.seek(0)
            plot_image_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
            plt.close(fig) # Cerrar la figura para liberar memoria
            app.logger.info(f"Graphics script {filename} executed successfully, plot generated.")
            return jsonify({'success': True, 'image': plot_image_base64, 'filename': filename})
        elif result and result.get('error'):
             app.logger.error(f"Error in graphics script {filename} via FileLoader: {result['error']}")
             return jsonify({'success': False, 'error': result['error']})
        else:
            app.logger.error(f"Unknown error or no figure returned by FileLoader for {filename}.")
            return jsonify({'success': False, 'error': 'Failed to generate plot or script had an issue.'}), 500

    except Exception as e:
        app.logger.error(f"Exception during graphics execution for {filename}: {e}")
        app.logger.error(traceback.format_exc())
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/elements/all')
def get_all_elements():
    """Get all elements from database."""
    try:
        elements = db_manager.get_all_elements()
        return jsonify({'success': True, 'elements': elements})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/elements/search')
def search_elements():
    """Search elements by term."""
    search_term = request.args.get('term', '')
    category = request.args.get('category', '')
    period = request.args.get('period', '')
    
    try:
        elements = db_manager.get_all_elements()
        
        # Apply filters
        filtered = []
        for element in elements:
            # Search filter
            matches_search = True
            if search_term:
                name_match = search_term.lower() in element.get('name', '').lower()
                symbol_match = search_term.lower() in element.get('symbol', '').lower()
                matches_search = name_match or symbol_match
            
            # Category filter
            matches_category = True
            if category and category != "All Categories":
                matches_category = element.get('category') == category
            
            # Period filter
            matches_period = True
            if period and period != "All Periods":
                period_num = period.replace("Period ", "")
                matches_period = str(element.get('period', '')) == period_num
            
            if matches_search and matches_category and matches_period:
                filtered.append(element)
        
        return jsonify({'success': True, 'elements': filtered})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/elements/visualize/<int:atomic_number>')
def visualize_element(atomic_number):
    """Create visualization for a specific element."""
    try:
        element = db_manager.get_element_by_atomic_number(atomic_number)
        if not element:
            return jsonify({'success': False, 'error': 'Element not found'})
        
        # Create comprehensive element visualization with 4 subplots
        fig = Figure(figsize=(14, 10), dpi=100)
        fig.patch.set_facecolor('white')
        fig.suptitle(f'{element.get("name", "Element")} - Complete Analysis', 
                    fontsize=16, fontweight='bold')
        
        # Subplot 1: Properties chart
        ax1 = fig.add_subplot(2, 2, 1)
        properties = {
            'Atomic Number': element.get('atomic_number', 0),
            'Atomic Weight': element.get('atomic_weight', 0),
            'Period': element.get('period', 0),
            'Group': element.get('group', 0),
            'Electronegativity': element.get('electronegativity', 0),
            'Melting Point (K)': element.get('melting_point', 0),
            'Boiling Point (K)': element.get('boiling_point', 0),
            'Density (g/cm³)': element.get('density', 0)
        }
        
        # Filter out None and 0 values
        valid_properties = {k: v for k, v in properties.items() 
                          if v is not None and v != 0 and v != ''}
        
        if valid_properties:
            names = list(valid_properties.keys())
            values = []
            for v in valid_properties.values():
                try:
                    values.append(float(v))
                except (ValueError, TypeError):
                    values.append(0)
            
            bars = ax1.bar(range(len(names)), values, 
                          color='lightblue', edgecolor='navy', alpha=0.7)
            ax1.set_xlabel('Properties')
            ax1.set_ylabel('Values')
            ax1.set_title('Element Properties')
            ax1.set_xticks(range(len(names)))
            ax1.set_xticklabels(names, rotation=45, ha='right')
            ax1.grid(True, alpha=0.3)
            
            # Add value labels
            for bar, value in zip(bars, values):
                height = bar.get_height()
                if height > 0:
                    ax1.text(bar.get_x() + bar.get_width()/2., height,
                           f'{value:.1f}', ha='center', va='bottom', fontsize=8)
        
        # Subplot 2: Periodic table position
        ax2 = fig.add_subplot(2, 2, 2)
        period = element.get('period', 1)
        group = element.get('group', 1)
        
        if period and group:
            ax2.scatter(group, period, s=300, c='red', alpha=0.8, edgecolors='black', linewidth=2)
            ax2.set_xlim(0, 19)
            ax2.set_ylim(0, 8)
            ax2.set_xlabel('Group')
            ax2.set_ylabel('Period')
            ax2.set_title('Position in Periodic Table')
            ax2.grid(True, alpha=0.3)
            ax2.invert_yaxis()
            ax2.text(group, period, element.get('symbol', 'X'), 
                    ha='center', va='center', fontweight='bold', fontsize=14, color='white')
        
        # Subplot 3: Category and electron configuration
        ax3 = fig.add_subplot(2, 2, 3)
        category = element.get('category', 'Unknown')
        electron_config = element.get('electron_configuration', 'Unknown')
        
        info_text = f"Category: {category}\n\nElectron Configuration:\n{electron_config}"
        ax3.text(0.5, 0.5, info_text, 
                transform=ax3.transAxes, ha='center', va='center',
                fontsize=11, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgreen", alpha=0.7))
        ax3.set_title('Classification & Configuration')
        ax3.axis('off')
        
        # Subplot 4: Atomic structure diagram (based on your mg_atom.py example)
        ax4 = fig.add_subplot(2, 2, 4)
        
        try:
            atomic_number = element.get('atomic_number', 1)
            atomic_weight = element.get('atomic_weight', atomic_number)
            econfig = element.get('electron_configuration', '1s1')
            
            # Setup the plot
            ax4.set_aspect('equal')
            ax4.set_xlim(-6, 6)
            ax4.set_ylim(-6, 6)
            ax4.axis('off')
            ax4.set_title('Atomic Structure', fontweight='bold')

            # Parse electron configuration like "1s2 2s2 2p6 3s2 3p1"
            import numpy as np
            import re
            
            shell_electrons = [0, 0, 0, 0]  # K(n=1), L(n=2), M(n=3), N(n=4)
            
            if econfig and econfig != 'Unknown':
                orbital_pattern = r'(\d+)[spdf](\d+)'
                matches = re.findall(orbital_pattern, econfig)
                
                for shell_num_str, electron_count_str in matches:
                    shell_num = int(shell_num_str) - 1
                    electron_count = int(electron_count_str)
                    
                    if 0 <= shell_num < 4:
                        shell_electrons[shell_num] += electron_count
            else:
                remaining = atomic_number
                max_per_shell = [2, 8, 18, 32]
                for i in range(4):
                    if remaining > 0:
                        shell_electrons[i] = min(remaining, max_per_shell[i])
                        remaining -= shell_electrons[i]
            
            # --- Nucleus particles (following your example style) ---
            protons = atomic_number
            neutrons = int(atomic_weight) - atomic_number if atomic_weight else 0
            
            nucleus_particles_data = (
                [{'type': 'proton', 'color': 'limegreen', 'text': 'p+'}] * protons +
                [{'type': 'neutron', 'color': 'red', 'text': ''}] * neutrons 
            )
            
            # Shuffle particles for random arrangement
            np.random.seed(atomic_number)  # Consistent arrangement per element
            shuffled_indices = np.random.permutation(len(nucleus_particles_data))
            shuffled_nucleus_particles = [nucleus_particles_data[i] for i in shuffled_indices]

            base_particle_size = 400
            jitter_range = 0.4
            
            for i, particle in enumerate(shuffled_nucleus_particles):
                x_particle = np.random.uniform(-jitter_range, jitter_range)
                y_particle = np.random.uniform(-jitter_range, jitter_range)
                
                ax4.scatter(
                    x_particle, y_particle, 
                    s=base_particle_size, 
                    color=particle['color'], 
                    edgecolors='black', 
                    linewidth=1.0, 
                    zorder=2 + i * 0.01 
                )
                
                if particle['text']: 
                    ax4.text(
                        x_particle, y_particle, particle['text'], 
                        color='black', 
                        fontsize=8, 
                        ha='center', va='center', 
                        zorder=3 + i * 0.01 
                    )
            
            # --- Electron shells and electrons (following your example) ---
            shell_radii = [2.2, 3.5, 4.8, 5.8]
            
            for i, num_electrons_in_shell in enumerate(shell_electrons):
                if i >= len(shell_radii) or num_electrons_in_shell <= 0:
                    continue
                
                radius = shell_radii[i]
                
                # Draw shell circle
                from matplotlib.patches import Circle
                circle = Circle((0, 0), radius, color='gray', fill=False, 
                               linewidth=1.5, linestyle='-', zorder=1)
                ax4.add_patch(circle)

                # Draw electrons
                electron_angle_step = 2 * np.pi / num_electrons_in_shell
                for j in range(num_electrons_in_shell):
                    angle = j * electron_angle_step
                    x_electron = radius * np.cos(angle)
                    y_electron = radius * np.sin(angle)
                    
                    # Electron shadow (subtle effect)
                    shadow_offset_x = 0.05
                    shadow_offset_y = -0.05
                    shadow_size_factor = 0.6
                    
                    ax4.plot(
                        x_electron + shadow_offset_x, y_electron + shadow_offset_y, 'o', 
                        markersize=15 * shadow_size_factor,
                        color='gray', 
                        markeredgecolor='black', 
                        linewidth=0.2, 
                        zorder=2.9 
                    )

                    # Main electron
                    ax4.plot(
                        x_electron, y_electron, 'o', 
                        markersize=15, 
                        color='silver', 
                        markeredgecolor='black', 
                        linewidth=0.5, 
                        zorder=3
                    )
                    
                    # Electron label
                    ax4.text(
                        x_electron, y_electron, 'e-', 
                        color='black', 
                        fontsize=8, 
                        ha='center', va='center', 
                        zorder=4
                    )
            
            # Add shell labels
            shell_names = ['K', 'L', 'M', 'N']
            for i, (radius, name) in enumerate(zip(shell_radii, shell_names)):
                if shell_electrons[i] > 0:
                    ax4.text(-radius-0.3, 0, name, fontsize=10, fontweight='bold', 
                           ha='center', va='center', color='darkblue')
            
        except Exception as e:
            # Fallback if atomic visualization fails
            ax4.text(0.5, 0.5, f"Atomic Structure\n{element.get('name', 'Element')}\n\nAtomic #: {element.get('atomic_number', 'N/A')}\nElectrons: {element.get('atomic_number', 'N/A')}", 
                    transform=ax4.transAxes, ha='center', va='center',
                    fontsize=12, fontweight='bold',
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow", alpha=0.7))
            ax4.set_title('Atomic Structure')
            ax4.axis('off')
        
        fig.tight_layout()
        
        # Convert to base64
        img_buffer = io.BytesIO()
        fig.savefig(img_buffer, format='png', bbox_inches='tight', dpi=100)
        img_buffer.seek(0)
        viz_img = base64.b64encode(img_buffer.getvalue()).decode()
        
        plt.close('all')  # Clean up
        
        return jsonify({
            'success': True,
            'visualization': viz_img,
            'element': element
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# Waves Module Routes
@app.route('/api/waves/generate', methods=['POST'])
def generate_wave():
    """Generate quantum wave visualization."""
    try:
        data = request.get_json()
        frequency = data.get('frequency', 1.0)
        amplitude = data.get('amplitude', 1.0)
        phase = data.get('phase', 0.0)
        wave_type = data.get('wave_type', 'sine')
        
        # Create wave visualization
        fig = Figure(figsize=(12, 8), dpi=100)
        fig.patch.set_facecolor('white')
        
        # Time array for quantum-scale visualization
        t = np.linspace(0, 4 * np.pi, 1000)
        
        # Calculate wave based on type
        if wave_type == 'sine':
            wave = amplitude * np.sin(frequency * t + phase * np.pi)
            wave_title = f"Quantum Sine Wave (f={frequency}Hz, A={amplitude}, φ={phase}π)"
        elif wave_type == 'cosine':
            wave = amplitude * np.cos(frequency * t + phase * np.pi)
            wave_title = f"Quantum Cosine Wave (f={frequency}Hz, A={amplitude}, φ={phase}π)"
        elif wave_type == 'square':
            wave = amplitude * np.sign(np.sin(frequency * t + phase * np.pi))
            wave_title = f"Quantum Square Wave (f={frequency}Hz, A={amplitude}, φ={phase}π)"
        elif wave_type == 'probability':
            wave = amplitude * np.sin(frequency * t + phase * np.pi)**2
            wave_title = f"Quantum Probability Wave (f={frequency}Hz, A={amplitude}, φ={phase}π)"
        else:
            wave = amplitude * np.sin(frequency * t + phase * np.pi)
            wave_title = f"Default Quantum Wave (f={frequency}Hz, A={amplitude}, φ={phase}π)"
        
        # Create subplots
        ax1 = fig.add_subplot(2, 2, 1)
        ax1.plot(t, wave, 'b-', linewidth=2, label=f'{wave_type.capitalize()} Wave')
        ax1.set_xlabel('Time (quantum units)')
        ax1.set_ylabel('Amplitude')
        ax1.set_title(wave_title)
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # Phase space representation
        ax2 = fig.add_subplot(2, 2, 2)
        derivative = np.gradient(wave, t)
        ax2.plot(wave, derivative, 'r-', linewidth=2, alpha=0.7)
        ax2.set_xlabel('Position')
        ax2.set_ylabel('Momentum')
        ax2.set_title('Phase Space Trajectory')
        ax2.grid(True, alpha=0.3)
        
        # Frequency spectrum
        ax3 = fig.add_subplot(2, 2, 3)
        fft_wave = np.fft.fft(wave)
        frequencies = np.fft.fftfreq(len(t), t[1] - t[0])
        magnitude = np.abs(fft_wave)
        ax3.plot(frequencies[:len(frequencies)//2], magnitude[:len(magnitude)//2], 'g-', linewidth=2)
        ax3.set_xlabel('Frequency (Hz)')
        ax3.set_ylabel('Magnitude')
        ax3.set_title('Frequency Spectrum')
        ax3.grid(True, alpha=0.3)
        
        # Energy distribution
        ax4 = fig.add_subplot(2, 2, 4)
        energy = wave**2
        ax4.fill_between(t, energy, alpha=0.6, color='purple')
        ax4.plot(t, energy, 'purple', linewidth=2)
        ax4.set_xlabel('Time (quantum units)')
        ax4.set_ylabel('Energy Density')
        ax4.set_title('Quantum Energy Distribution')
        ax4.grid(True, alpha=0.3)
        
        fig.tight_layout()
        
        # Convert to base64
        img_buffer = io.BytesIO()
        fig.savefig(img_buffer, format='png', bbox_inches='tight', dpi=100)
        img_buffer.seek(0)
        plot_img = base64.b64encode(img_buffer.getvalue()).decode()
        
        plt.close('all')
        
        # Calculate wave properties
        max_amplitude = np.max(np.abs(wave))
        rms_value = np.sqrt(np.mean(wave**2))
        total_energy = np.sum(energy)
        
        info_text = f"""Wave Analysis:
Type: {wave_type.capitalize()}
Frequency: {frequency} Hz
Amplitude: {amplitude}
Phase: {phase}π radians
Maximum Amplitude: {max_amplitude:.3f}
RMS Value: {rms_value:.3f}
Total Energy: {total_energy:.3f}
Period: {2*np.pi/frequency:.3f} quantum units"""
        
        return jsonify({
            'success': True,
            'plot_image': plot_img,
            'info_text': info_text
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# Pandas Module Routes
@app.route('/api/pandas/load/<dataset>')
def load_dataset(dataset):
    """Load a sample dataset."""
    filename = f"{dataset}.csv"
    file_path = os.path.join(DATASETS_BASE_DIR, filename)

    app.logger.info(f"Attempting to load dataset: {file_path}")

    if not os.path.exists(file_path):
        app.logger.error(f"Dataset file not found: {file_path}")
        available_datasets = []
        if os.path.exists(DATASETS_BASE_DIR):
            available_datasets = [f.split('.')[0] for f in os.listdir(DATASETS_BASE_DIR) if f.endswith('.csv')]
        
        return jsonify({
            'success': False, 
            'error': f"Dataset '{dataset}' (file: {filename}) not found in {DATASETS_BASE_DIR}. Available: {available_datasets}"
        }), 404

    try:
        df = pd.read_csv(file_path)
        preview = df.head().to_html(classes='table table-striped', justify='left')
        
        app.logger.info(f"Dataset {filename} loaded successfully.")
        return jsonify({'success': True, 'preview': preview, 'dataset_name': dataset})
    except pd.errors.EmptyDataError:
        app.logger.error(f"Empty data error for dataset: {file_path}")
        return jsonify({'success': False, 'error': f"The dataset file '{filename}' is empty."}), 400
    except Exception as e:
        app.logger.error(f"Error loading dataset {filename}: {e}")
        app.logger.error(traceback.format_exc())
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/pandas/analyze/<dataset>/<analysis_type>')
def analyze_data(dataset, analysis_type):
    """Perform data analysis on the loaded dataset."""
    try:
        # Retrieve the dataframe
        df = pd.read_csv(os.path.join(DATASETS_BASE_DIR, f"{dataset}.csv"))
        
        # Create analysis based on type
        fig = Figure(figsize=(12, 8), dpi=100)
        fig.patch.set_facecolor('white')
        
        summary = None
        
        if analysis_type == 'describe':
            # Statistical summary
            summary = df.describe().to_string()
            
            # Create correlation heatmap
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 1:
                ax = fig.add_subplot(1, 1, 1)
                corr_matrix = df[numeric_cols].corr()
                im = ax.imshow(corr_matrix, cmap='coolwarm', aspect='auto')
                
                # Add colorbar
                fig.colorbar(im, ax=ax)
                
                # Set ticks and labels
                ax.set_xticks(range(len(numeric_cols)))
                ax.set_yticks(range(len(numeric_cols)))
                ax.set_xticklabels(numeric_cols, rotation=45)
                ax.set_yticklabels(numeric_cols)
                
                # Add correlation values
                for i in range(len(numeric_cols)):
                    for j in range(len(numeric_cols)):
                        ax.text(j, i, f'{corr_matrix.iloc[i, j]:.2f}', 
                               ha='center', va='center')
                
                ax.set_title('Correlation Matrix')
            
        elif analysis_type == 'correlation':
            # Correlation analysis
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) >= 2:
                ax = fig.add_subplot(1, 1, 1)
                corr_matrix = df[numeric_cols].corr()
                
                # Create heatmap using matplotlib
                im = ax.imshow(corr_matrix, cmap='RdYlBu_r', aspect='auto', vmin=-1, vmax=1)
                fig.colorbar(im, ax=ax)
                
                ax.set_xticks(range(len(numeric_cols)))
                ax.set_yticks(range(len(numeric_cols)))
                ax.set_xticklabels(numeric_cols, rotation=45)
                ax.set_yticklabels(numeric_cols)
                
                for i in range(len(numeric_cols)):
                    for j in range(len(numeric_cols)):
                        ax.text(j, i, f'{corr_matrix.iloc[i, j]:.2f}', 
                               ha='center', va='center', 
                               color='white' if abs(corr_matrix.iloc[i, j]) > 0.5 else 'black')
                
                ax.set_title('Correlation Analysis')
                summary = corr_matrix.to_string()
            
        elif analysis_type == 'histogram':
            # Histogram of numeric columns
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            n_cols = min(4, len(numeric_cols))
            
            for i, col in enumerate(numeric_cols[:n_cols]):
                ax = fig.add_subplot(2, 2, i+1)
                ax.hist(df[col].dropna(), bins=20, alpha=0.7, edgecolor='black')
                ax.set_title(f'Distribution of {col}')
                ax.set_xlabel(col)
                ax.set_ylabel('Frequency')
                ax.grid(True, alpha=0.3)
                
        elif analysis_type == 'scatter':
            # Scatter plot of first two numeric columns
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) >= 2:
                ax = fig.add_subplot(1, 1, 1)
                x_col, y_col = numeric_cols[0], numeric_cols[1]
                ax.scatter(df[x_col], df[y_col], alpha=0.6)
                ax.set_xlabel(x_col)
                ax.set_ylabel(y_col)
                ax.set_title(f'Scatter Plot: {x_col} vs {y_col}')
                ax.grid(True, alpha=0.3)
                
        elif analysis_type == 'boxplot':
            # Box plots of numeric columns
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            n_cols = min(4, len(numeric_cols))
            
            for i, col in enumerate(numeric_cols[:n_cols]):
                ax = fig.add_subplot(2, 2, i+1)
                ax.boxplot(df[col].dropna())
                ax.set_title(f'Box Plot of {col}')
                ax.set_ylabel(col)
                ax.grid(True, alpha=0.3)
        
        fig.tight_layout()
        
        # Convert to base64
        img_buffer = io.BytesIO()
        fig.savefig(img_buffer, format='png', bbox_inches='tight', dpi=100)
        img_buffer.seek(0)
        plot_img = base64.b64encode(img_buffer.getvalue()).decode()
        
        plt.close('all')
        
        info_text = f"Analysis Type: {analysis_type.replace('_', ' ').title()}\nDataset: {dataset}\nRows: {len(df)}\nColumns: {len(df.columns)}"
        
        return jsonify({
            'success': True,
            'plot_image': plot_img,
            'summary': summary,
            'info_text': info_text
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# Mathematical Tools Module Routes
@app.route('/api/math/matrix/create', methods=['POST'])
def create_matrix_api():
    print("[DEBUG-MATH] API /api/math/matrix/create called")
    try:
        data = request.get_json()
        matrix_type = data.get('matrix_type', 'random')
        size = int(data.get('size', 3))
        
        if size < 1 or size > 10: # Limitar tamaño por seguridad/rendimiento
            return jsonify({'success': False, 'error': 'Matrix size must be between 1 and 10.'})

        matrix = []
        np.random.seed(None) # Refrescar seed para aleatoriedad

        if matrix_type == 'random':
            matrix = np.random.rand(size, size) * 10 # Valores entre 0 y 10
        elif matrix_type == 'identity':
            matrix = np.identity(size)
        elif matrix_type == 'zeros':
            matrix = np.zeros((size, size))
        elif matrix_type == 'ones':
            matrix = np.ones((size, size))
        elif matrix_type == 'symmetric':
            temp_matrix = np.random.rand(size, size) * 10
            matrix = (temp_matrix + temp_matrix.T) / 2
        elif matrix_type == 'diagonal':
            matrix = np.diag(np.random.rand(size) * 10)
        # TODO: Orthogonal matrix generation is more complex, placeholder for now
        elif matrix_type == 'orthogonal': 
            # Simplificado: Crear una matriz aleatoria y luego ortogonalizar con QR
            # Esto no garantiza una distribución uniforme de matrices ortogonales aleatorias
            A = np.random.rand(size, size)
            Q, R = scipy.linalg.qr(A)
            matrix = Q
        else:
            return jsonify({'success': False, 'error': 'Invalid matrix type'})
        
        # Convertir a lista de listas para JSON, y redondear floats
        matrix_list = [[round(val, 3) for val in row] for row in matrix.tolist()]
        
        print(f"[DEBUG-MATH] Matrix created: {matrix_list}")
        return jsonify({'success': True, 'matrix': matrix_list, 'size': size, 'type': matrix_type})
    except Exception as e:
        print(f"[DEBUG-MATH] Error in create_matrix_api: {str(e)}\n{traceback.format_exc()}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/math/matrix/analyze', methods=['POST'])
def analyze_matrix_api():
    print("[DEBUG-MATH] API /api/math/matrix/analyze called")
    try:
        data = request.get_json()
        matrix_list = data.get('matrix')
        operation = data.get('operation')
        
        if not matrix_list or not operation:
            return jsonify({'success': False, 'error': 'Missing matrix or operation'})
            
        matrix = np.array(matrix_list)
        result_description = ""
        # Placeholder para visualizaciones si fueran necesarias más adelante
        # visualization_img = None 

        if operation == 'eigenvalues':
            if matrix.shape[0] != matrix.shape[1]:
                return jsonify({'success': False, 'error': 'Eigenvalues require a square matrix.'})
            try:
                eigenvalues, eigenvectors = scipy.linalg.eig(matrix)
                # Convertir complex a string para JSON si es necesario
                eigenvalues_str = [str(e) for e in eigenvalues]
                result_description = f"Eigenvalues: {eigenvalues_str}"
                 # eigenvectors son columnas, podríamos devolverlas también si el frontend las usa
            except scipy.linalg.LinAlgError as lae:
                return jsonify({'success': False, 'error': f'Linear algebra error: {str(lae)}'})
        elif operation == 'svd':
            try:
                U, s, Vh = scipy.linalg.svd(matrix)
                singular_values_str = [str(round(val, 3)) for val in s]
                result_description = f"Singular Values: {singular_values_str}\nU shape: {U.shape}, Vh shape: {Vh.shape}"
            except scipy.linalg.LinAlgError as lae:
                return jsonify({'success': False, 'error': f'Linear algebra error: {str(lae)}'})
        elif operation == 'determinant':
            if matrix.shape[0] != matrix.shape[1]:
                return jsonify({'success': False, 'error': 'Determinant requires a square matrix.'})
            try:
                det = scipy.linalg.det(matrix)
                result_description = f"Determinant: {det:.3f}"
            except scipy.linalg.LinAlgError as lae:
                return jsonify({'success': False, 'error': f'Linear algebra error: {str(lae)}'})
        elif operation == 'inverse':
            if matrix.shape[0] != matrix.shape[1]:
                return jsonify({'success': False, 'error': 'Inverse requires a square matrix.'})
            try:
                inv_matrix = scipy.linalg.inv(matrix)
                inv_matrix_list = [[round(val, 3) for val in row] for row in inv_matrix.tolist()]
                result_description = f"Inverse Matrix: {inv_matrix_list}"
            except scipy.linalg.LinAlgError:
                 return jsonify({'success': False, 'error': 'Matrix is singular, cannot compute inverse.'})
            except ValueError as ve: # Por si la matriz no es cuadrada antes de inv
                 return jsonify({'success': False, 'error': str(ve)})
        elif operation == 'rank':
            rank = np.linalg.matrix_rank(matrix)
            result_description = f"Rank: {rank}"
        elif operation == 'condition':
            cond = np.linalg.cond(matrix)
            result_description = f"Condition Number: {cond:.3e}"
        elif operation == 'trace':
            if matrix.shape[0] != matrix.shape[1]:
                return jsonify({'success': False, 'error': 'Trace requires a square matrix.'})
            trace = np.trace(matrix)
            result_description = f"Trace: {trace:.3f}"
        elif operation == 'norm': # Frobenius norm por defecto
            norm = scipy.linalg.norm(matrix, 'fro')
            result_description = f"Frobenius Norm: {norm:.3f}"
        else:
            return jsonify({'success': False, 'error': 'Invalid operation'})

        print(f"[DEBUG-MATH] Analysis result: {result_description}")        
        return jsonify({'success': True, 'description': result_description})

    except Exception as e:
        print(f"[DEBUG-MATH] Error in analyze_matrix_api: {str(e)}\n{traceback.format_exc()}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/math/graph/create', methods=['POST'])
def create_graph_api():
    print("[DEBUG-MATH-GRAPH] API /api/math/graph/create called")
    try:
        data = request.get_json()
        graph_type = data.get('graph_type', 'random')
        num_nodes = int(data.get('num_nodes', 5))
        probability = float(data.get('probability', 0.3))

        if num_nodes < 1 or num_nodes > 50: # Limitar por rendimiento
            return jsonify({'success': False, 'error': 'Number of nodes must be between 1 and 50.'})

        G = None
        if graph_type == 'random':
            G = nx.gnp_random_graph(num_nodes, probability, seed=None)
        elif graph_type == 'complete':
            G = nx.complete_graph(num_nodes)
        elif graph_type == 'cycle':
            G = nx.cycle_graph(num_nodes)
        elif graph_type == 'path':
            G = nx.path_graph(num_nodes)
        elif graph_type == 'star':
            G = nx.star_graph(num_nodes) # n = num_nodes + 1 total (n-1 radios), aqui n es el total de nodos incluyendo el centro
        elif graph_type == 'wheel':
            G = nx.wheel_graph(num_nodes) # n es el total de nodos
        else:
            return jsonify({'success': False, 'error': 'Invalid graph type'})
        
        adj_matrix = nx.to_numpy_array(G).tolist()
        num_edges = G.number_of_edges()

        print(f"[DEBUG-MATH-GRAPH] Graph created: nodes={num_nodes}, edges={num_edges}, type={graph_type}")
        return jsonify({
            'success': True, 
            'adjacency_matrix': adj_matrix,
            'num_nodes': num_nodes,
            'num_edges': num_edges,
            'graph_type': graph_type
        })
    except Exception as e:
        print(f"[DEBUG-MATH-GRAPH] Error in create_graph_api: {str(e)}\n{traceback.format_exc()}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/math/graph/analyze', methods=['POST'])
def analyze_graph_api():
    print("[DEBUG-MATH-GRAPH] API /api/math/graph/analyze called")
    try:
        data = request.get_json()
        adj_matrix_list = data.get('adjacency_matrix')
        if not adj_matrix_list:
            return jsonify({'success': False, 'error': 'Missing adjacency matrix'})

        # Convert list of lists to NetworkX graph
        adj_matrix_np = np.array(adj_matrix_list)
        G = nx.from_numpy_array(adj_matrix_np)

        properties = {
            'num_nodes': G.number_of_nodes(),
            'num_edges': G.number_of_edges(),
            'density': nx.density(G),
            'is_connected': nx.is_connected(G) if G.number_of_nodes() > 0 else False,
            'average_degree': sum(d for n, d in G.degree()) / G.number_of_nodes() if G.number_of_nodes() > 0 else 0
        }
        
        shortest_paths_data = None
        if properties['is_connected'] and G.number_of_nodes() > 0:
            try:
                diameter = nx.diameter(G)
                avg_shortest_path = nx.average_shortest_path_length(G)
                shortest_paths_data = {
                    'diameter': diameter,
                    'average_distance': avg_shortest_path
                }
            except nx.NetworkXError as nx_err: 
                print(f"[DEBUG-MATH-GRAPH] NetworkXError in shortest path calculations: {nx_err}")
                shortest_paths_data = {'diameter': 'N/A (e.g. disconnected)', 'average_distance': 'N/A'}
        
        graph_viz_img = None
        if G.number_of_nodes() > 0 and G.number_of_nodes() < 50: # Evitar dibujar grafos muy grandes
            try:
                fig, ax = plt.subplots(figsize=(8, 6), dpi=100)
                nx.draw(G, ax=ax, with_labels=True, node_color='skyblue', node_size=700, edge_color='gray')
                ax.set_title(f"Graph Visualization ({G.number_of_nodes()} nodes, {G.number_of_edges()} edges)", fontsize=10)
                buf = io.BytesIO()
                fig.savefig(buf, format='png', bbox_inches='tight')
                plt.close(fig) # Cerrar la figura para liberar memoria
                buf.seek(0)
                graph_viz_img = base64.b64encode(buf.getvalue()).decode('utf-8')
                print("[DEBUG-MATH-GRAPH] Graph visualization generated.")
            except Exception as viz_err:
                print(f"[DEBUG-MATH-GRAPH] Error generating graph visualization: {viz_err}")
                # No enviar imagen si falla la visualización, pero el resto puede ser exitoso

        print(f"[DEBUG-MATH-GRAPH] Graph properties: {properties}")
        return jsonify({
            'success': True, 
            'properties': properties,
            'shortest_paths': shortest_paths_data,
            'visualization': graph_viz_img 
        })
    except Exception as e:
        print(f"[DEBUG-MATH-GRAPH] Error in analyze_graph_api: {str(e)}\n{traceback.format_exc()}")
        return jsonify({'success': False, 'error': str(e)})

# --- Rutas para el Módulo Notebooks ---
@app.route('/api/notebooks/files', methods=['GET'])
def get_notebook_files_api():
    notebooks_dir = NOTEBOOKS_BASE_DIR
    files = []
    print(f"[DEBUG] Attempting to list files from: {os.path.abspath(notebooks_dir)}")
    
    if not os.path.exists(notebooks_dir):
        print(f"[DEBUG] Notebooks directory {notebooks_dir} does NOT exist.")
        try:
            os.makedirs(notebooks_dir)
            print(f"[DEBUG] Created notebooks directory {notebooks_dir} as it was missing.")
            example_file_path = os.path.join(notebooks_dir, 'example_notebook.py')
            if not os.path.exists(example_file_path):
                 with open(example_file_path, 'w', encoding='utf-8') as f:
                     f.write('# Example Notebook\nprint("Hello from AppSpyder Notebook!")\nimport matplotlib.pyplot as plt\nimport numpy as np\nx = np.linspace(0, 10, 100)\nplt.plot(x, np.sin(x))\nplt.title("Example Sine Wave")')
                 print(f"[DEBUG] Created example notebook: {example_file_path}")
                 files.append('example_notebook.py')

        except Exception as e_create:
            print(f"[DEBUG] Failed to create notebooks directory {notebooks_dir}: {e_create}")
            return jsonify({'success': False, 'error': f'Notebooks directory not found and could not be created at {notebooks_dir}'})
    
    try:
        for file_name in os.listdir(notebooks_dir):
            if file_name.endswith('.py'):
                if file_name not in files:
                    files.append(file_name)
        print(f"[DEBUG] Found notebook files: {files}")
        return jsonify({'success': True, 'files': files})
    except Exception as e:
        print(f"[DEBUG] Error listing notebook files: {str(e)}")
        return jsonify({'success': False, 'error': f'Error listing notebook files: {str(e)}'})

@app.route('/api/notebooks/load/<path:filename>', methods=['GET'])
def load_notebook_script_api(filename):
    if not filename:
        return jsonify({"success": False, "error": "No filename provided"}), 400
    if '..' in filename or filename.startswith('/'): # Basic security check
        return jsonify({"success": False, "error": "Invalid filename"}), 400

    full_file_path = os.path.join(NOTEBOOKS_BASE_DIR, filename)
    app.logger.info(f"Loading notebook script content from: {full_file_path}")

    if not os.path.exists(full_file_path) or not os.path.isfile(full_file_path):
        app.logger.error(f"Notebook script not found: {full_file_path}")
        return jsonify({"success": False, "error": "Notebook script not found"}), 404

    try:
        with open(full_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        formatted_content = format_python_code(content)
        
        return jsonify({
            "success": True, 
            "filename": filename, 
            "content": content, # Contenido crudo
            "formatted_content": formatted_content # Contenido formateado
        })
    except Exception as e:
        app.logger.error(f"Error loading notebook script {filename}: {e}")
        app.logger.error(traceback.format_exc())
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/notebooks/execute/<path:filename>', methods=['GET'])
def execute_notebook_api(filename):
    if not filename:
        return jsonify({"success": False, "error": "No filename provided"}), 400
    if '..' in filename or filename.startswith('/'): # Basic security check
        return jsonify({"success": False, "error": "Invalid filename"}), 400

    full_file_path = os.path.join(NOTEBOOKS_BASE_DIR, filename)
    app.logger.info(f"Executing notebook script: {full_file_path}")

    if not os.path.exists(full_file_path) or not os.path.isfile(full_file_path):
        app.logger.error(f"Notebook script not found for execution: {full_file_path}")
        return jsonify({"success": False, "error": "Notebook script not found"}), 404

    try:
        # Usar FileLoader para ejecutar el script
        execution_result = file_loader.execute_notebook_script(full_file_path)
        
        stdout_output = execution_result.get('stdout_output', '')
        figure_base64 = execution_result.get('figure_base64', None)

        # Formatear stdout si es necesario (Pygments para tracebacks, etc.)
        formatted_stdout = format_python_code(stdout_output) if stdout_output else "<p>No standard output produced.</p>"
        
        app.logger.info(f"Notebook {filename} executed. Stdout length: {len(stdout_output)}. Figure generated: {figure_base64 is not None}")

        return jsonify({
            "success": True,
            "filename": filename,
            "stdout": formatted_stdout, # Usar el stdout formateado
            "image": figure_base64
        })
    except Exception as e:
        app.logger.error(f"Error executing notebook {filename}: {e}")
        app.logger.error(traceback.format_exc())
        # Devolver el traceback en el stdout si es posible, para depuración en el frontend
        error_output = f"Error executing notebook:\n{traceback.format_exc()}"
        formatted_error_output = format_python_code(error_output)
        return jsonify({"success": False, "error": str(e), "stdout": formatted_error_output}), 500

@app.route('/api/generate_sample_pdf')
def generate_sample_pdf():
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="¡Hola Mundo desde un PDF generado con Flask y PyFPDF!", ln=1, align="C")
        
        # Guardar PDF en un buffer de bytes
        pdf_output_buffer = io.BytesIO()
        # pdf_bytes = pdf.output(dest='S').encode('latin-1') # 'S' para string, luego encode a bytes
        pdf_bytes = pdf.output(dest='B') # 'B' para obtener bytes directamente
        pdf_output_buffer.write(pdf_bytes)
        pdf_output_buffer.seek(0)
        
        return send_file(
            pdf_output_buffer,
            as_attachment=True,
            download_name='informe_ejemplo.pdf',
            mimetype='application/pdf'
        )
    except Exception as e:
        app.logger.error(f"Error generando PDF de ejemplo: {e}")
        app.logger.error(traceback.format_exc())
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    # La función ensure_directories() en config.py ya se habrá ejecutado al importar config.
    # Puedes añadir más lógica de inicialización aquí si es necesario.
    print(f"Starting Flask app. Static folder: {app.static_folder}")
    print(f"CIRCUITS_BASE_DIR: {CIRCUITS_BASE_DIR}")
    print(f"GRAPHS_BASE_DIR: {GRAPHS_BASE_DIR}")
    print(f"NOTEBOOKS_BASE_DIR: {NOTEBOOKS_BASE_DIR}")
    print(f"DATASETS_BASE_DIR: {DATASETS_BASE_DIR}")
    app.run(host='0.0.0.0', port=5000, debug=True)