# Rapport d'Analyse Hive - Personne 6

Ce rapport documente les requêtes analytiques exécutées dans Hive pour extraire des informations commerciales à partir du jeu de données e-commerce Olist.

## 1. Validation des Données
Avant de commencer l'analyse, nous avons vérifié la cohérence des données.
*   **Nombre total de lignes** : 111 708 lignes chargées avec succès dans la table `commandes`.

## 2. Analyses de Base

### Top 5 des Commandes par Montant
Nous avons identifié les transactions les plus importantes pour comprendre les clients à forte valeur.
| id_commande | Montant | Note Client |
| :--- | :--- | :--- |
| 0812eb902a67711a1cb742b3cdaa65ae | 6 735,0 | 5 |
| f5136e38d1a14a4dbd87dff67da82701 | 6 499,0 | 5 |
| a96610ab360d42a2e5335a3998b4718a | 4 799,0 | 5 |
| 199af31afc78c699f0dbf71fb178d4d4 | 4 690,0 | 4 |
| 8dbc85d1447242f3b127dda390d56e19 | 4 590,0 | 5 |

### Répartition par Statut de Commande
La majorité des commandes sont "delivered" (livrées), ce qui indique un flux opérationnel sain.
*   **Livrées (delivered)** : 109 370
*   **Expédiées (shipped)** : 1 099
*   **Annulées (canceled)** : 525

## 3. Analyse Financière

### Chiffre d'Affaires (CA) par Mois (Tendance)
Le chiffre d'affaires affiche une forte tendance à la hausse, culminant en novembre 2017 (période du Black Friday) avec **1 000 640,27**.
*   **Pic** : Nov 2017 (~1M BRL)
*   **Moyenne 2018** : Croissance soutenue autour de 900k-980k BRL par mois.

### Comparaison Annuelle (2017 vs 2018)
L'activité a progressé de manière significative en un an :
*   **2017** : 50 386 commandes | 6 092 921,02 BRL
*   **2018** : 60 958 commandes | 7 325 034,51 BRL
*   **Croissance** : Augmentation d'environ 20% des revenus.

## 4. Aperçu des Produits

### Top 10 des Produits les plus vendus
| ID Produit | Quantité Vendue |
| :--- | :--- |
| 422879e10f46682990de24d770e7f83d | 792 |
| aca2eb7d00ea1a7b8ebd4e68314663af | 636 |
| 368c6c730842d78016ad823897a372db | 547 |

## 5. Résumé des Requêtes SQL utilisées
1.  **Agrégations** : `SUM(montant_total)`, `COUNT(*)`
2.  **Traitement des dates** : `substr(date_commande, 1, 7)` pour le groupement mensuel.
3.  **Filtrage** : `WHERE annee IN ('2017', '2018')`
4.  **Tri** : `ORDER BY total_vendu DESC`
