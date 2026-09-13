import streamlit as st
import re


def is_dark_mode():
    try:
        return st.get_option("theme.base") != "light"
    except Exception:
        return True


def apply_global_style():
    dark = is_dark_mode()

    if dark:
        theme = {
            "bg": "#0B1020",
            "sidebar": "#10162A",
            "card": "#151D32",
            "card2": "#19233B",
            "text": "#F5F7FF",
            "muted": "#AAB4CC",
            "border": "rgba(167, 139, 250, 0.24)",
            "purple": "#A78BFA",
            "teal": "#5EEAD4",
            "green": "#86EFAC",
            "glow": "rgba(94, 234, 212, 0.12)",
        }
    else:
        theme = {
            "bg": "#F6FAF9",
            "sidebar": "#EDF5F3",
            "card": "#FFFFFF",
            "card2": "#F3F8F6",
            "text": "#17212B",
            "muted": "#53636D",
            "border": "rgba(40, 75, 72, 0.22)",
            "purple": "#6948D9",
            "teal": "#087F73",
            "green": "#277A4A",
            "glow": "rgba(8, 127, 115, 0.09)",
        }

    css = """
    <style>

    :root {
        --mh-bg: __BG__;
        --mh-sidebar: __SIDEBAR__;
        --mh-card: __CARD__;
        --mh-card2: __CARD2__;
        --mh-text: __TEXT__;
        --mh-muted: __MUTED__;
        --mh-border: __BORDER__;
        --mh-purple: __PURPLE__;
        --mh-teal: __TEAL__;
        --mh-green: __GREEN__;
        --mh-glow: __GLOW__;
    }

    /* Main application */
    html, body, [data-testid="stApp"], [data-testid="stAppViewContainer"] {
        background: var(--mh-bg) !important;
        color: var(--mh-text) !important;
    }

    [data-testid="stAppViewContainer"] {
        background:
            radial-gradient(circle at 88% 0%, var(--mh-glow), transparent 28%),
            var(--mh-bg) !important;
    }

    /* Keep Streamlit's Deploy and menu controls visible */
    [data-testid="stHeader"],
    header[data-testid="stHeader"] {
        background: var(--mh-bg) !important;
        box-shadow: none !important;
        color: var(--mh-text) !important;
    }

    [data-testid="stToolbar"] {
        display: flex !important;
    }

    [data-testid="stToolbar"] button,
    [data-testid="stToolbar"] button span,
    [data-testid="stToolbar"] svg {
        color: var(--mh-text) !important;
    }

    [data-testid="stDecoration"] {
        display: none !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"],
    [data-testid="stSidebar"] > div:first-child {
        background: var(--mh-sidebar) !important;
        color: var(--mh-text) !important;
        border-right: 1px solid var(--mh-border);
    }

    [data-testid="stSidebar"] * {
        color: var(--mh-text);
    }

    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span {
        color: var(--mh-text) !important;
    }

    /* Streamlit page navigation */
    [data-testid="stSidebarNav"] a,
    [data-testid="stSidebarNav"] span,
    [data-testid="stSidebarNav"] p {
        color: var(--mh-text) !important;
        font-weight: 600 !important;
    }

    [data-testid="stSidebarNav"] a:hover {
        background: var(--mh-glow) !important;
        color: var(--mh-teal) !important;
        border-radius: 9px;
    }

    [data-testid="stSidebarNav"] a[aria-current="page"] {
        background: var(--mh-glow) !important;
        color: var(--mh-teal) !important;
        border-radius: 9px;
        font-weight: 800 !important;
    }

    /* Main content */
    .block-container {
        max-width: 1500px;
        padding-top: 1.5rem !important;
        padding-bottom: 3rem !important;
    }

    /* Hero */
    .hero {
        padding: .8rem 0 1.1rem;
    }

    .hero-kicker {
        display: inline-flex;
        align-items: center;
        padding: .35rem .7rem;
        border-radius: 999px;
        background: var(--mh-glow);
        border: 1px solid var(--mh-border);
        color: var(--mh-teal) !important;
        font-size: .7rem;
        font-weight: 850;
        letter-spacing: .06em;
        text-transform: uppercase;
        margin-bottom: .75rem;
    }

    .hero-title {
        font-size: clamp(2.1rem, 4vw, 3.35rem);
        font-weight: 850;
        line-height: 1.03;
        letter-spacing: -.045em;
        color: var(--mh-text) !important;
    }

    .hero-subtitle {
        margin-top: .55rem;
        font-size: 1.2rem;
        font-weight: 750;
        color: var(--mh-text) !important;
    }

    .hero-description {
        margin-top: .45rem;
        max-width: 1050px;
        color: var(--mh-muted) !important;
        line-height: 1.65;
    }

    .section-title {
        font-size: 1.55rem;
        font-weight: 820;
        letter-spacing: -.025em;
        margin: 1.55rem 0 .75rem;
        color: var(--mh-text) !important;
    }

    /* Sidebar custom branding */
    .sidebar-brand {
        padding: .3rem .05rem 1rem;
    }

    .sidebar-brand-title {
        font-size: 1.15rem;
        font-weight: 820;
        color: var(--mh-text) !important;
    }

    .sidebar-brand-sub {
        color: var(--mh-muted) !important;
        font-size: .75rem;
    }

    /* Gamification */
    .journey-card {
        margin: .5rem 0 1rem;
        padding: .9rem;
        border: 1px solid var(--mh-border);
        border-radius: 16px;
        background: linear-gradient(135deg, var(--mh-card), var(--mh-card2));
        box-shadow: 0 8px 28px rgba(0, 0, 0, .08);
    }

    .journey-top {
        display: flex;
        justify-content: space-between;
        margin-bottom: .55rem;
    }

    .journey-title {
        color: var(--mh-text) !important;
        font-weight: 780;
        font-size: .86rem;
    }

    .journey-xp {
        color: var(--mh-teal) !important;
        font-size: .76rem;
        font-weight: 850;
    }

    .xp-track {
        height: 7px;
        border-radius: 20px;
        background: rgba(127, 127, 127, .16);
        overflow: hidden;
    }

    .xp-fill {
        height: 100%;
        border-radius: 20px;
        background: linear-gradient(90deg, var(--mh-purple), var(--mh-teal));
    }

    .badge-row {
        display: flex;
        gap: .3rem;
        margin-top: .6rem;
        flex-wrap: wrap;
    }

    .badge {
        padding: .23rem .45rem;
        border-radius: 999px;
        background: var(--mh-glow);
        border: 1px solid var(--mh-border);
        color: var(--mh-text) !important;
        font-size: .64rem;
        font-weight: 750;
    }

    /* KPI cards */
    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, var(--mh-card), var(--mh-card2)) !important;
        border: 1px solid var(--mh-border) !important;
        border-radius: 17px !important;
        padding: 1rem 1.05rem !important;
        min-height: 108px;
        box-shadow: 0 8px 28px rgba(0, 0, 0, .07);
    }

    div[data-testid="stMetricLabel"],
    div[data-testid="stMetricLabel"] * {
        color: var(--mh-text) !important;
        opacity: .82;
        font-weight: 700 !important;
    }

    div[data-testid="stMetricValue"],
    div[data-testid="stMetricValue"] * {
        color: var(--mh-text) !important;
        font-weight: 850 !important;
    }

    /* Cards */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-color: var(--mh-border) !important;
        border-radius: 16px !important;
        background: var(--mh-card) !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] h1,
    div[data-testid="stVerticalBlockBorderWrapper"] h2,
    div[data-testid="stVerticalBlockBorderWrapper"] h3,
    div[data-testid="stVerticalBlockBorderWrapper"] p {
        color: var(--mh-text) !important;
    }

    /* Findings */
    .finding {
        padding: 1rem 1.1rem;
        margin: .55rem 0;
        border: 1px solid var(--mh-border);
        border-left: 4px solid var(--mh-teal);
        border-radius: 14px;
        background: linear-gradient(110deg, var(--mh-card), var(--mh-card2));
        color: var(--mh-text) !important;
        box-shadow: 0 5px 20px rgba(0, 0, 0, .05);
    }

    .finding strong {
        color: var(--mh-teal) !important;
    }

    .stat-pill {
        display: inline-block;
        padding: .32rem .62rem;
        margin: .15rem .2rem .2rem 0;
        border-radius: 999px;
        background: var(--mh-glow);
        border: 1px solid var(--mh-border);
        color: var(--mh-text) !important;
        font-size: .72rem;
        font-weight: 750;
    }

    .mission-number {
        color: var(--mh-purple) !important;
        font-size: .7rem;
        font-weight: 850;
        letter-spacing: .08em;
        text-transform: uppercase;
    }

    /* Inputs and select boxes */
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {
        border-radius: 11px !important;
        background: var(--mh-card) !important;
        border-color: var(--mh-border) !important;
    }

    div[data-baseweb="select"] input,
    div[data-baseweb="input"] input {
        color: var(--mh-text) !important;
        -webkit-text-fill-color: var(--mh-text) !important;
    }

    div[data-baseweb="select"] [data-testid="stMarkdownContainer"],
    div[data-baseweb="select"] [role="option"] {
        color: var(--mh-text) !important;
    }

    ul[role="listbox"] {
        background: var(--mh-card) !important;
        border: 1px solid var(--mh-border) !important;
    }

    ul[role="listbox"] li {
        color: var(--mh-text) !important;
        background: var(--mh-card) !important;
    }

    ul[role="listbox"] li:hover {
        background: var(--mh-glow) !important;
    }

    [data-baseweb="select"] *,
    [data-baseweb="input"] * {
        color: var(--mh-text) !important;
    }

    /* Radio buttons and checkboxes */
    div[data-testid="stRadio"] label,
    div[data-testid="stRadio"] label p,
    div[data-testid="stCheckbox"] label,
    div[data-testid="stCheckbox"] label p {
        color: var(--mh-text) !important;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 12px !important;
        border: 1px solid var(--mh-border) !important;
        color: var(--mh-text) !important;
        font-weight: 750 !important;
    }

    /* Dataframe */
    [data-testid="stDataFrame"] {
        border: 1px solid var(--mh-border);
        border-radius: 12px;
        overflow: hidden;
    }

    /* Footer */
    .footer-note {
        color: var(--mh-muted) !important;
        font-size: .78rem;
        margin-top: 2rem;
        padding-top: .8rem;
        border-top: 1px solid var(--mh-border);
    }

    </style>
    """

    for key, value in theme.items():
        css = css.replace(f"__{key.upper()}__", value)

    st.markdown(css, unsafe_allow_html=True)


def page_header(
    title,
    subtitle=None,
    description=None,
    level="Mental Health Analytics",
):
    subtitle_html = (
        f'<div class="hero-subtitle">{subtitle}</div>'
        if subtitle
        else ""
    )

    description_html = (
        f'<div class="hero-description">{description}</div>'
        if description
        else ""
    )

    html = f"""
    <div class="hero">
        <div class="hero-kicker">🧠 {level}</div>
        <div class="hero-title">{title}</div>
        {subtitle_html}
        {description_html}
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)
    st.divider()


def section_title(title):
    st.markdown(
        f'<div class="section-title">{title}</div>',
        unsafe_allow_html=True,
    )


def finding(text):
    # Streamlit Markdown is not parsed inside a custom HTML div.
    # Convert the literal Markdown bold markers used by the dashboard
    # into HTML before rendering the finding card.
    text = str(text).replace("**", "<strong>")

    # The simple replacement above creates paired strong tags for the
    # dashboard's intentional bold spans. Close them in pairs.
    parts = text.split("<strong>")
    if len(parts) > 1:
        rebuilt = [parts[0]]
        for i, part in enumerate(parts[1:], start=1):
            if i % 2 == 1:
                rebuilt.append("<strong>" + part + "</strong>")
            else:
                rebuilt.append(part)
        text = "".join(rebuilt)

    st.markdown(
        f'<div class="finding">{text}</div>',
        unsafe_allow_html=True,
    )


def plotly_template():
    """
    Return a Plotly template that uses the same colors as the dashboard.

    We intentionally avoid Plotly's built-in plotly_white/plotly_dark templates
    because those templates can introduce a white chart canvas that clashes
    with the application's custom theme.
    """
    dark = is_dark_mode()

    if dark:
        return {
            "layout": {
                "paper_bgcolor": "#0B1020",
                "plot_bgcolor": "#0F1526",
                "font": {
                    "color": "#F5F7FF",
                    "family": "Arial, sans-serif",
                },
                "title": {
                    "font": {
                        "color": "#F5F7FF",
                    }
                },
                "xaxis": {
                    "color": "#D8E0F0",
                    "gridcolor": "rgba(216,224,240,0.16)",
                    "zerolinecolor": "rgba(216,224,240,0.18)",
                    "linecolor": "rgba(216,224,240,0.20)",
                },
                "yaxis": {
                    "color": "#D8E0F0",
                    "gridcolor": "rgba(216,224,240,0.16)",
                    "zerolinecolor": "rgba(216,224,240,0.18)",
                    "linecolor": "rgba(216,224,240,0.20)",
                },
                "legend": {
                    "font": {
                        "color": "#F5F7FF",
                    }
                },
            }
        }

    return {
        "layout": {
            "paper_bgcolor": "#F6FAF9",
            "plot_bgcolor": "#FFFFFF",
            "font": {
                "color": "#17212B",
                "family": "Arial, sans-serif",
            },
            "title": {
                "font": {
                    "color": "#17212B",
                }
            },
            "xaxis": {
                "color": "#34444E",
                "gridcolor": "rgba(52,68,78,0.12)",
                "zerolinecolor": "rgba(52,68,78,0.16)",
                "linecolor": "rgba(52,68,78,0.20)",
            },
            "yaxis": {
                "color": "#34444E",
                "gridcolor": "rgba(52,68,78,0.12)",
                "zerolinecolor": "rgba(52,68,78,0.16)",
                "linecolor": "rgba(52,68,78,0.20)",
            },
            "legend": {
                "font": {
                    "color": "#17212B",
                }
            },
        }
    }


def register_page(page_name, xp=10):
    if "mh_pages_visited" not in st.session_state:
        st.session_state.mh_pages_visited = set()

    st.session_state.mh_pages_visited.add(page_name)

    points = {
        "Overview": 10,
        "Demographics": 15,
        "Mental Health": 15,
        "Workplace Support": 15,
        "Workplace Culture": 15,
        "Treatment Analysis": 20,
        "Statistical Analysis": 20,
        "Executive Insights": 20,
    }

    visited = len(st.session_state.mh_pages_visited)

    total_xp = min(
        sum(points.get(page, 10) for page in st.session_state.mh_pages_visited),
        130,
    )

    progress = min(total_xp / 130, 1.0)

    st.sidebar.markdown("### 🧠 Mental Health Analytics")
    st.sidebar.caption("Interactive Survey Experience")

    st.sidebar.markdown("**✨ Analytics Journey**")
    st.sidebar.markdown(f"**{total_xp} XP**")
    st.sidebar.progress(
        progress,
        text=f"{visited}/8 sections explored",
    )

    badges = []

    if visited >= 1:
        badges.append("🌱 Explorer")
    if visited >= 3:
        badges.append("🔎 Pattern Hunter")
    if visited >= 5:
        badges.append("🧠 Insight Seeker")
    if visited >= 8:
        badges.append("🏆 Wellness Analyst")

    if badges:
        st.sidebar.caption("Badges unlocked")
        st.sidebar.markdown("  ".join(f"`{badge}`" for badge in badges))

    st.sidebar.divider()
