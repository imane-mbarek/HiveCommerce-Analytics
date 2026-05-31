# scripts/test_hive_connection.py
# Validation de la connexion HiveServer2 via PyHive (depuis l'hôte)
# Prérequis : pip install pyhive thrift pandas
# Usage     : python scripts/test_hive_connection.py

import sys

try:
    from pyhive import hive
    import pandas as pd
except ImportError:
    print("❌ Dépendances manquantes : pip install pyhive thrift pandas")
    sys.exit(1)

HOST, PORT = "localhost", 10000

print("=" * 50)
print(" TEST CONNEXION HIVESERVER2")
print("=" * 50)

# Test 1 — Connexion
print("\n[1/5] Connexion...")
try:
    conn = hive.Connection(host=HOST, port=PORT,
                           username="root", database="default", auth="NOSASL")
    cur = conn.cursor()
    print("  ✅ Connexion établie")
except Exception as e:
    print(f"  ❌ {e}")
    print("  Assurez-vous que la stack est lancée : python scripts/start.py")
    sys.exit(1)

# Test 2 — SHOW DATABASES
print("\n[2/5] SHOW DATABASES...")
cur.execute("SHOW DATABASES")
dbs = [r[0] for r in cur.fetchall()]
print(f"  ✅ Bases disponibles : {dbs}")

# Test 3 — Créer ecommerce_db
print("\n[3/5] CREATE DATABASE ecommerce_db...")
cur.execute("CREATE DATABASE IF NOT EXISTS ecommerce_db")
print("  ✅ Base ecommerce_db disponible")

# Test 4 — SHOW TABLES
print("\n[4/5] SHOW TABLES dans ecommerce_db...")
cur.execute("USE ecommerce_db")
cur.execute("SHOW TABLES")
tables = [r[0] for r in cur.fetchall()]
print(f"  ✅ Tables : {tables if tables else '(aucune — normal à ce stade)'}")

# Test 5 — SELECT
print("\n[5/5] SELECT 1+1...")
cur.execute("SELECT 1+1")
print(f"  ✅ Résultat : {cur.fetchone()[0]}")

cur.close()
conn.close()

print(f"""
{"=" * 50}
 ✅ TOUS LES TESTS RÉUSSIS
    HiveServer2 accessible sur {HOST}:{PORT}
{"=" * 50}
""")
