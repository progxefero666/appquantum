"""
Simple superposition quantum circuit for the AppSpyder Circuits module.
This creates a superposition state on a single qubit.
"""

def create_circuit():
    """Create a simple superposition quantum circuit."""
    try:
        from qiskit import QuantumCircuit
        
        # Create a 1-qubit circuit with 1 classical bit for measurement
        qc = QuantumCircuit(1, 1)
        
        # Apply Hadamard gate to create superposition
        qc.h(0)
        
        # Measure the qubit
        qc.measure(0, 0)
        
        return qc
        
    except ImportError:
        # Fallback if Qiskit is not available
        return "Qiskit not available - install with: pip install qiskit"
    except Exception as e:
        return f"Error creating circuit: {str(e)}"