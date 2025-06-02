# public\circuit\test\cr_test_a.py

"""
User quantum circuit: test A (Bell State Creation)
"""

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister # Añadimos QuantumRegister y ClassicalRegister
from qiskit_aer import AerSimulator # Necesario para run_quantum_circuit
from collections import Counter # Necesario para el procesamiento de conteos

def create_circuit() -> QuantumCircuit:
    """
    Crea un circuito cuántico que demuestra entrelazamiento cuántico (estado de Bell).
    
    Returns:
        QuantumCircuit: Un circuito cuántico con cúbits entrelazados.
    """
    # Necesitamos 2 cúbits para el entrelazamiento
    qr = QuantumRegister(2, 'q')
    # Necesitamos 2 bits clásicos para las mediciones
    cr = ClassicalRegister(2, 'c')
    
    circuit = QuantumCircuit(qr, cr)
    
    circuit.h(qr[0]) # Aplica Hadamard al primer cúbit para ponerlo en superposición
    circuit.cx(qr[0], qr[1]) # Aplica CNOT usando el primer cúbit como control
    
    # Medimos ambos cúbits. El orden de los bits clásicos importa:
    # cr[0] medirá qr[0], cr[1] medirá qr[1]
    circuit.measure(qr[0], cr[0])
    circuit.measure(qr[1], cr[1])
    
    return circuit

def run_quantum_circuit(circuit: QuantumCircuit) -> dict:
    """
    Ejecuta un circuito cuántico en un simulador y devuelve los conteos de las mediciones.
    Esta es una función genérica que puede ser utilizada por cualquier circuito.
    
    Args:
        circuit (QuantumCircuit): El circuito cuántico a ejecutar.
        
    Returns:
        dict: Un diccionario con los conteos de los resultados de las mediciones.
    """
    simulator = AerSimulator() # Usamos el simulador por defecto (QasmSimulator)
    
    # Ejecuta el circuito 1024 veces (shots) para obtener resultados probabilísticos
    job = simulator.run(circuit, shots=1024)
    
    # Espera a que el trabajo termine y obtiene los resultados
    result = job.result()
    
    # Obtiene los conteos de las mediciones
    counts = result.get_counts(circuit)
    
    return counts

def interpret_test_a_result(counts: dict) -> str:
    """
    Interpreta los conteos de las mediciones del circuito de test A (estado de Bell).
    
    Args:
        counts (dict): El diccionario de conteos de las mediciones.
        
    Returns:
        str: Una cadena de texto con la interpretación de los resultados.
    """
    # Para un estado de Bell ideal, esperaríamos '00' y '11' casi al 50%.
    total_shots = sum(counts.values())
    
    interpretation = "Resultados del Bell State (entrelazamiento):\n"
    
    for outcome, count in counts.items():
        percentage = (count / total_shots) * 100
        # Qiskit los bits se leen de derecha a izquierda (qubit 0 a la derecha, qubit 1 a la izquierda)
        # outcome '00' significa q1=0, q0=0
        # outcome '11' significa q1=1, q0=1
        interpretation += f"  '{outcome}' (q1={outcome[0]}, q0={outcome[1]}): {count} conteos ({percentage:.2f}%)\n"
    
    if '00' in counts and '11' in counts:
        # Esto es una simplificación; en un caso real, haríamos un test estadístico
        interpretation += "  Los resultados '00' y '11' dominan, indicando entrelazamiento. Qubits correlacionados."
    else:
        interpretation += "  Los resultados no muestran la correlación esperada para un Bell State."

    return interpretation