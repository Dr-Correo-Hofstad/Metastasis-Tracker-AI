import math
import unittest

class SepsisRedoxSimulationEngine:
    def __init__(self, baseline_hydration: float, wbc_count_uL: float):
        """
        Initializes the Systemic Electron-Transfer and Bioenergetic Engine.
        """
        self.chi = max(0.5, min(1.5, baseline_hydration))
        self.wbc = wbc_count_uL
        
        # Reference thresholds for covalent matrix stability (Normalized scaling units)
        self.critical_covalent_pore_limits = {
            "cortical_bone":   0.65, # Critical threshold for structural osteolysis
            "tendon_cartilage": 0.50,
            "skin_epithelium": 0.40
        }

    def simulate_enzyme_redox_degradation(self, enzyme_type: str, enzyme_concentration_uM: float, initial_covalent_density: float, exposure_time_sec: int) -> dict:
        """
        Calculates covalent bond cleavage, electron-transfer decay rates, 
        and structural material failure thresholds over time.
        """
        e_conc = max(0.0, enzyme_concentration_uM)
        current_covalent_potential = max(0.0, min(1.0, initial_covalent_density))
        
        # Kinetic parameters mapped to your database types
        # Enzymes alter the local electron transport landscape
        if enzyme_type.lower() in ["collagenase", "mmp_protease"]:
            k_cleavage = 0.015 * (1.0 / self.chi)
            target_matrix = "cortical_bone"
        elif enzyme_type.lower() in ["phospholipase", "lipase"]:
            k_cleavage = 0.022
            target_matrix = "skin_epithelium"
        else:
            k_cleavage = 0.008
            target_matrix = "tendon_cartilage"

        time_series_log = []
        phi_crit = self.critical_covalent_pore_limits.get(target_matrix, 0.50)

        for t in range(exposure_time_sec):
            # 1. Calculate dynamic electron-transfer cleavage rate
            # Local electron loss is a function of enzyme payload and current bond thickness
            cleavage_flux = k_cleavage * e_conc * current_covalent_potential
            
            # 2. Update current covalent bond structural density (Logarithmic electron decay loop)
            current_covalent_potential -= cleavage_flux
            current_covalent_potential = max(0.0, current_covalent_potential)
            
            # Evaluate mechanical osteolysis state status
            structural_failure = current_covalent_potential < phi_crit

            time_series_log.append({
                "second": t,
                "covalent_electron_density": round(current_covalent_potential, 4),
                "instantaneous_cleavage_flux": round(cleavage_flux, 5),
                "structural_failure_active": structural_failure
            })

        return {
            "mapped_substrate_matrix": target_matrix.upper(),
            "final_covalent_density_rating": round(current_covalent_potential, 4),
            "critical_osteolysis_threshold": phi_crit,
            "pathological_liquefaction_detected": current_covalent_potential < phi_crit,
            "timeline_logs": time_series_log
        }

import math
import unittest

class ExtendedSepsisCalciumEngine:
    def __init__(self, total_blood_volume_L: float, gfr_L_min: float):
        """
        Extends the bioenergetic platform to track chemical mineral extraction,
        stoichiometric dissolution, and systemic hypercalcemia risks.
        """
        self.v_blood = max(1.0, total_blood_volume_L)
        self.gfr_L_sec = gfr_L_min / 60.0
        
        # Physiological baselines (mg/dL)
        self.current_serum_ca = 9.5 
        self.hypercalcemia_cutoff = 12.0

    def simulate_osteolytic_calcium_cascade(self, base_cleavage_flux_mg_s: float, bone_volume_cm3: float, timeline_sec: int) -> dict:
        """
        Solves the mass-balance differential loop for calcium release into the blood stream.
        """
        time_series = []
        # Renal excretion clearing constant for ionized minerals
        kappa_renal = 0.15 
        
        # Convert blood volume from Liters to deciliters (1 L = 10 dL) for mg/dL calculations
        v_blood_dL = self.v_blood * 10.0

        for t in range(timeline_sec):
            # 1. Stoichiometric Extraction: Hydroxyapatite is ~39.89% Calcium by mass
            total_lattice_melt_mg_s = base_cleavage_flux_mg_s * (bone_volume_cm3 * 1.05)
            ca_mass_influx_mg = 0.3989 * total_lattice_melt_mg_s
            
            # 2. ODE Solver: dCa/dt = Influx - Outflux
            ca_clearance_mg = kappa_renal * self.gfr_L_sec * self.current_serum_ca * 10.0
            net_delta_ca_mg = ca_mass_influx_mg - ca_clearance_mg
            
            # Update blood pool concentration concentration vector
            self.current_serum_ca += (net_delta_ca_mg / v_blood_dL)
            self.current_serum_ca = max(0.0, self.current_serum_ca)
            
            # Intercept threshold boundaries check
            hypercalcemia_active = self.current_serum_ca > self.hypercalcemia_cutoff

            time_series.append({
                "second": t,
                "serum_calcium_mg_dL": round(self.current_serum_ca, 3),
                "instantaneous_release_mg": round(ca_mass_influx_mg, 4),
                "hypercalcemia_crisis": hypercalcemia_active
            })

        return {
            "final_serum_calcium_mg_dL": round(self.current_serum_ca, 3),
            "hypercalcemia_induced_arrhythmia_risk": self.current_serum_ca > self.hypercalcemia_cutoff,
            "simulation_trajectory": time_series
        }


# =====================================================================
# CI/CD SCHEMATIC AUTOMATED CHECKS
# =====================================================================
class TestMineralExtractionBoundaries(unittest.TestCase):
    def test_stoichiometric_calcium_caps(self):
        """
        AUTOMATED CHECK: Validates that hypercalcemia arrays flag systemic crisis
        states properly under massive bone mass melting constraints.
        """
        engine = ExtendedSepsisCalciumEngine(total_blood_volume_L=5.0, gfr_L_min=0.120)
        
        # Test acute matrix dissolution spike (1.5 mg/s cleavage flux)
        report = engine.simulate_osteolytic_calcium_cascade(
            base_cleavage_flux_mg_s=1.5, bone_volume_cm3=1200.0, timeline_sec=10
        )
        
        # Confirms data tracker captures the crisis state accurately
        if report["final_serum_calcium_mg_dL"] > 12.0:
            self.assertTrue(report["hypercalcemia_induced_arrhythmia_risk"])

# =====================================================================
# AUTOMATED SUITE DIAGNOSTIC ASSERTIONS
# =====================================================================
class TestSepsisRedoxBoundaries(unittest.TestCase):
    def setUp(self):
        # Setup engine assuming standard healthy hydration norms
        self.engine = SepsisRedoxSimulationEngine(baseline_hydration=1.0, wbc_count_uL=6500.0)

    def test_covalent_decay_determinism(self):
        """
        VERIFICATION: Assures that higher enzyme payloads yield faster 
        electron depletion rates across similar temporal brackets.
        """
        # Run standard low-stress profile
        report_low = self.engine.simulate_enzyme_redox_degradation(
            enzyme_type="collagenase", enzyme_concentration_uM=5.0, initial_covalent_density=1.0, exposure_time_sec=15
        )
        # Run high-stress septic shock profile
        report_high = self.engine.simulate_enzyme_redox_degradation(
            enzyme_type="collagenase", enzyme_concentration_uM=50.0, initial_covalent_density=1.0, exposure_time_sec=15
        )

        # Assertion checking: High concentration must deplete covalent density significantly more
        self.assertLess(report_high["final_covalent_density_rating"], report_low["final_covalent_density_rating"])
        print(f" -> Test Passed: Low concentration density remaining ({report_low['final_covalent_density_rating']}) vs Severe Sepsis density remaining ({report_high['final_covalent_density_rating']})")

if __name__ == "__main__":
    unittest.main()
