#!/usr/bin/env python3
import unittest
import os
import json
import sys

# Ensure src directory visibility for command-line runner utilities
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, "src"))

from biomass_scaler import PycnogonidBiomassEngine
from population_engine import PycnogonidPopulationEngine
from species_selector import PycnogonidSpeciesSelector

class TestSpeciesInitialSelectionScaling(unittest.TestCase):

    def setUp(self):
        """
        Sets up the master UI selection tool and core arithmetic execution blocks.
        """
        self.selector_tool = PycnogonidSpeciesSelector()
        
        # Instantiate placeholder engine profiles representing base structural assets
        self.bio_engine = PycnogonidBiomassEngine({
            "base_femur_length_mm": 10.0, 
            "base_leg_radius_mm": 0.5
        })
        
        # Generic initial config template passed prior to choice mapping
        placeholder_pop_config = {
            "breeding_matrix_config": {
                "leslie_matrix_coefficients": {
                    "fecundity_adult_f": 1.0, "fecundity_brooding_f": 1.0,
                    "survival_larva_to_juv": 0.1, "survival_juv_to_adult": 0.1, "adult_retention_rate": 0.9
                },
                "environmental_sensitivities": {
                    "optimal_breeding_temp_c": 10.0, "thermal_exponential_limit_q10": 2.0,
                    "turbulence_fertilization_penalty_exponent": 1.5, "optimal_ph": 8.1, "ph_tolerance_sigma": 0.3
                }
            }
        }
        self.pop_engine = PycnogonidPopulationEngine(placeholder_pop_config)

    def test_nymphon_australe_initialization_bounds(self):
        """
        Verifies initialization of Nymphon australe selects polar deep-sea thresholds.
        """
        # Select target index at the beginning of workflow
        selection_success = self.selector_tool.apply_selection_to_engines(
            target_species_key="Nymphon_australe",
            biomass_engine=self.bio_engine,
            population_engine=self.pop_engine
        )
        
        self.assertTrue(selection_success)
        
        # Assert morphology constraints shift to slender nymphonid benchmarks
        self.assertEqual(self.bio_engine.base_leg_rad, 0.50)
        
        # Assert demographic matrices scale to cold abyssal constants
        self.assertEqual(self.pop_engine.opt_temp, 1.5)
        self.assertEqual(self.pop_engine.base_f_adult, 450.0)
        self.assertEqual(self.pop_engine.sigma_ph, 0.15) # Rigid pH ceiling matching abyssal stability

    def test_pycnogonum_littorale_initialization_bounds(self):
        """
        Verifies initialization of Pycnogonum littorale selects robust intertidal thresholds.
        """
        # Select target index at the beginning of workflow
        selection_success = self.selector_tool.apply_selection_to_engines(
            target_species_key="Pycnogonum_littorale",
            biomass_engine=self.bio_engine,
            population_engine=self.pop_engine
        )
        
        self.assertTrue(selection_success)
        
        # Assert morphology constraints shift to thick, rugose pycnogonid structures
        self.assertEqual(self.bio_engine.base_leg_rad, 0.85)
        
        # Assert demographic matrices scale to resilient shallow littoral constants
        self.assertEqual(self.pop_engine.opt_temp, 14.0)
        self.assertEqual(self.pop_engine.base_f_adult, 185.0)
        self.assertEqual(self.pop_engine.sigma_ph, 0.35) # Broad pH buffer matching tide pool variance

if __name__ == "__main__":
    unittest.main()
