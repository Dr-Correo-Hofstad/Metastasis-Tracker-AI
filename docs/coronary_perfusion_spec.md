# Coronary Perfusion Failure States & Link Integrity Specifications

## 1. Overview
This technical reference defines the biophysical equations mapping coronary artery perfusion collapse secondary to critical diastolic hypotension ($DBP < 40\text{ mmHg}$) and details the automated script parameters used to sweep documentation directories for broken relative links.

---

## 2. Mathematical Architecture

### A. Diastolic Coronary Perfusion Pressure ($CPP$) Tracking
Myocardial oxygenation occurs almost entirely during cardiac diastole. The forward perfusion pressure drive gradient ($CPP$, mmHg) maps as:

\[CPP(t) = DBP(t) - LVEDP(t)\]

### B. Coronary Blood Flow ($CBF$) Loss Function
When systemic shock causes $DBP$ to drop beneath the 40 mmHg auto-regulatory threshold limit, Coronary Blood Flow ($CBF$, mL/min) collapses linearly relative to the critical zero-flow endpoint ($CPP_{\text{zero}} = 7.5\text{ mmHg}$):

\[CBF(t) = CBF_{\text{basal}} \times \left( \frac{CPP(t) - 7.5}{55.0 - 7.5} \right) \times \chi\]

If $CBF(t) \le 0.35 \times CBF_{\text{basal}}$ for a duration timeline $\Delta t \ge 180\text{ seconds}$, myocardial contractility vectors fail, committing an automated `MYOCARDIAL_INFARCTION_ARREST` crisis flag to the tracking registers.

---

## 3. Automation Task Infrastructure Shortcuts

Automate documentation cross-checking and diagnostic log scanning via short terminal shortcuts:

*   **Markdown Link Validation**: To parse all `.md` files inside the `docs/` directory and check for broken local file paths before compiling repository updates, run the verification tool:
    ```bash
    make check-links
    ```

*   **HDF5 Coronary Perfusion Scan**: To extract packed single-precision single arrays from storage containers and scan them for hidden low-pressure ischemia anomalies, execute the parser driver:
    ```bash
    make scan-perfusion
    ```
