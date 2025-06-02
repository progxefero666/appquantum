"""
Example quantum circuit for the AppSpyder Circuits module.
This creates a simple Bell state (quantum entanglement) circuit.
"""

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

def create_circuit():
    """Create a Bell state quantum circuit."""
    # Create quantum and classical registers
    qreg = QuantumRegister(2, 'q')
    creg = ClassicalRegister(2, 'c')
    
    # Create the circuit
    circuit = QuantumCircuit(qreg, creg, name='Bell State')
    
    # Apply Hadamard gate to first qubit
    circuit.h(qreg[0])
    
    # Apply CNOT gate (controlled by first qubit, target is second qubit)
    circuit.cx(qreg[0], qreg[1])
    
    # Add measurement
    circuit.measure(qreg, creg)
    
    return circuit

# Create the circuit (this variable will be found by the file loader)
circuit = create_circuit()
