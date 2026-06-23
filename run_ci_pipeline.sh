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
