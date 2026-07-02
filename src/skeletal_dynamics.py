import math
"""
Metastasis-Tracker-AI: Section 10 - Multi-Planar Flow Equations
Module: src/skeletal_dynamics.py
Author: Archival Software Component

This extension provides the mathematical and computational engines to calculate 
real-time fluid density shifts and multi-planar calcium resorption vectors 
across orthogonal bone matrices driven by prostatic/Skene's glandular collapse.
"""

import numpy as np

class MultiPlanarSkeletalDynamics:
    def __init__(self, pelvic_voxel_grid: np.ndarray, voxel_spacing_mm: tuple = (0.5, 0.5, 1.0)):
        """
        Initializes the Section 10 Multi-Planar bone fluid transit grid.
        
        :param pelvic_voxel_grid: 3D float array representing co-registered Hounsfield/Tesla metrics.
        :param voxel_spacing_mm: Dimensions of individual voxel bounds (dx, dy, dz).
        """
        self.grid = pelvic_voxel_grid.astype(np.float32)
        self.dx, self.dy, self.dz = voxel_spacing_mm
        self.depth, self.height, self.width = self.grid.shape

    def compute_multi_planar_gradients(self) -> tuple:
        """
        Calculates independent spatial gradient tensors across three orthogonal planes
        (Axonal-Z, Coronal-Y, Sagittal-X) to track skeletal fluid leaching fronts.
        
        Returns:
            Tuple of np.ndarray matrices mapping (grad_z, grad_y, grad_x).
        """
        print("[INFO] Executing Section 10 Multi-Planar spatial gradient divergence maps...")
        
        # Central finite difference models to resolve directional erosion vectors
        grad_z = np.gradient(self.grid, axis=0) / self.dz
        grad_y = np.gradient(self.grid, axis=1) / self.dy
        grad_x = np.gradient(self.grid, axis=2) / self.dx
        
        return grad_z, grad_y, grad_x

    def evaluate_realtime_density_shifts(self, baseline_grid: np.ndarray, diffusion_coefficient: float = 0.12) -> dict:
        """
        Computes the time-dependent fluid density shift (dH/dt) and maps calcium 
        resorption velocity profiles leached into the venous skeletal interconnect.
        
        :param baseline_grid: Prior co-registered 3D array baseline for delta subtraction profiles.
        :param diffusion_coefficient: Permeability factor modeling structural bone porosity.
        """
        if baseline_grid.shape != self.grid.shape:
            raise ValueError("[ERROR] Dimensional mismatch across compared longitudinal 3D voxel arrays.")

        # 1. Compute direct temporal density variance (dH/dt)
        temporal_shift_matrix = self.grid - baseline_grid.astype(np.float32)
        
        # 2. Extract multi-planar spatial gradients
        gz, gy, gx = self.compute_multi_planar_gradients()
        
        # 3. Calculate 3D Laplacian (Divergence of Gradient) to model systemic fluid leaching
        laplacian_z = np.gradient(gz, axis=0) / self.dz
        laplacian_y = np.gradient(gy, axis=1) / self.dy
        laplacian_x = np.gradient(gx, axis=2) / self.dx
        total_laplacian = laplacian_z + laplacian_y + laplacian_x
        
        # 4. Segment depleted marrow zones where low-pH acidosis has leached native bone minerals
        # Attenuation shifts below local thresholds denote structural calcium loss vectors
        calcium_depletion_mask = (temporal_shift_matrix < -25.0) & (self.grid < 200.0)
        
        # Compute multi-planar breakdown ratios
        sagittal_loss_index = float(np.sum(np.abs(gx)[calcium_depletion_mask]))
        coronal_loss_index = float(np.sum(np.abs(gy)[calcium_depletion_mask]))
        axial_loss_index = float(np.sum(np.abs(gz)[calcium_depletion_mask]))
        
        density_metrics = {
            "mean_global_shift": float(np.mean(temporal_shift_matrix)),
            "peak_resorption_velocity": float(np.min(temporal_shift_matrix)),
            "marrow_depletion_voxels": int(np.sum(calcium_depletion_mask)),
            "directional_vectors": {
                "sagittal_x_leach": sagittal_loss_index,
                "coronal_y_leach": coronal_loss_index,
                "axial_z_leach": axial_loss_index
            },
            "net_skeletal_flux": float(np.sum(diffusion_coefficient * total_laplacian))
        }
        
        print("[SUCCESS] Section 10 multi-planar fluid mechanics loops evaluated cleanly.")
        return density_metrics

class DynamicSkeletalEngine:
    def __init__(self, height_cm: float, weight_kg: float, body_build: str, hydration_level: float):
        """
        Initializes the Dynamic Osseous Skeleton and Bone Marrow Engine.
        Structural matrices adapt dynamically to baseline anthropometrics.
        """
        self.height_cm = height_cm
        self.weight_kg = weight_kg
        self.build = body_build.lower()
        self.chi = max(0.5, min(1.5, hydration_level)) # Hydration vector factor
        
        # Ingest baseline metrics matching repository protocols
        self.bsa = 0.007184 * (self.height_cm ** 0.725) * (self.weight_kg ** 0.425)
        self.lbm = 1.10 * self.weight_kg - 128 * ((self.weight_kg / self.height_cm) ** 2)
        
        # Calculate global skeletal parameters
        self.total_skeleton_mass_kg = self._calculate_skeletal_mass()
        self.bone_density_g_cm3 = 1.92

    def _calculate_skeletal_mass(self) -> float:
        if self.build == "ectomorph":
            c_frame = 0.13
        elif self.build == "endomorph":
            c_frame = 0.18
        else:
            c_frame = 0.15 # Mesomorphic baseline norm
        return c_frame * math.pow(self.lbm, 0.95)

    def generate_regional_skeletal_matrix(self, mechanical_strain_load: float) -> dict:
        """
        Partitions global skeletal mass into functional bone matrices, 
        tracking structural density, trabecular voids, and active marrow volumes.
        
        :param mechanical_strain_load: Multiplier representing physical exertion force (1.0 = resting)
        """
        w_skel_g = self.total_skeleton_mass_kg * 1000.0
        
        # Regional distributions: { Identity: (Mass_Fraction, Bone_Count, Has_Red_Marrow) }
        regions = {
            "cranial_facial":      (0.12, 22, False),
            "axial_spine":         (0.20, 26, True),
            "thoracic_cage":       (0.15, 25, True),
            "upper_extremities":   (0.23, 64, False),
            "lower_pelvic_matrix": (0.30, 69, True)
        }

        # Bone Mineral Density (BMD) adjusts dynamically via Wolff's Law approximations
        # Dehydration strains bone matrix turnover pathways
        bmd_baseline = 1.25 * self.chi  # g/cm² reference unit scaling
        bmd_dynamic = bmd_baseline * (1.0 + 0.08 * (mechanical_strain_load - 1.0))

        regional_matrix = {}
        for name, (fraction, count, has_marrow) in regions.items():
            reg_mass = w_skel_g * fraction
            reg_volume_cm3 = reg_mass / self.bone_density_g_cm3
            
            # Active adult red marrow is localized to axial/pelvic trabecular spaces
            if has_marrow:
                # Marrow space volume scales with overall bone volume and hydration thickness
                marrow_vol_cm3 = (reg_volume_cm3 * 0.18) * self.chi
                structural_void_fraction = 0.35
            else:
                marrow_vol_cm3 = 0.0
                structural_void_fraction = 0.08 # Cortical dominance

            # Structural critical failure threshold (Fractal bone load ceiling in Newtons)
            fracture_threshold_N = 4500.0 * bmd_dynamic * (reg_mass / w_skel_g)

            regional_matrix[name] = {
                "bone_count": count,
                "total_regional_mass_g": round(reg_mass, 1),
                "total_regional_volume_cm3": round(reg_volume_cm3, 1),
                "structural_porosity_fraction": structural_void_fraction,
                "active_red_marrow_volume_cm3": round(marrow_vol_cm3, 2),
                "local_bone_mineral_density_g_cm2": round(bmd_dynamic, 3),
                "calculated_fracture_threshold_newtons": round(fracture_threshold_N, 1)
            }

        return regional_matrix

    def calculate_bone_marrow_sinusoidal_flux(self, regional_matrix: dict, local_perfusion_pressure_mmHg: float) -> dict:
        """
        Models the cell-shedding and mass transport kinetics out of the trabecular bone 
        marrow niches directly into neighboring vascular generation loops.
        """
        # Baseline shedding coefficient (cells exiting per cm³ of marrow per mmHg per second)
        k_sinusoidal = 4.2e2
        p_local = max(5.0, min(120.0, local_perfusion_pressure_mmHg))
        
        total_marrow_volume = sum(r["active_red_marrow_volume_cm3"] for r in regional_matrix.values())
        
        # Cellular efflux rate equation: J = K * V * P
        cell_efflux_rate_sec = k_sinusoidal * total_marrow_volume * p_local
        
        # Scale up microvascular blood flow resistance inside bone canals if dehydration is active
        intraosseous_vascular_resistance_multiplier = 1.0 + 0.4 * (1.0 - self.chi)

        return {
            "total_systemic_red_marrow_volume_cm3": round(total_marrow_volume, 2),
            "sinusoidal_perfusion_pressure_mmHg": p_local,
            "sinusoidal_cell_shedding_rate_seconds": int(cell_efflux_rate_sec),
            "intraosseous_vascular_resistance_multiplier": round(intraosseous_vascular_resistance_multiplier, 2),
            "hematopoietic_niche_status": "HIGH TURNOVER" if p_local > 40.0 else "BASAL RETENTION STATE"
        }

# =====================================================================
# Operational Verification Matrix
# =====================================================================
if __name__ == "__main__":
    # Simulate an athletic patient under high physical strain (Strain load = 1.5, e.g. sprinting/lifting)
    engine = DynamicSkeletalEngine(height_cm=180.0, weight_kg=78.0, body_build="mesomorph", hydration_level=1.0)
    
    print("=========================================================================")
    print("DYNAMIC OSSEOUS SKELETON AND HEMATOPOIETIC MARROW LOGS")
    print("=========================================================================\n")
    
    # 1. Generate the dynamic structural bone matrix profile
    skeletal_matrix = engine.generate_regional_skeletal_matrix(mechanical_strain_load=1.5)
    print(f"--- 1. STRUCTURAL FRAMEWORK PARTITIONING ( Wolff's Law Strain: 1.5 ) ---")
    print(f" Calculated Dry Skeletal Mass: {engine.total_skeleton_mass_kg:.2f} kg")
    
    spine = skeletal_matrix["axial_spine"]
    pelvis = skeletal_matrix["lower_pelvic_matrix"]
    upper_limb = skeletal_matrix["upper_extremities"]
    
    print(f"  -> Spine Node Matrix  | Mass: {spine['total_regional_mass_g']}g | Local BMD: {spine['local_bone_mineral_density_g_cm2']} g/cm²")
    print(f"  -> Pelvis Node Matrix | Mass: {pelvis['total_regional_mass_g']}g | Red Marrow Pool: {pelvis['active_red_marrow_volume_cm3']} cm³")
    print(f"  -> Upper Extremities  | Mass: {upper_limb['total_regional_mass_g']}g | Fracture Ceiling: {upper_limb['calculated_fracture_threshold_newtons']} N\n")

    # 2. Compute live sinusoidal cell-shedding kinetics into circulation loops
    # Simulate a local nutrient artery perfusion pressure of 45 mmHg
    marrow_kinetics = engine.calculate_bone_marrow_sinusoidal_flux(skeletal_matrix, local_perfusion_pressure_mmHg=45.0)
    print("--- 2. BONE MARROW SINUSOIDAL EMISSION KINETICS ---")
    print(f" Systemic Adult Red Marrow Capacity: {marrow_kinetics['total_systemic_red_marrow_volume_cm3']} cm³")
    print(f" Local Perfusion Delivery Pressure:  {marrow_kinetics['sinusoidal_perfusion_pressure_mmHg']} mmHg")
    print(f" Sinusoidal Cell Influx Into Flow:   {marrow_kinetics['sinusoidal_cell_shedding_rate_seconds']:,} cells/second")
    print(f" Intraosseous Resistance Multiplier: {marrow_kinetics['intraosseous_vascular_resistance_multiplier']}x base")
    print(f" Hematopoietic Structural Status:     {marrow_kinetics['hematopoietic_niche_status']}")
