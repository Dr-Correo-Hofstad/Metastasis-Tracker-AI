import math

class TissueTraumaSimulationEngine:
    def __init__(self, tip_radius_microns: float):
        """
        Initializes the Mechanical Trauma and Puncture Engine.
        
        :param tip_radius_microns: The radius of curvature of the sharp contact point.
                                   Smaller values simulate extreme sharpness.
        """
        self.r_tip_m = tip_radius_microns * 1e-6
        # Tip area calculation: A = pi * r^2
        self.a_tip_m2 = math.pi * (self.r_tip_m ** 2)

        # Ultimate Tensile Strength Reference Matrix (converted to Pascals: MPa * 1e6)
        self.tissue_strength_matrix = {
            "capillary_vein":  1.1 * 1e6,  # ~1.1 MPa
            "macro_artery":    2.8 * 1e6,  # ~2.8 MPa
            "brain_neural":    0.03 * 1e6, # ~0.03 MPa (Highly fragile viscoelastic matrix)
            "sinus_mucosa":    0.85 * 1e6, # ~0.85 MPa
            "ocular_sclera":   5.2 * 1e6,  # ~5.2 MPa
            "airway_wall":     1.4 * 1e6,  # ~1.4 MPa
            "cortical_bone":   135.0 * 1e6 # ~135.0 MPa (Highly mineralized grid)
        }

    def calculate_puncture_mechanics(self, tissue_type: str, contact_force_newtons: float) -> dict:
        """
        Computes localized contact stress and checks for structural boundary failure.
        
        :param tissue_type: Key target matching the tissue profile matrix
        :param contact_force_newtons: Force vector acting perpendicular to the wall substrate
        """
        target_key = tissue_type.lower()
        sigma_uts = self.tissue_strength_matrix.get(target_key, 1.0 * 1e6)

        # 1. Puncture Stress Equation: Sigma = Force / Area
        if self.a_tip_m2 > 0:
            calculated_stress_pascal = contact_force_newtons / self.a_tip_m2
        else:
            calculated_stress_pascal = 0.0

        # 2. Rupture Check Loop
        structural_rupture_active = calculated_stress_pascal > sigma_uts
        
        # Calculate dynamic safety margin factor (Values < 1.0 represent immediate structural failure)
        safety_margin = sigma_uts / calculated_stress_pascal if calculated_stress_pascal > 0 else 100.0

        return {
            "target_tissue_identity": tissue_type.upper(),
            "applied_perpendicular_force_newtons": contact_force_newtons,
            "calculated_point_stress_MPa": round(calculated_stress_pascal / 1e6, 2),
            "tissue_strength_threshold_MPa": round(sigma_uts / 1e6, 2),
            "structural_safety_margin_index": round(safety_margin, 4),
            "barrier_rupture_status": "CRITICAL_HEMORRHAGE_ALERT" if structural_rupture_active else "INTACT_ELASTIC_DEFORMATION",
            "lesion_profile": "Perforation / Wall Tear" if structural_rupture_active else "None"
        }

    def evaluate_vascular_flow_hemorrhage(self, generation_node: dict, contact_force_newtons: float) -> dict:
        """
        Evaluates vascular network integrity by analyzing local vessel class 
        pressures alongside point-contact forces.
        """
        gen = generation_node.get("generation", 0)
        vessel_radius = generation_node.get("radius_m", 0.01)
        local_ph = generation_node.get("local_ph", 7.40)
        
        # Isolate class based on generational geometry parameters
        if gen == 30 or vessel_radius < 10e-6:
            tissue_class = "capillary_vein"
        elif gen == 0 or vessel_radius > 0.005:
            tissue_class = "macro_artery"
        else:
            tissue_class = "capillary_vein" # Microvascular arteriole default

        report = self.calculate_puncture_mechanics(tissue_class, contact_force_newtons)
        
        # Extreme acidosis weakens cell wall collagen crosslinks, lowering tissue thresholds
        if local_ph < 7.10:
            report["calculated_point_stress_MPa"] *= 1.25 # Artificial amplification under acid stress
            if report["calculated_point_stress_MPa"] > report["tissue_strength_threshold_MPa"]:
                report["barrier_rupture_status"] = "CRITICAL_HEMORRHAGE_ALERT"
                report["lesion_profile"] = "Acid-Accelerated Vascular Perforation"

        return report

# =====================================================================
# Operational Verification Pipeline Sandbox
# =====================================================================
if __name__ == "__main__":
    # Instantiate trauma engine analyzing an object apex sharp point tip radius of 2.5 microns
    trauma_engine = TissueTraumaSimulationEngine(tip_radius_microns=2.5)
    
    print("=========================================================================")
    print("MECHANICAL TRAUMA & TISSUE PUNCTURE COMPARTMENT LOGS")
    print("=========================================================================\n")
    
    # Test Node A: Extremely low contact force (0.05 Newtons) acting on fragile brain tissue
    print("--- SCENARIO 1: CENTRAL NERVOUS SYSTEM NEURAL TISSUE MECHANICAL STRESS ---")
    brain_test = trauma_engine.calculate_puncture_mechanics(tissue_type="brain_neural", contact_force_newtons=0.05)
    print(f" Applied Force:            {brain_test['applied_perpendicular_force_newtons']} Newtons")
    print(f" Point Stress Exerted:     {brain_test['calculated_point_stress_MPa']} MPa (Tissue Max Capacity: {brain_test['tissue_strength_threshold_MPa']} MPa)")
    print(f" Boundary Security Status: {brain_test['barrier_rupture_status']}")
    print(f" Confirmed Lesion Outcome: {brain_test['lesion_profile']}\n")

    # Test Node B: Moderate contact force (1.5 Newtons) acting on an arterial wall node
    print("--- SCENARIO 2: SYSTEMIC VASCULAR PATH ARTERY REGION STRESS ---")
    mock_arteriolar_generation = {"generation": 18, "radius_m": 0.00012, "local_ph": 7.02} # Local acid stress active
    artery_test = trauma_engine.evaluate_vascular_flow_hemorrhage(mock_arteriolar_generation, contact_force_newtons=1.5)
    print(f" Target Vessel Class:      {artery_test['target_tissue_identity']}")
    print(f" Point Stress Exerted:     {artery_test['calculated_point_stress_MPa']} MPa (Tissue Max Capacity: {artery_test['tissue_strength_threshold_MPa']} MPa)")
    print(f" Boundary Security Status: {artery_test['barrier_rupture_status']}")
    print(f" Confirmed Lesion Outcome: {artery_test['lesion_profile']}\n")

    # Test Node C: High contact force (10.0 Newtons) hitting mineralized cortical bone tissue
    print("--- SCENARIO 3: METABOLIC MARROW INTEGRITY CORTICAL BONE STRESS ---")
    bone_test = trauma_engine.calculate_puncture_mechanics(tissue_type="cortical_bone", contact_force_newtons=10.0)
    print(f" Applied Force:            {bone_test['applied_perpendicular_force_newtons']} Newtons")
    print(f" Point Stress Exerted:     {bone_test['calculated_point_stress_MPa']} MPa (Tissue Max Capacity: {bone_test['tissue_strength_threshold_MPa']} MPa)")
    print(f" Boundary Security Status: {bone_test['barrier_rupture_status']}")
    print(f" Confirmed Lesion Outcome: {bone_test['lesion_profile']}")
