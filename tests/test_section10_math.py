"""
Metastasis-Tracker-AI: Section 10 Finite Differences Regression Suite
Filename: tests/test_section10_math.py
Author: Archival Test Component

This testing module leverages pytest to systematically validate the numerical
precision, gradient directionality, and Laplacian divergence models implemented 
in the Section 10 skeletal fluid transit pipeline.
"""

import pytest
import numpy as np
from src.skeletal_dynamics import MultiPlanarSkeletalDynamics

@pytest.fixture
def standard_voxel_spacing():
    """Provides uniform spatial dimensions matching default pipeline calibrations."""
    return (0.5, 0.5, 1.0)  # (dx, dy, dz) in millimeters

@pytest.fixture
def localized_cube_dimensions():
    """Defines a compact grid shape optimized for high-speed matrix execution."""
    return (16, 16, 16)  # (Z, Y, X) voxel matrix shape

def test_finite_differences_linear_gradient_precision(localized_cube_dimensions, standard_voxel_spacing):
    """
    Verifies that Section 10 finite difference equations calculate a known,
    uniform linear density gradient with exact mathematical precision across axes.
    """
    dims = localized_cube_dimensions
    dx, dy, dz = standard_voxel_spacing
    
    # Construct a flat validation volume
    test_volume = np.zeros(dims, dtype=np.float32)
    
    # Inject a clean, linear slope along the Sagittal-X axis (axis 2)
    # Intensity climbs by exactly 10 units per voxel index increment
    for x in range(dims[2]):
        test_volume[:, :, x] = x * 10.0
        
    engine = MultiPlanarSkeletalDynamics(test_volume, voxel_spacing_mm=standard_voxel_spacing)
    gz, gy, gx = engine.compute_multi_planar_gradients()
    
    # Assert non-targeted planes evaluate to zero slope vectors
    np.testing.assert_array_equal(gz, 0.0)
    np.testing.assert_array_equal(gy, 0.0)
    
    # Assert Sagittal-X gradient matches analytical derivation: delta_val / dx -> 10.0 / 0.5 = 20.0
    # Center slices ignore boundary truncation limits and must equate to exactly 20.0
    np.testing.assert_array_almost_equal(gx[:, :, 2:-2], 20.0, decimal=4)

def test_laplacian_divergence_null_in_uniform_fields(localized_cube_dimensions, standard_voxel_spacing):
    """
    Ensures that a completely uniform, noise-free tissue density field results in a 
    net zero Laplacian flux, preventing false positive leaching markers.
    """
    # Initialize a homogeneous solid bone field block
    homogeneous_volume = np.full(localized_cube_dimensions, 200.0, dtype=np.float32)
    baseline_volume = homogeneous_volume.copy()
    
    engine = MultiPlanarSkeletalDynamics(homogeneous_volume, voxel_spacing_mm=standard_voxel_spacing)
    metrics = engine.evaluate_realtime_density_shifts(baseline_volume, diffusion_coefficient=0.12)
    
    # Assert zero fluid shift and zero net skeletal flux
    assert metrics["mean_global_shift"] == 0.0
    assert metrics["marrow_depletion_voxels"] == 0
    assert metrics["net_skeletal_flux"] == 0.0
    assert metrics["directional_vectors"]["sagittal_x_leach"] == 0.0
    assert metrics["directional_vectors"]["coronal_y_leach"] == 0.0
    assert metrics["directional_vectors"]["axial_z_leach"] == 0.0

def test_asymmetric_erosion_flux_separation(localized_cube_dimensions, standard_voxel_spacing):
    """
    Validates that a highly directional, asymmetric erosion path registers 
    disproportionate leached mass indicators on its target plane.
    """
    dims = localized_cube_dimensions
    baseline = np.full(dims, 180.0, dtype=np.float32)
    eroded = baseline.copy()
    
    # Inject severe, isolated erosion explicitly down the Coronal-Y plane (axis 1)
    # This leaves the Sagittal-X layout relatively stable
    eroded[5, 2:14, 5] -= 100.0  
    
    engine = MultiPlanarSkeletalDynamics(eroded, voxel_spacing_mm=standard_voxel_spacing)
    metrics = engine.evaluate_realtime_density_shifts(baseline, diffusion_coefficient=0.12)
    
    directional = metrics["directional_vectors"]
    
    # Assert that Coronal-Y plane calculation registers a prominent local leaching vector
    assert directional["coronal_y_leach"] > directional["sagittal_x_leach"]
    assert metrics["marrow_depletion_voxels"] > 0

def test_dimensional_mismatch_exception_handling(standard_voxel_spacing):
    """
    Guarantees that passing inconsistent matrix arrays across tracking timelines 
    triggers explicit ValueError exceptions rather than outputting corrupted data.
    """
    volume_a = np.zeros((8, 8, 8), dtype=np.float32)
    volume_b = np.zeros((8, 8, 10), dtype=np.float32)  # Mismatched dimension track
    
    engine = MultiPlanarSkeletalDynamics(volume_a, voxel_spacing_mm=standard_voxel_spacing)
    
    with pytest.raises(ValueError, match="Dimensional mismatch across compared longitudinal 3D voxel arrays."):
        engine.evaluate_realtime_density_shifts(volume_b)
