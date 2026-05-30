import pandas as pd
import os
# =================== ÉTAPE 1 : Charger les 2 fichiers CSV ===================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

orders  = pd.read_csv(os.path.join(DATA_DIR, "olist_orders_dataset.csv"))
items   = pd.read_csv(os.path.join(DATA_DIR, "olist_order_items_dataset.csv"))
reviews = pd.read_csv(os.path.join(DATA_DIR, "olist_order_reviews_dataset.csv"))

print(f"Orders : {len(orders)} lignes")
print(f"Items  : {len(items)} lignes")
print(f"reviews  : {len(reviews)} lignes")

# -=================== Fusionner les 2 fichiers sur order_id ===================
df = pd.merge(
    items,
    orders[["order_id", "customer_id",
            "order_status", "order_purchase_timestamp"]],
    on="order_id", how = "inner"
)
reviews_clean = reviews[["order_id", "review_score"]].drop_duplicates(subset="order_id", keep="last")  
df = pd.merge(df, reviews_clean, on="order_id", how="left")                                            
print(f"Après fusion : {len(df)} lignes")

# =================== ÉTAPE 3 : Renommer les colonnes ===================
df = df.rename(columns={
    "order_id"                 : "id_commande",
    "customer_id"              : "id_client",
    "product_id"               : "id_produit",
    "order_purchase_timestamp" : "date_commande",
    "order_item_id"            : "quantite",
    "price"                    : "montant_total",
    "order_status"             : "statut",
    "review_score"             : "note_client"
})
# =================== ÉTAPE 4 : Garder uniquement les colonnes utiles ===================
df = df[["id_commande", "id_client", "id_produit",
        "date_commande", "quantite", "montant_total", "statut", "note_client"]]

# =================== ÉTAPE 5 : Nettoyage ===================
avant = len(df)
df = df.dropna()
print("apres la supression des valeurs manquantes : \n")
print(df.info())
avant = len(df)
df = df.drop_duplicates()
print("apres la supression des duplicates : \n")
print(df.info())

# Corriger les types
df["quantite"]     = df["quantite"].astype(int)
df["montant_total"]= df["montant_total"].astype(float)
df["note_client"]  = df["note_client"].astype(int)

# Corriger le format de la date → YYYY-MM-DD
df["date_commande"] = pd.to_datetime(
    df["date_commande"], errors="coerce"
).dt.strftime("%Y-%m-%d")
df = df.dropna(subset=["date_commande"])

# Supprimer valeurs aberrantes
df = df[df["quantite"]     > 0]
df = df[df["montant_total"] > 0]
df = df[df["note_client"].between(1, 5)]

# =================== ÉTAPE 6 : Rapport + Sauvegarde ===================
print("\n=== RAPPORT DE NETTOYAGE ===")
print(df.dtypes)
print(df.describe())
print(f"\n Lignes finales : {len(df)}")

output_path = os.path.join(DATA_DIR, "commandes_ecommerce.csv")
df.to_csv(output_path, index=False)
print(f"✓ Fichier sauvegardé : {output_path}")