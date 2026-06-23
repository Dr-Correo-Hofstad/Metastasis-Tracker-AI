import math

class PycnogonidBiomassEngine:
    def __init__(self, baseline_config):
        """
        Initializes bioenergetic scaling and gonopore volume constraints.
        """
        self.num_legs = 8
        self.single_egg_vol = (4.0 / 3.0) * math.pi * (0.04 ** 3) # mm3 based on 0.08mm diameter
        self.packing_efficiency = 0.64
        self.wall_thickness_scalar = 0.85
        
        # Baseline structural morphology
        self.base_femur_len = baseline_config.get("base_femur_length_mm", 10.0)
        self.base_leg_rad = baseline_config.get("base_leg_radius_mm", 0.6)
        
        # Live metabolic state
        self.accumulated_protein_vol = 0.0 # mm3 of usable absorbed nutrients
        
    def calculate_morphology(self, condition_factor):
        """
        Dynamically scales the organism's width profile (Thick vs. Skinny).
        Returns total internal leg cavity volume available for egg storage.
        """
        # Apply condition factor to leg thickness profile
        current_rad = self.base_leg_rad * condition_factor
        internal_cavity_rad = current_rad * self.wall_thickness_scalar
        
        # Compute combined cylinder volumes of hollow leg cavities
        single_leg_cavity_vol = math.pi * (internal_cavity_rad ** 2) * self.base_femur_len
        total_cavity_volume = single_leg_cavity_vol * self.num_legs
        
        return {
            "scaled_radius_mm": current_rad,
            "internal_cavity_vol_mm3": total_cavity_volume
        }

    def process_nutrient_tick(self, dynamic_liquefaction_rate, delta_time, condition_factor):
        """
        Updates internal nutrient pools minus metabolic maintenance costs.
        """
        # Nutrient intake rate from pre-oral digestion
        intake_vol = dynamic_liquefaction_rate * 0.05 * 0.80 * delta_time # rate * saliva * efficiency
        
        # Basal metabolic drain scales upward if the organism is structurally thicker
        maintenance_drain = 0.002 * condition_factor * delta_time
        
        self.accumulated_protein_vol += (intake_vol - maintenance_drain)
        self.accumulated_protein_vol = max(0.0, self.accumulated_protein_vol)
        
        return self.accumulated_protein_vol

    def calculate_replication_yield(self, condition_factor):
        """
        Calculates maximum realistic replication volumes matching the 
        physical limits of the leg gonopores and available protein mass.
        """
        morph = self.calculate_morphology(condition_factor)
        max_cavity_capacity = morph["internal_cavity_vol_mm3"]
        
        # 1. Yield bound strictly by absorbed protein mass
        mass_bounded_yield = self.accumulated_protein_vol / self.single_egg_vol
        
        # 2. Yield bound strictly by leg segment geometry limits
        geometry_bounded_yield = (max_cavity_capacity / self.single_egg_vol) * self.packing_efficiency
        
        # Realized replication is governed by the limiting factor
        realized_egg_output = min(mass_bounded_yield, geometry_bounded_yield)
        actual_eggs = math.floor(realized_egg_output)
        
        # Deduct used protein mass from internal reserves upon self-replication event
        self.accumulated_protein_vol -= (actual_eggs * self.single_egg_vol)
        
        return {
            "eggs_extruded_via_gonopores": actual_eggs,
            "residual_protein_reserve_mm3": self.accumulated_protein_vol,
            "limiting_factor": "PROTEIN_MASS" if mass_bounded_yield < geometry_bounded_yield else "LEG_GEOMETRY"
        }

# ==============================================================================
# Verification Loop Example
# ==============================================================================
if __name__ == "__main__":
    setup = {"base_femur_length_mm": 8.0, "base_leg_radius_mm": 0.5}
    
    # 🧪 Scenario A: A starved, skinny individual
    print("--- SCENARIO A: Skinny Profile (Condition Factor = 0.75) ---")
    skinny_engine = PycnogonidBiomassEngine(setup)
    skinny_engine.accumulated_protein_vol = 0.05 # Limited nutrient pool
    
    yield_a = skinny_engine.calculate_replication_yield(condition_factor=0.75)
    print(f"Eggs Released: {yield_a['eggs_extruded_via_gonopores']}")
    print(f"Limiting Constraint: {yield_a['limiting_factor']}\n")
    
    # 🧪 Scenario B: A robust, thick individual with abundant available protein
    print("--- SCENARIO B: Thick Profile (Condition Factor = 1.40) ---")
    thick_engine = PycnogonidBiomassEngine(setup)
    thick_engine.accumulated_protein_vol = 12.0 # Massive liquefied protein pool
    
    yield_b = thick_engine.calculate_replication_yield(condition_factor=1.40)
    print(f"Eggs Released: {yield_b['eggs_extruded_via_gonopores']}")
    print(f"Limiting Constraint: {yield_b['limiting_factor']}")
