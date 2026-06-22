import math
import random

class PycnogonidStateMatrix:
    def __init__(self, config_data):
        """
        Initializes the agent state machine with physical and environmental parameters.
        """
        self.agent_id = config_data.get("agent_id", "pyc_agent_unnamed")
        self.current_state = "FREE_SWIMMING"
        
        # Physical metrics
        self.leg_span = config_data["physical_properties"]["leg_span_mm"]
        self.r_leg = config_data["physical_properties"]["leg_ratio_r"]
        self.base_velocity = 0.5  # mm/sec baseline speed
        
        # Optimal baselines for marine arthopods
        self.env_optima = {
            "temperature": 12.0,      # °C
            "sigma_t": 6.0,
            "ph": 8.1,                # Standard ocean pH
            "sigma_ph": 0.4,
            "noise_ambient": 40.0,    # dB (underwater baseline)
            "noise_decay_lambda": 0.015
        }
        
    def calculate_environmental_modifiers(self, env_context):
        """
        Evaluates current temperature, pH, and acoustic noise to generate the HSI.
        """
        t = env_context.get("temperature", 12.0)
        ph = env_context.get("ph", 8.1)
        noise = env_context.get("noise_level_db", 40.0)
        
        # 1. Temperature Curve
        f_t = math.exp(-((t - self.env_optima["temperature"]) ** 2) / (2 * (self.env_optima["sigma_t"] ** 2)))
        
        # 2. pH Response Curve
        f_ph = math.exp(-((ph - self.env_optima["ph"]) ** 2) / (2 * (self.env_optima["sigma_ph"] ** 2)))
        
        # 3. Noise Stress Penalty
        delta_noise = max(0.0, noise - self.env_optima["noise_ambient"])
        f_n = math.exp(-self.env_optima["noise_decay_lambda"] * delta_noise)
        
        # Geometric mean calculation for HSI
        hsi = (f_t * f_ph * f_n) ** (1.0 / 3.0)
        
        # Calculate ectothermic metabolic shift (Q10 rule)
        q10_modifier = 2.0 ** ((t - self.env_optima["temperature"]) / 10.0)
        
        return {
            "hsi": hsi,
            "velocity_scalar": hsi * q10_modifier,
            "kinetic_stress": 1.0 - f_n
        }

    def evaluate_state_tick(self, env_context, telemetry):
        """
        Executes one evaluation cycle of the behavioral state machine matrix.
        """
        modifiers = self.calculate_environmental_modifiers(env_context)
        hsi = modifiers["hsi"]
        
        # Extract environment/telemetry inputs
        delta_c = env_context.get("chemical_gradient_delta_c", 0.0)
        w_host = telemetry.get("w_host", 0.0)
        p_penetrate = telemetry.get("p_penetrate", 0.0)
        time_elapsed = telemetry.get("time_elapsed", 0.0)
        
        # Apply noise disruptions to tracking precision
        effective_gradient = delta_c * (1.0 - modifiers["kinetic_stress"])

        # State transition evaluation logic
        if self.current_state == "FREE_SWIMMING":
            if hsi < 0.15:
                self.current_state = "DEAD"
            elif effective_gradient > 0.45:
                self.current_state = "HOST_SEEKING"
                
        elif self.current_state == "HOST_SEEKING":
            if hsi < 0.20 or effective_gradient <= 0.10:
                self.current_state = "FREE_SWIMMING"
            elif p_penetrate >= 0.75 and w_host > 5.0:
                self.current_state = "ENCYSTED_FEEDING"
                
        elif self.current_state == "ENCYSTED_FEEDING":
            # Galls offer partial protection, making agents less sensitive to pH/Noise changes
            buffered_hsi = hsi * 1.5
            if buffered_hsi < 0.10 or telemetry.get("host_alive") is False:
                self.current_state = "DEAD"
            elif telemetry.get("larval_length_mm", 0.0) >= 2.5:
                self.current_state = "INTERNAL_FREE_MOVING"
                
        elif self.current_state == "INTERNAL_FREE_MOVING":
            if p_penetrate >= 0.60:
                self.current_state = "FREE_LIVING_ADULT"
                
        elif self.current_state == "FREE_LIVING_ADULT":
            if hsi < 0.15:
                self.current_state = "DEAD"
            elif telemetry.get("eggs_mature") is True:
                self.current_state = "FREE_SWIMMING"  # Re-enters loop to shed brood

        # Update and return adjusted speed vector step
        current_speed = self.base_velocity * modifiers["velocity_scalar"]
        return {
            "current_state": self.current_state,
            "calculated_hsi": hsi,
            "step_velocity_mm_sec": 0.0 if self.current_state in ["ENCYSTED_FEEDING", "DEAD"] else current_speed
        }
