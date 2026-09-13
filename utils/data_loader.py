from pathlib import Path
import pandas as pd
import streamlit as st

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_DIR / "outputs" / "cleaned_data" / "mental_health_tech_final.csv"

@st.cache_data
def load_data():
    if not DATA_PATH.exists():
        st.error(f"Dataset not found:\n\n{DATA_PATH}")
        st.stop()

    data = pd.read_csv(DATA_PATH)

    if "Timestamp" in data.columns:
        data["Timestamp"] = pd.to_datetime(data["Timestamp"], errors="coerce")

    return data
