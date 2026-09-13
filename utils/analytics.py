import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency
from utils.styling import register_page

def treatment_rate(data):
    if data.empty:
        return 0.0
    return data["treatment"].eq("Yes").mean() * 100

def grouped_treatment_rate(data, column):
    if data.empty or column not in data.columns:
        return pd.DataFrame(columns=[column, "Respondents", "Treated", "Treatment Rate"])

    result = (
        data.groupby(column, dropna=False)
        .agg(
            Respondents=("treatment", "size"),
            Treated=("treatment", lambda x: (x == "Yes").sum()),
        )
        .reset_index()
    )
    result["Treatment Rate"] = (result["Treated"] / result["Respondents"] * 100).round(2)
    return result

def cramers_v(data, feature, target="treatment"):
    if feature not in data.columns or target not in data.columns:
        return np.nan, np.nan

    subset = data[[feature, target]].dropna()

    if subset.empty or subset[feature].nunique() < 2 or subset[target].nunique() < 2:
        return np.nan, np.nan

    table = pd.crosstab(subset[feature], subset[target])
    if table.shape[0] < 2 or table.shape[1] < 2:
        return np.nan, np.nan

    chi2, p_value, _, _ = chi2_contingency(table)
    n = table.to_numpy().sum()
    phi2 = chi2 / n
    r, k = table.shape

    phi2corr = max(0, phi2 - ((k - 1) * (r - 1)) / max(n - 1, 1))
    rcorr = r - ((r - 1) ** 2) / max(n - 1, 1)
    kcorr = k - ((k - 1) ** 2) / max(n - 1, 1)
    denominator = min(kcorr - 1, rcorr - 1)

    v = np.nan if denominator <= 0 else np.sqrt(phi2corr / denominator)
    return p_value, v

def association_strength(v):
    if pd.isna(v):
        return "Not available"
    if v < .10:
        return "Very small"
    if v < .20:
        return "Small"
    if v < .30:
        return "Moderate"
    if v < .50:
        return "Large"
    return "Strong"

def apply_filters(data, country, gender, age_group, company_size,
                  work_arrangement, treatment_status, family_history):
    filtered = data.copy()
    filters = {
        "Country": country,
        "Gender": gender,
        "Age_Group": age_group,
        "Company_Size_Group": company_size,
        "Remote_Work_Status": work_arrangement,
        "Treatment_Status": treatment_status,
        "Mental_Health_History": family_history,
    }

    for column, selected in filters.items():
        if selected and column in filtered.columns:
            filtered = filtered[filtered[column].isin(selected)]

    return filtered

def render_sidebar_filters(data):
    import streamlit as st

    st.sidebar.markdown("## 🎯 Filters")

    country = st.sidebar.multiselect(
        "Country", sorted(data["Country"].dropna().unique()), key="filter_country"
    )
    gender = st.sidebar.multiselect(
        "Gender", sorted(data["Gender"].dropna().unique()), key="filter_gender"
    )
    age_group = st.sidebar.multiselect(
        "Age Group", list(data["Age_Group"].dropna().unique()), key="filter_age_group"
    )
    company_size = st.sidebar.multiselect(
        "Company Size", list(data["Company_Size_Group"].dropna().unique()), key="filter_company_size"
    )
    work_arrangement = st.sidebar.multiselect(
        "Work Arrangement", sorted(data["Remote_Work_Status"].dropna().unique()),
        key="filter_work_arrangement"
    )
    treatment_status = st.sidebar.multiselect(
        "Treatment Status", sorted(data["Treatment_Status"].dropna().unique()),
        key="filter_treatment_status"
    )
    family_history = st.sidebar.multiselect(
        "Family History", sorted(data["Mental_Health_History"].dropna().unique()),
        key="filter_family_history"
    )

    filtered = apply_filters(
        data, country, gender, age_group, company_size,
        work_arrangement, treatment_status, family_history
    )

    st.sidebar.divider()
    st.sidebar.metric("Filtered Respondents", f"{len(filtered):,}")
    return filtered
