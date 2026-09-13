import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import chi2_contingency

from utils.data_loader import load_data
from utils.styling import (
    apply_global_style,
    page_header,
    section_title,
    plotly_template,
)

st.set_page_config(
    page_title="Statistical Analysis",
    page_icon="📊",
    layout="wide",
)

apply_global_style()

df = load_data()

if df.empty:
    st.error("No data available.")
    st.stop()


# Page-specific styling

st.html(
    """
    <style>

    [data-testid="stSidebarNav"] {
        padding: 0.35rem 0.25rem 0.75rem 0.25rem !important;
    }

    [data-testid="stSidebarNav"] ul {
        gap: 0.25rem !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    [data-testid="stSidebarNav"] li {
        margin: 0 0 0.32rem 0 !important;
        padding: 0 !important;
    }

    [data-testid="stSidebarNav"] li a {
        display: flex !important;
        align-items: center !important;
        width: 100% !important;
        min-height: 44px !important;
        box-sizing: border-box !important;
        padding: 10px 12px !important;
        border-radius: 10px !important;
        border: 1px solid transparent !important;
        background: transparent !important;
        color: #F8FAFC !important;
        text-decoration: none !important;
        font-size: 0.91rem !important;
        font-weight: 750 !important;
        line-height: 1.25 !important;
        transition: background .18s ease, border-color .18s ease,
                    transform .18s ease, box-shadow .18s ease !important;
    }

    [data-testid="stSidebarNav"] li a:hover {
        background: rgba(45, 212, 191, 0.08) !important;
        border-color: rgba(45, 212, 191, 0.32) !important;
        color: #FFFFFF !important;
        transform: translateX(2px) !important;
        box-shadow: 0 4px 12px rgba(15,23,42,.14) !important;
    }

    [data-testid="stSidebarNav"] li a[aria-current="page"] {
        background: rgba(45,212,191,.13) !important;
        border: 1px solid rgba(45,212,191,.38) !important;
        color: #FFFFFF !important;
        box-shadow: inset 3px 0 0 #2DD4BF,
                    0 4px 14px rgba(15,23,42,.16) !important;
    }
    /* Page top clearance */
    .stMainBlockContainer {
        padding-top: 3.5rem !important;
    }

    [data-testid="stAppViewContainer"] .main .block-container {
        padding-top: 3.5rem !important;
    }

    .main .block-container {
        padding-top: 3.5rem !important;
    }

    .stat-hero {
        position: static !important;
        margin-top: 0 !important;
        padding: 0.35rem 0 0.75rem 0;
    }

    .stat-kpi {
        background: rgba(30, 41, 59, 0.72);
        border: 1px solid rgba(129, 140, 248, 0.30);
        border-radius: 12px;
        padding: 13px 15px;
        min-height: 105px;
        box-sizing: border-box;
    }

    .stat-kpi-label {
        font-size: 12px;
        font-weight: 650;
        opacity: 0.72;
        margin-bottom: 7px;
    }

    .stat-kpi-value {
        font-size: 27px;
        font-weight: 800;
        line-height: 1.05;
        margin-bottom: 5px;
    }

    .stat-kpi-note {
        font-size: 11px;
        opacity: 0.68;
        line-height: 1.2;
    }

    .stat-insight {
        background: rgba(30, 64, 175, 0.22);
        border: 1px solid rgba(96, 165, 250, 0.20);
        border-radius: 10px;
        padding: 11px 13px;
        line-height: 1.35;
        margin: 5px 0;
    }

    .stat-significant {
        background: rgba(16, 185, 129, 0.13);
        border: 1px solid rgba(52, 211, 153, 0.24);
        border-radius: 10px;
        padding: 10px 13px;
        margin: 5px 0;
    }

    .stat-warning {
        background: rgba(245, 158, 11, 0.11);
        border: 1px solid rgba(245, 158, 11, 0.22);
        border-radius: 10px;
        padding: 10px 13px;
        margin: 5px 0;
    }

    .stat-small {
        font-size: 11px;
        opacity: 0.68;
    }

    .stat-badge {
        display: inline-block;
        padding: 3px 8px;
        border-radius: 999px;
        font-size: 11px;
        font-weight: 700;
        background: rgba(129, 140, 248, 0.16);
        border: 1px solid rgba(129, 140, 248, 0.22);
    }

    .stat-table-wrap {
        width: 100%;
        overflow-x: auto;
        border: 1px solid rgba(129, 140, 248, 0.25);
        border-radius: 12px;
        background: rgba(9, 14, 27, 0.72);
        box-shadow: 0 8px 22px rgba(0, 0, 0, 0.12);
        margin: 8px 0 12px 0;
    }

    .stat-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        font-size: 13px;
    }

    .stat-table th {
        padding: 12px 14px;
        background: rgba(30, 41, 59, 0.92);
        color: #dbeafe;
        font-weight: 750;
        border-bottom: 1px solid rgba(129, 140, 248, 0.22);
        white-space: nowrap;
        text-align: right;
    }

    .stat-table th:first-child {
        text-align: left;
    }

    .stat-table td {
        padding: 11px 14px;
        color: #e5e7eb;
        border-bottom: 1px solid rgba(148, 163, 184, 0.10);
        white-space: nowrap;
        text-align: right;
        font-variant-numeric: tabular-nums;
    }

    .stat-table td:first-child {
        text-align: left;
    }

    .stat-table tbody tr:last-child td {
        border-bottom: 0;
    }

    .stat-table tbody tr:hover td {
        background: rgba(129, 140, 248, 0.08);
    }

    .stat-table .row-label {
        color: #c4b5fd;
        font-weight: 750;
    }

    .stat-table .count-cell {
        position: relative;
        min-width: 135px;
        overflow: hidden;
    }

    .stat-table .count-bar {
        position: absolute;
        left: 10px;
        right: 10px;
        bottom: 4px;
        height: 3px;
        border-radius: 99px;
        background: rgba(94, 234, 212, 0.45);
        transform-origin: left center;
        pointer-events: none;
    }

    .stat-table .count-value {
        position: relative;
        z-index: 1;
        font-weight: 800;
    }

    .stat-table .expected-cell {
        font-weight: 750;
        border-left: 1px solid rgba(148, 163, 184, 0.08);
    }

    .stat-table .sig-yes {
        color: #86efac;
        font-weight: 800;
    }

    .stat-table .sig-no {
        color: #94a3b8;
        font-weight: 650;
    }

    .stat-table .strength {
        color: #c4b5fd;
        font-weight: 700;
    }

    .stat-table .p-value {
        font-weight: 700;
        font-variant-numeric: tabular-nums;
    }

    .stat-table-note {
        font-size: 12px;
        color: #94a3b8;
        margin: 2px 0 8px 0;
    }

    .stats-sidebar-shell {
        width: 100%;
        max-height: calc(100vh - 430px);
        box-sizing: border-box;
        border: 1px solid rgba(139, 92, 246, 0.58);
        border-radius: 16px;
        background: linear-gradient(145deg, rgba(25, 35, 58, 0.96), rgba(17, 25, 45, 0.98));
        padding: 16px;
        margin-top: 8px;
        overflow-y: auto;
        overflow-x: hidden;
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.16), inset 0 1px 0 rgba(255, 255, 255, 0.025);
    }

    .stats-sidebar-shell.single-view {
        min-height: 470px;
    }

    .stats-sidebar-shell.deep-dive {
        height: auto;
        min-height: 0;
        max-height: none;
        overflow: visible;
    }

    .stats-sidebar-shell::-webkit-scrollbar {
        width: 5px;
    }

    .stats-sidebar-shell::-webkit-scrollbar-track {
        background: transparent;
    }

    .stats-sidebar-shell::-webkit-scrollbar-thumb {
        background: rgba(148, 163, 184, 0.28);
        border-radius: 999px;
    }

    .stats-sidebar-title {
        font-size: 16px;
        font-weight: 800;
        color: #f8fafc;
        margin: 0 0 12px 0;
        line-height: 1.2;
    }

    .stats-sidebar-respondents {
        border: 1px solid rgba(129, 140, 248, 0.22);
        border-radius: 12px;
        background: rgba(10, 17, 32, 0.44);
        padding: 11px 12px;
        margin-bottom: 14px;
        flex: 0 0 auto;
    }

    .stats-sidebar-section {
        border: 1px solid rgba(129, 140, 248, 0.28);
        border-radius: 12px;
        background: rgba(10, 17, 32, 0.34);
        padding: 12px;
        box-sizing: border-box;
        min-height: 0;
    }

    .stats-sidebar-section.single-view {
        min-height: 340px;
    }

    .stats-sidebar-section-heading {
        color: #f8fafc;
        font-size: 15px;
        font-weight: 800;
        line-height: 1.2;
        margin-bottom: 4px;
    }

    .stats-sidebar-section-subtitle {
        color: #60a5fa;
        font-size: 11px;
        font-weight: 750;
        margin-bottom: 10px;
    }

    .stats-sidebar-kpi {
        border: 1px solid rgba(129, 140, 248, 0.18);
        border-radius: 9px;
        background: rgba(15, 23, 42, 0.50);
        padding: 11px 10px;
        margin-top: 7px;
        box-sizing: border-box;
        min-height: 58px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .stats-sidebar-section.single-view .stats-sidebar-kpi {
        min-height: 66px;
        padding: 12px 10px;
    }

    .stats-sidebar-kpi.highlight {
        border-color: rgba(45, 212, 191, 0.34);
        background: rgba(45, 212, 191, 0.08);
    }

    .stats-sidebar-kpi-label {
        color: #94a3b8;
        font-size: 10px;
        line-height: 1.2;
        margin-bottom: 4px;
    }

    .stats-sidebar-kpi-value {
        color: #f8fafc;
        font-size: 14px;
        font-weight: 800;
        line-height: 1.25;
        word-break: break-word;
    }

    .stats-sidebar-dynamic {
        display: flex;
        flex-direction: column;
        gap: 0;
    }

    .stats-sidebar-flex-space {
        min-height: 0;
    }

    .stats-sidebar-filter-box {
        margin-top: 10px;
        border: 1px solid rgba(129, 140, 248, 0.18);
        border-radius: 9px;
        padding: 7px 8px;
        background: rgba(15, 23, 42, 0.38);
    }

    .stats-sidebar-label {
        font-size: 9px;
        text-transform: uppercase;
        letter-spacing: 0.09em;
        color: #94a3b8;
        font-weight: 800;
        margin-bottom: 4px;
    }

    .stats-sidebar-filter {
        display: inline-block;
        padding: 4px 7px;
        margin: 2px 2px 2px 0;
        border-radius: 999px;
        background: rgba(129, 140, 248, 0.12);
        border: 1px solid rgba(129, 140, 248, 0.20);
        color: #c4b5fd;
        font-size: 9px;
        font-weight: 750;
    }
    </style>
    """
)


# Page header

page_header(
    "📊 Statistical Analysis",
    "Which relationships are statistically meaningful?",
    "Use chi-square tests and Cramér's V to validate treatment-related relationships. "
    "Explore significance, association strength, respondent counts, and the underlying "
    "contingency tables interactively.",
)


# Main filters

with st.container(border=True):
    st.markdown("### 🎛️ Explore the Evidence")
    st.caption(
        "Filters are applied before the statistical tests. This lets you test whether "
        "relationships remain visible within a selected respondent population."
    )

    f1, f2, f3, f4, f5 = st.columns(5)

    with f1:
        gender_values = sorted(
            df["Gender"].dropna().astype(str).unique().tolist()
        )
        selected_gender = st.selectbox(
            "Gender",
            ["All", *gender_values],
            key="stats_gender",
        )

    with f2:
        age_order = ["18-24", "25-34", "35-44", "45-54", "55-64", "65+"]
        age_values = df["Age_Group"].dropna().astype(str).unique().tolist()
        age_values = [
            x for x in age_order if x in age_values
        ] + sorted(
            x for x in age_values if x not in age_order
        )
        selected_age = st.selectbox(
            "Age Group",
            ["All", *age_values],
            key="stats_age",
        )

    with f3:
        company_values = sorted(
            df["Company_Size_Group"].dropna().astype(str).unique().tolist()
        )
        selected_company = st.selectbox(
            "Company Size",
            ["All", *company_values],
            key="stats_company",
        )

    with f4:
        remote_values = sorted(
            df["Remote_Work_Status"].dropna().astype(str).unique().tolist()
        )
        selected_remote = st.selectbox(
            "Remote Work",
            ["All", *remote_values],
            key="stats_remote",
        )

    with f5:
        treatment_values = sorted(
            df["treatment"].dropna().astype(str).unique().tolist()
        )
        selected_treatment = st.selectbox(
            "Treatment",
            ["All", *treatment_values],
            key="stats_treatment",
        )


# Apply filters

filtered = df.copy()

if selected_gender != "All":
    filtered = filtered[filtered["Gender"].astype(str) == selected_gender]

if selected_age != "All":
    filtered = filtered[filtered["Age_Group"].astype(str) == selected_age]

if selected_company != "All":
    filtered = filtered[
        filtered["Company_Size_Group"].astype(str) == selected_company
    ]

if selected_remote != "All":
    filtered = filtered[
        filtered["Remote_Work_Status"].astype(str) == selected_remote
    ]

if selected_treatment != "All":
    filtered = filtered[
        filtered["treatment"].astype(str) == selected_treatment
    ]


if filtered.empty:
    st.warning("No respondents match the selected filters.")
    st.stop()


active_filters = []
for label, value in [
    ("Gender", selected_gender),
    ("Age Group", selected_age),
    ("Company Size", selected_company),
    ("Remote Work", selected_remote),
    ("Treatment", selected_treatment),
]:
    if value != "All":
        active_filters.append(f"{label}: {value}")

if active_filters:
    st.caption(
        "🎯 Active filters: "
        + " • ".join(active_filters)
        + f"  |  {len(filtered):,} respondents"
    )
else:
    st.caption(f"🎯 All respondents  |  {len(filtered):,} respondents")


# Statistical configuration

FEATURES = [
    ("work_interfere", "Work Interference"),
    ("family_history", "Family History"),
    ("care_options", "Care Options"),
    ("benefits", "Benefits"),
    ("Gender", "Gender"),
    ("anonymity", "Anonymity"),
    ("leave", "Leave"),
    ("mental_health_consequence", "Mental Health Consequence"),
    ("mental_health_interview", "Mental Health Interview"),
    ("phys_health_interview", "Physical Health Interview"),
    ("phys_health_consequence", "Physical Health Consequence"),
    ("supervisor", "Supervisor Support"),
    ("coworkers", "Coworker Support"),
    ("mental_vs_physical", "Mental vs Physical Health"),
]

DISPLAY_ORDER = {
    label: i for i, (_, label) in enumerate(FEATURES)
}



def html_escape(value):
    import html
    return html.escape(str(value))


def render_count_table(dataframe, expected=False):
    """Render a compact dashboard-style matrix with CSS."""
    columns = list(dataframe.columns)
    max_value = float(np.nanmax(dataframe.to_numpy())) if dataframe.size else 1.0
    max_value = max(max_value, 1.0)
    index_label = dataframe.index.name or "Category"

    header = (
        f"<th>{html_escape(index_label)}</th>"
        + "".join(f"<th>{html_escape(c)}</th>" for c in columns)
    )

    body = []
    for idx, row in dataframe.iterrows():
        cells = [f'<td class="row-label">{html_escape(idx)}</td>']

        for column in columns:
            value = float(row[column])

            if expected:
                intensity = min(value / max_value, 1.0)
                background = (
                    f"rgba(96, 165, 250, "
                    f"{0.06 + intensity * 0.24:.2f})"
                )
                cells.append(
                    f'<td class="expected-cell" style="background:{background};">'
                    f"{value:.1f}</td>"
                )
            else:
                ratio = min(value / max_value, 1.0)
                cells.append(
                    f'<td class="count-cell">'
                    f'<span class="count-value">{value:,.0f}</span>'
                    f'<span class="count-bar" style="transform:scaleX({ratio:.3f});"></span>'
                    f"</td>"
                )

        body.append("<tr>" + "".join(cells) + "</tr>")

    return (
        '<div class="stat-table-wrap">'
        '<table class="stat-table">'
        f"<thead><tr>{header}</tr></thead>"
        f"<tbody>{''.join(body)}</tbody>"
        "</table></div>"
    )


def render_residual_table(dataframe):
    """Render standardized residuals as a clean neutral matrix."""
    columns = list(dataframe.columns)
    index_label = dataframe.index.name or "Category"

    header = (
        f"<th>{html_escape(index_label)}</th>"
        + "".join(f"<th>{html_escape(c)}</th>" for c in columns)
    )

    body = []
    for idx, row in dataframe.iterrows():
        cells = [f'<td class="row-label">{html_escape(idx)}</td>']

        for column in columns:
            value = float(row[column])
            cells.append(
                f'<td class="numeric">{value:+.2f}</td>'
            )

        body.append("<tr>" + "".join(cells) + "</tr>")

    return (
        '<div class="stat-table-wrap">'
        '<table class="stat-table">'
        f"<thead><tr>{header}</tr></thead>"
        f"<tbody>{''.join(body)}</tbody>"
        "</table></div>"
    )


def render_results_table(dataframe):
    """Render the full statistical results table with semantic emphasis."""
    headers = list(dataframe.columns)
    header = "".join(f"<th>{html_escape(c)}</th>" for c in headers)
    body = []

    for _, row in dataframe.iterrows():
        cells = []

        for column in headers:
            value = row[column]

            if pd.isna(value):
                text = "—"
            elif column == "P-value":
                text = html_escape(value)
            elif column == "Cramér's V":
                text = html_escape(value)
            elif column == "Chi-square":
                text = html_escape(value)
            elif column == "Significant":
                text = html_escape(value)
            else:
                text = html_escape(value)

            cls = []
            if column == headers[0]:
                cls.append("row-label")
            if column in {"P-value", "Cramér's V", "Chi-square", "Valid Respondents", "Degrees of Freedom"}:
                cls.append("p-value")
            if column == "Significant":
                cls.append("sig-yes" if str(value) == "Yes" else "sig-no")
            if column == "Association Strength":
                cls.append("strength")

            cells.append(f'<td class="{" ".join(cls)}">{text}</td>')

        body.append("<tr>" + "".join(cells) + "</tr>")

    return (
        '<div class="stat-table-wrap">'
        '<table class="stat-table">'
        f"<thead><tr>{header}</tr></thead>"
        f"<tbody>{''.join(body)}</tbody>"
        "</table></div>"
    )

def association_strength(v):
    if pd.isna(v):
        return "Not available"
    if v < 0.10:
        return "Very weak"
    if v < 0.20:
        return "Weak"
    if v < 0.30:
        return "Moderate"
    if v < 0.50:
        return "Strong"
    return "Very strong"


def significance_label(p):
    if pd.isna(p):
        return "Not available"
    if p < 0.001:
        return "p < 0.001"
    if p < 0.01:
        return "p < 0.01"
    if p < 0.05:
        return "p < 0.05"
    return "Not significant"


def run_test(data, feature):
    test_data = data[[feature, "treatment"]].dropna().copy()

    if feature == "work_interfere":
        test_data = test_data[test_data[feature] != "Not Answered"]

    if test_data.empty or test_data[feature].nunique() < 2 or test_data["treatment"].nunique() < 2:
        return {
            "p_value": np.nan,
            "cramers_v": np.nan,
            "n": len(test_data),
            "dof": np.nan,
            "chi2": np.nan,
            "table": pd.DataFrame(),
            "expected": pd.DataFrame(),
        }

    table = pd.crosstab(test_data[feature], test_data["treatment"])

    if table.shape[0] < 2 or table.shape[1] < 2:
        return {
            "p_value": np.nan,
            "cramers_v": np.nan,
            "n": len(test_data),
            "dof": np.nan,
            "chi2": np.nan,
            "table": table,
            "expected": pd.DataFrame(),
        }

    chi2, p_value, dof, expected = chi2_contingency(table)

    n = table.to_numpy().sum()
    min_dim = min(table.shape) - 1

    cramers = np.sqrt((chi2 / n) / min_dim) if n > 0 and min_dim > 0 else np.nan

    expected_df = pd.DataFrame(
        expected,
        index=table.index,
        columns=table.columns,
    )

    return {
        "p_value": float(p_value),
        "cramers_v": float(cramers),
        "n": int(n),
        "dof": int(dof),
        "chi2": float(chi2),
        "table": table,
        "expected": expected_df,
    }


# Run all tests

test_results = []

for column, label in FEATURES:
    if column not in filtered.columns:
        continue

    result = run_test(filtered, column)

    p = result["p_value"]
    v = result["cramers_v"]

    test_results.append(
        {
            "Column": column,
            "Relationship": label,
            "Valid Respondents": result["n"],
            "Chi-square": result["chi2"],
            "Degrees of Freedom": result["dof"],
            "P-value": p,
            "Cramér's V": v,
            "Association Strength": association_strength(v),
            "Significant": "Yes" if pd.notna(p) and p < 0.05 else "No",
        }
    )

results = pd.DataFrame(test_results)

if results.empty:
    st.warning("No statistical relationships could be calculated.")
    st.stop()

results["Significance Order"] = results["P-value"].fillna(1)
results = results.sort_values(
    ["Cramér's V", "P-value"],
    ascending=[False, True],
    na_position="last",
).reset_index(drop=True)


# Executive statistical snapshot

section_title("📌 Statistical Snapshot")

valid_results = results.dropna(subset=["P-value", "Cramér's V"]).copy()
significant = valid_results[valid_results["P-value"] < 0.05].copy()

if not valid_results.empty:
    strongest = valid_results.iloc[0]
    smallest_p = valid_results.loc[valid_results["P-value"].idxmin()]
    strongest_significant = (
        significant.iloc[0] if not significant.empty else None
    )
else:
    strongest = None
    smallest_p = None
    strongest_significant = None

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.html(
        f"""
        <div class="stat-kpi">
            <div class="stat-kpi-label">TESTS EVALUATED</div>
            <div class="stat-kpi-value">{len(valid_results)}</div>
            <div class="stat-kpi-note">relationships with usable chi-square results</div>
        </div>
        """
    )

with k2:
    st.html(
        f"""
        <div class="stat-kpi">
            <div class="stat-kpi-label">SIGNIFICANT RELATIONSHIPS</div>
            <div class="stat-kpi-value">{len(significant)}</div>
            <div class="stat-kpi-note">p &lt; 0.05 within the filtered population</div>
        </div>
        """
    )

with k3:
    strongest_v = strongest["Cramér's V"] if strongest is not None else np.nan
    value = f"{strongest_v:.3f}" if strongest is not None else "N/A"
    name = strongest["Relationship"] if strongest is not None else "N/A"
    st.html(
        f"""
        <div class="stat-kpi">
            <div class="stat-kpi-label">STRONGEST ASSOCIATION</div>
            <div class="stat-kpi-value">{value}</div>
            <div class="stat-kpi-note">{name}</div>
        </div>
        """
    )

with k4:
    smallest_p_value = smallest_p["P-value"] if smallest_p is not None else np.nan
    value = f"{smallest_p_value:.2e}" if smallest_p is not None else "N/A"
    name = smallest_p["Relationship"] if smallest_p is not None else "N/A"
    st.html(
        f"""
        <div class="stat-kpi">
            <div class="stat-kpi-label">SMALLEST P-VALUE</div>
            <div class="stat-kpi-value">{value}</div>
            <div class="stat-kpi-note">{name}</div>
        </div>
        """
    )



def _sidebar_kpi(label, value, highlight=False):
    highlight_class = " highlight" if highlight else ""
    return (
        f'<div class="stats-sidebar-kpi{highlight_class}">'
        f'<div class="stats-sidebar-kpi-label">{html_escape(label)}</div>'
        f'<div class="stats-sidebar-kpi-value">{html_escape(value)}</div>'
        '</div>'
    )


def _sidebar_section(icon, title, subtitle, kpis, css_class=""):
    classes = "stats-sidebar-section"
    if css_class:
        classes += f" {css_class}"

    html = (
        f'<div class="{classes}">'
        f'<div class="stats-sidebar-section-heading">{icon} {html_escape(title)}</div>'
        f'<div class="stats-sidebar-section-subtitle">{html_escape(subtitle)}</div>'
    )

    for label, value, highlight in kpis:
        html += _sidebar_kpi(label, value, highlight)

    html += '</div>'
    return html


def render_stats_sidebar(view_name, filtered_data, results_data, selected_row=None, observed_data=None):
    """Render dynamic statistical intelligence without overlapping cards."""
    shell_class = "stats-sidebar-shell"
    if view_name in {
        "🏆 Association Ranking",
        "📉 Significance Map",
        "📋 Full Results",
    }:
        shell_class += " single-view"
    elif view_name == "🔎 Relationship Deep Dive":
        shell_class += " deep-dive"

    sidebar_html = (
        f'<div class="{shell_class}">'
        '<div class="stats-sidebar-title">📌 Page Intelligence</div>'
        '<div class="stats-sidebar-respondents">'
        '<div class="stats-sidebar-label">RESPONDENTS</div>'
        f'<div class="stats-sidebar-kpi-value" style="font-size:18px;">{len(filtered_data):,}</div>'
        '</div>'
    )

    significant_count = int(
        (results_data["P-value"] < 0.05).sum()
    ) if not results_data.empty else 0

    if view_name == "🏆 Association Ranking":
        strongest = results_data.iloc[0] if not results_data.empty else None
        average_v = (
            results_data["Cramér's V"].mean()
            if not results_data.empty else np.nan
        )

        sidebar_html += _sidebar_section(
            "🏆",
            "Association Ranking",
            "Relationship strength",
            [
                ("Relationships tested", f"{len(results_data)}", False),
                ("Significant relationships", f"{significant_count}", True),
                ("Average Cramér's V", f"{average_v:.3f}", False),
                (
                    "Strongest relationship",
                    str(strongest["Relationship"]) if strongest is not None else "N/A",
                    False,
                ),
            ],
            css_class="single-view",
        )

    elif view_name == "📉 Significance Map":
        strongest_evidence = (
            results_data.loc[results_data["P-value"].idxmin()]
            if not results_data.empty else None
        )
        median_v = (
            results_data["Cramér's V"].median()
            if not results_data.empty else np.nan
        )

        sidebar_html += _sidebar_section(
            "📉",
            "Significance Map",
            "Statistical evidence",
            [
                ("Significant relationships", f"{significant_count} / {len(results_data)}", True),
                ("Median Cramér's V", f"{median_v:.3f}", False),
                (
                    "Strongest evidence",
                    str(strongest_evidence["Relationship"])
                    if strongest_evidence is not None else "N/A",
                    False,
                ),
                ("Significance threshold", "p < 0.05", False),
            ],
            css_class="single-view",
        )

    elif view_name == "🔎 Relationship Deep Dive" and selected_row is not None:
        sidebar_html += _sidebar_section(
            "🔎",
            "Relationship Deep Dive",
            str(selected_row["Relationship"]),
            [
                ("Cramér's V", f'{selected_row["Cramér's V"]:.3f}', True),
                ("Association strength", str(selected_row["Association Strength"]), False),
                ("Chi-square", f'{selected_row["Chi-square"]:.2f}', False),
                ("Valid respondents", f'{int(selected_row["Valid Respondents"]):,}', False),
            ],
        )

        if observed_data is not None and not observed_data.empty:
            totals = observed_data.sum(axis=1).sort_values(ascending=False)
            largest = totals.index[0]
            largest_n = int(totals.iloc[0])

            sidebar_html += _sidebar_section(
                "👥",
                "Respondent Distribution",
                "Selected relationship",
                [
                    ("Largest category", str(largest), False),
                    ("Category respondents", f"{largest_n:,}", False),
                ],
            )

    else:
        sidebar_html += _sidebar_section(
            "📋",
            "Full Results",
            "Statistical result set",
            [
                ("Relationships tested", f"{len(results_data)}", False),
                ("Significant relationships", f"{significant_count}", True),
                ("Not significant", f"{len(results_data) - significant_count}", False),
            ],
            css_class="single-view",
        )

    active_filters = []
    for label, value in [
        ("Gender", selected_gender),
        ("Age", selected_age),
        ("Company", selected_company),
        ("Remote", selected_remote),
        ("Treatment", selected_treatment),
    ]:
        if value != "All":
            active_filters.append(f"{label}: {value}")

    if active_filters:
        chips = "".join(
            f'<span class="stats-sidebar-filter">{html_escape(item)}</span>'
            for item in active_filters
        )
        sidebar_html += (
            '<div class="stats-sidebar-filter-box">'
            '<div class="stats-sidebar-label">ACTIVE FILTERS</div>'
            f'{chips}'
            '</div>'
        )

    sidebar_html += "</div>"
    st.sidebar.html(sidebar_html)


# Main interactive analysis views

section_title("🔬 Statistical Evidence Explorer")

analysis_view = st.radio(
    "Choose an analysis view",
    [
        "🏆 Association Ranking",
        "📉 Significance Map",
        "🔎 Relationship Deep Dive",
        "📋 Full Results",
    ],
    horizontal=True,
    key="stats_analysis_view",
)


# Association ranking

if analysis_view == "🏆 Association Ranking":

    render_stats_sidebar(analysis_view, filtered, valid_results)

    plot_data = valid_results.sort_values("Cramér's V", ascending=True)

    fig = px.bar(
        plot_data,
        x="Cramér's V",
        y="Relationship",
        orientation="h",
        text="Cramér's V",
        color="Cramér's V",
        color_continuous_scale=["#7C3AED", "#C4B5FD"],
        template="plotly_dark",
        title="Treatment Associations Ranked by Cramér's V",
        hover_data={
            "Cramér's V": ":.3f",
            "P-value": ":.2e",
            "Valid Respondents": True,
            "Association Strength": True,
        },
    )

    fig.update_traces(
        texttemplate="%{text:.3f}",
        textposition="outside",
        marker_line_width=0,
    )

    fig.update_layout(
        template=plotly_template(),
        height=max(470, len(plot_data) * 31),
        margin=dict(l=20, r=80, t=65, b=40),
        xaxis_title="Cramér's V",
        yaxis_title="",
        coloraxis_showscale=False,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="stats_association_ranking",
    )

    if strongest is not None:
        st.html(
            f"""
            <div class="stat-insight">
                <strong>💡 Strongest observed association:</strong>
                {strongest['Relationship']} has Cramér's V =
                <strong>{strongest["Cramér's V"]:.3f}</strong>
                ({strongest["Association Strength"]}).
                Its chi-square test has p =
                <strong>{strongest["P-value"]:.2e}</strong>.
            </div>
            """
        )


# Significance map

elif analysis_view == "📉 Significance Map":

    render_stats_sidebar(analysis_view, filtered, valid_results)

    map_data = valid_results.copy()
    map_data["-log10(p)"] = -np.log10(
        map_data["P-value"].clip(lower=1e-300)
    )
    map_data["Result"] = np.where(
        map_data["P-value"] < 0.05,
        "Significant",
        "Not significant",
    )

    fig = px.scatter(
        map_data,
        x="Cramér's V",
        y="-log10(p)",
        size="Valid Respondents",
        color="Result",
        color_discrete_map={
            "Significant": "#FB7185",
            "Not significant": "#64748B",
        },
        hover_name="Relationship",
        hover_data={
            "Cramér's V": ":.3f",
            "P-value": ":.2e",
            "Valid Respondents": True,
            "Association Strength": True,
            "-log10(p)": ":.2f",
        },
        template=plotly_template(),
        title="Association Strength vs Statistical Significance",
    )

    fig.add_hline(
        y=-np.log10(0.05),
        line_dash="dash",
        annotation_text="p = 0.05",
        annotation_position="top right",
    )

    fig.update_layout(
        height=520,
        margin=dict(l=30, r=30, t=65, b=45),
        xaxis_title="Cramér's V",
        yaxis_title="-log10(p-value)",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="stats_significance_map",
    )

    st.caption(
        "Moving upward means stronger statistical evidence; moving right means "
        "a larger association effect size. Point size represents valid respondents."
    )


# Relationship deep dive

elif analysis_view == "🔎 Relationship Deep Dive":

    relationship_options = valid_results["Relationship"].tolist()

    selected_relationship = st.selectbox(
        "Select a relationship to inspect",
        relationship_options,
        key="stats_relationship_selector",
    )

    selected_row = valid_results[
        valid_results["Relationship"] == selected_relationship
    ].iloc[0]

    selected_column = selected_row["Column"]
    selected_result = run_test(filtered, selected_column)

    selected_v = selected_row["Cramér's V"]
    selected_p = selected_row["P-value"]
    selected_chi2 = selected_row["Chi-square"]

    d1, d2, d3, d4 = st.columns(4)

    with d1:
        st.metric(
            "Cramér's V",
            f"{selected_v:.3f}",
            selected_row["Association Strength"],
        )

    with d2:
        st.metric(
            "P-value",
            f"{selected_p:.2e}",
            "Significant" if selected_row["P-value"] < 0.05 else "Not significant",
        )

    with d3:
        st.metric(
            "Chi-square",
            f"{selected_chi2:.2f}",
            f"{int(selected_row['Degrees of Freedom'])} df",
        )

    with d4:
        st.metric(
            "Valid respondents",
            f"{int(selected_row['Valid Respondents']):,}",
        )

    observed = selected_result["table"].copy()

    render_stats_sidebar(
        analysis_view,
        filtered,
        valid_results,
        selected_row=selected_row,
        observed_data=observed,
    )

    if not observed.empty:
        tab1, tab2, tab3 = st.tabs(
            [
                "📊 Observed Counts",
                "🧮 Expected Counts",
                "📐 Standardized Residuals",
            ]
        )

        with tab1:
            st.caption(
                "Click a row to inspect that category. The bars make larger observed counts stand out."
            )

            observed_display = observed.copy()
            observed_display.index.name = selected_relationship

            st.html(render_count_table(observed_display, expected=False))

            selected_category = st.selectbox(
                "Inspect an observed-count category",
                observed_display.index.tolist(),
                key="stats_observed_row_selector",
            )

            selected_rows = [observed_display.index.get_loc(selected_category)]

            if selected_rows:
                selected_index = observed_display.index[selected_rows[0]]
                selected_counts = observed_display.loc[selected_index]
                total_row = int(selected_counts.sum())

                breakdown = []
                for outcome, count in selected_counts.items():
                    pct = count / total_row * 100 if total_row else 0
                    breakdown.append(
                        f"{outcome}: {int(count):,} ({pct:.1f}%)"
                    )

                st.info(
                    f"🔎 **{selected_index}** — {total_row:,} respondents  |  "
                    + " • ".join(breakdown)
                )

                # Compact treatment summary
                no_count = int(selected_counts.get("No", 0))
                yes_count = int(selected_counts.get("Yes", 0))
                treatment_total = no_count + yes_count
                no_pct = no_count / treatment_total * 100 if treatment_total else 0
                yes_pct = yes_count / treatment_total * 100 if treatment_total else 0
                treatment_gap = abs(no_pct - yes_pct)

                metric_1, metric_2, metric_3 = st.columns(3)

                with metric_1:
                    st.metric(
                        "No Treatment",
                        f"{no_count:,}",
                        f"{no_pct:.1f}% of group",
                    )

                with metric_2:
                    st.metric(
                        "Treatment",
                        f"{yes_count:,}",
                        f"{yes_pct:.1f}% of group",
                    )

                with metric_3:
                    st.metric(
                        "Treatment Gap",
                        f"{treatment_gap:.1f} pp",
                        "absolute difference",
                    )

                # Clear two-column comparison. A vertical column chart makes
                # the treatment outcomes visually distinct instead of stacking
                # them into one continuous bar.
                share_df = pd.DataFrame(
                    {
                        "Treatment": ["No", "Yes"],
                        "Share": [no_pct, yes_pct],
                        "Respondents": [no_count, yes_count],
                    }
                )

                selected_fig = px.bar(
                    share_df,
                    x="Treatment",
                    y="Share",
                    color="Treatment",
                    color_discrete_map={
                        "No": "#A78BFA",
                        "Yes": "#2DD4BF",
                    },
                    text="Share",
                    title=f"Treatment Split — {selected_index}",
                    custom_data=["Respondents"],
                )

                selected_fig.update_traces(
                    texttemplate="%{text:.1f}%",
                    textposition="outside",
                    marker_line_width=0,
                    hovertemplate=(
                        "<b>%{x} Treatment</b><br>"
                        "Respondents: %{customdata[0]:,}<br>"
                        "Share: %{y:.1f}%<extra></extra>"
                    ),
                )

                selected_fig.update_layout(
                    template=plotly_template(),
                    showlegend=False,
                    height=330,
                    margin=dict(l=30, r=30, t=60, b=45),
                    xaxis=dict(
                        title="Treatment Outcome",
                        categoryorder="array",
                        categoryarray=["No", "Yes"],
                    ),
                    yaxis=dict(
                        title="Share of respondents",
                        range=[0, 100],
                        ticksuffix="%",
                        dtick=20,
                    ),
                    hoverlabel=dict(
                        bgcolor="rgba(15, 23, 42, 0.96)",
                    ),
                )

                st.plotly_chart(
                    selected_fig,
                    use_container_width=True,
                    key="stats_observed_selected_chart",
                )

                st.caption(
                    f"Observed count: {no_count:,} reported no treatment and "
                    f"{yes_count:,} reported treatment within the {selected_index} group."
                )
            else:
                st.caption(
                    "Click a row in the table to explore its treatment distribution."
                )

        with tab2:
            expected_raw = selected_result["expected"]
            expected = expected_raw.round(1)
            expected.index.name = selected_relationship

            st.caption(
                "Expected counts represent the number of respondents predicted in each "
                "cell if the selected variable and treatment status were independent. "
                "Darker cells indicate larger expected counts; compare these values with Observed Counts to see where the chi-square difference comes from."
            )

            st.html(render_count_table(expected, expected=True))

            expected_selection = st.selectbox(
                "Inspect an expected-count row",
                expected.index.tolist(),
                key="stats_expected_row_selector",
            )

            expected_row = expected.loc[expected_selection]
            expected_total = float(expected_row.sum())

            expected_breakdown = []
            for outcome, value in expected_row.items():
                share = value / expected_total * 100 if expected_total else 0
                expected_breakdown.append(
                    f"{outcome}: {value:.1f} ({share:.1f}%)"
                )

            st.info(
                f"🧮 **{expected_selection}** — expected total {expected_total:.1f}  |  "
                + " • ".join(expected_breakdown)
            )

            # Grouped columns make the statistical comparison explicit:
            # observed counts are shown beside the counts expected under
            # independence for the same treatment outcomes.
            observed_row = observed.loc[expected_selection]

            comparison_df = pd.DataFrame(
                {
                    "Treatment": expected_row.index.tolist() * 2,
                    "Count Type": (
                        ["Observed"] * len(expected_row)
                        + ["Expected"] * len(expected_row)
                    ),
                    "Count": (
                        observed_row.astype(float).tolist()
                        + expected_row.astype(float).tolist()
                    ),
                }
            )

            expected_fig = px.bar(
                comparison_df,
                x="Treatment",
                y="Count",
                color="Count Type",
                barmode="group",
                text="Count",
                color_discrete_map={
                    "Observed": "#2DD4BF",
                    "Expected": "#F59E0B",
                },
                title=f"Observed vs Expected — {expected_selection}",
                hover_data={
                    "Count": ":.1f",
                    "Count Type": True,
                    "Treatment": True,
                },
            )

            expected_fig.update_traces(
                texttemplate="%{text:.1f}",
                textposition="outside",
                marker_line_width=0,
                hovertemplate=(
                    "<b>%{fullData.name}</b><br>"
                    "Treatment: %{x}<br>"
                    "Count: %{y:.1f}<extra></extra>"
                ),
            )

            expected_fig.update_layout(
                template=plotly_template(),
                height=340,
                margin=dict(l=20, r=20, t=60, b=35),
                yaxis_title="Respondents",
                xaxis_title="Treatment",
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1,
                ),
                hoverlabel=dict(
                    bgcolor="rgba(15, 23, 42, 0.96)",
                ),
            )

            st.plotly_chart(
                expected_fig,
                use_container_width=True,
                key="stats_expected_selected_chart",
            )

            st.caption(
                "Expected = what the counts would be if treatment and the selected "
                "variable were independent. Observed = the actual survey counts."
            )

        with tab3:
            expected = selected_result["expected"]
            residuals = (
                (observed - expected)
                / np.sqrt(expected.replace(0, np.nan))
            ).round(2)

            residuals.index.name = selected_relationship

            st.caption(
                "Values show how far the observed count differs from the count expected "
                "if the two variables were independent: positive values are above expected, "
                "negative values are below expected, and values closer to zero are closer "
                "to the expected count."
            )

            st.html(render_residual_table(residuals))


        if selected_row["P-value"] < 0.05:
            st.html(
                f"""
                <div class="stat-significant">
                    <strong>✅ Evidence of association.</strong>
                    The relationship between <strong>{selected_relationship}</strong>
                    and treatment status is statistically significant at the
                    5% level (p = {selected_row["P-value"]:.2e}).
                    Cramér's V = {selected_row["Cramér's V"]:.3f}.
                </div>
                """
            )
        else:
            st.html(
                f"""
                <div class="stat-warning">
                    <strong>ℹ️ No statistically significant association detected.</strong>
                    For <strong>{selected_relationship}</strong>, p =
                    {selected_row["P-value"]:.2e}, which is not below 0.05.
                </div>
                """
            )


# Full results

else:

    render_stats_sidebar(analysis_view, filtered, valid_results)

    display = valid_results.copy()

    display["P-value"] = display["P-value"].map(
        lambda x: f"{x:.4f}"
    )
    display["Cramér's V"] = display["Cramér's V"].map(
        lambda x: f"{x:.3f}"
    )
    display["Chi-square"] = display["Chi-square"].map(
        lambda x: f"{x:.3f}"
    )

    display = display[
        [
            "Relationship",
            "Valid Respondents",
            "Chi-square",
            "Degrees of Freedom",
            "P-value",
            "Cramér's V",
            "Association Strength",
            "Significant",
        ]
    ]

    st.html(render_results_table(display))


    csv_data = display.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇️ Download Statistical Results",
        data=csv_data,
        file_name="statistical_analysis_results.csv",
        mime="text/csv",
        key="stats_download_results",
    )


# How to interpret

section_title("📚 How to Read the Results")

read_1, read_2 = st.columns(2)

with read_1:
    st.markdown(
        """
        **Chi-square test**

        Tests whether treatment status and the selected categorical variable
        appear independent.

        **P-value**

        A value below 0.05 is treated here as evidence against independence.
        Smaller values indicate stronger statistical evidence, but do not measure
        the size of the relationship.
        """
    )

with read_2:
    st.markdown(
        """
        **Cramér's V**

        Measures the strength of association between the categorical variables.
        Values closer to 0 indicate weaker association; larger values indicate
        stronger association.

        **Important**

        Statistical significance does not imply practical importance, and
        association does not imply causation.
        """
    )


# Methodology and limitations

section_title("🧪 Methodology & Limitations")

st.markdown(
    """
    **Method used:** Pearson's chi-square test of independence with Cramér's V
    as the effect-size measure.

    **Treatment is the outcome:** Each relationship is tested against the
    `treatment` variable.

    **Missing/unknown handling:** Rows missing either variable are excluded from
    that individual test. `Not Answered` is excluded from Work Interference so
    the category does not distort the comparison.

    **Interpretation:** These results describe associations in the 2014 survey
    population. They do not establish that a workplace factor causes treatment
    behavior.

    **Filtering:** Statistical results are recalculated after the page filters,
    so smaller filtered populations can produce less stable estimates.
    """
)


# Compact footer

st.caption(
    "Source: 2014 Mental Health in Tech Survey • "
    "Chi-square + Cramér's V • p < 0.05 used as the significance threshold • "
    "Association does not imply causation."
)
