import pandas as pd
import os
from datetime import datetime


os.makedirs("logs", exist_ok=True)
os.makedirs("results", exist_ok=True)

orders = pd.read_csv("data/olist_orders_dataset.csv")
items = pd.read_csv("data/olist_order_items_dataset.csv")
reviews = pd.read_csv("data/olist_order_reviews_dataset.csv")
ecommerce = pd.read_csv("data/commandes_ecommerce.csv")

print("✔ Datasets chargés")


def analyze(name, df):
    print(f"\n===== {name} =====")
    print("Shape:", df.shape)
    print("Types:\n", df.dtypes)
    print("Describe:\n", df.describe(include="all"))

analyze("ORDERS", orders)
analyze("ITEMS", items)
analyze("REVIEWS", reviews)
analyze("ECOMMERCE", ecommerce)


log_path = "logs/initial_state.txt"

with open(log_path, "w", encoding="utf-8") as f:
    f.write("=== DATA INGESTION LOG ===\n")
    f.write(f"Date: {datetime.now()}\n\n")

    datasets = {
        "orders": orders,
        "items": items,
        "reviews": reviews,
        "ecommerce": ecommerce
    }

    for name, df in datasets.items():
        f.write(f"\n--- {name.upper()} ---\n")
        f.write(f"Shape: {df.shape}\n")
        f.write(str(df.dtypes))
        f.write("\n")

print("✔ Logs sauvegardés")



# Fusion orders + items
df = orders.merge(items, on="order_id", how="inner")


price_col = None
for col in ["price", "item_price", "payment_value"]:
    if col in df.columns:
        price_col = col
        break

if price_col:
    result = df.groupby("product_id")[price_col].sum().reset_index()
    result.columns = ["product_id", "ca_total"]

    result.to_csv("results/ca_products.csv", index=False)
    print("✔ CA par produit exporté")
else:
    df.head().to_csv("results/sample.csv", index=False)
    print("✔ Export sample créé")


try:
    from pyhive import hive

    conn = hive.Connection(
        host="localhost",
        port=10000,
        username="hive"
    )

    print("✔ Connexion Hive OK")

except Exception:
    conn = None
    print("⚠ Hive non disponible → mode local activé")
except Exception as e:
    print("⚠ Hive non connecté (normal si pas configuré)")
    print(e)

print("✔ INGESTION TERMINÉE")