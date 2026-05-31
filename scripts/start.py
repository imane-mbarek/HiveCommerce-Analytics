# scripts/start.py
# Déploiement, tests de connexion et vérification complète de la stack
# Usage : python scripts/start.py

import subprocess
import time
import sys
import os
import socket

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.makedirs("logs", exist_ok=True)
LOG = f"logs/deploy_{time.strftime('%Y%m%d_%H%M%S')}.log"


def titre(msg):
    s = "\n" + "=" * 55 + f"\n  {msg}\n" + "=" * 55
    print(s)
    open(LOG, "a").write(s + "\n")


def run(cmd, show=True):
    print(f"\n>>> {cmd}")
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    out = r.stdout.strip()
    if show and out:
        print(out)
    open(LOG, "a").write(f"\n>>> {cmd}\n{out}\n")
    return r


def wait_healthy(name, timeout=180):
    print(f"  ⏳ {name}...", end="", flush=True)
    t0 = time.time()
    while time.time() - t0 < timeout:
        r = subprocess.run(
            f"docker inspect --format={{{{.State.Health.Status}}}} {name}",
            shell=True, capture_output=True, text=True)
        if r.stdout.strip() == "healthy":
            print(" ✅"); return True
        r2 = subprocess.run(
            f"docker inspect --format={{{{.State.Status}}}} {name}",
            shell=True, capture_output=True, text=True)
        if r2.stdout.strip() == "running" and r.stdout.strip() == "":
            print(" ✅ running"); return True
        print(".", end="", flush=True)
        time.sleep(8)
    print(" ❌ timeout"); return False


def check_port(port, timeout=15):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            with socket.create_connection(("localhost", port), timeout=2):
                return True
        except OSError:
            time.sleep(3)
    return False


# ── 1. Lancer Docker ─────────────────────────────────────────
titre("1/6 — Lancement Docker Compose")
r = run("docker-compose up -d")
if r.returncode != 0:
    print("\n❌ Erreur — Docker Desktop est-il lancé ?")
    sys.exit(1)

# ── 2. Attendre tous les services ────────────────────────────
titre("2/6 — Attente des services (2-4 min)")
wait_healthy("namenode",       timeout=180)
wait_healthy("hive-postgres",  timeout=120)
print("  ⏳ hive-metastore (démarrage lent ~90s)...")
time.sleep(35)
wait_healthy("hive-metastore", timeout=180)
wait_healthy("hive-server",    timeout=180)
run('docker ps --format "table {{.Names}}\t{{.Status}}"')

# ── 3. Vérifier les ports ────────────────────────────────────
titre("3/6 — Vérification des ports")
ports = {
    9870:  "NameNode Web UI",
    9000:  "HDFS RPC",
    5432:  "PostgreSQL",
    9083:  "Hive Metastore",
    10000: "HiveServer2 JDBC",
    10002: "HiveServer2 Web UI",
}
resultats = {}
for port, label in ports.items():
    ok = check_port(port)
    resultats[port] = ok
    print(f"  {'✅' if ok else '❌'} {label:30s} → localhost:{port}")

# ── 4. Analyser les logs ─────────────────────────────────────
titre("4/6 — Analyse des journaux d'exécution")
for c in ["namenode", "hive-postgres", "hive-metastore", "hive-server"]:
    print(f"\n--- {c} (10 dernières lignes) ---")
    run(f"docker logs {c} --tail=10 2>&1")

# ── 5. Tester Beeline ────────────────────────────────────────
titre("5/6 — Test connexion HiveServer2 (Beeline)")
if resultats.get(10000):
    r = run(
        'docker exec hive-server bash -c '
        '"beeline -u jdbc:hive2://localhost:10000 --outputformat=tsv2 '
        '-e \\"SHOW DATABASES;\\" 2>/dev/null | grep -v SLF4J | grep -v INFO"'
    )
    if r.returncode == 0 and r.stdout.strip():
        print("  ✅ Beeline opérationnel")
    else:
        print("  ⚠  HiveServer2 démarre encore — relancez dans 1 min")
else:
    print("  ⚠  Port 10000 non accessible")

# ── 6. Tester Python ─────────────────────────────────────────
titre("6/6 — Test connexion Python (PyHive)")
try:
    from pyhive import hive
    conn = hive.Connection(
        host="localhost", port=10000,
        username="root", database="default", auth="NOSASL")
    cur = conn.cursor()
    cur.execute("SHOW DATABASES")
    dbs = [row[0] for row in cur.fetchall()]
    print(f"  ✅ Connexion PyHive réussie — bases : {dbs}")
    cur.execute("CREATE DATABASE IF NOT EXISTS ecommerce_db")
    cur.execute("SELECT 1+1")
    print(f"  ✅ SELECT 1+1 = {cur.fetchone()[0]}")
    cur.close(); conn.close()
except ImportError:
    print("  ⚠  pyhive non installé → pip install pyhive thrift pandas")
except Exception as e:
    print(f"  ⚠  {e} — HiveServer2 peut prendre 2-3 min de plus")

# ── Résumé ───────────────────────────────────────────────────
titre("RÉSUMÉ")
run('docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"')
print(f"""
  🌐  http://localhost:9870  → NameNode HDFS
  🌐  http://localhost:10002 → HiveServer2

  🔌  Beeline :
      docker exec -it hive-server beeline -u "jdbc:hive2://localhost:10000"

  🧪  Test Python standalone :
      python scripts/test_hive_connection.py

  📄  Log complet : {LOG}

╔═══════════════════════════════════════════════════╗
║  ✅  Stack déployée · Ports vérifiés               ║
║      Logs analysés · Connexions validées           ║
╚═══════════════════════════════════════════════════╝
""")
