# public\graphs\mg_atom.py
import numpy as np
import matplotlib.pyplot as plt
import random 

def create_graph_figure():
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect('equal')
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.axis('off') # Ocultar ejes

    # --- Datos del átomo (Litio como ejemplo, Z=3, N=4) ---
    protons = 3
    neutrons = 4
    electron_shells = [2, 1] 

    # --- Configuración del Núcleo ---
    nucleus_center_x, nucleus_center_y = 0, 0
    
    # Crear una lista de todas las partículas del núcleo
    nucleus_particles_data = (
        [{'type': 'proton', 'color': 'limegreen', 'text': 'p+'}] * protons +
        [{'type': 'neutron', 'color': 'red', 'text': ''}] * neutrons 
    )
    
    shuffled_indices = np.random.permutation(len(nucleus_particles_data))
    shuffled_nucleus_particles = [nucleus_particles_data[i] for i in shuffled_indices]

    base_particle_size = 600 
    jitter_range = 0.5 

    for i, particle in enumerate(shuffled_nucleus_particles): 
        x_particle = nucleus_center_x + np.random.uniform(-jitter_range, jitter_range)
        y_particle = nucleus_center_y + np.random.uniform(-jitter_range, jitter_range)
        
        ax.scatter(
            x_particle, y_particle, 
            s=base_particle_size, 
            color=particle['color'], 
            edgecolors='black', 
            linewidth=1.0, 
            zorder=2 + i * 0.01 
        )
        
        if particle['text']: 
            ax.text(
                x_particle, y_particle, particle['text'], 
                color='black' if particle['type'] == 'proton' else 'white', 
                fontsize=9, 
                ha='center', va='center', 
                zorder=3 + i * 0.01 
            )

    # --- Configuración de las Capas Electrónicas y Electrones ---
    shell_radii = [2.8, 5.5] 

    for i, num_electrons_in_shell in enumerate(electron_shells):
        if i >= len(shell_radii):
            break
        
        radius = shell_radii[i]
        
        circle = plt.Circle((0, 0), radius, color='gray', fill=False, linewidth=1.5, linestyle='-', zorder=1)
        ax.add_artist(circle)

        if num_electrons_in_shell > 0:
            electron_angle_step = 2 * np.pi / num_electrons_in_shell
            for j in range(num_electrons_in_shell):
                angle = j * electron_angle_step
                x_electron = radius * np.cos(angle)
                y_electron = radius * np.sin(angle)
                
                # Sombra mas sutil para el electron
                shadow_offset_x = 0.05 # Muy pequeño desplazamiento a la derecha
                shadow_offset_y = -0.05 # Muy pequeño desplazamiento hacia abajo
                shadow_size_factor = 0.6 # Sombra mas pequeña que el electron
                
                ax.plot(
                    x_electron + shadow_offset_x, y_electron + shadow_offset_y, 'o', 
                    markersize=20 * shadow_size_factor, # Tamaño de la sombra ajustado
                    color='gray', # Color de la sombra
                    markeredgecolor='black', 
                    linewidth=0.2, # Borde mas fino para la sombra
                    zorder=2.9 # Zorder justo detras del electron principal
                )

                # Electron principal: color plateado, mas grande
                ax.plot(
                    x_electron, y_electron, 'o', 
                    markersize=20, 
                    color='silver', 
                    markeredgecolor='black', 
                    linewidth=0.5, 
                    zorder=3
                )
                
                # Texto 'e-' dentro del electron (negro y mas grande)
                ax.text(
                    x_electron, y_electron, 'e-', 
                    color='black', 
                    fontsize=10, 
                    ha='center', va='center', 
                    zorder=4
                )

    return fig
