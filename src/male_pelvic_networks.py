import math

class MalePelvicSimulationEngine:
    def __init__(self, height_cm: float, weight_kg: float, hydration_level: float):
        """
        Initializes the male reproductive and urinary system templates.
        All mathematical properties scale dynamically from core patient baselines.
        """
        self.height_cm = height_cm
        self.height_m = height_cm / 100.0
        self.weight = weight_kg
        self.chi = max(0.5, min(1.5, hydration_level)) # Hydration balancing constant
        
        # Base anthropometrics matching repository protocols
        self.bsa = 0.007184 * (self.height_cm ** 0.725) * (self.weight ** 0.425)
        self.cardiac_output_L_min = self.bsa * 3.0 * math.sqrt(self.chi)

    def generate_reproductive_network(self) -> dict:
        """
        Generates dimensions and structural tracking boundaries for the 
        symmetrical male gonadal systems and anatomical conduits.
        """
        w = self.weight
        base_testis_mass_g = 0.24 * w # Structural weight scaling factor

        reproductive_tree = {
            "bilateral_testicles": {
                "left_testicle": {
                    "mass_g": round(base_testis_mass_g * 1.03, 2),
                    "dimensions_cm": {"length": 4.5, "width": 2.8, "depth": 3.0},
                    "gonadal_artery_origin": "Abdominal Aorta (Gen 6 Line)",
                    "venous_drainage_sink": "Left Renal Vein (High hydrostatic resistance point)"
                },
                "right_testicle": {
                    "mass_g": round(base_testis_mass_g * 0.97, 2),
                    "dimensions_cm": {"length": 4.3, "width": 2.6, "depth": 2.8},
                    "gonadal_artery_origin": "Abdominal Aorta (Gen 6 Line)",
                    "venous_drainage_sink": "Inferior Vena Cava (Direct low-resistance confluence)"
                }
            },
            "vas_deferens_bilateral": {
                "length_cm": 35.0,
                "internal_lumen_diameter_mm": 0.5,
                "propulsion_mechanism": "Smooth Muscle Peristaltic Wave"
            },
            "accessory_glands": {
                "prostate_gland": {
                    "estimated_volume_cm3": round(20.0 * (w / 70.0), 2),
                    "encased_urethral_segment_length_cm": 3.0,
                    "secretion_ph": 6.50
                },
                "seminal_vesicles_bilateral": {
                    "volume_cm3": 4.5 * self.chi,
                    "secretion_ph": 7.50
                }
            }
        }
        return reproductive_tree

    def generate_urinary_network(self) -> dict:
        """
        Calculates structural values and filtration capacities for the 
        male urinary tract, mapping into the extended shared urethral channel.
        """
        w = self.weight
        kidney_mass_base = 1.45 * (w ** 0.95)
        
        total_renal_volume_cm3 = ((kidney_mass_base * 1.05) + (kidney_mass_base * 0.98)) / 1.05
        gfr_mL_min = 0.00055 * total_renal_volume_cm3 * 1000.0

        return {
            "kidney_filtration_matrix": {
                "left_kidney_mass_g": round(kidney_mass_base * 1.05, 2),
                "right_kidney_mass_g": round(kidney_mass_base * 0.98, 2),
                "calculated_gfr_mL_min": round(gfr_mL_min, 2),
                "allocated_renal_blood_flow_L_min": round(self.cardiac_output_L_min * 0.22, 3)
            },
            "ureters_bilateral": {
                "length_cm": 30.0, "lumen_diameter_cm": 0.35,
                "peristaltic_frequency_per_min": 3.5
            },
            "urinary_bladder": {
                "maximum_capacity_mL": round(500.0 * self.chi, 1),
                "resting_wall_thickness_cm": 0.40
            },
            "shared_urethral_conduit": {
                "total_length_cm": 19.5,
                "segment_breakdown_lengths_cm": {
                    "prostatic_segment": 3.0,
                    "membranous_segment": 1.5,
                    "penile_spongy_segment": 15.0
                },
                "mean_diameter_cm": 0.6,
                "flush_peak_velocity_m_s": 0.42 # High fluid kinetic velocity wash
            }
        }

    def build_pelvic_dataset(self) -> dict:
        return {
            "patient_pelvic_metrics": {
                "calculated_bsa_m2": self.bsa,
                "cardiac_output_L_min": self.cardiac_output_L_min
            },
            "reproductive_system_matrix": self.generate_reproductive_network(),
            "urinary_system_matrix": self.generate_urinary_network()
        }

# =====================================================================
# Execution & Sample Output Verification
# =====================================================================
if __name__ == "__main__":
    # Simulate a male patient (Height: 180cm, Weight: 75kg, Hydration: 1.0)
    engine = MalePelvicSimulationEngine(height_cm=180.0, weight_kg=75.0, hydration_level=1.0)
    dataset = engine.build_pelvic_dataset()
    
    print("=========================================================================")
    print("MALE PELVIC SYSTEM GEOMETRY & FLOW VERIFICATION LOGS")
    print("=========================================================================\n")
    
    # 1. Inspect Reproductive Track Arrays
    repro = dataset["reproductive_system_matrix"]
    print("--- 1. REPRODUCTIVE MATRIX CONDUITS ---")
    print(f" Left Testicle Structural Mass:  {repro['bilateral_testicles']['left_testicle']['mass_g']} g | Sink: {repro['bilateral_testicles']['left_testicle']['venous_drainage_sink']}")
    print(f" Right Testicle Structural Mass: {repro['bilateral_testicles']['right_testicle']['mass_g']} g | Sink: {repro['bilateral_testicles']['right_testicle']['venous_drainage_sink']}")
    print(f" Vas Deferens Transit Length:    {repro['vas_deferens_bilateral']['length_cm']} cm | Mode: {repro['vas_deferens_bilateral']['propulsion_mechanism']}")
    print(f" Prostate Encased Core Segment:  {repro['accessory_glands']['prostate_gland']['encased_urethral_segment_length_cm']} cm\n")
    
    # 2. Inspect Urinary Track Arrays
    urinary = dataset["urinary_system_matrix"]
    print("--- 2. SHARED URINARY CONDUIT PATHWAYS ---")
    print(f" Total Urethral Pathway Length:  {urinary['shared_urethral_conduit']['total_length_cm']} cm")
    print(f"  -> Spongy Penile Segment:      {urinary['shared_urethral_conduit']['segment_breakdown_lengths_cm']['penile_spongy_segment']} cm")
    print(f" Fluid Flushing Wash Velocity:   {urinary['shared_urethral_conduit']['flush_peak_velocity_m_s']} m/s")
    print(f" Systemic GFR Filtration Rate:   {urinary['kidney_filtration_matrix']['calculated_gfr_mL_min']} mL/min")
