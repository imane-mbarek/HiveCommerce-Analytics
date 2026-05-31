# HiveCommerce Dashboard

Minimal Streamlit dashboard for HiveCommerce analytics.

Prerequisites
- Python 3.9+
- Create and activate a virtual environment (recommended)
- Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app

```bash
streamlit run dashboard/app.py
```

Features
- Sidebar filters: `Villes`, `Catégories`, période
- KPIs: chiffre d'affaires, nombre de commandes, panier moyen
- Interactive charts: CA par catégorie (barres), évolution temporelle (ligne) via Plotly
- Export: boutons pour exporter les graphiques en PNG dans `dashboard/charts/` (utilise `kaleido`)
- Prediction panel: estimation du montant d'une commande par `city`, `category` et `date` (modèle RandomForest)

Model
- If `dashboard/models/sales_model.pkl` is missing, the app will train a RandomForest model from `dashboard/data/sales.csv` on first run.

Troubleshooting
- If image export fails, ensure `kaleido` is installed: `pip install -U kaleido`.
