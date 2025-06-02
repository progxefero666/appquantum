import { Physic } from "../pyshic";


/**
 * class Electromagnetism
 */
export class ElectroMag {

    public static readonly CULOMBIO: number = 1.602176634e-19; // Coulombs (C)

    /**
     * Calculates the electric flux (Φ) through a closed surface using Gauss's Law.
     * Φ = Q / ε₀
     * @param totalCharge The total electric charge enclosed within the surface (in Coulombs).
     * @returns The electric flux in N·m²/C or V·m.
     */
    public static calculateElectricFlux(totalCharge: number): number {
        return totalCharge / Physic.PERMITIVITI_0;
    }

    /**
     * Calculates the magnitude of the electric field (E) for a spherically symmetric charge
     * distribution, outside the distribution.
     * E = Φ / (4 * PI * r^2)
     * @param flux The electric flux (Φ) calculated for a Gaussian surface (N·m²/C or V·m).
     * @param radius The distance from the center of the charge distribution (radius of the Gaussian surface) in meters.
     * @returns The magnitude of the electric field in N/C or V/m.
     */
    public static calculateElectricFieldMagnitude(flux: number, radius: number): number {
        return flux / (4 * Math.PI * Math.pow(radius, 2));
    }

    /**
     * Calculates the linear charge density (λ) of an object.
     * λ = Q / L
     * @param totalCharge The total charge on the object (in Coulombs).
     * @param length The length over which the charge is distributed (in meters).
     * @returns The linear charge density in C/m.
     */
    public static calculateLinearChargeDensity(totalCharge: number, length: number): number {
        if (length === 0) {
            console.warn("Attempted to calculate linear charge density with zero length. Returning 0.");
            return 0;
        }
        return totalCharge / length;
    }

    /**
     * Calculates the surface charge density (σ) of an object.
     * σ = Q / A
     * @param totalCharge The total charge on the object (in Coulombs).
     * @param area The surface area over which the charge is distributed (in square meters).
     * @returns The surface charge density in C/m².
     */
    public static calculateSurfaceChargeDensity(totalCharge: number, area: number): number {
        return totalCharge / area;
    }

    /**
     * Calculates the volume charge density (ρ) of an object.
     * ρ = Q / V
     * @param totalCharge The total charge on the object (in Coulombs).
     * @param volume The volume over which the charge is distributed (in cubic meters).
     * @returns The volume charge density in C/m³.
     */
    public static calculateVolumeChargeDensity(totalCharge: number, volume: number): number {
        return totalCharge / volume;
    }

}//end class