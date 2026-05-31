#!/usr/bin/env bash
# metastore-init.sh — Initialisation du schéma Hive Metastore dans PostgreSQL
# Usage : bash docker/metastore-init.sh

set -e

echo "=========================================="
echo " Initialisation Hive Metastore (PostgreSQL)"
echo "=========================================="

echo "[1/2] Attente de PostgreSQL..."
until docker exec hive-postgres pg_isready -U hive -d metastore_db > /dev/null 2>&1; do
  echo "  → attente 5s..."; sleep 5
done
echo "  ✓ PostgreSQL disponible"

echo "[2/2] Initialisation du schéma Metastore..."
docker exec hive-metastore bash -c "
  schematool -dbType postgres -initSchema 2>&1 | tail -10
"

echo ""
echo " ✅ Schéma Metastore initialisé dans PostgreSQL"
echo "=========================================="
