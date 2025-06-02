# Example Quantum Circuit
from qiskit import QuantumCircuit

# Create a 2-qubit Bell state circuit
qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0,1], [0,1])

# To make this file discoverable by the app, ensure it's a .py file.
# The circuit object should be named 'circuit' or be the last expression.
circuit = qc 