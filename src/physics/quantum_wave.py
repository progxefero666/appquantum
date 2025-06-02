"""
Quantum Wave Physics for AppSpyder application.
Based on the TypeScript WaveDef class with quantum mechanical properties.
"""

import math
import numpy as np
from typing import Dict, Any

class PhysicsConstants:
    """Physical constants for quantum calculations."""
    # Time and length scales
    NANOSECOND = 1e-9
    NANOMETER = 1e-9
    
    # Fundamental constants
    C = 299792458  # m/s - speed of light
    PERMITIVITI_0 = 1
    PLANCK_CONSTANT = 6.62607015e-34  # J⋅s
    PLANCK_REDUCED = 1.054571817e-34  # ℏ (h-bar)
    EULERS_NUMBER = math.e  # 2.718281828459045
    
    # Particle masses (in kg)
    ELECTRON_MASS = 9.1093837015e-31
    PROTON_MASS = 1.67262192369e-27
    NEUTRON_MASS = 1.67492749804e-27
    
    # Gravitational constants
    NEWTON_G = 9.80665  # m/s² - standard gravity
    G = 6.67430e-11  # m³/kg·s² - gravitational constant
    EINSTEIN_FACTOR = (8 * math.pi * 6.67430e-11) / (299792458 ** 4)  # s²/kg·m

class QuantumWave:
    """
    Quantum wave definition with particle properties.
    
    Formulas:
    - x(t) = A * sin(2π*freq*t)
    - u(x,t) = A * cos(kx - ωt + φ)
    - k = 2π/λ
    - λ = v/f => λ = c/f => v = λ*f
    - ω = 2π*f (or ω = 2π/T)
    - E = ℏω (for quantum particles)
    - p = ℏk (de Broglie relation)
    - λ = h/p (de Broglie wavelength)
    """

    def __init__(self, frequency: float, amplitude: float, mass: float = None):
        """
        Initialize quantum wave with given parameters.
        
        Args:
            frequency: Wave frequency in Hz
            amplitude: Maximum amplitude
            mass: Particle mass in kg (optional, defaults to electron mass)
        """
        self.frequency = frequency
        self.amplitude_max = amplitude
        self.particle_mass = mass if mass is not None else PhysicsConstants.ELECTRON_MASS
        self.phase = 0.0
        
        # Calculated properties
        self.energy = 0.0
        self.momentum = 0.0
        self.wavelength = 0.0
        self.period = 0.0
        self.wave_velocity = 0.0
        self.particle_velocity = 0.0
        self.angular_frequency = 0.0  # ω
        self.wave_number = 0.0  # k
        
        self._calculate_all_parameters()

    def _calculate_all_parameters(self) -> None:
        """Calculate all wave and particle parameters from basic inputs."""
        # Angular frequency: ω = 2πf
        self.angular_frequency = 2 * math.pi * self.frequency
        
        # Quantum energy relation: E = ℏω
        self.energy = PhysicsConstants.PLANCK_REDUCED * self.angular_frequency
        
        # For a free particle: E = p²/(2m) (non-relativistic)
        # So: p = √(2mE)
        self.momentum = math.sqrt(2 * self.particle_mass * self.energy)
        
        # de Broglie wavelength: λ = h/p
        self.wavelength = PhysicsConstants.PLANCK_CONSTANT / self.momentum
        
        # Wave number: k = 2π/λ
        self.wave_number = 2 * math.pi / self.wavelength
        
        # Period: T = 1/f
        self.period = 1.0 / self.frequency
        
        # Phase velocity: v = λf
        self.wave_velocity = self.wavelength * self.frequency
        
        # Particle velocity: v = p/m
        self.particle_velocity = self.momentum / self.particle_mass

    def get_amplitude_at(self, time: float) -> float:
        """
        Get wave amplitude at given time (temporal oscillation).
        
        Args:
            time: Time in seconds
            
        Returns:
            Amplitude at given time
        """
        return self.amplitude_max * math.cos(self.angular_frequency * time + self.phase)

    def get_phase_at(self, distance: float, time: float) -> float:
        """
        Get wave phase at given position and time.
        φ(x, t) = kx - ωt + φ
        
        Args:
            distance: Position in meters
            time: Time in seconds
            
        Returns:
            Phase value
        """
        return (self.wave_number * distance) - (self.angular_frequency * time) + self.phase

    def get_wave_function(self, distance: float, time: float) -> float:
        """
        Complete wave function: ψ(x,t) = A * cos(kx - ωt + φ)
        
        Args:
            distance: Position in meters
            time: Time in seconds
            
        Returns:
            Wave function value
        """
        phase = self.get_phase_at(distance, time)
        return self.amplitude_max * math.cos(phase)

    def get_oscillation_velocity_at(self, time: float) -> float:
        """
        Calculate oscillation velocity (vertical motion).
        dy/dt = -Aω*sin(ωt)
        
        Args:
            time: Time in seconds
            
        Returns:
            Oscillation velocity
        """
        return -self.amplitude_max * self.angular_frequency * math.sin(
            self.angular_frequency * time + self.phase
        )

    def get_oscillation_acceleration_at(self, time: float) -> float:
        """
        Calculate oscillation acceleration (vertical motion).
        d²y/dt² = -Aω²*cos(ωt)
        
        Args:
            time: Time in seconds
            
        Returns:
            Oscillation acceleration
        """
        return -self.amplitude_max * (self.angular_frequency ** 2) * math.cos(
            self.angular_frequency * time + self.phase
        )

    def get_probability_density(self, distance: float, time: float) -> float:
        """
        Get probability density |ψ(x,t)|²
        
        Args:
            distance: Position in meters
            time: Time in seconds
            
        Returns:
            Probability density
        """
        wave_value = self.get_wave_function(distance, time)
        return wave_value ** 2

    def get_group_velocity(self) -> float:
        """
        Calculate group velocity for wave packet.
        For free particle: v_g = p/m
        
        Returns:
            Group velocity
        """
        return self.particle_velocity

    def get_phase_velocity(self) -> float:
        """
        Calculate phase velocity.
        v_p = ω/k
        
        Returns:
            Phase velocity
        """
        return self.angular_frequency / self.wave_number

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert wave properties to dictionary for JSON serialization.
        
        Returns:
            Dictionary with all wave properties
        """
        return {
            'frequency': self.frequency,
            'amplitude_max': self.amplitude_max,
            'particle_mass': self.particle_mass,
            'phase': self.phase,
            'energy': self.energy,
            'momentum': self.momentum,
            'wavelength': self.wavelength,
            'period': self.period,
            'wave_velocity': self.wave_velocity,
            'particle_velocity': self.particle_velocity,
            'angular_frequency': self.angular_frequency,
            'wave_number': self.wave_number,
            'group_velocity': self.get_group_velocity(),
            'phase_velocity': self.get_phase_velocity()
        }

    def get_properties_summary(self) -> str:
        """
        Get formatted summary of wave properties.
        
        Returns:
            Formatted string with wave properties
        """
        return f"""Quantum Wave Properties:
Frequency: {self.frequency:.2e} Hz
Angular frequency (ω): {self.angular_frequency:.2e} rad/s
Wavelength (λ): {self.wavelength:.2e} m
Wave number (k): {self.wave_number:.2e} m⁻¹
Period (T): {self.period:.2e} s

Particle Properties:
Mass: {self.particle_mass:.2e} kg
Energy: {self.energy:.2e} J
Momentum: {self.momentum:.2e} kg⋅m/s
Particle velocity: {self.particle_velocity:.2e} m/s

Wave Velocities:
Phase velocity: {self.get_phase_velocity():.2e} m/s
Group velocity: {self.get_group_velocity():.2e} m/s

Amplitude: {self.amplitude_max:.3f}
Phase: {self.phase:.3f} rad"""