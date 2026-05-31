# Binôme 2 — P3 : Infrastructure Hive

> **Rôle** : Déploiement complet de l'infrastructure via conteneurs Docker.

## Architecture déployée

```
NameNode (HDFS)
├── DataNode 1
├── DataNode 2
└── DataNode 3

PostgreSQL (Metastore DB)
Hive Metastore  → connecté à PostgreSQL
HiveServer2     → connecté au Metastore
```

## Structure du projet

```
p3/
├── docker-compose.yml           ← Orchestration complète des services
├── hadoop.env                   ← Variables Hadoop partagées
├── docker/
│   ├── hdfs-init.sh             ← Initialisation arborescence HDFS
│   └── metastore-init.sh        ← Initialisation schéma PostgreSQL
├── scripts/
│   ├── start.py                 ← Script de démarrage automatique
│   └── preprocessing_dataset.py ← Nettoyage du dataset
├── data/                        ← Dossier pour les fichiers CSV source
├── hive/                        ← Requêtes HiveQL (Binôme 3)
├── python/                      ← Scripts Python (Trinôme)
├── dashboard/                   ← Application Streamlit (Trinôme)
└── requirements.txt             ← Dépendances Python
```

## Démarrage

### Prérequis
- Docker Desktop lancé
- Python 3.8+

### Tout en une commande

```bash
python scripts/start.py
```

Le script déploie automatiquement :
1. Lance tous les conteneurs Docker
2. Attend que chaque service soit healthy
3. Initialise l'arborescence HDFS
4. Initialise le schéma Metastore dans PostgreSQL
5. Affiche la vérification finale

### Interfaces web

| Service        | URL                         |
|----------------|-----------------------------|
| NameNode HDFS  | http://localhost:9870        |
| HiveServer2    | http://localhost:10002       |
| PostgreSQL     | localhost:5432               |

### Connexion Beeline

```bash
docker exec -it hive-server beeline -u "jdbc:hive2://localhost:10000"
```

### Arrêt

```bash
docker-compose down
# Pour supprimer les volumes aussi :
docker-compose down -v
```

## Ports exposés

| Port  | Service              |
|-------|----------------------|
| 9870  | NameNode Web UI      |
| 9000  | HDFS RPC             |
| 5432  | PostgreSQL           |
| 9083  | Hive Metastore       |
| 10000 | HiveServer2 JDBC     |
| 10002 | HiveServer2 Web UI   |
