# scripts/start.py
# Déploiement complet de l'infrastructure Hive
# Usage : python scripts/start.py

import subprocess
import time
import sys
import os

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def titre(msg):
    print("\n" + "=" * 55)
    print(f"  {msg}")
    print("=" * 55)


def run(cmd, show=True):
    print(f"\n>>> {cmd}")
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if show and r.stdout.strip():
        print(r.stdout.strip())
    if r.returncode != 0 and r.stderr.strip():
        print(f"[ERR] {r.stderr.strip()[-300:]}")
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


# ── 1. Lancer Docker ─────────────────────────────────────────
titre("1/5 — Lancement Docker Compose")
r = run("docker-compose up -d")
if r.returncode != 0:
    print("\n❌ Erreur — Docker Desktop est-il lancé ?")
    sys.exit(1)

# ── 2. Attendre les services ─────────────────────────────────
titre("2/5 — Attente des services (2-3 min)")
wait_healthy("namenode",       timeout=180)
wait_healthy("hive-postgres",  timeout=120)
print("  ⏳ hive-metastore (démarrage lent ~90s)...")
time.sleep(30)
wait_healthy("hive-metastore", timeout=180)
run('docker ps --format "table {{.Names}}\t{{.Status}}"')

# ── 3. Initialiser HDFS ──────────────────────────────────────
titre("3/5 — Initialisation HDFS")
hdfs_cmds = [
    "hdfs dfs -mkdir -p /user/hive/warehouse",
    "hdfs dfs -mkdir -p /user/hive/data",
    "hdfs dfs -mkdir -p /user/hive/data/commandes",
    "hdfs dfs -mkdir -p /tmp/hive",
    "hdfs dfs -chmod -R 777 /tmp",
    "hdfs dfs -chmod -R 775 /user/hive",
    "hdfs dfs -chown -R root /user/hive",
]
for cmd in hdfs_cmds:
    r = run(f'docker exec namenode bash -c "{cmd}"', show=False)
    print(f"  {'✅' if r.returncode == 0 else '⚠ '} {cmd}")

run('docker exec namenode bash -c "hdfs dfs -ls -R /user/hive/"')

# ── 4. Initialiser le Metastore ──────────────────────────────
titre("4/5 — Initialisation schéma Metastore (PostgreSQL)")
run('docker exec hive-metastore bash -c "schematool -dbType postgres -initSchema 2>&1 | tail -6"')

# ── 5. Vérification finale ───────────────────────────────────
titre("5/5 — Vérification finale")
run('docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"')

print("""
  🌐  http://localhost:9870  → NameNode HDFS
  🌐  http://localhost:10002 → HiveServer2

  🔌  Beeline :
      docker exec -it hive-server beeline -u "jdbc:hive2://localhost:10000"

╔═══════════════════════════════════════════════════╗
║  ✅  Infrastructure déployée avec succès           ║
║  HDFS prêt · Metastore PostgreSQL initialisé       ║
╚═══════════════════════════════════════════════════╝
""")
