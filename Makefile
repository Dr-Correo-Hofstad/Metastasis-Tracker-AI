# =====================================================================
# Metastasis-Tracker-AI Platform Automation Controller Makefile
# =====================================================================

.PHONY: test validate run-ui parse archive local-webhook help

# Default target executes complete continuous validation bounds
all: validate test

validate:
	@echo "Executing continuous integration diagnostic drivers..."
	./run_pipeline.sh

test:
	@echo "Running end-to-end multi-module pipeline validation assertions..."
	python3 -m unittest tests/test_integration_pipeline.py

run-ui:
	@echo "Launching real-time command-line bioenergetic dashboard panel..."
	python3 src/metabolic_dashboard_engine.py

parse:
	@echo "Decoding compressed .medbin streams to raw console layout text..."
	python3 src/medbin_terminal_parser.py

archive:
	@echo "Initiating file compression on historical binary telemetry trees..."
	python3 src/telemetry_archiver.py

local-webhook:
	@echo "Launching local test loop server to catch outbound alert JSON streams..."
	chmod +x tests/test_local_webhook.sh
	./tests/test_local_webhook.sh

help:
	@echo "========================================================================="
	@echo "  METASTASIS-TRACKER-AI CONTROL SYSTEM MAKEFILE INTERFACE"
	@echo "========================================================================="
	@echo "  make validate        - Executes the main shell pipeline driver checking permissions"
	@echo "  make test            - Runs the synchronized end-to-end integration test suites"
	@echo "  make run-ui          - Launches the real-time live terminal patient telemetry table"
	@echo "  make parse           - Decodes medbin files directly to text rows on the screen"
	@echo "  make archive         - Compresses historical data files into zipped packages"
	@echo "  make local-webhook   - Tests JSON notification hooks using background listeners"
	@echo "========================================================================="
