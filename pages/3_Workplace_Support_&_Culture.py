import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils.data_loader import load_data
from utils.analytics import grouped_treatment_rate
from utils.styling import (
    apply_global_style,
    page_header,
    section_title,
    plotly_template,
)


# Page configuration

st.set_page_config(
    page_title="Workplace Support",
    page_icon="🏢",
    layout="wide",
)

apply_global_style()


# Native Streamlit sidebar navigation buttons
st.markdown(
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
    </style>
    """,
    unsafe_allow_html=True,
)


# Page spacing

st.markdown(
    """
    <style>
    .stMainBlockContainer {
        padding-top: 2.25rem !important;
    }

    [data-testid="stAppViewContainer"] .main .block-container {
        padding-top: 2.25rem !important;
    }

    [data-testid="stSidebar"] {
        border-right: 1px solid rgba(128, 128, 128, 0.18);
    }

    [data-testid="stSidebar"] [data-testid="stMetric"] {
        margin-bottom: 0.1rem;
        padding: 0;
        background: transparent;
        border: 0;
    }

    [data-testid="stSidebar"] [data-testid="stMetricLabel"] {
        font-size: 0.68rem;
    }

    [data-testid="stSidebar"] [data-testid="stMetricValue"] {
        font-size: 0.9rem;
    }

    [data-testid="stSidebar"] p {
        font-size: 0.76rem;
        line-height: 1.25;
        margin-bottom: 0.2rem;
    }

    [data-testid="stSidebar"] h3 {
        font-size: 0.9rem;
        margin-top: 0.25rem;
        margin-bottom: 0.25rem;
    }

    [data-testid="stSidebar"] .stMarkdown {
        margin-bottom: 0.08rem;
    }

    [data-testid="stSidebar"] .stCaption {
        margin-bottom: 0.05rem;
    }


    /* Page Intelligence panel */
    [data-testid="stSidebar"] .mh-sidebar-intelligence {
        margin-top: 0.45rem;
        padding: 18px 16px 20px 16px;
        min-height: calc(100vh - 430px);
        box-sizing: border-box;
        border: 1px solid rgba(124, 58, 237, 0.42);
        border-radius: 16px;
        background: linear-gradient(180deg, #18233b 0%, #141d33 100%);
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.035);
    }

    [data-testid="stSidebar"] .mh-sidebar-title {
        display: flex;
        align-items: center;
        gap: 8px;
        color: #f8fafc;
        font-size: 0.98rem;
        font-weight: 750;
        line-height: 1.2;
        margin-bottom: 16px;
    }

    [data-testid="stSidebar"] .mh-sidebar-pin {
        font-size: 0.98rem;
    }

    [data-testid="stSidebar"] .mh-sidebar-respondents {
        padding: 11px 12px;
        margin-bottom: 14px;
        border-radius: 11px;
        background: rgba(15, 23, 42, 0.58);
        border: 1px solid rgba(148, 163, 184, 0.16);
    }

    [data-testid="stSidebar"] .mh-sidebar-label {
        color: #94a3b8;
        font-size: 0.61rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        line-height: 1.2;
        margin-bottom: 4px;
    }

    [data-testid="stSidebar"] .mh-sidebar-number {
        color: #f8fafc;
        font-size: 1.05rem;
        font-weight: 750;
        line-height: 1.15;
    }

    [data-testid="stSidebar"] .mh-sidebar-section {
        margin-top: 2px;
        padding: 14px 13px 15px 13px;
        border: 1px solid rgba(96, 165, 250, 0.24);
        border-radius: 12px;
        background: rgba(15, 23, 42, 0.42);
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.025);
        box-sizing: border-box;
    }

    [data-testid="stSidebar"] .mh-sidebar-section-name {
        color: #f1f5f9;
        font-size: 0.86rem;
        font-weight: 750;
        line-height: 1.3;
        margin-bottom: 13px;
    }

    [data-testid="stSidebar"] .mh-sidebar-row {
        display: flex;
        flex-direction: column;
        gap: 3px;
        margin-bottom: 10px;
        color: #94a3b8;
        font-size: 0.68rem;
        line-height: 1.25;
    }

    [data-testid="stSidebar"] .mh-sidebar-row strong {
        color: #dbeafe;
        font-size: 0.78rem;
        font-weight: 700;
    }

    [data-testid="stSidebar"] .mh-sidebar-focus {
        margin-top: 11px;
        padding: 10px 11px;
        border: 1px solid rgba(124, 58, 237, 0.24);
        border-left: 3px solid #7c3aed;
        border-radius: 8px;
        background: rgba(124, 58, 237, 0.11);
    }

    [data-testid="stSidebar"] .mh-sidebar-focus-value {
        color: #e9d5ff;
        font-size: 0.78rem;
        font-weight: 650;
        line-height: 1.3;
    }

    [data-testid="stSidebar"] .mh-sidebar-detail {
        margin-top: 11px;
        padding-top: 9px;
        border-top: 1px solid rgba(148, 163, 184, 0.12);
        color: #b8c4d6;
        font-size: 0.7rem;
        font-weight: 600;
        line-height: 1.5;
    }

    [data-testid="stSidebar"] .mh-sidebar-subtitle {
        color: #93c5fd;
        font-size: 0.69rem;
        font-weight: 700;
        line-height: 1.3;
        margin: -4px 0 10px 0;
    }

    [data-testid="stSidebar"] .mh-sidebar-stats {
        display: flex;
        flex-direction: column;
        gap: 6px;
    }

    [data-testid="stSidebar"] .mh-sidebar-stat {
        padding: 7px 8px;
        border-radius: 8px;
        background: rgba(15, 23, 42, 0.52);
        border: 1px solid rgba(148, 163, 184, 0.10);
    }

    [data-testid="stSidebar"] .mh-sidebar-stat-accent {
        background: rgba(45, 212, 191, 0.08);
        border-color: rgba(45, 212, 191, 0.22);
    }

    [data-testid="stSidebar"] .mh-sidebar-stat-label {
        color: #94a3b8;
        font-size: 0.59rem;
        font-weight: 650;
        line-height: 1.15;
        margin-bottom: 3px;
    }

    [data-testid="stSidebar"] .mh-sidebar-stat-value {
        color: #e2e8f0;
        font-size: 0.76rem;
        font-weight: 750;
        line-height: 1.25;
        overflow-wrap: anywhere;
    }

    [data-testid="stSidebar"] .mh-sidebar-compare {
        padding: 8px;
        margin-bottom: 6px;
        border-radius: 9px;
        background: rgba(15, 23, 42, 0.52);
        border: 1px solid rgba(96, 165, 250, 0.14);
    }

    [data-testid="stSidebar"] .mh-sidebar-compare:last-child {
        margin-bottom: 0;
    }

    [data-testid="stSidebar"] .mh-sidebar-compare-name {
        color: #f1f5f9;
        font-size: 0.72rem;
        font-weight: 750;
        line-height: 1.25;
        margin-bottom: 5px;
    }

    [data-testid="stSidebar"] .mh-sidebar-compare .mh-sidebar-stat {
        background: transparent;
        border: 0;
        padding: 2px 0;
    }

    [data-testid="stSidebar"] .mh-sidebar-compare .mh-sidebar-stat-accent {
        background: transparent;
        border: 0;
    }

    /* Page-specific workplace filter panel */
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-color: rgba(96, 165, 250, 0.28) !important;
        border-radius: 14px !important;
        background: linear-gradient(180deg, rgba(15, 23, 42, 0.72) 0%, rgba(15, 23, 42, 0.52) 100%) !important;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.025) !important;
    }

    .workplace-filter-header {
        padding: 2px 0 4px 0;
    }

    .workplace-filter-header h2 {
        margin: 0 0 7px 0;
        color: #f8fafc;
        font-size: 1.22rem;
        line-height: 1.25;
        font-weight: 750;
    }

    .workplace-filter-header p {
        margin: 0 0 10px 0;
        color: #94a3b8;
        font-size: 0.78rem;
        line-height: 1.4;
    }

    [data-testid="stVerticalBlockBorderWrapper"] [data-testid="stHorizontalBlock"] {
        gap: 0.8rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# Load data

df = load_data()

if df.empty:
    st.warning("No survey data is available.")
    st.stop()

filtered = df.copy()


# Shared chart configuration

CHART_CONFIG = {
    "displayModeBar": True,
    "displaylogo": False,
    "responsive": True,
    "scrollZoom": True,
    "modeBarButtonsToRemove": [
        "lasso2d",
        "select2d",
    ],
}


# Workplace support configuration

SUPPORT_FEATURES = [
    ("benefits", "Mental Health Benefits", "💚"),
    ("care_options", "Mental Health Care Options", "🩺"),
    ("wellness_program", "Wellness Program", "🌱"),
    ("seek_help", "Resources to Seek Help", "🧭"),
    ("anonymity", "Anonymity", "🔐"),
    ("leave", "Ease of Taking Leave", "🕊️"),
]

SUPPORT_COLORS = {
    "benefits": {
        "main": "#22C55E",
        "light": "#86EFAC",
        "dark": "#15803D",
    },
    "care_options": {
        "main": "#F97316",
        "light": "#FDBA74",
        "dark": "#C2410C",
    },
    "wellness_program": {
        "main": "#14B8A6",
        "light": "#5EEAD4",
        "dark": "#0F766E",
    },
    "seek_help": {
        "main": "#3B82F6",
        "light": "#93C5FD",
        "dark": "#1D4ED8",
    },
    "anonymity": {
        "main": "#A855F7",
        "light": "#D8B4FE",
        "dark": "#7E22CE",
    },
    "leave": {
        "main": "#EC4899",
        "light": "#F9A8D4",
        "dark": "#BE185D",
    },
}


# Workplace culture configuration

CULTURE_FEATURES = [
    ("coworkers", "Coworker Support", "👥"),
    ("supervisor", "Supervisor Support", "🧑‍💼"),
    (
        "mental_health_consequence",
        "Mental Health Consequences",
        "🧠",
    ),
    (
        "mental_health_interview",
        "Mental Health Interview",
        "🎤",
    ),
    (
        "phys_health_interview",
        "Physical Health Interview",
        "🏥",
    ),
    (
        "mental_vs_physical",
        "Mental vs Physical Health",
        "⚖️",
    ),
]

CULTURE_PALETTES = {
    "coworkers": [
        "#7C3AED",
        "#A78BFA",
        "#C4B5FD",
        "#DDD6FE",
    ],
    "supervisor": [
        "#0EA5E9",
        "#38BDF8",
        "#7DD3FC",
        "#BAE6FD",
    ],
    "mental_health_consequence": [
        "#F43F5E",
        "#FB7185",
        "#FDA4AF",
        "#FECDD3",
    ],
    "mental_health_interview": [
        "#14B8A6",
        "#2DD4BF",
        "#5EEAD4",
        "#99F6E4",
    ],
    "phys_health_interview": [
        "#F59E0B",
        "#FBBF24",
        "#FCD34D",
        "#FDE68A",
    ],
    "mental_vs_physical": [
        "#EC4899",
        "#F472B6",
        "#F9A8D4",
        "#FBCFE8",
    ],
}

SUPPORT_LOOKUP = {
    f"{icon} {title}": column
    for column, title, icon in SUPPORT_FEATURES
}

SUPPORT_DETAIL_LOOKUP = {
    f"{icon} {title}": (column, title, icon)
    for column, title, icon in SUPPORT_FEATURES
}

CULTURE_LOOKUP = {
    title: (column, icon)
    for column, title, icon in CULTURE_FEATURES
}


# Sidebar state
# These values are updated by the analysis controls below.
support_comparison_mode = "Support Availability"
selected_support_mechanism = "💚 Mental Health Benefits"
selected_support_detail = "💚 Mental Health Benefits"

culture_compare_one = "Coworker Support"
culture_compare_two = "Supervisor Support"
culture_explore_signal = "Coworker Support"
culture_dashboard_signal = "Coworker Support"


# Helper functions

def get_yes_rate(column):
    if filtered.empty:
        return 0.0
    return filtered[column].eq("Yes").mean() * 100


def get_treatment_data(column):
    data = grouped_treatment_rate(
        filtered,
        column,
    ).copy()

    if column not in data.columns:
        return pd.DataFrame()

    data = data.dropna(
        subset=[
            column,
            "Treatment Rate",
        ]
    )

    data = data.rename(
        columns={
            column: "Response",
        }
    )

    data["Response"] = data["Response"].astype(str)

    return data


def build_treatment_chart(
    data,
    mechanism_title,
    color,
):
    chart_data = data.sort_values(
        "Treatment Rate",
        ascending=True,
    ).copy()

    fig = px.bar(
        chart_data,
        x="Treatment Rate",
        y="Response",
        orientation="h",
        text="Treatment Rate",
        title=f"Treatment Rate by {mechanism_title}",
        template=plotly_template(),
    )

    fig.update_traces(
        marker_color=color,
        marker_line_width=0,
        texttemplate="%{text:.1f}%",
        textposition="outside",
        cliponaxis=False,
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Treatment Rate: <b>%{x:.1f}%</b>"
            "<extra></extra>"
        ),
    )

    fig.update_layout(
        height=450,
        margin=dict(
            l=25,
            r=90,
            t=70,
            b=45,
        ),
        showlegend=False,
        title=dict(
            x=0.01,
            xanchor="left",
            font=dict(size=17),
        ),
    )

    fig.update_xaxes(
        title="Treatment Rate",
        range=[0, 100],
        ticksuffix="%",
        showgrid=True,
        zeroline=False,
    )

    fig.update_yaxes(
        title="Response",
    )

    return fig


def culture_counts(column):
    data = (
        filtered[column]
        .fillna("Unknown")
        .value_counts()
        .rename_axis("Response")
        .reset_index(name="Respondents")
    )
    return data


def culture_distribution(column):
    data = culture_counts(column)
    total = data["Respondents"].sum()

    if total > 0:
        data["Percentage"] = (
            data["Respondents"] / total * 100
        )
    else:
        data["Percentage"] = 0.0

    return data


def culture_signal_kpis(column):
    data = culture_distribution(column)

    if data.empty:
        return {
            "total": 0,
            "top_response": "N/A",
            "top_count": 0,
            "top_percentage": 0.0,
            "second_response": "N/A",
            "second_percentage": 0.0,
            "gap": 0.0,
        }

    top_row = data.iloc[0]

    if len(data) > 1:
        second_row = data.iloc[1]
        second_response = str(second_row["Response"])
        second_percentage = float(second_row["Percentage"])
    else:
        second_response = "N/A"
        second_percentage = 0.0

    top_response = str(top_row["Response"])
    top_count = int(top_row["Respondents"])
    top_percentage = float(top_row["Percentage"])

    return {
        "total": int(data["Respondents"].sum()),
        "top_response": top_response,
        "top_count": top_count,
        "top_percentage": top_percentage,
        "second_response": second_response,
        "second_percentage": second_percentage,
        "gap": top_percentage - second_percentage,
    }


def make_culture_distribution_chart(
    column,
    title,
    palette,
    horizontal=False,
):
    data = culture_distribution(column)

    if horizontal:
        fig = px.bar(
            data,
            x="Percentage",
            y="Response",
            orientation="h",
            text="Percentage",
            color="Response",
            color_discrete_sequence=palette,
            title=title,
            hover_data={
                "Respondents": True,
                "Percentage": ":.1f",
            },
        )
    else:
        fig = px.bar(
            data,
            x="Response",
            y="Percentage",
            text="Percentage",
            color="Response",
            color_discrete_sequence=palette,
            title=title,
            hover_data={
                "Respondents": True,
                "Percentage": ":.1f",
            },
        )

    fig.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside",
        marker_line_width=0,
    )

    fig.update_layout(
        template=plotly_template(),
        showlegend=False,
        height=430,
        margin=dict(
            l=45,
            r=30,
            t=65,
            b=60,
        ),
        title_x=0.02,
        hoverlabel=dict(
            bgcolor="#111827",
            font_size=13,
        ),
    )

    if horizontal:
        fig.update_xaxes(
            title="Respondents (%)",
            range=[0, 100],
        )
        fig.update_yaxes(
            title="Response",
        )
    else:
        fig.update_yaxes(
            title="Respondents (%)",
            range=[0, 100],
        )
        fig.update_xaxes(
            title="Response",
        )

    return fig


def make_culture_comparison_chart(
    column_one,
    title_one,
    column_two,
    title_two,
):
    data_one = culture_distribution(column_one).copy()
    data_one["Signal"] = title_one

    data_two = culture_distribution(column_two).copy()
    data_two["Signal"] = title_two

    comparison = pd.concat(
        [
            data_one,
            data_two,
        ],
        ignore_index=True,
    )

    response_order = (
        comparison["Response"]
        .drop_duplicates()
        .tolist()
    )

    fig = px.bar(
        comparison,
        x="Response",
        y="Percentage",
        color="Signal",
        barmode="group",
        text="Percentage",
        category_orders={
            "Response": response_order,
        },
        color_discrete_map={
            title_one: CULTURE_PALETTES[column_one][0],
            title_two: CULTURE_PALETTES[column_two][0],
        },
        title=f"{title_one} vs {title_two}",
        hover_data={
            "Respondents": True,
            "Percentage": ":.1f",
            "Signal": True,
        },
    )

    fig.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside",
        marker_line_width=0,
    )

    fig.update_layout(
        template=plotly_template(),
        barmode="group",
        height=460,
        margin=dict(
            l=45,
            r=30,
            t=75,
            b=65,
        ),
        title_x=0.02,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
        ),
        hoverlabel=dict(
            bgcolor="#111827",
            font_size=13,
        ),
    )

    fig.update_yaxes(
        title="Respondents (%)",
        range=[0, 100],
    )

    fig.update_xaxes(
        title="Response",
    )

    return fig


def render_culture_signal_kpis(column):
    kpis = culture_signal_kpis(column)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "👥 Respondents",
            f"{kpis['total']:,}",
        )

    with c2:
        st.metric(
            "🏆 Most Common",
            kpis["top_response"],
        )

    with c3:
        st.metric(
            "📊 Top Response Share",
            f"{kpis['top_percentage']:.1f}%",
        )

    with c4:
        st.metric(
            "📏 Top vs #2 Gap",
            f"{kpis['gap']:.1f} pp",
        )


def render_culture_signal_summary(column, title):
    kpis = culture_signal_kpis(column)

    st.info(
        f"**{title}:** the most common response is "
        f"**{kpis['top_response']}** with "
        f"**{kpis['top_percentage']:.1f}%** of respondents "
        f"({kpis['top_count']:,} people)."
    )


# Page header

page_header(
    "🏢 Workplace Support",
    "Investigate workplace support and culture",
    "Explore the resources, policies, communication patterns, and workplace signals "
    "that shape the mental-health experience of employees.",
    level="Workplace Support Intelligence",
)


# Page-specific workplace filters

with st.container(border=True):
    st.markdown(
        """
        <div class="workplace-filter-header">
            <h2>🧭 Explore the Workplace</h2>
            <p>
                Refine the respondent population before exploring support resources and workplace culture.
                Filters are specific to the workplace analysis.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    f1, f2, f3, f4, f5 = st.columns(5)

    with f1:
        workplace_gender = st.selectbox(
            "Gender",
            ["All"] + sorted(df["Gender"].dropna().astype(str).unique().tolist()),
            key="workplace_filter_gender",
        )

    with f2:
        workplace_age = st.selectbox(
            "Age Group",
            ["All"] + sorted(df["Age_Group"].dropna().astype(str).unique().tolist()),
            key="workplace_filter_age_group",
        )

    with f3:
        workplace_company = st.selectbox(
            "Company Size",
            ["All"] + sorted(df["Company_Size_Group"].dropna().astype(str).unique().tolist()),
            key="workplace_filter_company_size",
        )

    with f4:
        workplace_remote = st.selectbox(
            "Remote Work",
            ["All"] + sorted(df["Remote_Work_Status"].dropna().astype(str).unique().tolist()),
            key="workplace_filter_remote_work",
        )

    with f5:
        workplace_treatment = st.selectbox(
            "Treatment",
            ["All"] + sorted(df["treatment"].dropna().astype(str).unique().tolist()),
            key="workplace_filter_treatment",
        )

filtered = df.copy()

if workplace_gender != "All":
    filtered = filtered[filtered["Gender"] == workplace_gender]

if workplace_age != "All":
    filtered = filtered[filtered["Age_Group"] == workplace_age]

if workplace_company != "All":
    filtered = filtered[filtered["Company_Size_Group"] == workplace_company]

if workplace_remote != "All":
    filtered = filtered[filtered["Remote_Work_Status"] == workplace_remote]

if workplace_treatment != "All":
    filtered = filtered[filtered["treatment"] == workplace_treatment]

if filtered.empty:
    st.warning("No respondents match the selected workplace filters. Adjust the filters to continue.")
    st.stop()


# Main workplace navigation
# Streamlit's native st.tabs() does not expose the active tab to Python.
# A segmented control gives us real widget state, so the sidebar can react
# to the section the user is actually viewing.

active_section = st.segmented_control(
    "Workplace section",
    options=[
        "🛟 Support & Resources",
        "🤝 Workplace Culture",
    ],
    default="🛟 Support & Resources",
    key="workplace_main_section",
    label_visibility="collapsed",
)

if active_section is None:
    active_section = "🛟 Support & Resources"


# Support & Resources

if active_section == "🛟 Support & Resources":

    section_title("📊 Support Availability")

    benefits_rate = get_yes_rate("benefits")
    care_rate = get_yes_rate("care_options")
    wellness_rate = get_yes_rate("wellness_program")
    help_rate = get_yes_rate("seek_help")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "💚 Benefits Available",
            f"{benefits_rate:.1f}%",
        )

    with c2:
        st.metric(
            "🩺 Care Options Available",
            f"{care_rate:.1f}%",
        )

    with c3:
        st.metric(
            "🌱 Wellness Program",
            f"{wellness_rate:.1f}%",
        )

    with c4:
        st.metric(
            "🧭 Help Resources",
            f"{help_rate:.1f}%",
        )

    section_title("🎮 Support System Explorer")

    support_explorer = st.segmented_control(
        "Support explorer",
        options=[
            "🧩 Compare Support",
            "🔎 Explore One Mechanism",
        ],
        default="🧩 Compare Support",
        key="support_explorer_section",
        label_visibility="collapsed",
    )

    if support_explorer is None:
        support_explorer = "🧩 Compare Support"

    if support_explorer == "🧩 Compare Support":

        st.markdown("### Compare workplace support mechanisms")
        st.caption(
            "Switch between support availability and treatment rates."
        )

        support_comparison_mode = st.radio(
            "Comparison",
            [
                "Support Availability",
                "Treatment Rate",
            ],
            horizontal=True,
            key="support_comparison_mode",
        )

        if support_comparison_mode == "Support Availability":

            availability_rows = []

            for column, title, icon in SUPPORT_FEATURES:
                total = len(filtered)
                available = filtered[column].eq("Yes").sum()

                availability_rows.append(
                    {
                        "Mechanism": f"{icon} {title}",
                        "Availability": (
                            available / total * 100
                            if total
                            else 0
                        ),
                        "Respondents": int(available),
                        "Column": column,
                    }
                )

            availability_data = pd.DataFrame(
                availability_rows
            ).sort_values(
                "Availability",
                ascending=True,
            )

            fig = px.bar(
                availability_data,
                x="Availability",
                y="Mechanism",
                orientation="h",
                text="Availability",
                title="Workplace Support Availability",
                template=plotly_template(),
            )

            colors = [
                SUPPORT_COLORS[row["Column"]]["main"]
                for _, row in availability_data.iterrows()
            ]

            fig.update_traces(
                marker_color=colors,
                marker_line_width=0,
                texttemplate="%{text:.1f}%",
                textposition="outside",
                cliponaxis=False,
                customdata=availability_data[
                    ["Respondents"]
                ],
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    "Availability: <b>%{x:.1f}%</b><br>"
                    "Respondents: <b>%{customdata[0]}</b>"
                    "<extra></extra>"
                ),
            )

            fig.update_layout(
                height=500,
                margin=dict(
                    l=25,
                    r=90,
                    t=75,
                    b=45,
                ),
                showlegend=False,
                title=dict(
                    x=0.01,
                    xanchor="left",
                    font=dict(size=18),
                ),
            )

            fig.update_xaxes(
                title="Respondents reporting support as available",
                range=[0, 100],
                ticksuffix="%",
            )

            fig.update_yaxes(title="")

            st.plotly_chart(
                fig,
                use_container_width=True,
                config=CHART_CONFIG,
                key="support_availability_comparison",
            )

            best_row = availability_data.iloc[-1]

            st.success(
                f"🏆 **Most commonly available support:** "
                f"{best_row['Mechanism']} — "
                f"**{best_row['Availability']:.1f}%** of respondents "
                f"reported it as available."
            )

        else:

            st.markdown("### Treatment rate comparison")

            selected_support_mechanism = st.selectbox(
                "Choose a support mechanism",
                list(SUPPORT_LOOKUP.keys()),
                key="comparison_treatment_mechanism",
            )

            selected_column = SUPPORT_LOOKUP[
                selected_support_mechanism
            ]

            selected_title = next(
                title
                for column, title, icon in SUPPORT_FEATURES
                if column == selected_column
            )

            selected_color = SUPPORT_COLORS[
                selected_column
            ]["main"]

            treatment_data = get_treatment_data(
                selected_column
            )

            if treatment_data.empty:
                st.warning(
                    "No treatment-rate data is available "
                    "for this mechanism."
                )
            else:
                fig = build_treatment_chart(
                    treatment_data,
                    selected_title,
                    selected_color,
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                    config=CHART_CONFIG,
                    key="support_treatment_comparison",
                )

    if support_explorer == "🔎 Explore One Mechanism":

        st.markdown("### 🔎 Explore one workplace support mechanism")

        st.caption(
            "Select a mechanism to see how treatment rates differ "
            "across its response categories."
        )

        selected_support_detail = st.selectbox(
            "Choose mechanism",
            list(SUPPORT_DETAIL_LOOKUP.keys()),
            key="support_mechanism_detail",
        )

        (
            selected_column,
            selected_title,
            selected_icon,
        ) = SUPPORT_DETAIL_LOOKUP[
            selected_support_detail
        ]

        selected_palette = SUPPORT_COLORS[
            selected_column
        ]

        mechanism_data = get_treatment_data(
            selected_column
        )

        if mechanism_data.empty:
            st.warning(
                "No data is available for this mechanism."
            )
        else:

            fig = build_treatment_chart(
                mechanism_data,
                selected_title,
                selected_palette["main"],
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                config=CHART_CONFIG,
                key="support_mechanism_detail_chart",
            )

            highest = mechanism_data.loc[
                mechanism_data["Treatment Rate"].idxmax()
            ]

            lowest = mechanism_data.loc[
                mechanism_data["Treatment Rate"].idxmin()
            ]

            highest_rate = float(
                highest["Treatment Rate"]
            )

            lowest_rate = float(
                lowest["Treatment Rate"]
            )

            treatment_gap = (
                highest_rate - lowest_rate
            )

            st.markdown("### 📌 What stands out?")

            k1, k2, k3 = st.columns(3)

            with k1:
                st.metric(
                    "🏆 Highest Treatment Rate",
                    f"{highest_rate:.1f}%",
                    highest["Response"],
                )

            with k2:
                st.metric(
                    "📉 Lowest Treatment Rate",
                    f"{lowest_rate:.1f}%",
                    lowest["Response"],
                )

            with k3:
                st.metric(
                    "⚖️ Treatment-Rate Gap",
                    f"{treatment_gap:.1f} pp",
                    "Highest minus lowest",
                )

            st.info(
                f"{selected_icon} **Current finding:** "
                f"respondents in the **{highest['Response']}** "
                f"category show the highest treatment rate at "
                f"**{highest_rate:.1f}%**. "
                f"The difference between the highest and lowest "
                f"categories is **{treatment_gap:.1f} percentage points**."
            )

    section_title("🏆 Support Scoreboard")

    score_rows = []

    for column, title, icon in SUPPORT_FEATURES:

        availability = get_yes_rate(column)
        treatment_data = get_treatment_data(column)

        yes_rows = treatment_data[
            treatment_data["Response"] == "Yes"
        ]

        if yes_rows.empty:
            treatment_when_yes = None
        else:
            treatment_when_yes = float(
                yes_rows["Treatment Rate"].iloc[0]
            )

        score_rows.append(
            {
                "Support Mechanism": f"{icon} {title}",
                "Availability": availability,
                "Treatment Rate when Available": (
                    treatment_when_yes
                ),
                "Column": column,
            }
        )

    score_data = pd.DataFrame(score_rows)

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            name="Support Available",
            x=score_data["Support Mechanism"],
            y=score_data["Availability"],
            text=score_data["Availability"],
            texttemplate="%{text:.1f}%",
            textposition="outside",
            marker_color=[
                SUPPORT_COLORS[column]["main"]
                for column in score_data["Column"]
            ],
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Support available: <b>%{y:.1f}%</b>"
                "<extra></extra>"
            ),
        )
    )

    fig.add_trace(
        go.Scatter(
            name="Treatment Rate when Available",
            x=score_data["Support Mechanism"],
            y=score_data[
                "Treatment Rate when Available"
            ],
            mode="lines+markers+text",
            text=score_data[
                "Treatment Rate when Available"
            ],
            texttemplate="%{text:.1f}%",
            textposition="top center",
            line=dict(width=3),
            marker=dict(size=10),
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Treatment rate when available: "
                "<b>%{y:.1f}%</b>"
                "<extra></extra>"
            ),
        )
    )

    fig.update_layout(
        template=plotly_template(),
        height=500,
        title="Support Availability vs Treatment Rate",
        margin=dict(
            l=25,
            r=30,
            t=75,
            b=110,
        ),
        yaxis=dict(
            title="Percentage",
            range=[0, 100],
            ticksuffix="%",
        ),
        xaxis=dict(
            title="",
            tickangle=-25,
        ),
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.01,
            xanchor="left",
            x=0,
        ),
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config=CHART_CONFIG,
        key="support_scoreboard",
    )

    section_title("💡 Key Takeaway")

    availability_summary = [
        {
            "column": column,
            "title": title,
            "icon": icon,
            "rate": get_yes_rate(column),
        }
        for column, title, icon in SUPPORT_FEATURES
    ]

    availability_summary.sort(
        key=lambda x: x["rate"],
        reverse=True,
    )

    best = availability_summary[0]
    second = availability_summary[1]

    st.success(
        f"💡 **Support signal:** "
        f"{best['icon']} **{best['title']}** has the highest "
        f"reported availability at **{best['rate']:.1f}%**, "
        f"followed by {second['icon']} **{second['title']}** "
        f"at **{second['rate']:.1f}%**."
    )

    st.caption(
        "Treatment differences across support responses are "
        "associations within this observational survey and should "
        "not be interpreted as evidence of causation."
    )


# Workplace Culture

if active_section == "🤝 Workplace Culture":

    culture_section = st.segmented_control(
        "Culture view",
        options=[
            "🔀 Compare Signals",
            "🔍 Explore One Signal",
            "📊 Culture Dashboard",
        ],
        default="🔀 Compare Signals",
        key="culture_view_section",
        label_visibility="collapsed",
    )

    if culture_section is None:
        culture_section = "🔀 Compare Signals"

    signal_titles = [
        title
        for _, title, _ in CULTURE_FEATURES
    ]

    if culture_section == "🔀 Compare Signals":

        section_title(
            "🔀 Compare Workplace Culture Signals"
        )

        st.caption(
            "Choose two dimensions and compare them side-by-side in one interactive chart."
        )

        selector_one, selector_two = st.columns(2)

        with selector_one:

            st.markdown("**Signal 1**")

            culture_compare_one = st.segmented_control(
                "Select Signal 1",
                options=signal_titles,
                default="Coworker Support",
                key="culture_compare_signal_one",
                label_visibility="collapsed",
            )

        with selector_two:

            st.markdown("**Signal 2**")

            culture_compare_two = st.segmented_control(
                "Select Signal 2",
                options=signal_titles,
                default="Supervisor Support",
                key="culture_compare_signal_two",
                label_visibility="collapsed",
            )

        if culture_compare_one is None:
            culture_compare_one = "Coworker Support"

        if culture_compare_two is None:
            culture_compare_two = "Supervisor Support"

        if culture_compare_one == culture_compare_two:

            st.warning(
                "Please choose two different signals."
            )

        else:

            column_one, icon_one = CULTURE_LOOKUP[
                culture_compare_one
            ]

            column_two, icon_two = CULTURE_LOOKUP[
                culture_compare_two
            ]

            k1, k2 = st.columns(2)

            with k1:

                kpis_one = culture_signal_kpis(
                    column_one
                )

                st.markdown(
                    f"### {icon_one} {culture_compare_one}"
                )

                st.metric(
                    "Most common response",
                    kpis_one["top_response"],
                    f"{kpis_one['top_percentage']:.1f}%",
                )

            with k2:

                kpis_two = culture_signal_kpis(
                    column_two
                )

                st.markdown(
                    f"### {icon_two} {culture_compare_two}"
                )

                st.metric(
                    "Most common response",
                    kpis_two["top_response"],
                    f"{kpis_two['top_percentage']:.1f}%",
                )

            comparison_fig = make_culture_comparison_chart(
                column_one,
                culture_compare_one,
                column_two,
                culture_compare_two,
            )

            st.plotly_chart(
                comparison_fig,
                use_container_width=True,
                config=CHART_CONFIG,
                key=(
                    f"culture_compare_"
                    f"{column_one}_"
                    f"{column_two}"
                ),
            )

            st.caption(
                "Percentages show the distribution of responses "
                "within the survey population."
            )

    if culture_section == "🔍 Explore One Signal":

        section_title(
            "🔍 Explore One Culture Signal"
        )

        st.caption(
            "Select one workplace culture dimension and investigate its response pattern."
        )

        culture_explore_signal = st.segmented_control(
            "Choose a culture signal",
            options=signal_titles,
            default="Coworker Support",
            key="culture_explore_selector",
            label_visibility="collapsed",
        )

        if culture_explore_signal is None:
            culture_explore_signal = "Coworker Support"

        explore_column, explore_icon = CULTURE_LOOKUP[
            culture_explore_signal
        ]

        st.markdown(
            f"### {explore_icon} {culture_explore_signal}"
        )

        render_culture_signal_kpis(
            explore_column
        )

        explore_fig = make_culture_distribution_chart(
            explore_column,
            f"{culture_explore_signal} — Response Distribution",
            CULTURE_PALETTES[explore_column],
            horizontal=True,
        )

        st.plotly_chart(
            explore_fig,
            use_container_width=True,
            config=CHART_CONFIG,
            key=f"culture_explore_{explore_column}",
        )

        render_culture_signal_summary(
            explore_column,
            culture_explore_signal,
        )

    if culture_section == "📊 Culture Dashboard":

        section_title(
            "📊 Workplace Culture Dashboard"
        )

        st.caption(
            "Choose one dimension at a time. The chart and KPI cards update automatically."
        )

        culture_dashboard_signal = st.segmented_control(
            "Choose a dashboard dimension",
            options=signal_titles,
            default="Coworker Support",
            key="culture_dashboard_selector",
            label_visibility="collapsed",
        )

        if culture_dashboard_signal is None:
            culture_dashboard_signal = "Coworker Support"

        dashboard_column, dashboard_icon = CULTURE_LOOKUP[
            culture_dashboard_signal
        ]

        st.markdown(
            f"### {dashboard_icon} {culture_dashboard_signal}"
        )

        dashboard_kpis = culture_signal_kpis(
            dashboard_column
        )

        k1, k2, k3, k4 = st.columns(4)

        with k1:
            st.metric(
                "👥 Respondents",
                f"{dashboard_kpis['total']:,}",
            )

        with k2:
            st.metric(
                "🏆 Highest Response",
                dashboard_kpis["top_response"],
            )

        with k3:
            st.metric(
                "📈 Highest Share",
                f"{dashboard_kpis['top_percentage']:.1f}%",
            )

        with k4:
            st.metric(
                "📏 Gap vs #2",
                f"{dashboard_kpis['gap']:.1f} pp",
            )

        dashboard_fig = make_culture_distribution_chart(
            dashboard_column,
            f"{dashboard_icon} {culture_dashboard_signal} — Response Distribution",
            CULTURE_PALETTES[dashboard_column],
            horizontal=False,
        )

        st.plotly_chart(
            dashboard_fig,
            use_container_width=True,
            config=CHART_CONFIG,
            key=f"culture_dashboard_{dashboard_column}",
        )

        st.markdown("### 📋 Response Breakdown")

        breakdown = culture_distribution(
            dashboard_column
        ).copy()

        breakdown["Percentage"] = (
            breakdown["Percentage"].round(1)
        )

        breakdown = breakdown.rename(
            columns={
                "Percentage": "Share",
            }
        )

        st.dataframe(
            breakdown,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Response": st.column_config.TextColumn(
                    "Response"
                ),
                "Respondents": st.column_config.NumberColumn(
                    "Respondents",
                    format="%d",
                ),
                "Share": st.column_config.NumberColumn(
                    "Share (%)",
                    format="%.1f%%",
                ),
            },
        )

    section_title("🚦 Culture Signal Summary")

    summary_data = [
        (
            "🧠 Mental Health Consequence: Yes",
            filtered[
                "mental_health_consequence"
            ].eq("Yes").mean() * 100,
        ),
        (
            "🎤 Mental Health Interview: Yes",
            filtered[
                "mental_health_interview"
            ].eq("Yes").mean() * 100,
        ),
        (
            "⚖️ Mental vs Physical: Yes",
            filtered[
                "mental_vs_physical"
            ].eq("Yes").mean() * 100,
        ),
    ]

    s1, s2, s3 = st.columns(3)

    for container, (label, value) in zip(
        (s1, s2, s3),
        summary_data,
    ):
        with container:
            st.metric(
                label,
                f"{value:.1f}%",
            )

    section_title("💡 Culture Takeaway")

    strongest = max(
        summary_data,
        key=lambda item: item[1],
    )

    st.info(
        f"**Strongest headline signal:** "
        f"{strongest[0]} is the highest of the three "
        f"summary indicators at **{strongest[1]:.1f}%**."
    )

    st.caption(
        "Source: 2014 Mental Health in Tech Survey • "
        "Observed relationships are associations, not evidence of causation."
    )


# Dynamic page-specific sidebar
# The sidebar contains only decision-useful statistics from the active view.


def sidebar_escape(value):
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


def sidebar_plain_label(value):
    text = str(value)
    for prefix in ["🧩 ", "🔎 ", "📊 ", "🔀 "]:
        text = text.replace(prefix, "")
    return text


def sidebar_stat(label, value, accent=False):
    accent_class = " mh-sidebar-stat-accent" if accent else ""
    return (
        f'<div class="mh-sidebar-stat{accent_class}">'
        f'<div class="mh-sidebar-stat-label">{sidebar_escape(label)}</div>'
        f'<div class="mh-sidebar-stat-value">{value}</div>'
        f'</div>'
    )


respondent_count = f"{len(filtered):,}"
sidebar_section = ""
sidebar_subtitle = ""
sidebar_stats_html = ""

if active_section == "🛟 Support & Resources":
    sidebar_section = "🛟 Support & Resources"

    if support_explorer == "🧩 Compare Support":
        if support_comparison_mode == "Support Availability":
            availability_values = []

            for column, title, icon in SUPPORT_FEATURES:
                availability_values.append(
                    {
                        "title": title,
                        "rate": get_yes_rate(column),
                    }
                )

            availability_values = sorted(
                availability_values,
                key=lambda x: x["rate"],
            )

            lowest = availability_values[0]
            highest = availability_values[-1]
            average = sum(x["rate"] for x in availability_values) / len(availability_values)
            spread = highest["rate"] - lowest["rate"]

            sidebar_subtitle = "Support availability"
            sidebar_stats_html = (
                sidebar_stat("Highest availability", f"{highest['rate']:.1f}%", True)
                + sidebar_stat("Most available", sidebar_escape(highest["title"]))
                + sidebar_stat("Lowest availability", f"{lowest['rate']:.1f}%")
                + sidebar_stat("Availability spread", f"{spread:.1f} pp")
                + sidebar_stat("Average across 6 mechanisms", f"{average:.1f}%")
            )

        else:
            sidebar_column = SUPPORT_LOOKUP.get(
                selected_support_mechanism,
                "benefits",
            )
            treatment_data = get_treatment_data(sidebar_column)
            sidebar_title = sidebar_plain_label(selected_support_mechanism)

            if not treatment_data.empty:
                high = treatment_data.loc[treatment_data["Treatment Rate"].idxmax()]
                low = treatment_data.loc[treatment_data["Treatment Rate"].idxmin()]
                overall_treatment = grouped_treatment_rate(filtered, sidebar_column)
                overall_treatment_rate = (
                    filtered["treatment"].eq("Yes").mean() * 100
                    if "treatment" in filtered.columns and len(filtered)
                    else 0.0
                )
                gap = float(high["Treatment Rate"]) - float(low["Treatment Rate"])

                sidebar_subtitle = f"Treatment rates · {sidebar_title}"
                sidebar_stats_html = (
                    sidebar_stat("Highest treatment", f"{float(high['Treatment Rate']):.1f}%", True)
                    + sidebar_stat("Response", sidebar_escape(high["Response"]))
                    + sidebar_stat("Lowest treatment", f"{float(low['Treatment Rate']):.1f}%")
                    + sidebar_stat("Treatment gap", f"{gap:.1f} pp")
                    + sidebar_stat("Overall treatment", f"{overall_treatment_rate:.1f}%")
                )
            else:
                sidebar_subtitle = f"Treatment rates · {sidebar_title}"
                sidebar_stats_html = sidebar_stat("Data", "No treatment breakdown available")

    else:
        detail_column = SUPPORT_DETAIL_LOOKUP.get(
            selected_support_detail,
            ("benefits", "Mental Health Benefits", "💚"),
        )[0]
        detail_title = sidebar_plain_label(selected_support_detail)
        detail_data = get_treatment_data(detail_column)
        availability_rate = get_yes_rate(detail_column)
        overall_treatment_rate = (
            filtered["treatment"].eq("Yes").mean() * 100
            if "treatment" in filtered.columns and len(filtered)
            else 0.0
        )

        sidebar_subtitle = f"Mechanism detail · {detail_title}"

        if not detail_data.empty:
            high = detail_data.loc[detail_data["Treatment Rate"].idxmax()]
            low = detail_data.loc[detail_data["Treatment Rate"].idxmin()]
            gap = float(high["Treatment Rate"]) - float(low["Treatment Rate"])

            sidebar_stats_html = (
                sidebar_stat("Support available", f"{availability_rate:.1f}%", True)
                + sidebar_stat("Highest treatment", f"{float(high['Treatment Rate']):.1f}%")
                + sidebar_stat("Highest-response group", sidebar_escape(high["Response"]))
                + sidebar_stat("Lowest treatment", f"{float(low['Treatment Rate']):.1f}%")
                + sidebar_stat("Treatment gap", f"{gap:.1f} pp")
            )
        else:
            sidebar_stats_html = sidebar_stat("Support available", f"{availability_rate:.1f}%", True)

else:
    sidebar_section = "🤝 Workplace Culture"

    if culture_section == "🔀 Compare Signals":
        column_one, icon_one = CULTURE_LOOKUP[culture_compare_one]
        column_two, icon_two = CULTURE_LOOKUP[culture_compare_two]
        kpis_one = culture_signal_kpis(column_one)
        kpis_two = culture_signal_kpis(column_two)

        sidebar_subtitle = "Two-signal comparison"
        sidebar_stats_html = (
            '<div class="mh-sidebar-compare">'
            f'<div class="mh-sidebar-compare-name">{sidebar_escape(culture_compare_one)}</div>'
            f'{sidebar_stat("Top response", sidebar_escape(kpis_one["top_response"]))}'
            f'{sidebar_stat("Top share", f"{kpis_one["top_percentage"]:.1f}%", True)}'
            '</div>'
            '<div class="mh-sidebar-compare">'
            f'<div class="mh-sidebar-compare-name">{sidebar_escape(culture_compare_two)}</div>'
            f'{sidebar_stat("Top response", sidebar_escape(kpis_two["top_response"]))}'
            f'{sidebar_stat("Top share", f"{kpis_two["top_percentage"]:.1f}%", True)}'
            '</div>'
        )

    elif culture_section == "🔍 Explore One Signal":
        column, icon = CULTURE_LOOKUP[culture_explore_signal]
        kpis = culture_signal_kpis(column)

        sidebar_subtitle = f"Signal detail · {culture_explore_signal}"
        sidebar_stats_html = (
            sidebar_stat("Respondents", f"{kpis['total']:,}", True)
            + sidebar_stat("Most common response", sidebar_escape(kpis["top_response"]))
            + sidebar_stat("Top response share", f"{kpis['top_percentage']:.1f}%")
            + sidebar_stat("Second response", sidebar_escape(kpis["second_response"]))
            + sidebar_stat("Gap vs #2", f"{kpis['gap']:.1f} pp")
        )

    else:
        column, icon = CULTURE_LOOKUP[culture_dashboard_signal]
        kpis = culture_signal_kpis(column)

        sidebar_subtitle = f"Dashboard signal · {culture_dashboard_signal}"
        sidebar_stats_html = (
            sidebar_stat("Most common response", sidebar_escape(kpis["top_response"]), True)
            + sidebar_stat("Top response share", f"{kpis['top_percentage']:.1f}%")
            + sidebar_stat("Second response", sidebar_escape(kpis["second_response"]))
            + sidebar_stat("Gap vs #2", f"{kpis['gap']:.1f} pp")
            + sidebar_stat("Respondents", f"{kpis['total']:,}")
        )

sidebar_html = f"""
<div class="mh-sidebar-intelligence">
    <div class="mh-sidebar-title">
        <span class="mh-sidebar-pin">📌</span>
        <span>Page Intelligence</span>
    </div>

    <div class="mh-sidebar-respondents">
        <div class="mh-sidebar-label">RESPONDENTS</div>
        <div class="mh-sidebar-number">{sidebar_escape(respondent_count)}</div>
    </div>

    <div class="mh-sidebar-section">
        <div class="mh-sidebar-section-name">{sidebar_escape(sidebar_section)}</div>
        <div class="mh-sidebar-subtitle">{sidebar_escape(sidebar_subtitle)}</div>
        <div class="mh-sidebar-stats">
            {sidebar_stats_html}
        </div>
    </div>
</div>
"""

st.sidebar.html(sidebar_html)

# Page footer

st.markdown("---")

st.caption(
    "Source: 2014 Mental Health in Tech Survey • "
    "Workplace Support combines support resources and workplace culture "
    "into two focused analysis tabs."
)
