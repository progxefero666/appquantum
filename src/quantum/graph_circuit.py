# src\quantum\graph_circuit.py

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from qiskit import QuantumCircuit
from qiskit.visualization import circuit_drawer

# --- ELIMINADO: Ya no necesitamos el diccionario DEFAULT_CIRCUIT_STYLE ---

def generate_circuit_diagram_figure(
    quantum_circuit: QuantumCircuit,
    # Eliminamos el parámetro 'style' para usar los estilos por defecto de Qiskit.
    # Si quisieras cambiar el tamaño, puedes modificar estos valores:
    fig_dpi: int = 100,      # DPI: Mayor DPI -> mayor resolución (y tamaño en píxeles si no se escala)
    fig_size: tuple = (6, 4) # Tamaño de la figura en pulgadas (ancho, alto).
                             # Comienza con algo más pequeño como (6,4) o (5,3) para GUIs.
                             # Si el circuito es muy complejo o tiene muchos qubits, puede que necesites más ancho.
) -> Figure:
    """
    Genera un objeto matplotlib Figure que contiene el diagrama del circuito cuántico dado.
    Utiliza el estilo de visualización predeterminado de Qiskit.

    Args:
        quantum_circuit: El objeto Qiskit QuantumCircuit a dibujar.
        fig_dpi: El DPI (puntos por pulgada) para la figura de Matplotlib.
        fig_size: Tupla (ancho, alto) para el tamaño de la figura en pulgadas.

    Returns:
        Un objeto matplotlib.figure.Figure con el diagrama del circuito.
        Devuelve None si ocurre un error o la entrada es inválida.
    """
    if not isinstance(quantum_circuit, QuantumCircuit):
        print("[GraphCircuit] Error: Invalid QuantumCircuit object provided.")
        return None

    try:
        # Crea una nueva figura de Matplotlib con el tamaño y DPI especificados.
        fig = Figure(figsize=fig_size, dpi=fig_dpi)
        
        # ELIMINADO: fig.patch.set_facecolor() para usar el fondo por defecto (transparente/blanco)
        # o el color de fondo del widget de CustomTkinter.

        # Añade unos Ejes que llenan toda la figura.
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis('off') # Desactiva las líneas y etiquetas de los ejes.

        # Dibuja el circuito sobre los Ejes creados.
        # Se elimina el parámetro 'style' para usar el estilo por defecto de Qiskit.
        circuit_drawer(
            quantum_circuit,
            output='mpl',
            ax=ax,
            interactive=False
        )
        
        print(f"[GraphCircuit] Circuit diagram figure generated for: {quantum_circuit.name if hasattr(quantum_circuit, 'name') else 'Unnamed'}")
        return fig

    except Exception as e:
        print(f"[GraphCircuit] Error generating circuit diagram: {e}")
        import traceback
        print(traceback.format_exc())
        
        # En caso de error, devuelve una figura simple con el mensaje de error
        error_fig = Figure(figsize=(6,2), dpi=72)
        error_ax = error_fig.add_subplot(111)
        error_ax.text(0.5, 0.5, f"Error generating circuit diagram:\n{e}",
                      horizontalalignment='center', verticalalignment='center',
                      fontsize=10, color='red', wrap=True)
        error_ax.axis('off')
        return error_fig