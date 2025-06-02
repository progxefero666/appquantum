

//public static EULERS_NUMBER: number = Math.E; 
//console.log(EULERS_NUMBER); // Salida: 2.718281828459045

import { Physic } from "../pyshic";

/**
 * class Gravity.NEWTON_G
 */
export class Gravity {

    
    public static readonly NEWTON_G: number = 9.80665; // m/s²

    public static readonly G: number = 6.67430e-11; // m³/kg s²    
    public static readonly EINSTEIN_FACTOR: number = (8 * Math.PI * Gravity.G) / Math.pow(Physic.C, 4);
    // 2.076616 × 10⁻⁴³ s²/kg·m.

    //public static readonly DEFORMATION_PERMITTIVITY_ANALOG: number = 8.854 * Math.pow(10, -12);

    public static getMassEnergy(mass: number): number {
        return mass * Math.pow(Physic.C, 2);
    }

}//end class


export class GravityUtil {

    public static getAttractionForze(distance: number, mass_a: number, mass_b: number): number {
        if (distance <= 0 || mass_a < 0 || mass_b < 0) { return 0; }
        const force: number = Gravity.G * (mass_a * mass_b) / (distance * distance);
        return force;
    }

    public static getWeight(mass: number): number {
        return Gravity.NEWTON_G * mass;
    }

    /**
   * Calculates the total "deforming influence" (Φ_analog) emanating from the mass.
   * This is analogous to electric flux Φ = Q / ε₀, but using mass as the source.
   * Φ_analog = mass_analog / PERMITIVITI_0
   * @param massAnalog The total "deforming mass" or "influence source" 
   * @returns The total deforming influence, analogous to electric flux.
   */
    public static calculateDeformationInfluenceFlux(massAnalog: number): number {
        return massAnalog / Physic.PERMITIVITI_0;
    }

    /**
     * Calculates the magnitude of the "deforming field" (E_analog) at a given distance
     * from a spherically symmetric mass source, outside its volume.
     * E_analog = Φ_analog / (4 * PI * r^2)
     * @param influenceFlux The total deforming influence flux (Φ_analog).
     * @param distance The distance from the center of the mass source (in meters).
     * @returns The magnitude of the deforming field.
     */
    public static calculateDeformationFieldMagnitude(influenceFlux: number, distance: number): number {
        return influenceFlux / (4 * Math.PI * Math.pow(distance, 2));
    }

}//end class