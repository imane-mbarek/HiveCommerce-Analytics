# Binôme 2 — P4 : Déploiement & Tests

> **Rôle** : Lancer la stack déployée par P3, analyser les journaux d'exécution, valider les connexions Beeline et Python.

## Ce que fait P4 par rapport à P3

P4 reprend l'infrastructure complète de P3 et ajoute la couche de **tests et validation** :

| Étape | P3 (Infrastructure) | P4 (Tests) |
|-------|----------------------|------------|
| docker-compose.yml | ✅ Rédigé | Identique |
| HDFS init | ✅ Rédigé | Identique |
| Metastore init | ✅ Rédigé | Identique |
| Démarrage automatique | `start.py` 5 étapes | `start.py` 6 étapes (+ports, logs, Beeline, PyHive) |
| Test connexion Python | — | `test_hive_connection.py` |
| Logs horodatés | — | `logs/deploy_YYYYMMDD_HHMMSS.log` |

## Structure du projet

```
p4/
├── docker-compose.yml               ← Identique à P3
├── hadoop.env                       ← Identique à P3
├── docker/
│   ├── hdfs-init.sh                 ← Identique à P3
│   └── metastore-init.sh            ← Identique à P3
├── scripts/
│   ├── start.py                     ← Déploiement + tests automatiques
│   ├── test_hive_connection.py      ← Test connexion PyHive standalone
│   └── preprocessing_dataset.py    ← Nettoyage du dataset
├── logs/                            ← Logs de déploiement horodatés
├── data/                            ← Dossier pour les CSV source
├── hive/                            ← Requêtes HiveQL (Binôme 3)
├── python/                          ← Scripts Python (Trinôme)
├── dashboard/                       ← Application Streamlit (Trinôme)
└── requirements.txt                 ← Dépendances Python
```

## Démarrage

### Prérequis
- Docker Desktop lancé
- Python 3.8+

### Tout en une commande (déploiement + tests)

```bash
python scripts/start.py
```

Le script exécute automatiquement 6 étapes :
1. Lance tous les conteneurs Docker
2. Attend que chaque service soit healthy
3. Vérifie l'accessibilité de chaque port
4. Analyse les 10 dernières lignes de logs de chaque conteneur
5. Teste la connexion Beeline (SHOW DATABASES)
6. Teste la connexion Python PyHive

Un log complet horodaté est sauvegardé dans `logs/`.

## Tester la connexion Python

```bash
# Pré-requis
pip install pyhive thrift pandas

# Test
python scripts/test_hive_connection.py
```

Le test valide 5 points : connexion, SHOW DATABASES, CREATE DATABASE, SHOW TABLES, SELECT.

## Interfaces web

| Service        | URL                         |
|----------------|-----------------------------|
| NameNode HDFS  | http://localhost:9870        |
| HiveServer2    | http://localhost:10002       |

## Connexion Beeline

```bash
docker exec -it hive-server beeline -u "jdbc:hive2://localhost:10000"
```

## Arrêt

```bash
docker-compose down
# Pour supprimer les volumes aussi :
docker-compose down -v
```
