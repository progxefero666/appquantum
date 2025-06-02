"""
3D Bloch Sphere visualization for quantum states.
This creates an interactive 3D visualization of the Bloch sphere with various quantum states.
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def create_plot():
    """Create a 3D Bloch sphere visualization."""
    
    fig = plt.figure(figsize=(12, 10))
    
    # Create 2x2 subplot layout for different views
    ax1 = fig.add_subplot(221, projection='3d')
    ax2 = fig.add_subplot(222, projection='3d')
    ax3 = fig.add_subplot(223, projection='3d')
    ax4 = fig.add_subplot(224, projection='3d')
    
    axes = [ax1, ax2, ax3, ax4]
    titles = ['Estado |0⟩', 'Estado |1⟩', 'Estado |+⟩ (Superposición)', 'Estado |+i⟩ (Fase)']
    
    # Define quantum states as Bloch vectors
    states = [
        [0, 0, 1],    # |0⟩ state (north pole)
        [0, 0, -1],   # |1⟩ state (south pole)
        [1, 0, 0],    # |+⟩ state (x-axis)
        [0, 1, 0]     # |+i⟩ state (y-axis)
    ]
    
    colors = ['red', 'blue', 'green', 'purple']
    
    for ax, title, state, color in zip(axes, titles, states, colors):
        # Create sphere
        u = np.linspace(0, 2 * np.pi, 50)
        v = np.linspace(0, np.pi, 50)
        x_sphere = np.outer(np.cos(u), np.sin(v))
        y_sphere = np.outer(np.sin(u), np.sin(v))
        z_sphere = np.outer(np.ones(np.size(u)), np.cos(v))
        
        # Plot transparent sphere
        ax.plot_surface(x_sphere, y_sphere, z_sphere, alpha=0.1, color='lightblue')
        
        # Plot coordinate axes
        ax.plot([-1.2, 1.2], [0, 0], [0, 0], 'k-', alpha=0.3, linewidth=1)
        ax.plot([0, 0], [-1.2, 1.2], [0, 0], 'k-', alpha=0.3, linewidth=1)
        ax.plot([0, 0], [0, 0], [-1.2, 1.2], 'k-', alpha=0.3, linewidth=1)
        
        # Add equator circle
        theta = np.linspace(0, 2*np.pi, 100)
        x_eq = np.cos(theta)
        y_eq = np.sin(theta)
        z_eq = np.zeros_like(theta)
        ax.plot(x_eq, y_eq, z_eq, 'k--', alpha=0.5, linewidth=1)
        
        # Plot state vector
        ax.quiver(0, 0, 0, state[0], state[1], state[2], 
                 color=color, arrow_length_ratio=0.1, linewidth=3)
        
        # Add state point
        ax.scatter(state[0], state[1], state[2], color=color, s=100, alpha=0.8)
        
        # Labels for axes
        ax.text(1.3, 0, 0, 'X', fontsize=10, fontweight='bold')
        ax.text(0, 1.3, 0, 'Y', fontsize=10, fontweight='bold')
        ax.text(0, 0, 1.3, 'Z', fontsize=10, fontweight='bold')
        
        # Labels for poles
        ax.text(0, 0, 1.2, '|0⟩', fontsize=12, fontweight='bold', ha='center')
        ax.text(0, 0, -1.2, '|1⟩', fontsize=12, fontweight='bold', ha='center')
        
        # Set equal aspect ratio and limits
        ax.set_xlim([-1.2, 1.2])
        ax.set_ylim([-1.2, 1.2])
        ax.set_zlim([-1.2, 1.2])
        ax.set_box_aspect([1,1,1])
        
        # Set title
        ax.set_title(title, fontsize=12, fontweight='bold', pad=20)
        
        # Remove axis ticks for cleaner look
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])
        
        # Set viewing angle
        ax.view_init(elev=20, azim=45)
    
    plt.tight_layout()
    plt.suptitle('Esfera de Bloch - Estados Cuánticos Fundamentales', 
                fontsize=16, fontweight='bold', y=0.98)
    
    return fig