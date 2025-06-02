"""
Bell State quantum circuit for the AppSpyder Circuits module.
This creates a Bell state (quantum entanglement) between two qubits.
"""

def create_circuit():
    """Create a Bell state quantum circuit."""
    try:
        from qiskit import QuantumCircuit
        
        # Create a 2-qubit circuit with 2 classical bits for measurement
        qc = QuantumCircuit(2, 2)
        
        # Apply Hadamard gate to the first qubit
        qc.h(0)
        
        # Apply CNOT gate with first qubit as control and second as target
        qc.cx(0, 1)
        
        # Measure both qubits
        qc.measure_all()
        
        return qc
        
    except ImportError:
        # Fallback if Qiskit is not available
        return "Qiskit not available - install with: pip install qiskit"
    except Exception as e:
        return f"Error creating circuit: {str(e)}"