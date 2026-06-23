#!/usr/bin/env bash

# ==============================================================================
# 🤖 HEADLESS COMPILE & AUTOMATION TOOL PASS RUNNER
# ==============================================================================

# Exit immediately if a command exits with a non-zero status
set -e

# --- Configuration Paths ---
PROJECT_NAME="MetastasisTrackerAI"
PLATFORM="Linux"
CONFIG="Development"
UE_ROOT="/workspace/UnrealEngine" # Adjust this to your absolute UE engine root path
PROJECT_PATH="/workspace/Metastasis-Tracker-AI/MetastasisTrackerAI.uproject"
REPORT_DIR="/workspace/Metastasis-Tracker-AI/Saved/AutomationReports"

# Ensure report directory exists
mkdir -p "$REPORT_DIR"

echo "====================================================="
echo "⚙️  STEP 1: Compiling C++ Subsystems via UnrealBuildTool..."
echo "====================================================="

# Execute hard link pass compiler via UBT command line
"$UE_ROOT/Engine/Build/BatchFiles/RunUBT.sh" \
    "$PROJECT_NAME" \
    "$PLATFORM" \
    "$CONFIG" \
    -Project="$PROJECT_PATH" \
    -NoHotReload \
    -Progress

echo "✅ Compilation successful!"
echo ""
echo "====================================================="
echo "🧪 STEP 2: Running Automated Test Suites via AutomationTool..."
echo "====================================================="

# Run headless tests. We isolate your specific custom classes using the filter 
# flag to skip standard engine test suites.
"$UE_ROOT/Engine/Build/BatchFiles/RunUAT.sh" RunUnreal \
    -project="$PROJECT_PATH" \
    -platform="$PLATFORM" \
    -configuration="$CONFIG" \
    -build \
    -run \
    -unattended \
    -nopause \
    -nullrhi \
    -ExecCmds="Automation RunTests Pycnogonid; Quit" \
    -ReportOutputPath="$REPORT_DIR"

# Check if reports were generated successfully
if [ -f "$REPORT_DIR/index.json" ]; then
    echo "✅ Automation testing pass completed!"
    echo "📊 Test report saved to: $REPORT_DIR/index.json"
else
    echo "⚠️  Testing finished, but no structural JSON report index was discovered."
fi

# Append this onto the end of your run_ci_pipeline.sh file:

echo "====================================================="
echo "🐍 STEP 3: Parsing UAT JSON Report Payload..."
echo "====================================================="

# Run the python script to validate the results and enforce terminal exit codes
python3 /workspace/Metastasis-Tracker-AI/src/parse_reports.py "$REPORT_DIR/index.json"

echo "====================================================="
echo "🐍 STEP 4: Executing Python Tracker Integration Tests..."
echo "====================================================="

# Run the python unittest framework directly from the command line
if python3 "$WORKSPACE_ROOT/tools/test_tracker_integration.py"; then
    echo "🚀 INTEGRATION SUCCESS: Tracker location math and data matrices verified clean!"
    exit 0
else
    echo "❌ INTEGRATION FAILURE: Tracker bridge encountered an unhandled exception or failed assertions."
    exit 1
fi

echo "====================================================="
echo "🐍 STEP 5: Verifying Species Initialization Selector..."
echo "====================================================="

# Execute the initialization test suite via the command line
if python3 "$PROJECT_ROOT/tools/test_species_initialization.py"; then
    echo "🚀 SELECTION VERIFIED: Species constants map cleanly at bootup workflow states!"
else
    echo "❌ SELECTION ERROR: Encountered unhandled exception or data mismatch during profile selection."
    exit 1
fi

echo "====================================================="
echo "🚀 Pipeline execution completed successfully!"
echo "====================================================="
