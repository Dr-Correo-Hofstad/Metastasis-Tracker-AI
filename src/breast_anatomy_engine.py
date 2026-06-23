import math

class BreastAnatomySimulationEngine:
    def __init__(self, height_cm: float, weight_kg: float, body_build: str, hydration_level: float):
        """
        Initializes the breast and mammary gland structural engine.
        Dimensions adapt dynamically to baseline patient metrics.
        """
        self.height_cm = height_cm
        self.weight_kg = weight_kg
        self.build = body_build.lower()
        self.chi = max(0.5, min(1.5, hydration_level)) # Hydration vector factor
        
        # Anthropometrics matching core repository specifications
        self.bmi = weight_kg / ((height_cm / 100.0) ** 2)
        self.bsa = 0.007184 * (height_cm ** 0.725) * (weight_kg ** 0.425)

    def calculate_breast_volume_and_partition(self, lactation_state: bool = False) -> dict:
        """
        Calculates total breast volume per side and partitions mass into 
        adipose support frameworks and active tubuloalveolar glandular tissue.
        """
        # Determine build coefficient
        if self.build == "ectomorph":
            c_build = 0.85
        elif self.build == "endomorph":
            c_build = 1.25
        else:
            c_build = 1.0

        # Master scaling formula matching somatic parameters
        base_volume_cm3 = c_build * math.pow((self.bmi / 22.0), 1.2) * (self.bsa * 150.0)
        
        # Adjust tissue fractions based on physiological state
        # Lactation causes glandular proliferation and hypertrophy
        if lactation_state:
            glandular_fraction = 0.35 * (self.chi ** 0.3)
            fat_fraction = 1.0 - glandular_fraction
            density_g_cm3 = 0.98  # Mixed parenchymal density
        else:
            glandular_fraction = 0.15
            fat_fraction = 0.85
            density_g_cm3 = 0.93  # High adipose content density

        total_volume_cm3 = base_volume_cm3 * (1.3 if lactation_state else 1.0)
        total_mass_g = total_volume_cm3 * density_g_cm3

        return {
            "total_volume_cm3_each": round(total_volume_cm3, 1),
            "total_mass_grams_each": round(total_mass_g, 1),
            "adipose_tissue_volume_cm3": round(total_volume_cm3 * fat_fraction, 1),
            "glandular_parenchyma_volume_cm3": round(total_volume_cm3 * glandular_fraction, 1),
            "tissue_density_g_cm3": density_g_cm3
        }

    def simulate_dynamic_milk_storage(self, current_fill_fraction: float) -> dict:
        """
        Models the equations and formulas for a dynamic sizing agent tracking
        the fluid volumes held within the lobules and lactiferous sinuses.
        
        :param current_fill_fraction: Scaling from 0.0 (empty) to 1.0 (fully engorged)
        """
        fill = max(0.0, min(1.0, current_fill_fraction))
        
        # Extract baseline glandular volume from partitions
        gland_data = self.calculate_breast_volume_and_partition(lactation_state=True)
        v_gland = gland_data["glandular_parenchyma_volume_cm3"]

        # 1. Formula for maximum storage capacity of the milk-holding spaces
        # Total capacity scales with the size of the glandular parenchyma and hydration state
        max_lobular_capacity_mL = (v_gland * 0.45) * self.chi
        max_sinus_capacity_mL = (v_gland * 0.15) * self.chi
        total_capacity_mL = max_lobular_capacity_mL + max_sinus_capacity_mL

        # 2. Dynamic tracking arrays for active fluid compartments
        active_lobular_volume_mL = max_lobular_capacity_mL * fill
        active_sinus_volume_mL = max_sinus_capacity_mL * (fill ** 1.3) # Sinuses dilate non-linearly
        current_fluid_load_mL = active_lobular_volume_mL + active_sinus_volume_mL

        # 3. Non-linear compliance pressure equation inside the sinus matrix
        # P = V / (C * chi) -> Internal tissue strain spikes as limits are hit
        compliance_base = 2.5
        if active_sinus_volume_mL > 0:
            internal_sinus_pressure_mmHg = active_sinus_volume_mL / (compliance_base * self.chi)
            internal_sinus_pressure_mmHg *= (1.0 + 3.0 * fill) # Extravascular pressure amplification
        else:
            internal_sinus_pressure_mmHg = 0.0

        return {
            "mammary_lactation_status": "ACTIVE / INITIALIZED",
            "maximum_storage_capacity_mL_each": round(total_capacity_mL, 1),
            "current_fluid_load_mL_each": round(current_fluid_load_mL, 1),
            "compartment_fluid_allocations": {
                "lobular_alveoli_volume_mL": round(active_lobular_volume_mL, 1),
                "lactiferous_sinuses_volume_mL": round(active_sinus_volume_mL, 1)
            },
            "internal_sinus_tissue_pressure_mmHg": round(internal_sinus_pressure_mmHg, 2),
            "glandular_engorged_state": "CRITICAL STRAIN" if fill >= 0.85 else ("NORMAL DISTENSION" if fill >= 0.3 else "RESTING / DECOMPRESSED")
        }

# =====================================================================
# Operational Verification Matrix
# =====================================================================
if __name__ == "__main__":
    # Simulate a lactating female patient (Height: 165cm, Weight: 60kg, Hydration: 1.0)
    engine = BreastAnatomySimulationEngine(height_cm=165.0, weight_kg=60.0, body_build="mesomorph", hydration_level=1.0)
    
    print("=========================================================================")
    print("MAMMARY GLAND STRUCTURAL DIMENSIONS & DYNAMIC FLUID LOGS")
    print("=========================================================================\n")
    
    # 1. Verify baseline non-lactating vs lactating partition frames
    resting_state = engine.calculate_breast_volume_and_partition(lactation_state=False)
    active_state = engine.calculate_breast_volume_and_partition(lactation_state=True)
    
    print("--- 1. ANATOMICAL TISSUE COMPARTMENT PARTITIONING ---")
    print(f" Resting State  -> Volume: {resting_state['total_volume_cm3_each']} cm³ | Glandular Matrix: {resting_state['glandular_parenchyma_volume_cm3']} cm³")
    print(f" Active Lactation -> Volume: {active_state['total_volume_cm3_each']} cm³ | Glandular Matrix: {active_state['glandular_parenchyma_volume_cm3']} cm³ (Hypertrophic Shift)\n")

    # 2. Test the dynamic sizing agent equations at 90% fluid engorged state
    print("--- 2. DYNAMIC MILK STORAGE SPACE AGENT EQUATIONS (90% FILL) ---")
    storage_report = engine.simulate_dynamic_milk_storage(current_fill_fraction=0.90)
    print(f" Maximum Storage Ceiling Pool: {storage_report['maximum_storage_capacity_mL_each']} mL per breast")
    print(f" Current Fluid Mass Volume:    {storage_report['current_fluid_load_mL_each']} mL per breast")
    print(f"  -> Alveolar Lobules Load:    {storage_report['compartment_fluid_allocations']['lobular_alveoli_volume_mL']} mL")
    print(f"  -> Lactiferous Sinus Load:   {storage_report['compartment_fluid_allocations']['lactiferous_sinuses_volume_mL']} mL")
    print(f" Hydrostatic Tissue Pressure:  {storage_report['internal_sinus_tissue_pressure_mmHg']} mmHg")
    print(f" Glandular Structural State:   {storage_report['glandular_engorged_state']}")
