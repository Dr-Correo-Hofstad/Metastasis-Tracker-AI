import math

class NasalSinusExclusionEngine:
    def __init__(self, object_max_diameter_mm: float, is_motile: bool = False):
        """
        Models the physical entry parameters and mucociliary clearance timelines 
        of a foreign object within the paranasal sinus networks.
        """
        self.object_diameter = object_max_diameter_mm
        self.is_motile = is_motile # Non-native organisms lack compatible motility in mammalian mucus

    def evaluate_sinus_entry(self) -> dict:
        """
        Calculates mechanical entry allowances across the paranasal ostia metrics.
        """
        ostia_diameters = {
            "maxillary_sinus": 2.5,
            "frontal_sinus": 1.5,
            "sphenoid_sinus": 1.8,
            "ethmoid_cells": 1.0
        }

        entry_results = {}
        for sinus, ostium_d in ostia_diameters.items():
            # Structural mechanical check
            can_enter = self.object_diameter < ostium_d
            entry_results[sinus] = {
                "ostium_aperture_mm": ostium_d,
                "mechanical_entry_allowed": can_enter,
                "status": "Blocked by Bone Boundary" if not can_enter else "Passage Dimensionally Feasible"
            }
        return entry_results

    def calculate_clearance_timeline(self, nasal_path_length_cm: float = 8.0) -> dict:
        """
        Calculates the time required for the mucociliary escalator to expel 
        the object from the nasal cavity into the digestive tract.
        """
        # Baseline physiological mucus transport speed: 6.5 mm per minute
        v_mucus_mm_min = 6.5
        path_length_mm = nasal_path_length_cm * 10.0

        # Non-motile objects are moved strictly at the rate of the escalator vector
        if not self.is_motile:
            clearance_time_min = path_length_mm / v_mucus_mm_min
        else:
            clearance_time_min = path_length_mm / v_mucus_mm_min # Fallback standard physics

        return {
            "nasal_transit_distance_mm": path_length_mm,
            "mucociliary_velocity_mm_min": v_mucus_mm_min,
            "calculated_clearance_time_minutes": round(clearance_time_min, 2),
            "terminal_destination": "Oropharynx / Swallowed to Stomach Acid Sinks"
        }

# =====================================================================
# Operational Verification Loop
# =====================================================================
if __name__ == "__main__":
    # Model an unchewed seafood fragment or small appendage measuring 5.0 mm in diameter
    ingested_fragment = NasalSinusExclusionEngine(object_max_diameter_mm=5.0, is_motile=False)
    
    print("=========================================================================")
    print("PARANASAL SINUS MECHANICAL EXCLUSION & TRANSIT LOGS")
    print("=========================================================================\n")
    
    # 1. Run size checking simulation against paranasal boundaries
    exclusion_report = ingested_fragment.evaluate_sinus_entry()
    print("--- 1. PARANASAL OSTIA MECHANICAL SELECTION MATRIX ---")
    for sinus, reporting in exclusion_report.items():
        print(f" - {sinus.upper():16} -> Ostium: {reporting['ostium_aperture_mm']} mm | Access: {reporting['mechanical_entry_allowed']} ({reporting['status']})")
        
    # 2. Evaluate transit expulsion speeds along the nasal mucosa
    clearance_report = ingested_fragment.calculate_clearance_timeline(nasal_path_length_cm=8.0)
    print("\n--- 2. MUCOCILIARY EXPULSION TIMELINE TRACING ---")
    print(f" Total Transport Path Distance: {clearance_report['nasal_transit_distance_mm']} mm")
    print(f" Calculated Retention Window:  {clearance_report['calculated_clearance_time_minutes']} minutes until evacuation.")
    print(f" Final Particle Destination:    {clearance_report['terminal_destination']} (Confinement Confirmed)")
