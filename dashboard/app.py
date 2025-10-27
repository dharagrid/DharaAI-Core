import streamlit as st
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import rasterio
import numpy as np
import pandas as pd
from PIL import Image
from dhara.config import DIRS
from dhara.ndvi_pipeline import process_ndvi
from dhara.predictor import predict_health
from dhara.feature_store import FEAT_DB
import sqlite3

st.set_page_config(page_title="Dhara.AI Dashboard", layout="wide")

st.title("🌾 Dhara.AI — Precision Agriculture Intelligence")
st.markdown("#### Visualize NDVI, field stats, and AI health predictions")


# === Dhara Branding ===
st.sidebar.image("https://raw.githubusercontent.com/dharagrid/DharaAI-Core/main/dashboard/dhara_logo.png", width=180)
st.sidebar.markdown("**Dhara.AI** — Precision Agriculture Intelligence 🌾")
st.markdown("<hr style='border:1px solid #E0E0E0;'>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#555;font-size:14px;'>© 2025 Dhara.AI — Vijayapura, India</p>", unsafe_allow_html=True)

# === Sidebar ===
st.sidebar.header("Options")
tif_file = st.sidebar.text_input("Enter NDVI GeoTIFF path:", "")
farm_id = st.sidebar.text_input("Farm ID:", "DemoFarm")
scan_date = st.sidebar.text_input("Scan Date (YYYY-MM-DD):", "2025-10-27")

if tif_file:
    try:
        # Display NDVI raster
        with rasterio.open(tif_file) as src:
            ndvi = src.read(1)
        st.subheader("NDVI Visualization")
        st.image(ndvi, caption="NDVI Map", use_column_width=True, clamp=True)

        # Show NDVI stats
        stats = process_ndvi(tif_file, farm_id, scan_date)
        st.subheader("NDVI Summary")
        st.json(stats)

        # Prediction
        st.subheader("AI Health Prediction")
        pred = predict_health(tif_file)
        st.json(pred)

        # Database summary
        with sqlite3.connect(FEAT_DB) as conn:
            df = pd.read_sql_query("SELECT * FROM field_features", conn)
        st.subheader("Feature Store Records")
        st.dataframe(df)

    except Exception as e:
        st.error(f"❌ Error: {e}")
else:
    st.info("Please enter a valid NDVI GeoTIFF path to begin.")


# === Dhara Analytics Panel ===
import matplotlib.pyplot as plt

st.subheader("📊 Dhara.AI Analytics — NDVI Time Series")

try:
    with sqlite3.connect(FEAT_DB) as conn:
        df = pd.read_sql_query("SELECT * FROM field_features ORDER BY scan_date ASC", conn)

    if not df.empty:
        farms = df["farm_id"].unique().tolist()
        selected_farms = st.multiselect("Select farms to compare:", farms, default=farms[:1])

        if selected_farms:
            fig, ax = plt.subplots()
            for farm in selected_farms:
                dsub = df[df["farm_id"] == farm]
                ax.plot(dsub["scan_date"], dsub["mean_ndvi"], marker="o", label=farm)
            ax.set_xlabel("Date")
            ax.set_ylabel("Mean NDVI")
            ax.set_title("NDVI Trend Over Time")
            ax.legend()
            st.pyplot(fig)

        st.metric("Latest Mean NDVI", f"{df['mean_ndvi'].iloc[-1]:.3f}")
        st.metric("Historical Average NDVI", f"{df['mean_ndvi'].mean():.3f}")
    else:
        st.info("No NDVI data found in feature store yet.")
except Exception as e:
    st.error(f"Analytics error: {e}")
