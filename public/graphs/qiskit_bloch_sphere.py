"""
Advanced Bloch Sphere visualization using Qiskit's native capabilities.
This creates official Qiskit Bloch sphere visualizations with quantum state evolution.
"""

import numpy as np
import matplotlib.pyplot as plt

def create_plot():
    """Create Qiskit-based Bloch sphere visualizations."""
    
    try:
        from qiskit.visualization import plot_bloch_vector
        from qiskit.quantum_info import Statevector
        from qiskit import QuantumCircuit
        
        # Create figure with subplots
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        fig.suptitle('Esfera de Bloch - Visualización con Qiskit', fontsize=16, fontweight='bold')
        
        # Define quantum states and their Bloch vectors
        states_info = [
            ('Estado |0⟩', [0, 0, 1]),
            ('Estado |1⟩', [0, 0, -1]),
            ('Estado |+⟩', [1, 0, 0]),
            ('Estado |-⟩', [-1, 0, 0]),
            ('Estado |+i⟩', [0, 1, 0]),
            ('Estado |-i⟩', [0, -1, 0])
        ]
        
        # Plot each state
        for i, (title, vector) in enumerate(states_info):
            row = i // 3
            col = i % 3
            ax = axes[row, col]
            
            # Use Qiskit's plot_bloch_vector
            plot_bloch_vector(vector, ax=ax, title=title)
            
        plt.tight_layout()
        return fig
        
    except ImportError:
        # Fallback if Qiskit visualization is not available
        return create_manual_bloch_sphere()

def create_manual_bloch_sphere():
    """Manual Bloch sphere implementation as fallback."""
    
    fig = plt.figure(figsize=(15, 10))
    
    # Create multiple 3D subplots
    positions = [(2, 3, 1), (2, 3, 2), (2, 3, 3), (2, 3, 4), (2, 3, 5), (2, 3, 6)]
    titles = ['|0⟩', '|1⟩', '|+⟩', '|-⟩', '|+i⟩', '|-i⟩']
    vectors = [[0, 0, 1], [0, 0, -1], [1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0]]
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown']
    
    for pos, title, vector, color in zip(positions, titles, vectors, colors):
        ax = fig.add_subplot(*pos, projection='3d')
        
        # Create sphere surface
        u = np.linspace(0, 2 * np.pi, 30)
        v = np.linspace(0, np.pi, 20)
        x = np.outer(np.cos(u), np.sin(v))
        y = np.outer(np.sin(u), np.sin(v))
        z = np.outer(np.ones(np.size(u)), np.cos(v))
        
        # Plot wireframe sphere
        ax.plot_wireframe(x, y, z, alpha=0.2, color='lightblue', linewidth=0.5)
        
        # Plot coordinate axes
        ax.plot([-1.2, 1.2], [0, 0], [0, 0], 'k-', alpha=0.4, linewidth=1)
        ax.plot([0, 0], [-1.2, 1.2], [0, 0], 'k-', alpha=0.4, linewidth=1)
        ax.plot([0, 0], [0, 0], [-1.2, 1.2], 'k-', alpha=0.4, linewidth=1)
        
        # Plot equatorial circles
        theta = np.linspace(0, 2*np.pi, 100)
        # XY plane (equator)
        ax.plot(np.cos(theta), np.sin(theta), np.zeros_like(theta), 'k--', alpha=0.3)
        # XZ plane
        ax.plot(np.cos(theta), np.zeros_like(theta), np.sin(theta), 'k--', alpha=0.3)
        # YZ plane
        ax.plot(np.zeros_like(theta), np.cos(theta), np.sin(theta), 'k--', alpha=0.3)
        
        # Plot state vector
        ax.quiver(0, 0, 0, vector[0], vector[1], vector[2], 
                 color=color, arrow_length_ratio=0.15, linewidth=4, alpha=0.8)
        
        # Add state point
        ax.scatter(vector[0], vector[1], vector[2], color=color, s=150, alpha=1.0, edgecolors='black')
        
        # Labels
        ax.text(1.4, 0, 0, 'X', fontsize=10, fontweight='bold')
        ax.text(0, 1.4, 0, 'Y', fontsize=10, fontweight='bold')
        ax.text(0, 0, 1.4, '|0⟩', fontsize=10, fontweight='bold')
        ax.text(0, 0, -1.4, '|1⟩', fontsize=10, fontweight='bold')
        
        # Set properties
        ax.set_xlim([-1.3, 1.3])
        ax.set_ylim([-1.3, 1.3])
        ax.set_zlim([-1.3, 1.3])
        ax.set_box_aspect([1,1,1])
        ax.set_title(f'Estado {title}', fontsize=12, fontweight='bold')
        
        # Remove ticks
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])
        
        # Set viewing angle for optimal view
        ax.view_init(elev=25, azim=45)
    
    plt.suptitle('Esfera de Bloch - Estados Cuánticos Básicos', fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    return fig