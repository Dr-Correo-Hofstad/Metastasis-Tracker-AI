import math

class IntravenousTransitModel:
    def __init__(self, introduced_mass_mg: float, particle_radius_um: float):
        """
        Models the hydrodynamic transit of introduced particulate matter 
        within the systemic venous return network.
        """
        self.mass_mg = introduced_mass_mg
        self.radius_m = particle_radius_um * 1e-6
        self.terminal_node_reached = False

    def calculate_venous_advection(self, patient_cardiac_output_L_min: float, hydration_level: float) -> dict:
        """
        Calculates the velocity and time-of-flight from a peripheral arm vein 
        (median cubital) to the superior vena cava trunk.
        """
        # Approximated segment path lengths (meters) and radii (meters) for venous classes
        venous_pipeline = [
            {"name": "peripheral_basilic_vein", "length_m": 0.25, "radius_m": 0.0025},
            {"name": "axillary_subclavian_vein", "length_m": 0.20, "radius_m": 0.0050},
            {"name": "superior_vena_cava",      "length_m": 0.07, "radius_m": 0.0100}
        ]

        # Convert cardiac output from L/min to m^3/s
        q_total_m3_s = (patient_cardiac_output_L_min / 1000.0) / 60.0
        
        total_transit_seconds = 0.0
        segment_logs = []

        for segment in venous_pipeline:
            # Calculate cross-sectional area
            area_m2 = math.pi * (segment["radius_m"] ** 2)
            
            # Venous flow velocity: v = Q / A (adjusted slightly by hydration viscosity)
            velocity_m_s = (q_total_m3_s / area_m2) * hydration_level
            
            # Time spent in this segment: t = d / v
            duration_s = segment["length_m"] / velocity_m_s
            total_transit_seconds += duration_s
            
            # Calculate localized wall shear rate: gamma = 4v / r
            shear_rate = (4.0 * velocity_m_s) / segment["radius_m"]

            segment_logs.append({
                "segment_identity": segment["name"],
                "fluid_velocity_m_s": round(velocity_m_s, 3),
                "wall_shear_rate_s1": round(shear_rate, 1),
                "segment_transit_time_seconds": round(duration_s, 3)
            })

        self.terminal_node_reached = True

        return {
            "total_transit_distance_meters": sum(s["length_m"] for s in venous_pipeline),
            "calculated_total_travel_time_seconds": round(total_transit_seconds, 3),
            "destination_chamber": "Right Atrium -> Right Ventricle -> Pulmonary Trunk",
            "segment_breakdowns": segment_logs
        }

    def evaluate_capillary_trapping_hazard(self) -> dict:
        """
        Evaluates mechanical filtration traps. Blood exiting the right heart goes 
        directly to the lungs, where small capillaries filter out particles.
        """
        particle_diameter_um = self.radius_m * 2.0 * 1e6
        
        # Pulmonary capillaries feature a standard micrometer ceiling (approx 6.0 to 8.0 um)
        pulmonary_capillary_diameter_um = 7.5
        
        # If the particle diameter exceeds the capillary diameter, mechanical embolization occurs
        is_trapped_in_lungs = particle_diameter_um > pulmonary_capillary_diameter_um

        return {
            "particle_diameter_microns": particle_diameter_um,
            "pulmonary_capillary_mesh_limit_microns": pulmonary_capillary_diameter_um,
            "mechanical_embolic_entrapment": is_trapped_in_lungs,
            "primary_organ_hazard_site": "Lungs (Pulmonary Capillary Bed Bed Extraction)" if is_trapped_in_lungs else "None (Systemic Recirculation)"
        }

# =====================================================================
# Verification Operational Loop
# =====================================================================
if __name__ == "__main__":
    # Simulate an introduced micro-particle (e.g., 50-micron diameter debris fragment)
    debris_particle = IntravenousTransitModel(introduced_mass_mg=0.15, particle_radius_um=25.0)
    
    print("=========================================================================")
    # Intravenous advection metrics calculation
    print("INTRAVASCULAR INTRAVENOUS TRANSIT TRACKING LOGS")
    print("=========================================================================\n")
    
    # Run transit solver for an average patient (5.5 L/min cardiac output)
    transit_report = debris_particle.calculate_venous_advection(patient_cardiac_output_L_min=5.5, hydration_level=1.0)
    print("--- 1. HYDRODYNAMIC TRANSIT TIMELINE TRAJECTORY ---")
    print(f" Total Path Vector Distance: {transit_report['total_transit_distance_meters']} meters")
    print(f" Cumulative Flight Duration: {transit_report['calculated_total_travel_time_seconds']} seconds to reach heart chamber.")
    print(f" Terminal Sink Target:      {transit_report['destination_chamber']}\n")
    
    print("   Segment Path Progress:")
    for step in transit_report["segment_breakdowns"]:
        print(f"    -> {step['segment_identity']:25} | Speed: {step['fluid_velocity_m_s']} m/s | Time: {step['segment_transit_time_seconds']}s")

    # Evaluate where the mechanical filtering trap isolates the matter
    filter_report = debris_particle.evaluate_capillary_trapping_hazard()
    print("\n--- 2. PULMONARY CAPILLARY SIZE SELECTION FILTER ---")
    print(f" Particle Dimension Scale:  {filter_report['particle_diameter_microns']} um")
    print(f" Mechanical Capillary Trap:  {filter_report['mechanical_embolic_entrapment']}")
    print(f" Terminal Extraction Site:   {filter_report['primary_organ_hazard_site']}")
