"""
Qiskit integration module for AppSpyder.
Handles quantum circuit execution and visualization with fallback support.
"""

import io
import base64
from typing import Optional, Dict, Any, Tuple
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

# Try to import Qiskit components
QISKIT_AVAILABLE = False
try:
    from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
    from qiskit_aer import AerSimulator
    from qiskit.visualization import plot_histogram, circuit_drawer
    from collections import Counter
    QISKIT_AVAILABLE = True
except ImportError:
    # Create mock classes for compatibility
    class QuantumCircuit:
        def __init__(self, *args, **kwargs):
            pass
    
    class QuantumRegister:
        def __init__(self, *args, **kwargs):
            pass
    
    class ClassicalRegister:
        def __init__(self, *args, **kwargs):
            pass
    
    class AerSimulator:
        def __init__(self, *args, **kwargs):
            pass
    
    Counter = dict

def is_qiskit_available() -> bool:
    """Check if Qiskit is available in the system."""
    return QISKIT_AVAILABLE

def execute_quantum_circuit(circuit_code: str) -> Tuple[Optional[Dict], Optional[str], bool]:
    """
    Execute quantum circuit code and return results.
    
    Returns:
        Tuple of (counts_dict, error_message, success_flag)
    """
    if not QISKIT_AVAILABLE:
        return None, "Qiskit not available", False
    
    try:
        # Create namespace for execution
        namespace = {
            'QuantumCircuit': QuantumCircuit,
            'QuantumRegister': QuantumRegister, 
            'ClassicalRegister': ClassicalRegister,
            'AerSimulator': AerSimulator,
            'Counter': Counter,
            'np': np
        }
        
        # Execute the circuit code
        exec(circuit_code, namespace)
        
        # Look for create_circuit function
        if 'create_circuit' not in namespace:
            return None, "No create_circuit function found", False
        
        # Create the circuit
        circuit = namespace['create_circuit']()
        
        # Look for run_quantum_circuit function
        if 'run_quantum_circuit' in namespace:
            counts = namespace['run_quantum_circuit'](circuit)
        else:
            # Use default execution
            simulator = AerSimulator()
            job = simulator.run(circuit, shots=1024)
            result = job.result()
            counts = result.get_counts(circuit)
        
        return counts, None, True
        
    except Exception as e:
        return None, str(e), False

def create_circuit_diagram(circuit_code: str, filename: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Create circuit diagram using Qiskit if available.
    
    Returns:
        Tuple of (base64_image, error_message)
    """
    if not QISKIT_AVAILABLE:
        return None, "Qiskit not available"
    
    try:
        # Execute code and get circuit
        namespace = {
            'QuantumCircuit': QuantumCircuit,
            'QuantumRegister': QuantumRegister,
            'ClassicalRegister': ClassicalRegister,
            'AerSimulator': AerSimulator,
            'Counter': Counter
        }
        
        exec(circuit_code, namespace)
        
        if 'create_circuit' not in namespace:
            return None, "No create_circuit function found"
        
        circuit = namespace['create_circuit']()
        
        # Create circuit diagram
        fig = circuit_drawer(circuit, output='mpl', style='iqx')
        
        # Convert to base64
        img_buffer = io.BytesIO()
        fig.savefig(img_buffer, format='png', bbox_inches='tight', dpi=100)
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        
        plt.close(fig)
        
        return img_base64, None
        
    except Exception as e:
        return None, str(e)

def create_histogram_plot(counts: Dict[str, int], title: str = "Measurement Results") -> Tuple[Optional[str], Optional[str]]:
    """
    Create histogram plot using Qiskit's plot_histogram if available.
    
    Returns:
        Tuple of (base64_image, error_message)
    """
    if not QISKIT_AVAILABLE:
        return None, "Qiskit not available"
    
    try:
        # Use Qiskit's plot_histogram
        fig = plot_histogram(
            counts,
            title=title,
            figsize=(10, 6),
            color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
        )
        
        # Style the figure
        fig.patch.set_facecolor('white')
        for ax in fig.get_axes():
            ax.grid(True, alpha=0.3, axis='y')
            ax.set_facecolor('white')
        
        # Convert to base64
        img_buffer = io.BytesIO()
        fig.savefig(img_buffer, format='png', bbox_inches='tight', dpi=100)
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        
        plt.close(fig)
        
        return img_base64, None
        
    except Exception as e:
        return None, str(e)

def get_qiskit_namespace():
    """Get Qiskit namespace for circuit execution."""
    return {
        'QuantumCircuit': QuantumCircuit,
        'QuantumRegister': QuantumRegister,
        'ClassicalRegister': ClassicalRegister,
        'AerSimulator': AerSimulator,
        'Counter': Counter,
        'np': np
    }