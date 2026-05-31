#!/usr/bin/env bash
# hdfs-init.sh — Initialisation de l'arborescence HDFS pour Hive
# Usage : bash docker/hdfs-init.sh

set -e

echo "=========================================="
echo " Initialisation arborescence HDFS"
echo "=========================================="

echo "[1/3] Attente du NameNode..."
until curl -sf http://localhost:9870 > /dev/null 2>&1; do
  echo "  → attente 5s..."; sleep 5
done
echo "  ✓ NameNode disponible"

echo "[2/3] Création des répertoires HDFS..."
docker exec namenode bash -c "
  hdfs dfs -mkdir -p /user/hive/warehouse &&
  hdfs dfs -mkdir -p /user/hive/data &&
  hdfs dfs -mkdir -p /user/hive/data/commandes &&
  hdfs dfs -mkdir -p /tmp/hive &&
  hdfs dfs -chmod -R 777 /tmp &&
  hdfs dfs -chmod -R 775 /user/hive &&
  hdfs dfs -chown -R root /user/hive
"
echo "  ✓ Répertoires créés"

echo "[3/3] Vérification..."
docker exec namenode bash -c "hdfs dfs -ls -R /user/hive/"

echo ""
echo " ✅ Arborescence HDFS initialisée"
echo "=========================================="
