# Splenic Filtration Matrix Technical Specification (`docs/splenic_clearance_spec.md`)

## 1. Overview
The Splenic Clearance module provides a biophysical model of structural filtration within the splenic red pulp sinuses. It tracks the mechanical capture, size-exclusion screening, and cellular removal of cellular debris and fragments left behind after sepsis treatment clears an active infection.

---

## 2. Mathematical Formulations

### A. Size-Exclusion Filtration Sieve Dynamics
Circulating cellular debris concentrations ($C_{\text{fragments}}$, particles/$\mu$L) track over execution steps using an ordinary differential equation (ODE) balancing fragment production against mechanical splenic grid extraction:

$$\frac{dC_{\text{fragments}}(t)}{dt} = -J_{\text{spleen\_filtration}}(t) + J_{\text{lysis\_input}}(t)$$

### B. Non-Linear Entrapment and Clogging Coefficients
The forward filtration flux ($J_{\text{spleen\_filtration}}$) drops as a function of fluid density shifts ($\chi$) and structural tissue overloading limits. If debris accumulates faster than macrophage digestion capacity, the system models a progressive mechanical filter clog:

$$J_{\text{spleen\_filtration}}(t) = Q_{\text{spleen}}(\chi) \times \eta_{\text{mesh}}(d_{\text{part}}) \times \left( 1.0 - \frac{M_{\text{splenic\_load}}(t)}{M_{\text{saturation\_cap}}} \right)$$

The mesh capture efficiency ($\eta_{\text{mesh}}$) follows a sigmoidal threshold function centered around the interendothelial slit width ceiling ($d_{\text{slit}} \approx 2.5\,\mu\text{m}$):

$$\eta_{\text{mesh}}(d_{\text{part}}) = \frac{1}{1 + e^{-k_{\text{mesh}} \cdot (d_{\text{part}} - d_{\text{slit}})}}$$

---

## 3. Tool Utilities Deployment

### A. Real-Time Console Data Streaming
To extract and debug logged trajectory metrics without launching heavy graphical plots, execute the compiled terminal data parser from your command line:

```bash
python3 src/medbin_terminal_parser.py
```

This reads the 36-byte packed data segments sequentially, validates the file headers, and prints structured tracking values in an easily scan-able text layout.

### B. Local Webhook Verifications
To test the outbound continuous integration JSON notification scripts locally, configure the execution permissions and run the background test script:

```bash
chmod +x tests/test_local_webhook.sh
./tests/test_local_webhook.sh
```
