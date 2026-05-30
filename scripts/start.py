# scripts/start.py
# Lance avec : python scripts/start.py
# Fait tout automatiquement à chaque redémarrage Docker

import subprocess
import time
import os
# Se placer dans le bon dossier

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run(cmd):
    print(f">>> {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout: print(result.stdout[-300:])
    return result

print("=== 1. Démarrage Docker ===")
run("docker-compose up -d")
print("Attente 60s...")
time.sleep(60)

print("=== 2. Init Metastore Hive ===")
run('docker exec hive-server bash -c "rm -rf /opt/hive/data/metastore_db && schematool -dbType derby -initSchema"')
time.sleep(10)

print("=== 3. Upload CSV vers HDFS ===")
run("docker cp data\\commandes_ecommerce.csv namenode:/tmp/commandes_ecommerce.csv")
run('docker exec namenode bash -c "hdfs dfs -mkdir -p /user/hive/data/commandes && hdfs dfs -put -f /tmp/commandes_ecommerce.csv /user/hive/data/commandes/"')

print("=== 4. Création table Hive ===")
run("""docker exec hive-server hive -e "CREATE DATABASE IF NOT EXISTS ecommerce_db; USE ecommerce_db; CREATE EXTERNAL TABLE IF NOT EXISTS commandes (id_commande STRING, id_client STRING, id_produit STRING, date_commande STRING, quantite INT, montant_total DOUBLE, statut STRING, note_client INT) ROW FORMAT DELIMITED FIELDS TERMINATED BY ',' STORED AS TEXTFILE LOCATION '/user/hive/data/commandes/' TBLPROPERTIES ('skip.header.line.count'='1');" """)

print("=== 5. Vérification ===")
run('docker exec hive-server hive -S -e "USE ecommerce_db; SELECT COUNT(*) FROM commandes;"')

print("\n✅ Tout est prêt ! Lance : python manage.py runserver")