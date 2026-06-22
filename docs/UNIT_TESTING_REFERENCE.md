🧪 Pycnogonid Simulation Subsystem: Unit Testing Reference

This document establishes the test suites, verification inputs, and expected edge-case tolerances for your continuous integration (CI) automation pipeline. These tests guarantee mathematical stability during extreme environmental anomalies.

* * * * *

🌊 1. Hydrodynamics & Viscosity Tests (`test_hydrodynamics.py`)

This suite isolates the transition between high-velocity open-water flow and high-resistance creeping flow regimes.

Test Case 1.1: Absolute Zero Fluid Velocity Bound

-   **Objective**: Ensure that a division-by-zero error is impossible if an agent enters an uninitialized or mathematically frozen environment (\(\mu = 0\)).
-   **Input Bounds**:
    -   `fluid_viscosity_pas` = `0.00000`
    -   `thrust_force_f` = `0.012`
-   **Expected Assertions**:
    -   The engine must intercept `0.0` and gracefully default to an execution error or an arbitrary maximum speed clamp.
    -   `step_velocity_mm_sec` must not evaluate to `NaN` or `Infinity`.

Test Case 1.2: Boundary Transition Constraint (\(n = 0.5 \to 1.0\))

-   **Objective**: Verify the discrete physics modifier switch when an agent changes states from free-swimming to encysted/internal.
-   **Input Tensors**:
    -   State `FREE_SWIMMING` \(\rightarrow \) State `ENCYSTED_FEEDING`
    -   `fluid_viscosity_pas` shifts from `0.001` (Water) to `1.000` (Dense Matrix).
-   **Expected Assertions**:
    -   `step_velocity_mm_sec` for an actively encysted agent must return exactly `0.0`.
    -   Internal moving velocity variables must scale linearly down matching the Stokes regime scaling factor (\(\frac{1}{\mu }\)).

* * * * *

🧪 2. Enzymatic Liquefaction Tests (`test_digestion.py`)

This suite validates the Michaelis-Menten multi-substrate loop, specifically monitoring competitive inhibition parameters and high-density structural limits.

Test Case 2.1: Competitive Exclusion Over-Saturation

-   **Objective**: Verify that adding an astronomical concentration of a single competing protein properly drives the digestion speed of secondary target proteins down to zero.
-   **Input Tensors**:
    -   `mesogleal_collagen_type_i` concentration = `0.05` \(\text{mg}/\text{mm}^3\)
    -   `actinoporin_complex` concentration = `100000.00` \(\text{mg}/\text{mm}^3\) (Artificial saturation)
-   **Expected Assertions**:
    -   The calculated value for \(R_{\text{liq}}\) targeting the collagen substrate must fall below a precision ceiling of `1e-7`.
    -   The total aggregate mass liquefaction rate must mathematically plateau at \(V_{\max }\) without experiencing numerical overflows.

Test Case 2.2: Extreme Tissue Density Inhibition (\(\rho \to \infty\))

-   **Objective**: Test if an infinitely dense structural substrate completely stops enzymatic breakdown.
-   **Input Bounds**:
    -   `structural_density_mg_mm3` = `500.0` (Impenetrable structural matrix barrier)
-   **Expected Assertions**:
    -   The denominator scaling component \((1 + \rho)\) must force the calculated \(R_{\text{liq}}\) down exponentially.
    -   The resultant growth metric variable \(k_{\text{current}}\) must drop below baseline maintenance requirements, triggering starvation logic.

* * * * *

📈 3. Demographic & Environment Stress Tests (`test_population.py`)

This suite evaluates the Lefkovitch matrix multiplier outputs under rapid, non-linear climate fluctuations.

Test Case 3.1: Extreme Alkaline pH Shock Collapse

-   **Objective**: Confirm population collapses occur when environmental context keys contain critical pH levels outside normal physiological limits.
-   **Input Profile**:
    -   `temperature` = `14.0`, `turbulence` = `0.0`, `ph` = `11.5`
-   **Expected Assertions**:
    -   The Gaussian scalar \(f(\text{pH})\) must return a value `< 0.0001`.
    -   The matrix entry for \(P_{\text{larva}\rightarrow \text{juv}}\) must resolve to `0.0`.
    -   Executing 3 consecutive projection loop iterations using `np.dot()` must verify a complete collapse of new larvae entries (\(n_{\text{larva}} \to 0\)).

Test Case 3.2: Carrying Capacity Logistic Governor

-   **Objective**: Ensure population totals smoothly cap off at the pre-configured carrying capacity ceiling without fluctuating erratically or trending to infinity.
-   **Input Setup**:
    -   `carrying_capacity` = `5000.0`
    -   Initial population counts vector = `[10000.0, 5000.0, 2000.0, 500.0]` (Intentionally over-crowded)
-   **Expected Assertions**:
    -   After exactly one execution tick, the sum total of all stages in the history array must equal exactly `5000.0`.
    -   The saturation scalar must maintain proper stage proportions while squashing absolute integer counts.

* * * * *

🏁 4. Automation Pipeline Integration Matrix

| Test Suite File | Minimum Execution Coverage | Allowed Float Divergence (`atol`) | Action on Failure |
| `test_hydrodynamics.py` | 100% Branches | `1e-5` | Halt Pipeline / Block Merge |
| `test_digestion.py` | 95% Lines | `1e-6` | Halt Pipeline / Block Merge |
| `test_population.py` | 100% Branches | `1e-4` | Flag Warning / Log Analytics |

* * * * *
