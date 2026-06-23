import struct
import os
import math
import matplotlib.pyplot as plt

class GraphicsMatrixMapper:
    def __init__(self, binary_input_filepath: str, output_image_path: str = "docs/telemetry_chart.png"):
        """
        Parses raw packed medical telemetry streams (.medbin) and maps them 
        directly into automated line charts for diagnostic review.
        """
        self.input_path = binary_input_filepath
        self.output_path = output_image_path

    def parse_and_plot_history(self):
        """
        Reads, extracts, and visualizes the binary row records securely.
        """
        if not os.path.exists(self.input_path):
            print(f"[-] Execution aborted: Source binary file missing at {self.input_path}")
            return False

        timesteps = []
        ph_records = []
        hco3_records = []
        ca_records = []
        pco2_records = []

        with open(self.input_path, "rb") as f:
            # Read and verify the custom 4-byte Magic Identifier header
            magic = f.read(4)
            if len(magic) < 4 or struct.unpack(">I", magic)[0] != 0x4D454442:
                print("[-] Fatal: Mismatched or corrupt file format architecture.")
                return False

            # Ingest 36-byte packed data payload structures
            # Format pattern matching: >IIfffffff (36 total bytes)
            while True:
                chunk = f.read(36)
                if len(chunk) < 36:
                    break
                
                unpacked = struct.unpack(">IIfffffff", chunk)
                
                timesteps.append(unpacked[0])
                ph_records.append(unpacked[2])
                hco3_records.append(unpacked[3])
                ca_records.append(unpacked[4])
                pco2_records.append(unpacked[7])

        if not timesteps:
            print("[-] Warning: Binary file parsed successfully but contained 0 rows.")
            return False

        # Build multi-panel subplot grid visualization architecture
        fig, axs = plt.subplots(2, 2, figsize=(12, 8))
        fig.suptitle("SYSTEMIC PATIENT METABOLIC TELEMETRY CASCADE MATRIX", fontsize=14, fontweight='bold')

        # Panel 1: Blood pH Trajectory Channel
        axs[0, 0].plot(timesteps, ph_records, color='crimson', marker='o', linewidth=2)
        axs[0, 0].set_title("Systemic Arterial Blood pH Baseline")
        axs[0, 0].set_ylabel("pH Units")
        axs[0, 0].grid(True, linestyle='--')

        # Panel 2: Bicarbonate Concentration Tracker
        axs[0, 1].plot(timesteps, hco3_records, color='teal', marker='s', linewidth=2)
        axs[0, 1].set_title("Plasma Bicarbonate (HCO3-) Pools")
        axs[0, 1].set_ylabel("Concentration (mEq/L)")
        axs[0, 1].grid(True, linestyle='--')

        # Panel 3: Serum Calcium Ion Extravasation Curve
        axs[1, 0].plot(timesteps, ca_records, color='darkorange', marker='^', linewidth=2)
        axs[1, 0].set_title("Serum Calcium Ion (Ca2+) Matrix Load")
        axs[1, 0].set_ylabel("Mass Density (mg/dL)")
        axs[1, 0].grid(True, linestyle='--')

        # Panel 4: Respiratory Partial Pressure (pCO2)
        axs[1, 1].plot(timesteps, pco2_records, color='navy', marker='d', linewidth=2)
        axs[1, 1].set_title("Partial Pressure of Carbon Dioxide (pCO2)")
        axs[1, 1].set_ylabel("Pressure (mmHg)")
        axs[1, 1].grid(True, linestyle='--')

        for ax in axs.flat:
            ax.set_xlabel("Timeline Step Increment (seconds)")

        plt.tight_layout()
        
        # Ensure output directory paths exist before saving files
        output_dir = os.path.dirname(self.output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        plt.savefig(self.output_path, dpi=150)
        plt.close()
        print(f"[+] Diagnostic map file successfully generated at: {self.output_path}")
        return True

# =====================================================================
# Standalone Local Verification Sandbox
# =====================================================================
if __name__ == "__main__":
    # Create fake binary diagnostic file data to verify graphics pipeline loop execution
    mock_bin_path = "tests/sandbox_telemetry.medbin"
    output_png = "docs/telemetry_chart.png"
    
    if not os.path.exists("tests"):
        os.makedirs("tests")
        
    print("Pre-packing localized binary mock logs...")
    with open(mock_bin_path, "wb") as bf:
        bf.write(struct.pack(">I", 0x4D454442)) # Pack standard MEDB magic number
        # Pack 5 sequential seconds of dynamic recovery/stress configurations
        for tick in range(1, 6):
            bf.write(struct.pack(">IIfffffff", tick, 1002, 7.42 - (tick*0.02), 24.0 - tick, 9.5 + (tick*0.5), 5.0, 98.2, 40.0 + (tick*2)))
            
    # Execute the graphical visualization loop runner
    mapper = GraphicsMatrixMapper(binary_input_filepath=mock_bin_path, output_image_path=output_png)
    mapper.parse_and_plot_history()
