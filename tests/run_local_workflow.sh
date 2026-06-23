#!/bin/bash

# =====================================================================
# Local Repository Workflow Verification and Testing Harness
# =====================================================================

set -e

CYAN='\033[0;36m'
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${CYAN}=========================================================================${NC}"
echo -e "${CYAN}   RUNNING LOCAL INTEGRATION WORKFLOW SUITE FOR ENVIRONMENT LOGS         ${NC}"
echo -e "${CYAN}=========================================================================${NC}"

echo -e "\n[STEP 1/4]: Executing automated configuration schema verifications..."
python3 src/fibrinolysis_verifier_core.py

echo -e "\n[STEP 2/4]: Running fluid advection reflex jet mechanical assertions..."
python3 src/respiratory_reflex_engine.py

echo -e "\n[STEP 3/4]: Running Laplace Law modified structural atelectasis tests..."
python3 src/pulmonary_collapse_engine.py

echo -e "\n[STEP 4/4]: Executing automated HDF5 database compliance rule checks..."
python3 src/pulmonary_hdf5_core.py

echo -e "\n${GREEN}=========================================================================${NC}"
echo -e "${GREEN} ✅ ALL LOCAL ENVIRONMENT WORKFLOW COMMANDS PASSED STRUCTURAL VERIFICATION ${NC}"
echo -e "${GREEN}=========================================================================${NC}"
