import os
from pathlib import Path
import uuid

import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
from datetime import date as _date
import importlib
import importlib.util


BASE_DIR = Path(__file__).parent
CHARTS_DIR = BASE_DIR / "charts"
CHARTS_DIR.mkdir(exist_ok=True)

# dynamic load model module (works whether running as script or package)
try:
    model_module = importlib.import_module("dashboard.model")
except Exception:
    spec = importlib.util.spec_from_file_location("dashboard_model", str(BASE_DIR / "model.py"))
    model_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(model_module)


def load_data() -> pd.DataFrame:
    data_path = BASE_DIR / "data" / "sales.csv"
    if data_path.exists():
        df = pd.read_csv(data_path, parse_dates=["date"]) if "date" in open(data_path).read() else pd.read_csv(data_path)
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"])
        return df

    # Generate synthetic sample data
    np.random.seed(42)
    n_days = 180
    dates = pd.date_range(end=pd.Timestamp.today(), periods=n_days)
    cities = ["Paris", "Lyon", "Marseille", "Toulouse", "Nice"]
    categories = ["Électronique", "Vêtements", "Maison", "Beauté"]

    rows = []
    order_counter = 1
    for d in dates:
        for _ in range(np.random.randint(5, 15)):
            rows.append(
                {
                    "date": d,
                    "city": np.random.choice(cities),
                    "category": np.random.choice(categories),
                    "sales": round(np.random.exponential(80) + 10, 2),
                    "order_id": order_counter,
                }
            )
            order_counter += 1

    df = pd.DataFrame(rows)
    return df


def main():
    st.set_page_config(page_title="HiveCommerce Dashboard", layout="wide")
    st.title("HiveCommerce — Dashboard Streamlit")

    df = load_data()

    # Sidebar filters
    st.sidebar.header("Filtres")
    cities = sorted(df["city"].unique())
    categories = sorted(df["category"].unique())

    selected_cities = st.sidebar.multiselect("Villes", cities, default=cities)
    selected_categories = st.sidebar.multiselect("Catégories", categories, default=categories)

    min_date = df["date"].min().date()
    max_date = df["date"].max().date()
    start_date, end_date = st.sidebar.date_input("Période", value=(min_date, max_date))

    # Apply filters
    mask = (
        df["city"].isin(selected_cities)
        & df["category"].isin(selected_categories)
        & (df["date"].dt.date >= start_date)
        & (df["date"].dt.date <= end_date)
    )
    dff = df.loc[mask].copy()

    # KPIs
    total_sales = dff["sales"].sum()
    total_orders = dff["order_id"].nunique()
    avg_order = dff["sales"].mean() if total_orders > 0 else 0

    kpi1, kpi2, kpi3 = st.columns([1, 1, 1])
    kpi1.metric(label="Chiffre d'affaires", value=f"€ {total_sales:,.2f}")
    kpi2.metric(label="Nombre de commandes", value=f"{int(total_orders):,}")
    kpi3.metric(label="Panier moyen", value=f"€ {avg_order:,.2f}")

    # Charts
    st.subheader("CA par catégorie")
    ca_cat = (
        dff.groupby("category", as_index=False)["sales"].sum().sort_values("sales", ascending=False)
    )
    fig_cat = px.bar(ca_cat, x="category", y="sales", labels={"sales": "CA", "category": "Catégorie"}, text_auto=True)
    fig_cat.update_layout(margin=dict(t=30, b=10))
    st.plotly_chart(fig_cat, use_container_width=True)

    st.subheader("Évolution temporelle du CA")
    ca_time = dff.groupby(pd.Grouper(key="date", freq="D"))["sales"].sum().reset_index()
    fig_time = px.line(ca_time, x="date", y="sales", labels={"sales": "CA", "date": "Date"}, markers=True)
    fig_time.update_layout(margin=dict(t=30, b=10))
    st.plotly_chart(fig_time, use_container_width=True)

    # Export options
    st.sidebar.header("Export")
    auto_export = st.sidebar.checkbox("Exporter automatiquement les graphiques en PNG", value=False)
    if st.sidebar.button("Exporter manuellement les graphiques" ):
        exported = export_charts(fig_cat, fig_time)
        if exported:
            st.sidebar.success("Graphiques exportés dans dashboard/charts/")

    if auto_export:
        export_charts(fig_cat, fig_time)

    # Prediction panel
    st.sidebar.header("Prédiction de vente (par commande)")
    try:
        payload = model_module.load_or_train(df)
        pred_city = st.sidebar.selectbox("Ville (prédiction)", cities, index=0)
        pred_category = st.sidebar.selectbox("Catégorie (prédiction)", categories, index=0)
        pred_date = st.sidebar.date_input("Date (prédiction)", value=_date.today())
        if st.sidebar.button("Estimer le montant de la commande"):
            pred = model_module.predict(payload, pred_city, pred_category, pred_date)
            st.sidebar.success(f"Montant estimé: € {pred:,.2f}")
    except Exception as e:
        st.sidebar.error(f"Modèle indisponible: {e}")


def export_charts(fig_cat, fig_time) -> bool:
    try:
        out1 = CHARTS_DIR / "ca_cat.png"
        out2 = CHARTS_DIR / "ca_time.png"
        # Use plotly.kaleido (kaleido must be installed)
        fig_cat.write_image(str(out1), engine="kaleido", format="png", scale=2)
        fig_time.write_image(str(out2), engine="kaleido", format="png", scale=2)
        return True
    except Exception as e:
        st.sidebar.error(f"Échec export: {e}")
        return False


if __name__ == "__main__":
    main()
