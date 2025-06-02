"""
Electromagnetism physics module for AppSpyder application.
Based on the TypeScript ElectroMag class with electromagnetic calculations.
"""

import math
import numpy as np
from typing import Dict, Any
from .quantum_wave import PhysicsConstants

class ElectroMag:
    """
    Electromagnetism class with electric field and charge density calculations.
    """
    
    # Electric charge constants
    COULOMB = 1.602176634e-19  # Elementary charge in Coulombs (C)
    
    @staticmethod
    def calculate_electric_flux(total_charge: float) -> float:
        """
        Calculates the electric flux (Φ) through a closed surface using Gauss's Law.
        Φ = Q / ε₀
        
        Args:
            total_charge: The total electric charge enclosed within the surface (in Coulombs)
            
        Returns:
            The electric flux in N·m²/C or V·m
        """
        return total_charge / PhysicsConstants.PERMITIVITI_0
    
    @staticmethod
    def calculate_electric_field_magnitude(flux: float, radius: float) -> float:
        """
        Calculates the magnitude of the electric field (E) for a spherically symmetric charge
        distribution, outside the distribution.
        E = Φ / (4 * π * r²)
        
        Args:
            flux: The electric flux (Φ) calculated for a Gaussian surface (N·m²/C or V·m)
            radius: The distance from the center of the charge distribution (radius of the Gaussian surface) in meters
            
        Returns:
            The magnitude of the electric field in N/C or V/m
        """
        if radius == 0:
            return 0
        return flux / (4 * math.pi * (radius ** 2))
    
    @staticmethod
    def calculate_linear_charge_density(total_charge: float, length: float) -> float:
        """
        Calculates the linear charge density (λ) of an object.
        λ = Q / L
        
        Args:
            total_charge: The total charge on the object (in Coulombs)
            length: The length over which the charge is distributed (in meters)
            
        Returns:
            The linear charge density in C/m
        """
        if length == 0:
            print("Warning: Attempted to calculate linear charge density with zero length. Returning 0.")
            return 0
        return total_charge / length
    
    @staticmethod
    def calculate_surface_charge_density(total_charge: float, area: float) -> float:
        """
        Calculates the surface charge density (σ) of an object.
        σ = Q / A
        
        Args:
            total_charge: The total charge on the object (in Coulombs)
            area: The surface area over which the charge is distributed (in square meters)
            
        Returns:
            The surface charge density in C/m²
        """
        if area == 0:
            print("Warning: Attempted to calculate surface charge density with zero area. Returning 0.")
            return 0
        return total_charge / area
    
    @staticmethod
    def calculate_volume_charge_density(total_charge: float, volume: float) -> float:
        """
        Calculates the volume charge density (ρ) of an object.
        ρ = Q / V
        
        Args:
            total_charge: The total charge on the object (in Coulombs)
            volume: The volume over which the charge is distributed (in cubic meters)
            
        Returns:
            The volume charge density in C/m³
        """
        if volume == 0:
            print("Warning: Attempted to calculate volume charge density with zero volume. Returning 0.")
            return 0
        return total_charge / volume
    
    @staticmethod
    def calculate_coulomb_force(charge1: float, charge2: float, distance: float) -> float:
        """
        Calculates the Coulomb force between two point charges.
        F = k * |q₁ * q₂| / r²
        where k = 1/(4πε₀) ≈ 8.99 × 10⁹ N·m²/C²
        
        Args:
            charge1: First charge in Coulombs
            charge2: Second charge in Coulombs
            distance: Distance between charges in meters
            
        Returns:
            Force magnitude in Newtons
        """
        if distance == 0:
            return float('inf')
        
        k = 1 / (4 * math.pi * PhysicsConstants.PERMITIVITI_0)  # Coulomb's constant
        if PhysicsConstants.PERMITIVITI_0 == 1:  # Use standard value if simplified
            k = 8.99e9  # N·m²/C²
        
        return k * abs(charge1 * charge2) / (distance ** 2)
    
    @staticmethod
    def calculate_electric_potential(charge: float, distance: float) -> float:
        """
        Calculates the electric potential at a distance from a point charge.
        V = k * Q / r
        
        Args:
            charge: Charge in Coulombs
            distance: Distance from charge in meters
            
        Returns:
            Electric potential in Volts
        """
        if distance == 0:
            return float('inf')
        
        k = 1 / (4 * math.pi * PhysicsConstants.PERMITIVITI_0)
        if PhysicsConstants.PERMITIVITI_0 == 1:
            k = 8.99e9
        
        return k * charge / distance

class GravityUtil:
    """
    Gravity utility class with gravitational calculations.
    Based on the TypeScript GravityUtil class.
    """
    
    @staticmethod
    def get_attraction_force(distance: float, mass_a: float, mass_b: float) -> float:
        """
        Calculate gravitational attraction force between two masses.
        F = G * m₁ * m₂ / r²
        
        Args:
            distance: Distance between masses in meters
            mass_a: First mass in kg
            mass_b: Second mass in kg
            
        Returns:
            Gravitational force in Newtons
        """
        if distance <= 0 or mass_a < 0 or mass_b < 0:
            return 0
        
        force = PhysicsConstants.G * (mass_a * mass_b) / (distance ** 2)
        return force
    
    @staticmethod
    def get_weight(mass: float) -> float:
        """
        Calculate weight using standard gravity.
        W = m * g
        
        Args:
            mass: Mass in kg
            
        Returns:
            Weight in Newtons
        """
        return PhysicsConstants.NEWTON_G * mass
    
    @staticmethod
    def get_mass_energy(mass: float) -> float:
        """
        Calculate mass-energy equivalence.
        E = mc²
        
        Args:
            mass: Mass in kg
            
        Returns:
            Energy in Joules
        """
        return mass * (PhysicsConstants.C ** 2)
    
    @staticmethod
    def calculate_deformation_influence_flux(mass_analog: float) -> float:
        """
        Calculates the total "deforming influence" (Φ_analog) emanating from the mass.
        This is analogous to electric flux Φ = Q / ε₀, but using mass as the source.
        Φ_analog = mass_analog / PERMITIVITI_0
        
        Args:
            mass_analog: The total "deforming mass" or "influence source"
            
        Returns:
            The total deforming influence, analogous to electric flux
        """
        return mass_analog / PhysicsConstants.PERMITIVITI_0
    
    @staticmethod
    def calculate_deformation_field_magnitude(influence_flux: float, distance: float) -> float:
        """
        Calculates the magnitude of the "deforming field" (E_analog) at a given distance
        from a spherically symmetric mass source, outside its volume.
        E_analog = Φ_analog / (4 * π * r²)
        
        Args:
            influence_flux: The total deforming influence flux (Φ_analog)
            distance: The distance from the center of the mass source (in meters)
            
        Returns:
            The magnitude of the deforming field
        """
        if distance == 0:
            return 0
        return influence_flux / (4 * math.pi * (distance ** 2))

class ElectroMagUtil:
    """
    Extended electromagnetic utilities with visualization helpers.
    """
    
    @staticmethod
    def create_field_line_points(charge: float, center_x: float = 0, center_y: float = 0, 
                                num_lines: int = 8, max_distance: float = 5) -> Dict[str, Any]:
        """
        Generate points for electric field line visualization.
        
        Args:
            charge: Charge magnitude (positive or negative)
            center_x: X coordinate of charge
            center_y: Y coordinate of charge
            num_lines: Number of field lines to generate
            max_distance: Maximum distance for field lines
            
        Returns:
            Dictionary with field line coordinates
        """
        field_lines = []
        
        for i in range(num_lines):
            angle = 2 * math.pi * i / num_lines
            line_points_x = []
            line_points_y = []
            
            for r in np.linspace(0.1, max_distance, 50):
                x = center_x + r * math.cos(angle)
                y = center_y + r * math.sin(angle)
                line_points_x.append(x)
                line_points_y.append(y)
            
            field_lines.append({
                'x': line_points_x,
                'y': line_points_y,
                'direction': 'outward' if charge > 0 else 'inward'
            })
        
        return {
            'field_lines': field_lines,
            'charge': charge,
            'center': [center_x, center_y]
        }
    
    @staticmethod
    def calculate_field_at_point(charges: list, positions: list, test_point: tuple) -> tuple:
        """
        Calculate electric field at a test point due to multiple charges.
        
        Args:
            charges: List of charge values
            positions: List of (x, y) positions for each charge
            test_point: (x, y) coordinates of test point
            
        Returns:
            (Ex, Ey) electric field components
        """
        Ex_total = 0
        Ey_total = 0
        
        for charge, (x_charge, y_charge) in zip(charges, positions):
            dx = test_point[0] - x_charge
            dy = test_point[1] - y_charge
            distance = math.sqrt(dx**2 + dy**2)
            
            if distance > 0:
                k = 8.99e9  # Coulomb's constant
                E_magnitude = k * abs(charge) / (distance**2)
                
                # Unit vector components
                unit_x = dx / distance
                unit_y = dy / distance
                
                # Apply sign of charge
                sign = 1 if charge > 0 else -1
                Ex_total += sign * E_magnitude * unit_x
                Ey_total += sign * E_magnitude * unit_y
        
        return (Ex_total, Ey_total)