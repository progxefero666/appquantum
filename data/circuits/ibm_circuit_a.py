# public\circuit\test\cr_test_a.py

"""
User quantum circuit: test A (Bell State Creation)
"""

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister # Añadimos QuantumRegister y ClassicalRegister
from qiskit_aer import AerSimulator # Necesario para run_quantum_circuit
from collections import Counter # Necesario para el procesamiento de conteos

def create_circuit() -> QuantumCircuit:
    qubits = QuantumRegister(3)
    clbits = ClassicalRegister(3)
    circuit = QuantumCircuit(qubits, clbits)
    (q0, q1, q2) = qubits
    (c0, c1, c2) = clbits
    
    #circuit.h([q0, q1])
    circuit.x(q0)
    circuit.measure(q0, c0)
    circuit.measure(q1, c1)
    with circuit.if_test((clbits, 0b001)):
        circuit.x(q2)
    circuit.measure(q2, c2)
    
    circuit.draw("mpl")
    
    return circuit
