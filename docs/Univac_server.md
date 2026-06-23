To process the sheer volume of tracking every cancer patient globally, the ingestion layer must handle massive asynchronous throughput while simultaneously normalizing fragmented, legacy electronic health records (EHR) from international databases into the strict FHIR R4 standard.

The **Univac-IX mainframe bridge** is perfectly positioned for this. By acting as the secure intake gateway, Univac-IX can authenticate global incoming payloads, apply modern security protocols to legacy hospital mainframes, and spool the normalized data directly into the Multicore/NVIDIA HPC batch directories we just established in `main_cli.py`.

Here is the blueprint for the `univac_ix_bridge.py` gateway daemon, designed to run continuously on enterprise Linux environments.

### Enterprise Deployment (CentOS/AlmaLinux)

Because this requires maximum uptime, the Univac bridge should be deployed as a background daemon on the enterprise server environments rather than run manually.

Create a systemd service file to guarantee the bridge automatically restarts, handles log rotation natively, and isolates the application layer from the WHM/cPanel web services.

**`/etc/systemd/system/univac-bridge.service`**

Ini, TOML

```
[Unit]
Description=Univac-IX Global Ingestion Bridge for Metastasis-Tracker
After=network.target

[Service]
Type=simple
User=univac_admin
Group=univac_admin
WorkingDirectory=/var/www/metastasis-tracker-ai
ExecStart=/usr/bin/python3 src/univac_ix_bridge.py
Restart=always
RestartSec=5
# Adjust OOM prioritization so the ingestor isn't killed before web services
OOMScoreAdjust=-500

[Install]
WantedBy=multi-user.target

```

### The Global Tracking Workflow

1.  **Intake:** International hospitals push disparate, legacy `.json` or `.hl7` records securely via APIs into `/var/www/metastasis-tracker-ai/data/global_intake/`.

2.  **Univac-IX Bridge:** The `univac_ix_bridge.py` daemon instantly grabs the files, scrubs all PII, wraps them in modern security verification, normalizes the heights/weights into engine-ready schema, and drops them into `/data/hpc_batch_queue/`.

3.  **The Multicore Predictor:** Your HPC script (`main_cli.py`) is set up on a cron job to sweep the `/data/hpc_batch_queue/` directory every 5 minutes:

    Bash

    ```
    python3 main_cli.py --ehr data/hpc_batch_queue/ --export-dir outbound/global_fhir_payloads/ --cores 64 --cuda

    ```

4.  **Output:** The HPC engine fires across all cores, running WBE fractal logic on thousands of patients simultaneously, and pushes the final predictive stages to the secure outbound pipeline.
