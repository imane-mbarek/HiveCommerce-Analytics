#!/bin/bash

# Robust automation for Binôme 1 - Personne 2
# Usage: ./scripts/run_hive_tests_personne2.sh

set -euo pipefail

echo "--- 0. Environment checks ---"
if ! command -v docker >/dev/null 2>&1; then
	echo "ERROR: docker CLI not found. Install Docker or run the PowerShell wrapper: scripts/run_hive_tests_personne2.ps1"
	exit 1
fi

echo "--- 1. Check hive-server2 container ---"
if ! docker ps --filter name=hive-server2 --format '{{.Names}}' | grep -q 'hive-server2' ; then
	echo "ERROR: Container 'hive-server2' is not running. Start the stack with: docker compose up -d"
	exit 1
fi

echo "--- 2. Beeline connectivity ---"
docker exec -i hive-server2 beeline -u jdbc:hive2://localhost:10000 -e "SHOW DATABASES;"

echo "--- 3. Managed vs External Tables ---"
if ! docker exec -i hive-server2 beeline -u jdbc:hive2://localhost:10000 -f /queries/table_types_comparison.hql; then
	echo "ERROR: table_types_comparison.hql failed" >&2
	exit 1
fi

echo "--- 4. File Formats (CSV, ORC, Parquet) ---"
if ! docker exec -i hive-server2 beeline -u jdbc:hive2://localhost:10000 -f /queries/file_formats_comparison.hql; then
	echo "ERROR: file_formats_comparison.hql failed" >&2
	exit 1
fi

echo "--- Done ---"
echo "Documentation available in: hive/binome1_personne2_documentation.md"
