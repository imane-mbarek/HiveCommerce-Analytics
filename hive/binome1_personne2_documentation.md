# Documentation : Section 4.1 — Partie 2

## Synthèse des Tests Pratiques Hive (Personne 2)

### 1. Validation de la Connectivité Beeline
La connexion à HiveServer2 a été validée avec succès via la CLI Beeline en utilisant l'URL JDBC : `jdbc:hive2://localhost:10000`. Cette étape confirme que le service HiveServer2 est opérationnel et capable de traiter les requêtes entrantes.

### 2. Typologies de Tables : Managed vs External
Les tests ont mis en évidence une différence fondamentale dans la gestion du cycle de vie des données :
- **Managed Table (`managed_sales`)** : Hive gère à la fois les métadonnées et les données physiques. Lors d'un `DROP TABLE`, les deux sont supprimés du HDFS.
- **External Table (`external_sales`)** : Hive ne gère que les métadonnées. Lors d'un `DROP TABLE`, les métadonnées sont supprimées mais les données physiques restent intactes dans le dossier HDFS spécifié (`LOCATION`). 
*Usage recommandé :* Utiliser des tables externes pour les données partagées entre plusieurs outils ou pour éviter les suppressions accidentelles.

### 3. Formats de Fichiers : ORC vs Parquet vs CSV
L'évaluation des formats a montré les bénéfices suivants :
- **CSV (TEXTFILE)** : Format lisible mais volumineux et lent pour les requêtes analytiques complexes.
- **ORC (Optimized Row Columnar)** : Excellente compression et optimisation pour Hive. Idéal pour les lectures intensives.
- **Parquet** : Format colonnaire très performant, particulièrement efficace pour les intégrations avec l'écosystème Spark.

**Conclusion :** Pour ce projet, nous privilégierons le format **ORC** pour les tables internes Hive afin d'optimiser le stockage et les temps de réponse des requêtes analytiques.

### Exécution automatisée des tests
Les scripts d'automatisation ont été ajoutés pour exécuter les vérifications depuis la racine du dépôt.

- Script PowerShell (Windows, tente de démarrer Docker Desktop si nécessaire) :

	powershell -ExecutionPolicy Bypass -File .\scripts\run_hive_tests_personne2.ps1

- Script Bash (Linux / WSL) :

	./scripts/run_hive_tests_personne2.sh

Prérequis :
- Docker Desktop installé et accès au démon `docker`.
- Le conteneur `hive-server2` lancé via `docker compose up -d` (depuis `docker-compose.yml`).

Si Docker Desktop ne démarre pas automatiquement, ouvre l'application Docker Desktop et attends que l'interface indique "Docker Desktop is running", puis relance le script PowerShell ci-dessus.

Les scripts exécutent dans l'ordre : connexion Beeline, création/validation de `MANAGED` et `EXTERNAL` tables (fichier [hive/queries/table_types_comparison.hql](hive/queries/table_types_comparison.hql)), puis création et comparaison des tables en `ORC` et `PARQUET` (fichier [hive/queries/file_formats_comparison.hql](hive/queries/file_formats_comparison.hql)).

Pour toute erreur, copier/coller la sortie du terminal et la partager dans l'issue ou avec l'équipe pour diagnostic.
