# src/chemical/chemicalgraphs/atomic_graphs.py

import numpy as np
import matplotlib.pyplot as plt
import random
import re

class AtomicGraphs:
    def __init__(self):
        pass

    @staticmethod
    def _parse_econfig(econfig_str: str) -> list[int]:
        shell_electrons = {}
        # Patron para extraer el numero de capa (n), subcapa (s,p,d,f) y electrones
        pattern = re.compile(r'(\d+)([spdf])(\d+)')
        
        parts = econfig_str.split()
        for part in parts:
            match = pattern.match(part)
            if match:
                n = int(match.group(1))
                electrons = int(match.group(3))
                shell_electrons[n] = shell_electrons.get(n, 0) + electrons
        
        # Construir la lista de electrones por capa principal
        if not shell_electrons:
            return []

        max_shell = max(shell_electrons.keys())
        result = [0] * max_shell
        for n, electrons in shell_electrons.items():
            if n > 0 and n <= max_shell:
                result[n-1] = electrons
        
        # Eliminar capas vacias al final si las hubiera
        while result and result[-1] == 0:
            result.pop()
        
        return result

    @staticmethod
    def create_graph_figure(atomic_number: int, mass_number: int, econfig_str: str):
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.set_aspect('equal')
        ax.set_xlim(-10, 10)
        ax.set_ylim(-10, 10)
        ax.axis('off')

        # --- Datos del átomo basados en los parámetros ---
        protons = atomic_number
        neutrons = mass_number - atomic_number
        electron_shells = AtomicGraphs._parse_econfig(econfig_str)

        # --- Configuración del Núcleo ---
        nucleus_center_x, nucleus_center_y = 0, 0
        
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
        # Radios de las capas. Ajustar si se necesitan mas de 4 capas
        shell_radii = [2.8, 5.5, 7.5, 9.0] 

        for i, num_electrons_in_shell in enumerate(electron_shells):
            if i >= len(shell_radii):
                # Si hay mas capas que radios definidos, puedes ajustar la logica
                # por ejemplo, extendiendo shell_radii dinamicamente o limitando las capas mostradas.
                # Por ahora, simplemente se detiene.
                break
            
            radius = shell_radii[i]
            
            from matplotlib.patches import Circle
            circle = Circle((0, 0), radius, color='gray', fill=False, linewidth=1.5, linestyle='-', zorder=1)
            ax.add_artist(circle)

            if num_electrons_in_shell > 0:
                electron_angle_step = 2 * np.pi / num_electrons_in_shell
                for j in range(num_electrons_in_shell):
                    angle = j * electron_angle_step
                    x_electron = radius * np.cos(angle)
                    y_electron = radius * np.sin(angle)
                    
                    # Sombra mas sutil para el electron
                    shadow_offset_x = 0.05 
                    shadow_offset_y = -0.05 
                    shadow_size_factor = 0.6 
                    
                    ax.plot(
                        x_electron + shadow_offset_x, y_electron + shadow_offset_y, 'o', 
                        markersize=20 * shadow_size_factor, 
                        color='gray', 
                        markeredgecolor='black', 
                        linewidth=0.2, 
                        zorder=2.9 
                    )

                    # Electron principal
                    ax.plot(
                        x_electron, y_electron, 'o', 
                        markersize=20, 
                        color='silver', 
                        markeredgecolor='black', 
                        linewidth=0.5, 
                        zorder=3
                    )
                    
                    # Texto 'e-' dentro del electron
                    ax.text(
                        x_electron, y_electron, 'e-', 
                        color='black', 
                        fontsize=10, 
                        ha='center', va='center', 
                        zorder=4
                    )

        return fig