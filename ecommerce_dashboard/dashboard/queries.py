# dashboard/queries.py
from .hive_connection import query_hive

def get_top_produits(limit=10):
    """Produits les plus vendus"""
    sql = f"""
        SELECT id_produit,
               SUM(quantite) AS total_vendu,
               SUM(montant_total) AS chiffre_affaires
        FROM commandes
        GROUP BY id_produit
        ORDER BY total_vendu DESC
        LIMIT {limit}
    """
    return query_hive(sql).to_dict('records')

def get_chiffre_affaires():
    """Chiffre d'affaires total"""
    sql = """
        SELECT ROUND(SUM(montant_total), 2) AS ca_total,
               COUNT(*)                     AS nb_commandes,
               ROUND(AVG(montant_total), 2) AS panier_moyen
        FROM commandes
    """
    return query_hive(sql).to_dict('records')[0]

def get_clients_fideles(limit=10):
    """Clients avec le plus de commandes"""
    sql = f"""
        SELECT id_client,
               COUNT(DISTINCT id_commande) AS nb_commandes,
               SUM(montant_total)          AS total_depense
        FROM commandes
        GROUP BY id_client
        ORDER BY nb_commandes DESC
        LIMIT {limit}
    """
    return query_hive(sql).to_dict('records')

def get_ventes_par_mois():
    """Ventes agrégées par mois"""
    sql = """
        SELECT SUBSTR(date_commande, 1, 7) AS mois,
               COUNT(*)                    AS nb_commandes,
               SUM(montant_total)          AS ca_mensuel
        FROM commandes
        GROUP BY SUBSTR(date_commande, 1, 7)
        ORDER BY mois ASC
    """
    return query_hive(sql).to_dict('records')

def get_repartition_statuts():
    """Répartition des statuts de commande"""
    sql = """
        SELECT statut,
               COUNT(*) AS nb
        FROM commandes
        GROUP BY statut
        ORDER BY nb DESC
    """
    return query_hive(sql).to_dict('records')

def get_notes_moyennes():
    """Distribution des notes clients"""
    sql = """
        SELECT note_client,
               COUNT(*) AS nb_avis
        FROM commandes
        WHERE note_client IS NOT NULL
        GROUP BY note_client
        ORDER BY note_client ASC
    """
    return query_hive(sql).to_dict('records')