import math

class OcularDynamicsSimulationEngine:
    def __init__(self, height_cm: float, weight_kg: float, hydration_level: float):
        """
        Initializes the Dynamic Ocular and Compartmental Fluid Model.
        Structural values adapt dynamically to global patient scalars.
        """
        self.height_cm = height_cm
        self.weight_kg = weight_kg
        self.chi = max(0.5, min(1.5, hydration_level)) # Hydration balancing constant
        
        # Pull baseline metrics matching core repository configurations
        self.bsa = 0.007184 * (self.height_cm ** 0.725) * (self.weight_kg ** 0.425)
        self.resting_iop_mmHg = 15.0

    def generate_ocular_compartment_matrix(self) -> dict:
        """
        Partitions the physical eye globe volume into distinct internal 
        fluid chambers and structural boundary layers.
        """
        # Baseline adult eye globe volume configuration
        v_globe_total_mL = 7.2 * math.sqrt(self.chi)
        
        # Volumetric compartment partitioning matrix
        v_vitreous = v_globe_total_mL * 0.80
        v_aqueous = v_globe_total_mL * 0.04
        v_structural_walls = v_globe_total_mL * 0.16
        
        # Dynamic Intraocular Pressure calculation based on current hydration profile
        dynamic_iop = self.resting_iop_mmHg * (1.0 + 0.3 * (1.0 - self.chi))

        return {
            "total_globe_volume_mL_each": round(v_globe_total_mL, 2),
            "total_globe_mass_g_each": round(v_globe_total_mL * 1.05, 2),
            "chambers": {
                "vitreous_body_humor_cm3": round(v_vitreous, 2),
                "aqueous_humor_anterior_pool_mL": round(v_aqueous, 2),
                "corneoscleral_structural_walls_cm3": round(v_structural_walls, 2)
            },
            "hemodynamic_pressure_metrics": {
                "calculated_iop_mmHg": round(dynamic_iop, 1),
                "aqueous_production_rate_uL_min": round(2.5 * self.chi, 3)
            }
        }

    def evaluate_ocular_ingress_routes(self, particle_diameter_um: float, local_icp_mmHg: float) -> dict:
        """
        Calculates entry mechanics, fluid clearance velocities, and geometric 
        filtration gate barriers across the three structural entry vectors.
        """
        # --- ROUTE A: EXTERNAL CONJUNCTIVAL FLUID WASH ---
        v_lacrimal_wash_mm_min = 1.2 * self.chi
        # External macro-particles under passive conditions are cleared by tearing
        route_a_washout_active = particle_diameter_um > 0.5 
        
        # --- ROUTE B: BRAIN PATHWAY (CAVERNOUS REVERSAL) ---
        # Retrograde venous flow unlocks if intracranial pressure overrides peripheral orbital pressures
        route_b_unlocked = local_icp_mmHg > 20.0
        
        # --- ROUTE C: SINUS PATHWAY (OPTIC SIEVE LIMIT) ---
        lamina_cribrosa_pore_limit_um = 3.5
        route_c_allowed = particle_diameter_um <= lamina_cribrosa_pore_limit_um

        return {
            "route_a_external_interface": {
                "lacrimal_flush_velocity_mm_min": v_lacrimal_wash_mm_min,
                "hydrodynamic_washout_risk": route_a_washout_active,
                "resolution": "Swept into Nasolacrimal Duct" if route_a_washout_active else "Surface Adhesion Feasible"
            },
            "route_b_cranial_venous_shunt": {
                "brain_icp_pressure_drive_mmHg": local_icp_mmHg,
                "retrograde_shunt_unlocked": route_b_unlocked,
                "resolution": "Retrograde Venous Transit Active" if route_b_unlocked else "Venous Valve Check Secure"
            },
            "route_c_sinus_perivascular_portal": {
                "lamina_cribrosa_filter_ceiling_microns": lamina_cribrosa_pore_limit_um,
                "mechanical_gate_clearance": route_c_allowed,
                "resolution": "Intraocular Infiltration Allowed" if route_c_allowed else "CRITICAL REJECTION (Blocked at Optic Nerve Sieve)"
            }
        }

# =====================================================================
# Operational Verification Pipeline Runner
# =====================================================================
if __name__ == "__main__":
    # Initialize the ocular simulation engine module
    ocular_engine = OcularDynamicsSimulationEngine(height_cm=175.0, weight_kg=72.0, hydration_level=1.0)
    
    print("=========================================================================")
    print("DYNAMIC OCULAR COMPARTMENT & ENTRANCE GATE ANALYSIS")
    print("=========================================================================\n")
    
    # 1. Verify structural eye volume partitioning and intraocular pressure
    eye_map = ocular_engine.generate_ocular_compartment_matrix()
    print("--- 1. OCULAR VOLUMETRIC & PRESSURE PARTITIONING ---")
    print(f" Total Calculated Globe Mass:  {eye_map['total_globe_mass_g_each']} grams")
    print(f" Vitreous Humor Core Capacity: {eye_map['chambers']['vitreous_body_humor_cm3']} cm³")
    print(f" Aqueous Humor Fluid Pool:     {eye_map['chambers']['aqueous_humor_anterior_pool_mL']} mL")
    print(f" Computed Intraocular Pressure: {eye_map['hemodynamic_pressure_metrics']['calculated_iop_mmHg']} mmHg\n")

    # 2. Evaluate entry mechanics for a microscopic 2.0-micron particle under high ICP stress (24 mmHg)
    print("--- 2. ENTRANCE GATE PERFORMANCE ( 2.0 Micron Micro-Particle | ICP: 24 mmHg ) ---")
    report = ocular_engine.evaluate_ocular_ingress_routes(particle_diameter_um=2.0, local_icp_mmHg=24.0)
    
    print(f" Route A (Outside Open) -> Fate: {report['route_a_external_interface']['resolution']}")
    print(f" Route B (Brain Loop)   -> Fate: {report['route_b_cranial_venous_shunt']['resolution']}")
    print(f" Route C (Sinus Portal) -> Fate: {report['route_c_sinus_perivascular_portal']['resolution']}")
