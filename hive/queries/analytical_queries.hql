-- hive/queries/analytical_queries.hql

-- USE ecommerce_db;

-- 1. Chiffre d'Affaires par Mois
-- Objectif : Analyser la tendance temporelle de l'activité
SELECT 
    substr(date_commande, 1, 7) as mois, 
    ROUND(SUM(montant_total), 2) as CA 
FROM commandes 
GROUP BY substr(date_commande, 1, 7) 
ORDER BY mois;

-- 2. Top 10 des Produits les plus vendus
-- Objectif : Identifier les best-sellers
SELECT 
    id_produit, 
    SUM(quantite) as total_vendu 
FROM commandes 
GROUP BY id_produit 
ORDER BY total_vendu DESC 
LIMIT 10;

-- 3. Comparaison Annuelle (Croissance)
-- Objectif : Mesurer la croissance du CA entre 2017 et 2018
SELECT 
    substr(date_commande, 1, 4) as annee, 
    COUNT(*) as total_commandes,
    ROUND(SUM(montant_total), 2) as CA_annuel
FROM commandes 
WHERE substr(date_commande, 1, 4) IN ('2017', '2018')
GROUP BY substr(date_commande, 1, 4);

-- 4. Analyse de la satisfaction (Note moyenne par statut)
-- Objectif : Vérifier si les délais de livraison impactent les notes
SELECT 
    statut, 
    ROUND(AVG(note_client), 2) as note_moyenne 
FROM commandes 
GROUP BY statut;
