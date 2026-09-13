from pathlib import Path

import streamlit as st

from utils.styling import apply_global_style, page_header
from utils.data_loader import load_data


st.set_page_config(
    page_title="Mental Health in Tech Analytics",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_global_style()

PROJECT_DIR = Path(__file__).resolve().parent
PAGES_DIR = PROJECT_DIR / "pages"


# Current project page files
PAGE_FILES = {
    "respondent_profile": "2_Respondent_Profile.py",
    "workplace_support_&_culture": "3_Workplace_Support_&_Culture.py",
    "mental_health_treatment": "4_Mental_Health_&_Treatment.py",
    "statistical_analysis": "5_Statistical_Analysis.py",
    "executive_insights": "6_Executive_Insights.py",
}


def get_page_path(page_key):
    """Return a page path relative to app.py for st.page_link()."""
    filename = PAGE_FILES.get(page_key)

    if not filename:
        return None

    page_path = PAGES_DIR / filename

    if not page_path.exists():
        return None

    return page_path.relative_to(PROJECT_DIR).as_posix()


# Load the cleaned survey so the Overview KPIs are data-driven.
try:
    df = load_data()
except Exception:
    df = None


def treatment_rate(data):
    if data is None or data.empty or "treatment" not in data.columns:
        return 0.0

    values = data["treatment"].astype(str).str.strip().str.lower()
    valid = values.isin(["yes", "no"])

    if not valid.any():
        return 0.0

    return float((values[valid] == "yes").mean() * 100)


def family_history_rate(data):
    if data is None or data.empty or "family_history" not in data.columns:
        return 0.0

    values = data["family_history"].astype(str).str.strip().str.lower()
    valid = values.isin(["yes", "no"])

    if not valid.any():
        return 0.0

    return float((values[valid] == "yes").mean() * 100)


def often_work_interference_rate(data):
    if data is None or data.empty or "work_interfere" not in data.columns:
        return 0.0

    values = data["work_interfere"].astype(str).str.strip().str.lower()
    valid = values != "not answered"

    if not valid.any():
        return 0.0

    return float((values[valid] == "often").mean() * 100)


# Overview styling
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1.25rem;
        padding-bottom: 2.5rem;
    }


    /* Streamlit multipage navigation */
    /* Make Overview + every page entry larger and button-like. */
    [data-testid="stSidebarNav"] {
        padding: 4px 0 12px 0 !important;
    }

    [data-testid="stSidebarNav"] ul {
        display: flex !important;
        flex-direction: column !important;
        gap: 6px !important;
        padding: 0 0 12px 0 !important;
        margin: 0 !important;
        border-bottom: 1px solid rgba(148, 163, 184, 0.24) !important;
    }

    [data-testid="stSidebarNav"] li {
        margin: 0 !important;
        padding: 0 !important;
        width: 100% !important;
    }

    [data-testid="stSidebarNav"] a {
        display: flex !important;
        align-items: center !important;
        width: 100% !important;
        min-height: 44px !important;
        box-sizing: border-box !important;
        padding: 9px 12px !important;
        margin: 0 !important;
        border: 1px solid transparent !important;
        border-radius: 10px !important;
        background: transparent !important;
        color: #f1f5f9 !important;
        text-decoration: none !important;
        font-size: 0.96rem !important;
        line-height: 1.2 !important;
        font-weight: 750 !important;
        transition:
            background 0.16s ease,
            border-color 0.16s ease,
            transform 0.16s ease,
            box-shadow 0.16s ease !important;
    }

    [data-testid="stSidebarNav"] a:hover {
        background: rgba(45, 212, 191, 0.10) !important;
        border-color: rgba(45, 212, 191, 0.30) !important;
        color: #ffffff !important;
        transform: translateX(2px) !important;
    }

    [data-testid="stSidebarNav"] a[aria-current="page"],
    [data-testid="stSidebarNav"] a[aria-current="true"] {
        background: linear-gradient(
            90deg,
            rgba(45, 212, 191, 0.15),
            rgba(96, 165, 250, 0.12)
        ) !important;
        border-color: rgba(45, 212, 191, 0.24) !important;
        color: #ffffff !important;
        box-shadow: inset 3px 0 0 #2dd4bf !important;
    }

    [data-testid="stSidebarNav"] a span {
        font-size: 0.96rem !important;
        font-weight: 750 !important;
        line-height: 1.2 !important;
    }

    /* Keep the navigation icon aligned and slightly larger. */
    [data-testid="stSidebarNav"] a svg {
        width: 1.05rem !important;
        height: 1.05rem !important;
        margin-right: 7px !important;
    }

    /* Give the navigation block a little more breathing room
       before the Project Information card. */
    [data-testid="stSidebarNav"] + div {
        margin-top: 4px !important;
    }

    /* Project Information sidebar */
    [data-testid="stSidebar"] {
        background: #0b1020;
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 0.8rem;
    }

    .project-sidebar {
        width: 100%;
        box-sizing: border-box;
        border: 1px solid rgba(139, 92, 246, 0.75);
        border-radius: 17px;
        background: linear-gradient(
            145deg,
            rgba(22, 29, 52, 0.98),
            rgba(12, 18, 35, 0.99)
        );
        padding: 14px;
    }

    .project-sidebar-title {
        color: #f8fafc;
        font-size: 1.02rem;
        line-height: 1.25;
        font-weight: 850;
        margin: 1px 0 12px 0;
    }

    .sidebar-card {
        border: 1px solid rgba(71, 85, 105, 0.55);
        border-radius: 12px;
        background: rgba(15, 23, 42, 0.72);
        padding: 11px;
        margin-bottom: 9px;
        box-sizing: border-box;
    }

    .sidebar-card.author-card {
        border-color: rgba(20, 184, 166, 0.55);
        background: linear-gradient(
            145deg,
            rgba(20, 184, 166, 0.12),
            rgba(15, 23, 42, 0.82)
        );
    }

    .sidebar-label {
        color: #60a5fa;
        font-size: 0.57rem;
        line-height: 1;
        letter-spacing: 0.10em;
        text-transform: uppercase;
        font-weight: 850;
        margin-bottom: 8px;
    }

    .sidebar-name {
        color: #f8fafc;
        font-size: 0.88rem;
        line-height: 1.25;
        font-weight: 850;
        margin-bottom: 4px;
    }

    .sidebar-role {
        color: #2dd4bf;
        font-size: 0.61rem;
        line-height: 1.3;
        font-weight: 750;
    }

    .sidebar-project-title {
        color: #f8fafc;
        font-size: 0.76rem;
        line-height: 1.3;
        font-weight: 850;
        margin-bottom: 5px;
    }

    .sidebar-description {
        color: #cbd5e1;
        font-size: 0.60rem;
        line-height: 1.5;
    }

    .sidebar-stat-row {
        display: flex;
        justify-content: space-between;
        gap: 10px;
        padding: 7px 0;
        border-bottom: 1px solid rgba(71, 85, 105, 0.35);
        color: #e2e8f0;
        font-size: 0.60rem;
    }

    .sidebar-stat-row:last-child {
        border-bottom: 0;
        padding-bottom: 1px;
    }

    .sidebar-stat-value {
        color: #f8fafc;
        font-weight: 850;
        text-align: right;
    }

    .toolkit {
        display: flex;
        flex-wrap: wrap;
        gap: 5px;
    }

    .tool {
        display: inline-block;
        border: 1px solid rgba(96, 165, 250, 0.30);
        border-radius: 7px;
        background: rgba(30, 41, 59, 0.90);
        color: #f8fafc;
        padding: 5px 7px;
        font-size: 0.56rem;
        line-height: 1;
        font-weight: 750;
    }

    .sidebar-list {
        color: #e2e8f0;
        font-size: 0.60rem;
        line-height: 1.55;
    }

    .sidebar-list div {
        margin-bottom: 1px;
    }

    /* KPI row */
    .overview-kpi {
        border: 1px solid rgba(139, 92, 246, 0.35);
        border-radius: 16px;
        padding: 17px 19px 15px 19px;
        min-height: 82px;
        background: linear-gradient(
            145deg,
            rgba(30, 41, 72, 0.78),
            rgba(20, 29, 51, 0.92)
        );
        box-sizing: border-box;
    }

    .overview-kpi-label {
        font-size: 0.82rem;
        font-weight: 600;
        opacity: 0.88;
        margin-bottom: 5px;
    }

    .overview-kpi-value {
        font-size: 1.75rem;
        line-height: 1;
        font-weight: 850;
    }

    /* Explore heading */
    .explore-heading {
        margin-top: 27px;
        margin-bottom: 3px;
    }

    .explore-caption {
        opacity: 0.70;
        margin-bottom: 15px;
    }

    /* Navigation card links */
    [data-testid="stPageLink"] {
        display: block !important;
        width: 100% !important;
        max-width: none !important;
        min-width: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        box-sizing: border-box !important;
    }

    [data-testid="stPageLink"] a {
        display: flex !important;
        width: 100% !important;
        max-width: none !important;
        min-width: 0 !important;
        height: 104px !important;
        min-height: 104px !important;
        max-height: 104px !important;
        box-sizing: border-box !important;
        display: flex !important;
        align-items: center !important;
        justify-content: space-between !important;
        gap: 18px !important;
        padding: 17px 20px !important;
        overflow: hidden !important;
        border-radius: 16px !important;
        border: 1px solid rgba(148, 163, 184, 0.22) !important;
        background: linear-gradient(
            145deg,
            rgba(25, 35, 58, 0.94),
            rgba(18, 27, 47, 0.97)
        ) !important;
        text-decoration: none !important;
        box-shadow: 0 7px 20px rgba(15, 23, 42, 0.10) !important;
        transition:
            transform 0.18s ease,
            border-color 0.18s ease,
            box-shadow 0.18s ease,
            background 0.18s ease !important;
        position: relative !important;
        overflow: hidden !important;
    }

    [data-testid="stPageLink"] a:hover {
        transform: translateY(-2px) !important;
        border-color: rgba(167, 139, 250, 0.62) !important;
        background: linear-gradient(
            145deg,
            rgba(30, 42, 70, 0.98),
            rgba(20, 31, 53, 0.99)
        ) !important;
        box-shadow: 0 12px 28px rgba(15, 23, 42, 0.17) !important;
    }

    [data-testid="stPageLink"] a::after {
        content: "→";
        flex: 0 0 auto;
        font-size: 1.45rem;
        font-weight: 800;
        margin-left: auto;
        opacity: 0.95;
    }

    /* Color-coded left accents */
    .nav-teal [data-testid="stPageLink"] a {
        border-left: 4px solid #2DD4BF !important;
    }

    .nav-purple [data-testid="stPageLink"] a {
        border-left: 4px solid #A78BFA !important;
    }

    .nav-blue [data-testid="stPageLink"] a {
        border-left: 4px solid #60A5FA !important;
    }

    .nav-pink [data-testid="stPageLink"] a {
        border-left: 4px solid #F472B6 !important;
    }

    .nav-amber [data-testid="stPageLink"] a {
        border-left: 4px solid #F59E0B !important;
    }

    /* Page-link label */
    [data-testid="stPageLink"] a p {
        white-space: pre-line !important;
        line-height: 1.45 !important;
        margin: 0 !important;
        font-size: 0.82rem !important;
        font-weight: 500 !important;
        opacity: 0.90;
        overflow: hidden !important;
    }

    /* Larger page titles inside each navigation card */
    [data-testid="stPageLink"] a strong {
        font-size: 1.02rem !important;
        line-height: 1.25 !important;
        font-weight: 850 !important;
    }

    /* Snapshot */
    .snapshot-heading {
        margin-top: 31px;
        margin-bottom: 10px;
    }

    .snapshot-text {
        font-size: 0.94rem;
        line-height: 1.7;
        opacity: 0.84;
        margin-bottom: 10px;
    }

    .overview-footer {
        border-top: 1px solid rgba(148, 163, 184, 0.18);
        margin-top: 28px;
        padding-top: 15px;
        opacity: 0.58;
        font-size: 0.80rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# Overview metrics
# These values must be calculated before the sidebar because the sidebar
# displays the same project snapshot.
respondents = len(df) if df is not None else 1259
treatment = treatment_rate(df) if df is not None else 50.6
family_history = family_history_rate(df) if df is not None else 39.1
often_interference = (
    often_work_interference_rate(df) if df is not None else 11.4
)

# Sidebar
with st.sidebar:
    sidebar_html = f"""
    <div class="project-sidebar">

        <div class="project-sidebar-title">
            📌 Project Information
        </div>

        <div class="sidebar-card author-card">
            <div class="sidebar-label">Author</div>
            <div class="sidebar-name">Kartikey Singh</div>
            <div class="sidebar-role">Data Analytics Project</div>
        </div>

        <div class="sidebar-card">
            <div class="sidebar-label">Project</div>
            <div class="sidebar-project-title">
                Mental Health in Tech Analytics
            </div>
            <div class="sidebar-description">
                Interactive analysis of mental-health experiences within the
                technology workplace.
            </div>
        </div>

        <div class="sidebar-card">
            <div class="sidebar-label">Dataset</div>
            <div class="sidebar-project-title">
                2014 Mental Health in Tech Survey
            </div>
            <div class="sidebar-description">
                Survey responses covering mental health, treatment,
                workplace support, culture, and demographics.
            </div>
        </div>

        <div class="sidebar-card">
            <div class="sidebar-label">Project Snapshot</div>

            <div class="sidebar-stat-row">
                <span>Respondents</span>
                <span class="sidebar-stat-value">{respondents:,}</span>
            </div>

            <div class="sidebar-stat-row">
                <span>Treatment rate</span>
                <span class="sidebar-stat-value">{treatment:.1f}%</span>
            </div>

            <div class="sidebar-stat-row">
                <span>Survey year</span>
                <span class="sidebar-stat-value">2014</span>
            </div>

            <div class="sidebar-stat-row">
                <span>Analytical focus</span>
                <span class="sidebar-stat-value">Mental health</span>
            </div>
        </div>

        <div class="sidebar-card">
            <div class="sidebar-label">Analytics Toolkit</div>

            <div class="toolkit">
                <span class="tool">Python</span>
                <span class="tool">Pandas</span>
                <span class="tool">Plotly</span>
                <span class="tool">Streamlit</span>
                <span class="tool">Statistics</span>
                <span class="tool">EDA</span>
            </div>
        </div>

        <div class="sidebar-card">
            <div class="sidebar-label">Analytical Areas</div>

            <div class="sidebar-list">
                <div>Respondent Profile</div>
                <div>Mental Health &amp; Treatment</div>
                <div>Workplace Support</div>
                <div>Workplace Culture</div>
                <div>Statistical Analysis</div>
                <div>Executive Insights</div>
            </div>
        </div>

    </div>
    """

    st.html(sidebar_html)


# Main header
st.markdown('<div style="height:0.25rem;"></div>', unsafe_allow_html=True)

page_header(
    "🧠 Mental Health in Tech Analytics",
    "Interactive Survey Intelligence",
    "Explore demographic patterns, mental-health experiences, workplace support & culture, treatment behavior, and statistically validated relationships.",
)


kpi_data = [
    ("👥", "Survey Respondents", f"{respondents:,}"),
    ("💚", "Treatment Rate", f"{treatment:.1f}%"),
    ("🧬", "Family History", f"{family_history:.1f}%"),
    ("⚡", "Work Interference: Often", f"{often_interference:.1f}%"),
]

kpi_columns = st.columns(4, gap="medium")

for column, (icon, label, value) in zip(kpi_columns, kpi_data):
    with column:
        st.html(
            f"""
            <div class="overview-kpi">
                <div class="overview-kpi-label">{icon} {label}</div>
                <div class="overview-kpi-value">{value}</div>
            </div>
            """
        )


# Explore the analytics
st.markdown(
    '<h3 class="explore-heading">🧭 Explore the Analytics</h3>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="explore-caption">'
    "Choose an analysis area below. Click anywhere on a card or its arrow "
    "to open the interactive page."
    "</div>",
    unsafe_allow_html=True,
)


cards = [
    {
        "key": "respondent_profile",
        "icon": "👥",
        "title": "Respondent Profile",
        "description": "Explore respondent profiles across gender, age, company size, countries, and work arrangements.",
        "accent": "nav-teal",
    },
    {
        "key": "mental_health_treatment",
        "icon": "🧠",
        "title": "Mental Health & Treatment",
        "description": "Investigate treatment behavior, family history, work interference, consequences, and treatment gaps.",
        "accent": "nav-purple",
    },
    {
        "key": "workplace_support_&_culture",
        "icon": "🏢",
        "title": "Workplace Support & Culture",
        "description": "Explore benefits, care options, wellness programs, anonymity, leave, and workplace culture.",
        "accent": "nav-blue",
    },
    {
        "key": "statistical_analysis",
        "icon": "📊",
        "title": "Statistical Analysis",
        "description": "Use Chi-square tests and Cramér's V to validate important associations.",
        "accent": "nav-amber",
    },
    {
        "key": "executive_insights",
        "icon": "💡",
        "title": "Executive Insights",
        "description": "Translate the strongest findings into actionable business recommendations.",
        "accent": "nav-pink",
    },
]


for row_start in range(0, len(cards), 2):
    row = cards[row_start:row_start + 2]
    columns = st.columns([1, 1], gap="medium")

    for column, card in zip(columns, row):
        with column:
            page_path = get_page_path(card["key"])

            st.markdown(
                f'<div class="{card["accent"]}">',
                unsafe_allow_html=True,
            )

            if page_path:
                # The complete card is the native Streamlit page link.
                # This makes the whole card clickable, not just the arrow.
                st.page_link(
                    page_path,
                    label=(
                        f"{card['icon']}  **{card['title']}**  \n"
                        f"{card['description']}"
                    ),
                    width="stretch",
                )
            else:
                st.error(
                    f"Page file missing: {PAGE_FILES[card['key']]}",
                    icon="⚠️",
                )

            st.markdown("</div>", unsafe_allow_html=True)

    if row_start + 2 < len(cards):
        st.markdown('<div style="height:18px;"></div>', unsafe_allow_html=True)


# Dashboard overview
st.markdown(
    '<h3 class="snapshot-heading">📌 Dashboard Overview</h3>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="snapshot-text">'
    "This dashboard analyzes the <strong>2014 Mental Health in Tech Survey</strong> "
    "to understand how mental-health experiences relate to treatment behavior, "
    "workplace support, and workplace culture."
    "</div>",
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="snapshot-text">'
    "The analytical flow moves from <strong>respondent profiles</strong>, to "
    "<strong>what they experienced</strong>, to <strong>how workplace factors "
    "relate to treatment</strong>, and finally to <strong>statistical validation "
    "and executive insights</strong>."
    "</div>",
    unsafe_allow_html=True,
)

st.html(
    """
    <div class="overview-footer">
        Source: 2014 Mental Health in Tech Survey ·
        Built with Python, Pandas, Plotly, Streamlit, and statistical testing.
    </div>
    """
)
