# Append this onto the end of your run_ci_pipeline.sh file:

echo "====================================================="
echo "🐍 STEP 3: Parsing UAT JSON Report Payload..."
echo "====================================================="

# Run the python script to validate the results and enforce terminal exit codes
python3 /workspace/Metastasis-Tracker-AI/src/parse_reports.py "$REPORT_DIR/index.json"
