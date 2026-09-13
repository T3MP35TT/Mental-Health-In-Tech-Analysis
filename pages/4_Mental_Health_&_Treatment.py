import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils.data_loader import load_data
from utils.analytics import grouped_treatment_rate, treatment_rate
from utils.styling import apply_global_style, page_header, section_title, finding, plotly_template

st.set_page_config(
    page_title="Mental Health & Treatment",
    page_icon="🧠",
    layout="wide",
)

apply_global_style()

df = load_data()

if df.empty:
    st.error("No data available.")
    st.stop()


# Page styling

st.html(
    """
    <style>

    /* Native Streamlit multipage sidebar navigation buttons */
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
        box-shadow: 0 4px 12px rgba(15, 23, 42, .14) !important;
    }

    [data-testid="stSidebarNav"] li a[aria-current="page"] {
        background: rgba(45, 212, 191, .13) !important;
        border: 1px solid rgba(45, 212, 191, .38) !important;
        color: #FFFFFF !important;
        box-shadow: inset 3px 0 0 #2DD4BF,
                    0 4px 14px rgba(15, 23, 42, .16) !important;
    }

    .block-container {
        padding-top: 2.8rem !important;
        padding-bottom: 1.5rem !important;
    }

    [data-testid="stSidebar"] .block-container {
        padding-top: 0.25rem !important;
        padding-left: 0.35rem !important;
        padding-right: 0.35rem !important;
        padding-bottom: 0.2rem !important;
    }

    [data-testid="stSidebar"] hr {
        margin: 0.25rem 0 !important;
    }

    .mh-sidebar-shell {
        width: 100%;
        min-height: 470px;
        max-height: calc(100vh - 430px);
        box-sizing: border-box;
        border: 1px solid rgba(139, 92, 246, 0.58);
        border-radius: 16px;
        background: linear-gradient(
            145deg,
            rgba(25, 35, 58, 0.96),
            rgba(17, 25, 45, 0.98)
        );
        padding: 14px;
        overflow-y: auto;
        overflow-x: hidden;
    }

    .mh-sidebar-shell-deep-dive {
        min-height: 0;
        max-height: none;
        overflow: visible;
    }

    .mh-sidebar-page-title {
        color: #f8fafc;
        font-size: 16px;
        font-weight: 800;
        line-height: 1.2;
        margin: 0 0 12px 0;
    }

    .mh-sidebar-big-value {
        color: #f8fafc;
        font-size: 18px;
        font-weight: 850;
        line-height: 1.15;
    }

    .mh-sidebar-section-title {
        font-size: 14px;
        font-weight: 800;
        line-height: 1.15;
        margin: 12px 0 3px 0;
        color: #f8fafc;
    }

    .mh-sidebar-description {
        font-size: 12px;
        line-height: 1.22;
        margin: 0 0 4px 0;
        opacity: 0.68;
    }

    .mh-sidebar-card {
        background: linear-gradient(
            145deg,
            rgba(30, 41, 59, 0.92),
            rgba(30, 41, 59, 0.78)
        );
        border: 1px solid rgba(129, 140, 248, 0.32);
        border-radius: 10px;
        padding: 9px 10px;
        margin: 0 0 8px 0;
        box-sizing: border-box;
    }

    .mh-sidebar-stat {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 8px;
        min-height: 23px;
        padding: 2px 0;
        border-bottom: 1px solid rgba(148, 163, 184, 0.12);
    }

    .mh-sidebar-stat:last-child {
        border-bottom: none;
    }

    .mh-sidebar-stat-label {
        font-size: 12px;
        line-height: 1.1;
        opacity: 0.76;
    }

    .mh-sidebar-stat-value {
        font-size: 14px;
        font-weight: 750;
        line-height: 1.1;
        text-align: right;
        white-space: nowrap;
    }

    .mh-sidebar-note {
        background: rgba(30, 64, 175, 0.30);
        border: 1px solid rgba(96, 165, 250, 0.16);
        border-radius: 8px;
        padding: 6px 8px;
        margin: 0 0 3px 0;
        font-size: 13px;
        line-height: 1.22;
    }

    .mh-sidebar-footnote {
        font-size: 10px;
        line-height: 1.15;
        margin: 0;
        opacity: 0.60;
    }

    .mh-sidebar-highlight {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 7px;
        padding: 3px 0;
    }

    .mh-sidebar-highlight-label {
        font-size: 12px;
        line-height: 1.15;
        opacity: 0.75;
    }

    .mh-sidebar-highlight-value {
        font-size: 14px;
        font-weight: 750;
        line-height: 1.1;
        text-align: right;
    }

    .mh-sidebar-category {
        font-size: 11px;
        line-height: 1.15;
        text-align: right;
        margin: -2px 0 2px 0;
        opacity: 0.62;
    }

    .treatment-insight {
        background: linear-gradient(
            135deg,
            rgba(20, 184, 166, 0.10),
            rgba(124, 58, 237, 0.10)
        );
        border: 1px solid rgba(129, 140, 248, 0.22);
        border-radius: 12px;
        padding: 12px 14px;
        margin: 8px 0;
    }

    .treatment-insight-title {
        font-size: 13px;
        font-weight: 750;
        margin-bottom: 5px;
    }

    .treatment-insight-body {
        font-size: 13px;
        line-height: 1.4;
        opacity: 0.86;
    }
    </style>
    """
)


# Page header

page_header(
    "🧠 Mental Health & Treatment",
    "Explore mental-health patterns and treatment behavior",
    "Move from mental-health indicators to treatment outcomes, treatment drivers, "
    "support-related differences, and the largest observed treatment gaps.",
    level="Mental Health & Treatment Intelligence",
)


# Page filters

with st.container(border=True):
    st.markdown("### 🎛️ Explore the Analysis")
    st.caption(
        "Refine the respondent population before exploring mental-health and treatment patterns. "
        "All analysis below responds to these filters."
    )

    filter_1, filter_2, filter_3, filter_4, filter_5 = st.columns(5)

    with filter_1:
        gender_values = (
            df["Gender"].dropna().astype(str).unique().tolist()
        )
        selected_gender = st.selectbox(
            "Gender",
            ["All", *sorted(gender_values)],
            key="mht_page_gender",
        )

    with filter_2:
        age_order = ["18-24", "25-34", "35-44", "45-54", "55-64", "65+"]
        age_values = (
            df["Age_Group"].dropna().astype(str).unique().tolist()
        )
        ordered_age_values = [x for x in age_order if x in age_values]
        remaining_age_values = sorted(
            x for x in age_values if x not in ordered_age_values
        )
        selected_age_group = st.selectbox(
            "Age Group",
            ["All", *ordered_age_values, *remaining_age_values],
            key="mht_page_age_group",
        )

    with filter_3:
        family_values = (
            df["family_history"].dropna().astype(str).unique().tolist()
        )
        selected_family = st.selectbox(
            "Family History",
            ["All", *sorted(family_values)],
            key="mht_page_family_history",
        )

    with filter_4:
        work_order = ["Never", "Rarely", "Sometimes", "Often", "Not Answered"]
        work_values = (
            df["work_interfere"].dropna().astype(str).unique().tolist()
        )
        ordered_work_values = [x for x in work_order if x in work_values]
        remaining_work_values = sorted(
            x for x in work_values if x not in ordered_work_values
        )
        selected_work = st.selectbox(
            "Work Interference",
            ["All", *ordered_work_values, *remaining_work_values],
            key="mht_page_work_interference",
        )

    with filter_5:
        consequence_values = (
            df["obs_consequence"].dropna().astype(str).unique().tolist()
        )
        selected_consequence = st.selectbox(
            "Observed Consequences",
            ["All", *sorted(consequence_values)],
            key="mht_page_observed_consequence",
        )


# Apply filters

filtered = df.copy()

if selected_gender != "All":
    filtered = filtered[filtered["Gender"].astype(str) == selected_gender]

if selected_age_group != "All":
    filtered = filtered[filtered["Age_Group"].astype(str) == selected_age_group]

if selected_family != "All":
    filtered = filtered[filtered["family_history"].astype(str) == selected_family]

if selected_work != "All":
    filtered = filtered[filtered["work_interfere"].astype(str) == selected_work]

if selected_consequence != "All":
    filtered = filtered[
        filtered["obs_consequence"].astype(str) == selected_consequence
    ]

if filtered.empty:
    st.warning("No respondents match the selected filters.")
    st.info("Try changing one or more filters to broaden the analysis.")
    st.stop()


active_filters = []

if selected_gender != "All":
    active_filters.append(f"Gender: {selected_gender}")
if selected_age_group != "All":
    active_filters.append(f"Age Group: {selected_age_group}")
if selected_family != "All":
    active_filters.append(f"Family History: {selected_family}")
if selected_work != "All":
    active_filters.append(f"Work Interference: {selected_work}")
if selected_consequence != "All":
    active_filters.append(f"Observed Consequences: {selected_consequence}")

if active_filters:
    st.caption(
        "🎯 Active filters: "
        + " • ".join(active_filters)
        + f"  |  {len(filtered):,} respondents"
    )
else:
    st.caption(f"🎯 All respondents  |  {len(filtered):,} respondents")


# Core treatment metrics

overall_treatment = treatment_rate(filtered)
treatment_yes = int(filtered["treatment"].eq("Yes").sum())
treatment_no = int(filtered["treatment"].eq("No").sum())


# Analysis navigation

analysis_section = st.segmented_control(
    "Analysis section",
    options=[
        "🧠 Mental Health Overview",
        "💊 Treatment Analysis",
    ],
    default="🧠 Mental Health Overview",
    key="mht_analysis_section",
    label_visibility="collapsed",
)

if analysis_section is None:
    analysis_section = "🧠 Mental Health Overview"


# Reusable helpers

def prepare_treatment_rates(dataframe, column):
    result = grouped_treatment_rate(dataframe, column).copy()

    if column not in result.columns:
        return pd.DataFrame()

    result = result.dropna(
        subset=[column, "Treatment Rate"]
    )

    if column == "work_interfere":
        result = result[result[column] != "Not Answered"]

    return result


def treatment_driver_summary(dataframe, column, label):
    data = prepare_treatment_rates(dataframe, column)

    if data.empty:
        return None

    high = data.loc[data["Treatment Rate"].idxmax()]
    low = data.loc[data["Treatment Rate"].idxmin()]

    return {
        "Dimension": label,
        "Column": column,
        "Highest Group": str(high[column]),
        "Highest Rate": float(high["Treatment Rate"]),
        "Lowest Group": str(low[column]),
        "Lowest Rate": float(low["Treatment Rate"]),
        "Gap": float(high["Treatment Rate"] - low["Treatment Rate"]),
        "Respondents": int(data["Respondents"].sum()),
    }


def render_treatment_driver_table(dataframe):
    rows = []

    dimensions = {
        "Gender": "Gender",
        "Age Group": "Age_Group",
        "Company Size": "Company_Size_Group",
        "Work Arrangement": "Remote_Work_Status",
        "Family History": "family_history",
        "Work Interference": "work_interfere",
        "Mental Health Consequences": "obs_consequence",
        "Benefits": "benefits",
        "Care Options": "care_options",
        "Anonymity": "anonymity",
        "Leave": "leave",
    }

    for label, column in dimensions.items():
        if column not in dataframe.columns:
            continue

        summary = treatment_driver_summary(
            dataframe,
            column,
            label,
        )

        if summary is not None:
            rows.append(summary)

    return pd.DataFrame(rows)


def treatment_distribution(dataframe):
    data = (
        dataframe["treatment"]
        .value_counts()
        .rename_axis("Treatment")
        .reset_index(name="Respondents")
    )

    data["Share"] = (
        data["Respondents"] / data["Respondents"].sum() * 100
    )

    return data


def render_dynamic_sidebar(active_section, overview_view=None, overview_lens=None, treatment_view=None):
    """Render the dynamic Page Intelligence sidebar."""

    def esc(value):
        return (
            str(value)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
        )

    def stat(label, value, accent=False):
        accent_class = " highlight" if accent else ""
        return (
            f'<div class="mh-sidebar-stat{accent_class}">'
            f'<span class="mh-sidebar-stat-label">{esc(label)}</span>'
            f'<span class="mh-sidebar-stat-value">{esc(value)}</span>'
            f'</div>'
        )

    def card(content):
        return f'<div class="mh-sidebar-card">{content}</div>'

    # Only Work Interference Deep Dive uses a content-sized Page Intelligence
    # card. All other views keep the existing spacious sidebar footprint.
    is_work_interference_deep_dive = (
        active_section == "🧠 Mental Health Overview"
        and overview_view == "🔍 Treatment Lens"
        and overview_lens == "Work Interference"
    )

    shell_class = "mh-sidebar-shell"
    if is_work_interference_deep_dive:
        shell_class += " mh-sidebar-shell-deep-dive"

    html = f'<div class="{shell_class}">'
    html += '<div class="mh-sidebar-page-title">📌 Page Intelligence</div>'

    html += card(
        '<div class="mh-sidebar-label">RESPONDENTS</div>'
        f'<div class="mh-sidebar-big-value">{len(filtered):,}</div>'
    )

    if active_section == "🧠 Mental Health Overview":
        if overview_view == "📊 Treatment Distribution":
            html += (
                '<div class="mh-sidebar-section-title">📊 Treatment Distribution</div>'
                '<div class="mh-sidebar-description">Treatment outcome snapshot</div>'
            )

            html += card(
                stat("Received treatment", f"{treatment_yes:,}", True)
                + stat("No treatment", f"{treatment_no:,}")
                + stat("Treatment share", f"{overall_treatment:.1f}%")
            )

            work_data = prepare_treatment_rates(filtered, "work_interfere")
            if not work_data.empty:
                high = work_data.loc[work_data["Treatment Rate"].idxmax()]
                low = work_data.loc[work_data["Treatment Rate"].idxmin()]

                html += card(
                    stat(
                        "Highest work-interference rate",
                        f"{float(high['Treatment Rate']):.1f}%",
                        True,
                    )
                    + stat("Group", high["work_interfere"])
                    + stat("Lowest rate", f"{float(low['Treatment Rate']):.1f}%")
                    + stat(
                        "Gap",
                        f"{float(high['Treatment Rate'] - low['Treatment Rate']):.1f} pp",
                    )
                )

        elif overview_view == "🔍 Treatment Lens" and overview_lens:
            html += (
                f'<div class="mh-sidebar-section-title">🔍 {esc(overview_lens)}</div>'
                f'<div class="mh-sidebar-description">Treatment-rate comparison</div>'
            )

            lens_map = {
                "Family History": "family_history",
                "Work Interference": "work_interfere",
                "Observed Consequences": "obs_consequence",
            }

            lens_col = lens_map[overview_lens]
            lens_data_sidebar = prepare_treatment_rates(filtered, lens_col)

            if not lens_data_sidebar.empty:
                high = lens_data_sidebar.loc[
                    lens_data_sidebar["Treatment Rate"].idxmax()
                ]
                low = lens_data_sidebar.loc[
                    lens_data_sidebar["Treatment Rate"].idxmin()
                ]
                gap = float(high["Treatment Rate"] - low["Treatment Rate"])

                html += card(
                    stat(
                        "Highest treatment",
                        f"{float(high['Treatment Rate']):.1f}%",
                        True,
                    )
                    + stat("Highest group", high[lens_col])
                    + stat("Lowest treatment", f"{float(low['Treatment Rate']):.1f}%")
                    + stat("Lowest group", low[lens_col])
                    + stat("Rate gap", f"{gap:.1f} pp")
                )

                if overview_lens == "Work Interference":
                    work_counts_sidebar = (
                        filtered["work_interfere"]
                        .value_counts()
                        .drop(labels=["Not Answered"], errors="ignore")
                    )

                    if not work_counts_sidebar.empty:
                        most_common = work_counts_sidebar.idxmax()
                        html += (
                            '<div class="mh-sidebar-note">'
                            f'<b>{esc(most_common)}</b> is the most common reported '
                            f'work-interference level with '
                            f'<b>{int(work_counts_sidebar.max()):,}</b> respondents.'
                            '</div>'
                        )

    else:
        html += (
            f'<div class="mh-sidebar-section-title">💊 '
            f'{esc(treatment_view or "Treatment Analysis")}</div>'
        )

        if treatment_view == "📊 Treatment Overview":
            html += card(
                stat("Received treatment", f"{treatment_yes:,}", True)
                + stat("No treatment", f"{treatment_no:,}")
                + stat("Treatment rate", f"{overall_treatment:.1f}%")
            )

        elif treatment_view == "🔎 Treatment Drivers":
            driver_data_sidebar = render_treatment_driver_table(filtered)

            if not driver_data_sidebar.empty:
                strongest = driver_data_sidebar.loc[
                    driver_data_sidebar["Gap"].idxmax()
                ]

                html += card(
                    stat(
                        "Largest observed gap",
                        f"{strongest['Gap']:.1f} pp",
                        True,
                    )
                    + stat("Dimension", strongest["Dimension"])
                    + stat("Highest group", strongest["Highest Group"])
                    + stat("Highest rate", f"{strongest['Highest Rate']:.1f}%")
                    + stat("Lowest group", strongest["Lowest Group"])
                    + stat("Lowest rate", f"{strongest['Lowest Rate']:.1f}%")
                )

        elif treatment_view == "🏢 Support & Treatment":
            support_rows_sidebar = []
            support_features_sidebar = [
                ("benefits", "Mental Health Benefits"),
                ("care_options", "Mental Health Care Options"),
                ("wellness_program", "Wellness Program"),
                ("seek_help", "Resources to Seek Help"),
                ("anonymity", "Anonymity"),
                ("leave", "Ease of Taking Leave"),
            ]

            for column, title in support_features_sidebar:
                data = prepare_treatment_rates(filtered, column)
                yes = data[data[column] == "Yes"] if not data.empty else pd.DataFrame()
                no = data[data[column] == "No"] if not data.empty else pd.DataFrame()

                if yes.empty or no.empty:
                    continue

                yes_rate = float(yes["Treatment Rate"].iloc[0])
                no_rate = float(no["Treatment Rate"].iloc[0])
                support_rows_sidebar.append(
                    (title, yes_rate, no_rate, yes_rate - no_rate)
                )

            if support_rows_sidebar:
                strongest = max(support_rows_sidebar, key=lambda x: x[3])

                html += card(
                    stat(
                        "Largest support gap",
                        f"{strongest[3]:.1f} pp",
                        True,
                    )
                    + stat("Mechanism", strongest[0])
                    + stat("Treatment if Yes", f"{strongest[1]:.1f}%")
                    + stat("Treatment if No", f"{strongest[2]:.1f}%")
                )

        elif treatment_view == "⚖️ Treatment Gaps":
            gap_data_sidebar = render_treatment_driver_table(filtered)

            if not gap_data_sidebar.empty:
                largest = gap_data_sidebar.loc[
                    gap_data_sidebar["Gap"].idxmax()
                ]

                html += card(
                    stat("Largest gap", f"{largest['Gap']:.1f} pp", True)
                    + stat("Dimension", largest["Dimension"])
                    + stat("Highest", f"{largest['Highest Rate']:.1f}%")
                    + stat("Lowest", f"{largest['Lowest Rate']:.1f}%")
                )

    if active_filters:
        html += (
            '<div class="mh-sidebar-footnote">'
            "Current filters: "
            + " • ".join(esc(x) for x in active_filters)
            + "</div>"
        )

    html += "</div>"

    st.sidebar.html(html)


# Mental Health Overview

if analysis_section == "🧠 Mental Health Overview":

    section_title("💚 Mental Health Overview")

    view = st.radio(
        "Choose an analysis view",
        [
            "📊 Treatment Distribution",
            "🔍 Treatment Lens",
        ],
        horizontal=True,
        key="mht_overview_view",
    )

    if view == "📊 Treatment Distribution":

        # Render the sidebar only after the active overview view is known.
        render_dynamic_sidebar(
            analysis_section,
            overview_view=view,
            overview_lens=None,
        )

        treatment_data = treatment_distribution(filtered)

        chart_col, metrics_col = st.columns([1.05, 1])

        with chart_col:
            fig = px.pie(
                treatment_data,
                names="Treatment",
                values="Respondents",
                hole=0.62,
                template=plotly_template(),
                title="Treatment Distribution",
                color="Treatment",
                color_discrete_map={
                    "Yes": "#5EEAD4",
                    "No": "#A78BFA",
                },
            )

            fig.update_traces(
                textposition="inside",
                textinfo="percent+label",
                hovertemplate=(
                    "<b>%{label}</b><br>"
                    "Respondents: <b>%{value:,}</b><br>"
                    "Share: <b>%{percent}</b>"
                    "<extra></extra>"
                ),
            )

            fig.add_annotation(
                text=f"<b>{overall_treatment:.1f}%</b><br>treated",
                x=0.5,
                y=0.5,
                showarrow=False,
                font=dict(size=18),
            )

            fig.update_layout(
                height=410,
                margin=dict(l=20, r=20, t=65, b=20),
                showlegend=False,
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                key="mht_treatment_distribution",
            )

        with metrics_col:
            st.markdown("### 📌 Treatment Snapshot")

            c1, c2 = st.columns(2)

            with c1:
                st.metric(
                    "💚 Received Treatment",
                    f"{treatment_yes:,}",
                    f"{treatment_yes / len(filtered) * 100:.1f}%",
                )

            with c2:
                st.metric(
                    "💜 No Treatment",
                    f"{treatment_no:,}",
                    f"{treatment_no / len(filtered) * 100:.1f}%",
                )

            st.metric(
                "🧠 Overall Treatment Rate",
                f"{overall_treatment:.1f}%",
            )

            st.info(
                "Treatment rate describes the filtered survey population. "
                "It is not a measure of mental-illness prevalence."
            )

    else:
        lens = st.radio(
            "Choose a treatment lens",
            [
                "Family History",
                "Work Interference",
                "Observed Consequences",
            ],
            horizontal=True,
            key="mht_treatment_lens",
        )

        lens_map = {
            "Family History": "family_history",
            "Work Interference": "work_interfere",
            "Observed Consequences": "obs_consequence",
        }

        # Render the sidebar once, after the selected lens is known.
        render_dynamic_sidebar(
            analysis_section,
            overview_view=view,
            overview_lens=lens,
        )

        lens_col = lens_map[lens]
        lens_data = prepare_treatment_rates(filtered, lens_col)

        if lens_data.empty:
            st.warning("Not enough data is available for the selected lens.")
        else:
            if lens == "Family History":
                palette = ["#F472B6", "#FB7185", "#FDA4AF"]
            elif lens == "Work Interference":
                palette = ["#38BDF8", "#22D3EE", "#06B6D4", "#0891B2"]
            else:
                palette = ["#34D399", "#10B981", "#059669"]

            fig = px.bar(
                lens_data,
                x="Treatment Rate",
                y=lens_col,
                orientation="h",
                text="Treatment Rate",
                template=plotly_template(),
                title=f"Treatment Rate by {lens}",
                color=lens_col,
                color_discrete_sequence=palette,
            )

            fig.update_traces(
                marker_line_width=0,
                texttemplate="%{text:.1f}%",
                textposition="outside",
                hovertemplate=(
                    "<b>%{y}</b><br>"
                    "Treatment rate: <b>%{x:.1f}%</b>"
                    "<extra></extra>"
                ),
            )

            fig.update_layout(
                height=430,
                margin=dict(l=20, r=75, t=65, b=35),
                xaxis=dict(
                    range=[0, 100],
                    ticksuffix="%",
                    title="Treatment Rate (%)",
                ),
                yaxis=dict(title=""),
                showlegend=False,
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                key=f"mht_lens_{lens_col}",
            )

            high = lens_data.loc[lens_data["Treatment Rate"].idxmax()]
            low = lens_data.loc[lens_data["Treatment Rate"].idxmin()]
            gap = float(high["Treatment Rate"] - low["Treatment Rate"])

            a, b, c = st.columns(3)

            with a:
                st.metric(
                    "🏆 Highest Treatment Rate",
                    f"{float(high['Treatment Rate']):.1f}%",
                    str(high[lens_col]),
                )

            with b:
                st.metric(
                    "📉 Lowest Treatment Rate",
                    f"{float(low['Treatment Rate']):.1f}%",
                    str(low[lens_col]),
                    delta_color="off",
                )

            with c:
                st.metric(
                    "⚖️ Rate Gap",
                    f"{gap:.1f} pp",
                    "highest vs lowest",
                )


        # Work Interference Deep Dive

        if lens == "Work Interference":
            section_title("⚡ Work Interference Deep Dive")

            work_counts = (
                filtered["work_interfere"]
                .value_counts()
                .rename_axis("Work Interference")
                .reset_index(name="Respondents")
            )

            work_counts = work_counts[
                work_counts["Work Interference"] != "Not Answered"
            ]

            work_order = ["Never", "Rarely", "Sometimes", "Often"]

            work_counts["Work Interference"] = pd.Categorical(
                work_counts["Work Interference"],
                categories=work_order,
                ordered=True,
            )

            work_counts = work_counts.sort_values("Work Interference")

            work_rates = prepare_treatment_rates(filtered, "work_interfere")

            if not work_rates.empty:
                work_rates["work_interfere"] = pd.Categorical(
                    work_rates["work_interfere"],
                    categories=work_order,
                    ordered=True,
                )
                work_rates = work_rates.sort_values("work_interfere")

            work_col_1, work_col_2 = st.columns(2)

            with work_col_1:
                fig = px.bar(
                    work_counts,
                    x="Work Interference",
                    y="Respondents",
                    text="Respondents",
                    template=plotly_template(),
                    title="Reported Work Interference",
                    color="Work Interference",
                    color_discrete_sequence=[
                        "#8B5CF6",
                        "#A855F7",
                        "#C084FC",
                        "#E879F9",
                    ],
                )

                fig.update_traces(
                    marker_line_width=0,
                    texttemplate="%{text:,}",
                    textposition="outside",
                    hovertemplate=(
                        "<b>%{x}</b><br>"
                        "Respondents: <b>%{y:,}</b>"
                        "<extra></extra>"
                    ),
                )

                fig.update_layout(
                    height=430,
                    margin=dict(l=20, r=25, t=65, b=45),
                    xaxis_title="",
                    yaxis_title="Respondents",
                    showlegend=False,
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                    key="mht_work_interference_counts",
                )

            with work_col_2:
                if work_rates.empty:
                    st.warning("No work-interference treatment data is available.")
                else:
                    fig = go.Figure()

                    fig.add_trace(
                        go.Scatter(
                            x=work_rates["work_interfere"],
                            y=work_rates["Treatment Rate"],
                            mode="lines+markers+text",
                            text=work_rates["Treatment Rate"],
                            texttemplate="%{text:.1f}%",
                            textposition="top center",
                            line=dict(width=4, color="#FB923C"),
                            marker=dict(
                                size=11,
                                color="#F97316",
                                line=dict(width=2, color="#FED7AA"),
                            ),
                            hovertemplate=(
                                "<b>%{x}</b><br>"
                                "Treatment rate: <b>%{y:.1f}%</b>"
                                "<extra></extra>"
                            ),
                        )
                    )

                    fig.update_layout(
                        template=plotly_template(),
                        height=430,
                        title="Treatment Rate Across Work Interference",
                        margin=dict(l=20, r=25, t=65, b=45),
                        xaxis=dict(
                            title="Work Interference",
                            categoryorder="array",
                            categoryarray=work_order,
                        ),
                        yaxis=dict(
                            title="Treatment Rate (%)",
                            range=[0, 100],
                            ticksuffix="%",
                        ),
                        showlegend=False,
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True,
                        key="mht_work_interference_rates",
                    )

            if not work_rates.empty:
                often_row = work_rates[work_rates["work_interfere"] == "Often"]
                never_row = work_rates[work_rates["work_interfere"] == "Never"]

                if not often_row.empty and not never_row.empty:
                    often_value = float(often_row["Treatment Rate"].iloc[0])
                    never_value = float(never_row["Treatment Rate"].iloc[0])
                    difference = often_value - never_value

                    finding(
                        f"⚡ Treatment rate is **{often_value:.1f}%** among respondents "
                        f"reporting work interference **Often**, versus "
                        f"**{never_value:.1f}%** among those reporting **Never** — a "
                        f"**{difference:.1f} percentage-point difference** in this "
                        f"survey population."
                    )



# Treatment Analysis

else:

    section_title("💊 Treatment Analysis")

    st.info(
        "Treatment is the primary outcome in this analysis. "
        "Use the views below to identify where treatment rates differ, "
        "which workplace/support dimensions show the largest gaps, "
        "and how many respondents sit behind each comparison."
    )

    treatment_view = st.segmented_control(
        "Treatment analysis view",
        options=[
            "📊 Treatment Overview",
            "🔎 Treatment Drivers",
            "🏢 Support & Treatment",
            "⚖️ Treatment Gaps",
        ],
        default="📊 Treatment Overview",
        key="mht_treatment_analysis_view",
        label_visibility="collapsed",
    )

    if treatment_view is None:
        treatment_view = "📊 Treatment Overview"

    render_dynamic_sidebar(
        analysis_section,
        treatment_view=treatment_view,
    )

    # Treatment Overview

    if treatment_view == "📊 Treatment Overview":

        section_title("📊 Treatment Overview")

        overview_data = treatment_distribution(filtered)

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric(
                "Treatment Rate",
                f"{overall_treatment:.1f}%",
            )

        with c2:
            st.metric(
                "Received Treatment",
                f"{treatment_yes:,}",
            )

        with c3:
            st.metric(
                "No Treatment",
                f"{treatment_no:,}",
            )

        with c4:
            st.metric(
                "Population",
                f"{len(filtered):,}",
            )

        chart_col, table_col = st.columns([1.15, 0.85])

        with chart_col:
            fig = px.bar(
                overview_data,
                x="Treatment",
                y="Respondents",
                text="Respondents",
                color="Treatment",
                color_discrete_map={
                    "Yes": "#5EEAD4",
                    "No": "#A78BFA",
                },
                template=plotly_template(),
                title="Treatment Outcomes",
            )

            fig.update_traces(
                texttemplate="%{text:,}",
                textposition="outside",
                marker_line_width=0,
                hovertemplate=(
                    "<b>%{x}</b><br>"
                    "Respondents: <b>%{y:,}</b><br>"
                    "<extra></extra>"
                ),
            )

            fig.update_layout(
                height=420,
                showlegend=False,
                margin=dict(l=30, r=30, t=65, b=45),
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                key="mht_treatment_overview_chart",
            )

        with table_col:
            st.markdown("### Respondent Breakdown")

            display_data = overview_data.rename(
                columns={
                    "Treatment": "Treatment",
                    "Respondents": "Respondents",
                    "Share": "Share (%)",
                }
            )

            display_data["Share (%)"] = display_data["Share (%)"].round(1)

            st.dataframe(
                display_data,
                use_container_width=True,
                hide_index=True,
            )

            st.markdown(
                f"""
                <div class="treatment-insight">
                    <div class="treatment-insight-title">💡 Read the outcome</div>
                    <div class="treatment-insight-body">
                        The current filtered population has a
                        <b>{overall_treatment:.1f}%</b> treatment rate,
                        based on <b>{treatment_yes:,}</b> respondents reporting
                        treatment out of <b>{len(filtered):,}</b>.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Treatment Drivers

    elif treatment_view == "🔎 Treatment Drivers":

        section_title("🔎 Treatment Drivers")

        st.caption(
            "Rank dimensions by the difference between their highest and lowest "
            "observed treatment rates. This is a descriptive comparison, not a causal model."
        )

        driver_data = render_treatment_driver_table(filtered)

        if driver_data.empty:
            st.warning("Not enough data is available to calculate treatment drivers.")
        else:
            driver_data = driver_data.sort_values(
                "Gap",
                ascending=True,
            )

            fig = px.bar(
                driver_data,
                x="Gap",
                y="Dimension",
                orientation="h",
                text="Gap",
                color="Gap",
                color_continuous_scale=[
                    "#C4B5FD",
                    "#7C3AED",
                ],
                template=plotly_template(),
                title="Treatment-Rate Spread by Dimension",
                hover_data={
                    "Highest Group": True,
                    "Highest Rate": ":.1f",
                    "Lowest Group": True,
                    "Lowest Rate": ":.1f",
                    "Respondents": True,
                },
            )

            fig.update_traces(
                texttemplate="%{text:.1f} pp",
                textposition="outside",
                marker_line_width=0,
                cliponaxis=False,
            )

            fig.update_layout(
                height=540,
                margin=dict(l=30, r=95, t=70, b=45),
                xaxis=dict(
                    title="Highest treatment rate − lowest treatment rate (pp)",
                    range=[0, max(10, float(driver_data["Gap"].max()) * 1.18)],
                ),
                yaxis=dict(title=""),
                coloraxis_showscale=False,
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                key="mht_treatment_driver_ranking",
            )

            display = driver_data[
                [
                    "Dimension",
                    "Highest Group",
                    "Highest Rate",
                    "Lowest Group",
                    "Lowest Rate",
                    "Gap",
                    "Respondents",
                ]
            ].copy()

            display = display.rename(
                columns={
                    "Highest Rate": "Highest Treatment (%)",
                    "Lowest Rate": "Lowest Treatment (%)",
                    "Gap": "Gap (pp)",
                }
            )

            display["Highest Treatment (%)"] = display["Highest Treatment (%)"].round(1)
            display["Lowest Treatment (%)"] = display["Lowest Treatment (%)"].round(1)
            display["Gap (pp)"] = display["Gap (pp)"].round(1)

            st.markdown("### 📋 Driver Detail")

            st.dataframe(
                display.sort_values("Gap (pp)", ascending=False),
                use_container_width=True,
                hide_index=True,
            )

            strongest = driver_data.iloc[-1]

            st.success(
                f"🏆 Largest observed treatment-rate spread: "
                f"**{strongest['Dimension']}** — "
                f"**{strongest['Gap']:.1f} percentage points**, "
                f"from **{strongest['Lowest Group']} "
                f"({strongest['Lowest Rate']:.1f}%)** to "
                f"**{strongest['Highest Group']} "
                f"({strongest['Highest Rate']:.1f}%)**."
            )

    # Support & Treatment

    elif treatment_view == "🏢 Support & Treatment":

        section_title("🏢 Support & Treatment")

        st.caption(
            "Examine how treatment rates differ across responses to workplace "
            "support mechanisms. These are observed associations within the survey."
        )

        support_features = [
            ("benefits", "Mental Health Benefits", "💚"),
            ("care_options", "Mental Health Care Options", "🩺"),
            ("wellness_program", "Wellness Program", "🌱"),
            ("seek_help", "Resources to Seek Help", "🧭"),
            ("anonymity", "Anonymity", "🔐"),
            ("leave", "Ease of Taking Leave", "🕊️"),
        ]

        support_rows = []

        for column, title, icon in support_features:
            data = prepare_treatment_rates(filtered, column)

            if data.empty:
                continue

            yes_rows = data[data[column] == "Yes"]

            no_rows = data[data[column] == "No"]

            yes_rate = (
                float(yes_rows["Treatment Rate"].iloc[0])
                if not yes_rows.empty
                else None
            )

            no_rate = (
                float(no_rows["Treatment Rate"].iloc[0])
                if not no_rows.empty
                else None
            )

            gap = (
                yes_rate - no_rate
                if yes_rate is not None and no_rate is not None
                else None
            )

            support_rows.append(
                {
                    "Support Mechanism": f"{icon} {title}",
                    "Yes Treatment Rate": yes_rate,
                    "No Treatment Rate": no_rate,
                    "Gap": gap,
                }
            )

        support_data = pd.DataFrame(support_rows)

        if support_data.empty:
            st.warning("No support-treatment comparisons are available.")
        else:
            chart_data = support_data.dropna(subset=["Gap"]).sort_values("Gap")

            fig = px.bar(
                chart_data,
                x="Gap",
                y="Support Mechanism",
                orientation="h",
                text="Gap",
                color="Gap",
                color_continuous_scale=[
                    "#A78BFA",
                    "#5EEAD4",
                ],
                template=plotly_template(),
                title="Treatment Rate Difference: Support Available vs Not Available",
                hover_data={
                    "Yes Treatment Rate": ":.1f",
                    "No Treatment Rate": ":.1f",
                },
            )

            fig.update_traces(
                texttemplate="%{text:.1f} pp",
                textposition="outside",
                marker_line_width=0,
                cliponaxis=False,
            )

            fig.update_layout(
                height=500,
                margin=dict(l=25, r=95, t=75, b=50),
                xaxis=dict(
                    title="Treatment-rate difference (Yes − No), pp",
                ),
                yaxis=dict(title=""),
                coloraxis_showscale=False,
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                key="mht_support_treatment_gap",
            )

            support_display = support_data.rename(
                columns={
                    "Yes Treatment Rate": "Treatment if Available (%)",
                    "No Treatment Rate": "Treatment if Not Available (%)",
                    "Gap": "Difference (pp)",
                }
            ).copy()

            for column in [
                "Treatment if Available (%)",
                "Treatment if Not Available (%)",
                "Difference (pp)",
            ]:
                support_display[column] = support_display[column].round(1)

            st.markdown("### 📋 Support-Level Treatment Detail")

            st.dataframe(
                support_display.sort_values(
                    "Difference (pp)",
                    ascending=False,
                    na_position="last",
                ),
                use_container_width=True,
                hide_index=True,
            )

            valid = support_data.dropna(subset=["Gap"])

            if not valid.empty:
                largest = valid.loc[valid["Gap"].idxmax()]
                smallest = valid.loc[valid["Gap"].idxmin()]

                st.info(
                    f"💡 Largest positive support-related treatment difference: "
                    f"**{largest['Support Mechanism']}**, "
                    f"**{largest['Gap']:.1f} pp** higher when the support response "
                    f"is **Yes** than **No**."
                )

                if smallest["Gap"] < 0:
                    st.warning(
                        f"⚠️ The direction is reversed for **{smallest['Support Mechanism']}**: "
                        f"the treatment rate is **{abs(smallest['Gap']):.1f} pp lower** "
                        f"for the Yes response than the No response."
                    )

    # Treatment Gaps

    else:

        section_title("⚖️ Treatment Gaps")

        st.caption(
            "Investigate the largest and smallest treatment-rate differences in the "
            "current population, then inspect the underlying respondent counts."
        )

        gap_data = render_treatment_driver_table(filtered)

        if gap_data.empty:
            st.warning("No treatment-gap data is available.")
        else:
            highest_gap = gap_data.loc[gap_data["Gap"].idxmax()]
            lowest_gap = gap_data.loc[gap_data["Gap"].idxmin()]

            c1, c2, c3 = st.columns(3)

            with c1:
                st.metric(
                    "Largest Dimension Gap",
                    f"{highest_gap['Gap']:.1f} pp",
                    highest_gap["Dimension"],
                )

            with c2:
                st.metric(
                    "Highest Treatment Group",
                    f"{highest_gap['Highest Rate']:.1f}%",
                    highest_gap["Highest Group"],
                )

            with c3:
                st.metric(
                    "Lowest Treatment Group",
                    f"{highest_gap['Lowest Rate']:.1f}%",
                    highest_gap["Lowest Group"],
                )

            gap_chart = gap_data.sort_values("Gap", ascending=True)

            fig = go.Figure()

            fig.add_trace(
                go.Bar(
                    x=gap_chart["Gap"],
                    y=gap_chart["Dimension"],
                    orientation="h",
                    text=gap_chart["Gap"],
                    texttemplate="%{text:.1f} pp",
                    textposition="outside",
                    marker_line_width=0,
                    hovertemplate=(
                        "<b>%{y}</b><br>"
                        "Treatment-rate gap: <b>%{x:.1f} pp</b><br>"
                        "Highest group: <b>%{customdata[0]}</b> "
                        "(%{customdata[1]:.1f}%)<br>"
                        "Lowest group: <b>%{customdata[2]}</b> "
                        "(%{customdata[3]:.1f}%)"
                        "<extra></extra>"
                    ),
                    customdata=gap_chart[
                        [
                            "Highest Group",
                            "Highest Rate",
                            "Lowest Group",
                            "Lowest Rate",
                        ]
                    ],
                )
            )

            fig.update_layout(
                template=plotly_template(),
                height=540,
                title="Observed Treatment-Rate Gaps",
                margin=dict(l=25, r=100, t=70, b=45),
                xaxis=dict(
                    title="Percentage points",
                    zeroline=True,
                ),
                yaxis=dict(title=""),
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                key="mht_treatment_gaps_chart",
            )

            st.markdown("### 🔬 Inspect the Largest Gap")

            st.write(
                f"**{highest_gap['Dimension']}** ranges from "
                f"**{highest_gap['Lowest Rate']:.1f}%** for "
                f"**{highest_gap['Lowest Group']}** to "
                f"**{highest_gap['Highest Rate']:.1f}%** for "
                f"**{highest_gap['Highest Group']}**."
            )

            st.dataframe(
                gap_data.sort_values("Gap", ascending=False)[
                    [
                        "Dimension",
                        "Highest Group",
                        "Highest Rate",
                        "Lowest Group",
                        "Lowest Rate",
                        "Gap",
                        "Respondents",
                    ]
                ].rename(
                    columns={
                        "Highest Rate": "Highest Treatment (%)",
                        "Lowest Rate": "Lowest Treatment (%)",
                        "Gap": "Gap (pp)",
                    }
                ),
                use_container_width=True,
                hide_index=True,
            )



# Key takeaway

section_title("💡 Key Takeaway")

driver_table = render_treatment_driver_table(filtered)

if not driver_table.empty:
    strongest = driver_table.loc[driver_table["Gap"].idxmax()]

    finding(
        f"📌 The current filtered population has a **{overall_treatment:.1f}%** "
        f"treatment rate. The largest descriptive treatment-rate spread is "
        f"across **{strongest['Dimension']}**, ranging from "
        f"**{strongest['Lowest Rate']:.1f}%** for "
        f"**{strongest['Lowest Group']}** to "
        f"**{strongest['Highest Rate']:.1f}%** for "
        f"**{strongest['Highest Group']}** — a "
        f"**{strongest['Gap']:.1f} percentage-point difference**."
    )
else:
    finding(
        f"📌 The current filtered population has a "
        f"**{overall_treatment:.1f}%** treatment rate."
    )


# Footer

st.caption(
    "Source: 2014 Mental Health in Tech Survey • "
    "Treatment rate ≠ mental-health prevalence • "
    "Observed differences are associations within an observational survey • "
    "Association does not imply causation • "
    "All visuals respond to the selected filters."
)
