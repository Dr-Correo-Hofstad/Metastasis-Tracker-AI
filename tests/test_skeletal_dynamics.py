"""
Metastasis-Tracker-AI: Section 10 Multi-Planar Test Suite
Filename: tests/test_skeletal_dynamics.py
"""

import pytest
import numpy as np
from src.skeletal_dynamics import MultiPlanarSkeletalDynamics

def test_section_10_multi_planar_fluid_leaching_vectors():
    """
    Verifies that the multi-planar equations correctly isolate directional 
    gradients and trace marrow mineral depletion values within voxel arrays.
    """
    shape = (16, 16, 16)
    
    # 1. Synthesize baseline structured bone voxel grid map
    baseline_volume = np.full(shape, 180.0, dtype=np.float32)
    
    # 2. Simulate progressive localized bone erosion (leaching) inside a target field
    # Create an active low-density erosion trough mimicking low-pH salivary proteolysis
    eroded_volume = baseline_volume.copy()
    eroded_volume[4:12, 4:12, 4:12] -= 80.0  # Force a -80.0 Hounsfield structural shift
    
    # Instantiate the Section 10 multi-planar tracking script
    dynamics_engine = MultiPlanarSkeletalDynamics(eroded_volume, voxel_spacing_mm=(0.5, 0.5, 1.0))
    
    # Calculate density delta shifts against baseline variables
    metrics = dynamics_engine.evaluate_realtime_density_shifts(baseline_volume, diffusion_coefficient=0.12)
    
    # Assert temporal delta metrics register negative shifts (loss of density)
    assert metrics["mean_global_shift"] < 0.0
    assert metrics["marrow_depletion_voxels"] > 0
    assert metrics["peak_resorption_velocity"] == pytest.approx(-80.0)
    
    # Assert directional vectors map non-zero tracking data across all three coordinate axes
    assert metrics["directional_vectors"]["sagittal_x_leach"] > 0.0
    assert metrics["directional_vectors"]["coronal_y_leach"] > 0.0
    assert metrics["directional_vectors"]["axial_z_leach"] > 0.0
