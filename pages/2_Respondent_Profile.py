import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils.data_loader import load_data
from utils.analytics import (
    treatment_rate,
    grouped_treatment_rate,
)
from utils.styling import (
    apply_global_style,
    page_header,
    section_title,
    finding,
    plotly_template,
)


st.set_page_config(
    page_title="Respondent Profile",
    page_icon="👥",
    layout="wide",
)

apply_global_style()
df = load_data()


# Demographics-specific visual styling
st.markdown(
    """
    <style>

    /* =========================================================
       GLOBAL SIDEBAR PAGE NAVIGATION
       ========================================================= */

    /* Sidebar navigation container */
    [data-testid="stSidebarNav"] {
        padding: 0.35rem 0.25rem 0.75rem 0.25rem !important;
    }

    /* Navigation list */
    [data-testid="stSidebarNav"] ul {
        gap: 0.25rem !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    /* Each navigation item */
    [data-testid="stSidebarNav"] li {
        margin: 0 0 0.32rem 0 !important;
        padding: 0 !important;
    }

    /* All page navigation buttons */
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

        transition:
            background 0.18s ease,
            border-color 0.18s ease,
            transform 0.18s ease,
            box-shadow 0.18s ease !important;
    }

    /* Text inside navigation buttons */
    [data-testid="stSidebarNav"] li a span {
        color: inherit !important;
        font-size: 0.91rem !important;
        font-weight: 750 !important;
    }

    /* Hover state */
    [data-testid="stSidebarNav"] li a:hover {
        background: rgba(45, 212, 191, 0.08) !important;
        border-color: rgba(45, 212, 191, 0.32) !important;
        color: #FFFFFF !important;

        transform: translateX(2px) !important;
        box-shadow: 0 4px 12px rgba(15, 23, 42, 0.14) !important;
    }

    /* Active/current page button */
    [data-testid="stSidebarNav"] li a[aria-current="page"] {
        background: rgba(45, 212, 191, 0.13) !important;
        border: 1px solid rgba(45, 212, 191, 0.38) !important;

        color: #FFFFFF !important;

        box-shadow:
            inset 3px 0 0 #2DD4BF,
            0 4px 14px rgba(15, 23, 42, 0.16) !important;
    }

    /* Active page text */
    [data-testid="stSidebarNav"] li a[aria-current="page"] span {
        color: #FFFFFF !important;
        font-weight: 800 !important;
    }

    /* Navigation icons */
    [data-testid="stSidebarNav"] li a svg {
        width: 17px !important;
        height: 17px !important;
        margin-right: 9px !important;
    }

    /* Keep sidebar navigation clean */
    [data-testid="stSidebarNav"] li a p {
        margin: 0 !important;
        padding: 0 !important;
    }


    /* =========================================================
       RESPONDENT PROFILE
       ========================================================= */

    .demo-mission {
        border: 1px solid rgba(94, 234, 212, .25);
        border-radius: 18px;
        padding: 1rem 1.1rem;
        background: linear-gradient(
            135deg,
            rgba(94, 234, 212, .08),
            rgba(167, 139, 250, .08)
        );
        margin: .5rem 0 1.2rem;
    }

    .demo-label {
        color: #5EEAD4;
        font-size: .72rem;
        font-weight: 850;
        letter-spacing: .09em;
        text-transform: uppercase;
    }

    .demo-title {
        font-size: 1.15rem;
        font-weight: 800;
        margin-top: .25rem;
    }

    .demo-copy {
        opacity: .78;
        line-height: 1.5;
        margin-top: .35rem;
    }

    .spotlight-card {
        border: 1px solid rgba(94, 234, 212, .22);
        border-radius: 16px;
        padding: 1rem 1.05rem;
        background: rgba(94, 234, 212, .055);
        min-height: 150px;
        box-sizing: border-box;
    }

    .spotlight-kicker {
        color: #A78BFA;
        font-size: .7rem;
        font-weight: 850;
        letter-spacing: .08em;
        text-transform: uppercase;
    }

    .spotlight-value {
        font-size: 2rem;
        font-weight: 900;
        margin-top: .25rem;
    }

    .spotlight-detail {
        opacity: .72;
        font-size: .86rem;
        margin-top: .2rem;
    }


    /* =========================================================
       PAGE INTELLIGENCE SIDEBAR
       ========================================================= */

    .demo-sidebar-shell {
        width: 100%;
        box-sizing: border-box;
        border: 1px solid rgba(139, 92, 246, .58);
        border-radius: 16px;
        background: linear-gradient(
            145deg,
            rgba(25, 35, 58, .96),
            rgba(17, 25, 45, .98)
        );
        padding: 14px;
        overflow: visible;
    }

    .demo-sidebar-title {
        color: #F8FAFC;
        font-size: 16px;
        font-weight: 850;
        line-height: 1.2;
        margin-bottom: 12px;
    }

    .demo-sidebar-card {
        border: 1px solid rgba(129, 140, 248, .28);
        border-radius: 11px;
        background: rgba(10, 17, 32, .42);
        padding: 9px 10px;
        margin-bottom: 8px;
        box-sizing: border-box;
    }

    .demo-sidebar-kicker {
        color: #60A5FA;
        font-size: 9px;
        font-weight: 800;
        letter-spacing: .08em;
        text-transform: uppercase;
        margin-bottom: 3px;
    }

    .demo-sidebar-view {
        color: #F8FAFC;
        font-size: 15px;
        font-weight: 850;
        line-height: 1.2;
    }

    .demo-sidebar-subtitle {
        color: #60A5FA;
        font-size: 10px;
        font-weight: 750;
        line-height: 1.25;
        margin-top: 3px;
        margin-bottom: 7px;
    }

    .demo-sidebar-stat {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: 8px;
        padding: 7px 0;
        border-bottom: 1px solid rgba(148, 163, 184, .12);
    }

    .demo-sidebar-stat:last-child {
        border-bottom: none;
    }

    .demo-sidebar-label {
        color: #94A3B8;
        font-size: 10px;
        line-height: 1.2;
    }

    .demo-sidebar-value {
        color: #F8FAFC;
        font-size: 12px;
        font-weight: 800;
        line-height: 1.2;
        text-align: right;
        word-break: break-word;
    }

    .demo-sidebar-stat.highlight {
        border: 1px solid rgba(45, 212, 191, .30);
        border-radius: 8px;
        background: rgba(45, 212, 191, .08);
        padding: 8px;
        margin: 5px 0;
    }

    .demo-sidebar-big {
        color: #F8FAFC;
        font-size: 19px;
        font-weight: 900;
        line-height: 1.1;
    }

    .demo-sidebar-note {
        border: 1px solid rgba(96, 165, 250, .18);
        border-radius: 9px;
        background: rgba(30, 64, 175, .16);
        padding: 8px 9px;
        color: #CBD5E1;
        font-size: 11px;
        line-height: 1.35;
    }


    /* =========================================================
       PROFILE SEGMENTED CONTROL
       ========================================================= */

    [data-testid="stSegmentedControl"] {
        margin-top: 4px;
        margin-bottom: 14px;
    }

    [data-testid="stSegmentedControl"] button {
        min-height: 42px !important;
        padding: 0 18px !important;
        font-size: 0.90rem !important;
        font-weight: 750 !important;
        border-radius: 9px !important;
    }

    [data-testid="stSegmentedControl"] button p {
        font-size: 0.90rem !important;
        font-weight: 750 !important;
    }

    [data-testid="stSegmentedControl"] button:hover {
        border-color: rgba(167, 139, 250, .70) !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


page_header(
    "👥 Respondent Profile",
    "Explore who is represented in the survey",
    "Compare gender, age, company size, and work arrangement — then use the treatment-rate lens to identify the strongest demographic patterns.",
    level="Respondent Intelligence",
)


# Page filters
with st.container(border=True):
    st.markdown("### 🎛️ Explore the Population")
    st.caption(
        "Refine the respondent population before exploring demographic patterns. "
        "All charts, metrics, and the intelligence sidebar respond to these filters."
    )

    filter_1, filter_2, filter_3, filter_4, filter_5 = st.columns(5)

    with filter_1:
        gender_values = (
            df["Gender"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_gender = st.selectbox(
            "Gender",
            ["All", *sorted(gender_values)],
            key="demo_page_gender",
        )

    with filter_2:
        age_order = [
            "18-24",
            "25-34",
            "35-44",
            "45-54",
            "55-64",
            "65+",
        ]

        age_values = (
            df["Age_Group"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        ordered_age_values = [
            x for x in age_order if x in age_values
        ]

        remaining_age_values = sorted(
            x for x in age_values
            if x not in ordered_age_values
        )

        selected_age_group = st.selectbox(
            "Age Group",
            [
                "All",
                *ordered_age_values,
                *remaining_age_values,
            ],
            key="demo_page_age_group",
        )

    with filter_3:
        company_values = (
            df["Company_Size_Group"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_company = st.selectbox(
            "Company Size",
            ["All", *sorted(company_values)],
            key="demo_page_company_size",
        )

    with filter_4:
        remote_values = (
            df["Remote_Work_Status"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_remote = st.selectbox(
            "Work Arrangement",
            ["All", *sorted(remote_values)],
            key="demo_page_remote_work",
        )

    with filter_5:
        treatment_values = (
            df["treatment"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_treatment = st.selectbox(
            "Treatment",
            ["All", *sorted(treatment_values)],
            key="demo_page_treatment",
        )


# Apply filters
filtered = df.copy()

if selected_gender != "All":
    filtered = filtered[
        filtered["Gender"].astype(str) == selected_gender
    ]

if selected_age_group != "All":
    filtered = filtered[
        filtered["Age_Group"].astype(str) == selected_age_group
    ]

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

if selected_gender != "All":
    active_filters.append(
        f"Gender: {selected_gender}"
    )

if selected_age_group != "All":
    active_filters.append(
        f"Age Group: {selected_age_group}"
    )

if selected_company != "All":
    active_filters.append(
        f"Company Size: {selected_company}"
    )

if selected_remote != "All":
    active_filters.append(
        f"Work Arrangement: {selected_remote}"
    )

if selected_treatment != "All":
    active_filters.append(
        f"Treatment: {selected_treatment}"
    )


if active_filters:
    st.caption(
        "🎯 Active filters: "
        + " • ".join(active_filters)
        + f"  |  {len(filtered):,} respondents"
    )
else:
    st.caption(
        f"🎯 All respondents  |  {len(filtered):,} respondents"
    )


# Dynamic Page Intelligence sidebar
def render_demo_sidebar(
    selected_lens,
    selected_dimension,
    group_col,
    profile_data,
    chart_data,
    filtered_data,
    active_filters_list,
    profile_view=None,
):
    def esc(value):
        return (
            str(value)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
        )

    def stat(label, value, highlight=False):
        cls = (
            "demo-sidebar-stat highlight"
            if highlight
            else "demo-sidebar-stat"
        )

        return (
            f'<div class="{cls}">'
            f'<span class="demo-sidebar-label">{esc(label)}</span>'
            f'<span class="demo-sidebar-value">{esc(value)}</span>'
            f'</div>'
        )

    html = (
        '<div class="demo-sidebar-shell">'
        '<div class="demo-sidebar-title">📌 Page Intelligence</div>'
        '<div class="demo-sidebar-card">'
        '<div class="demo-sidebar-kicker">RESPONDENTS</div>'
        f'<div class="demo-sidebar-big">{len(filtered_data):,}</div>'
        '</div>'
    )

    html += (
        '<div class="demo-sidebar-card">'
        '<div class="demo-sidebar-kicker">CURRENT VIEW</div>'
        f'<div class="demo-sidebar-view">{esc(selected_dimension)}</div>'
        f'<div class="demo-sidebar-subtitle">{esc(selected_lens)}</div>'
    )

    if not profile_data.empty:
        largest = profile_data.loc[
            profile_data["Respondents"].idxmax()
        ]

        smallest = profile_data.loc[
            profile_data["Respondents"].idxmin()
        ]

        share = (
            float(largest["Respondents"])
            / len(filtered_data)
            * 100
        )

        html += stat(
            "Largest group",
            str(largest[group_col]),
            True,
        )

        html += stat(
            "Largest group share",
            f"{share:.1f}%",
        )

        html += stat(
            "Largest group respondents",
            f"{int(largest['Respondents']):,}",
        )

        html += stat(
            "Smallest group",
            str(smallest[group_col]),
        )

    if (
        selected_lens == "Treatment Rate"
        and not chart_data.empty
    ):
        strongest = chart_data.loc[
            chart_data["Treatment Rate"].idxmax()
        ]

        weakest = chart_data.loc[
            chart_data["Treatment Rate"].idxmin()
        ]

        gap = float(
            strongest["Treatment Rate"]
            - weakest["Treatment Rate"]
        )

        html += (
            "</div>"
            '<div class="demo-sidebar-card">'
            '<div class="demo-sidebar-kicker">TREATMENT SIGNAL</div>'
        )

        html += stat(
            "Highest treatment rate",
            f"{float(strongest['Treatment Rate']):.1f}%",
            True,
        )

        html += stat(
            "Highest group",
            str(strongest[group_col]),
        )

        html += stat(
            "Lowest treatment rate",
            f"{float(weakest['Treatment Rate']):.1f}%",
        )

        html += stat(
            "Lowest group",
            str(weakest[group_col]),
        )

        html += stat(
            "Treatment-rate gap",
            f"{gap:.1f} pp",
        )

        html += "</div>"

    else:
        html += "</div>"

        if not profile_data.empty:
            total_groups = profile_data[group_col].nunique()

            median_count = float(
                profile_data["Respondents"].median()
            )

            html += (
                '<div class="demo-sidebar-card">'
                '<div class="demo-sidebar-kicker">PROFILE SIGNAL</div>'
            )

            html += stat(
                "Groups represented",
                str(total_groups),
            )

            html += stat(
                "Median group size",
                f"{median_count:.0f}",
            )

            html += stat(
                "Largest vs smallest",
                f"{int(largest['Respondents']):,} vs "
                f"{int(smallest['Respondents']):,}",
            )

            html += "</div>"

    if profile_view:
        html += (
            '<div class="demo-sidebar-card">'
            '<div class="demo-sidebar-kicker">PROFILE VIEW</div>'
            f'<div class="demo-sidebar-view">{esc(profile_view)}</div>'
            '<div class="demo-sidebar-subtitle">'
            "Respondent profile section"
            "</div>"
            "</div>"
        )

    if active_filters_list:
        html += (
            '<div class="demo-sidebar-note">'
            "<b>Active filters:</b><br>"
            + "<br>".join(
                esc(x) for x in active_filters_list
            )
            + "</div>"
        )

    html += "</div>"

    st.sidebar.html(html)


# Headline metrics
gender_counts = filtered["Gender"].value_counts()
age_valid = filtered["Age"].dropna()

remote_counts = filtered[
    "Remote_Work_Status"
].value_counts()


c1, c2, c3, c4 = st.columns(4)


with c1:
    st.metric(
        "👥 Respondents",
        f"{len(filtered):,}",
        "of filtered respondents",
        help="Number of respondents remaining after the page filters.",
    )


with c2:
    st.metric(
        "♀️ Largest Gender Group",
        (
            str(gender_counts.idxmax())
            if not gender_counts.empty
            else "N/A"
        ),
        (
            f"{int(gender_counts.max()):,} respondents"
            if not gender_counts.empty
            else ""
        ),
    )


with c3:
    st.metric(
        "🎂 Median Age",
        (
            f"{age_valid.median():.0f}"
            if not age_valid.empty
            else "N/A"
        ),
        "years",
    )


with c4:
    remote_pct = (
        filtered["remote_work"].eq("Yes").mean() * 100
        if len(filtered)
        else 0
    )

    st.metric(
        "💻 Remote Workers",
        f"{remote_pct:.1f}%",
        "of filtered respondents",
    )


# Demographic explorer
section_title("🔎 Demographic Explorer")


lens_options = {
    "Treatment Rate": "treatment",
    "Respondent Count": "count",
}


selected_lens = st.radio(
    "Choose your lens",
    list(lens_options.keys()),
    horizontal=True,
    key="demographics_lens",
)


dimension_options = {
    "Gender": "Gender",
    "Age Group": "Age_Group",
    "Company Size": "Company_Size_Group",
    "Work Arrangement": "Remote_Work_Status",
}


selected_dimension = st.selectbox(
    "Choose a demographic dimension",
    list(dimension_options.keys()),
    key="demographics_dimension",
)


group_col = dimension_options[selected_dimension]


def build_profile_data(data, column):
    if column not in data.columns:
        return pd.DataFrame(
            columns=[
                column,
                "Respondents",
            ]
        )

    counts = (
        data[column]
        .dropna()
        .astype(str)
        .value_counts()
        .rename_axis(column)
        .reset_index(name="Respondents")
    )

    if column == "Age_Group":
        order = [
            "18-24",
            "25-34",
            "35-44",
            "45-54",
            "55-64",
            "65+",
        ]

        counts[column] = pd.Categorical(
            counts[column],
            categories=order,
            ordered=True,
        )

        counts = counts.sort_values(column)

    return counts


profile_data = build_profile_data(
    filtered,
    group_col,
)


# Chart palettes for each demographic dimension
treatment_palettes = {
    "Gender": "#2DD4BF",
    "Age_Group": "#A78BFA",
    "Company_Size_Group": "#60A5FA",
    "Remote_Work_Status": "#F472B6",
}


count_palettes = {
    "Gender": "#14B8A6",
    "Age_Group": "#8B5CF6",
    "Company_Size_Group": "#3B82F6",
    "Remote_Work_Status": "#EC4899",
}


if selected_lens == "Treatment Rate":

    chart_data = grouped_treatment_rate(
        filtered,
        group_col,
    ).copy()

    chart_data = chart_data.dropna(
        subset=[
            group_col,
            "Treatment Rate",
        ]
    )

    count_data = profile_data.rename(
        columns={
            "Respondents": "Respondent Count"
        }
    )

    chart_data = chart_data.merge(
        count_data[
            [
                group_col,
                "Respondent Count",
            ]
        ],
        on=group_col,
        how="left",
    )

    if group_col == "Age_Group":
        order = [
            "18-24",
            "25-34",
            "35-44",
            "45-54",
            "55-64",
            "65+",
        ]

        chart_data[group_col] = pd.Categorical(
            chart_data[group_col],
            categories=order,
            ordered=True,
        )

    chart_data = chart_data.sort_values(
        "Treatment Rate"
    )

    treatment_color = treatment_palettes.get(
        group_col,
        "#7DD3FC",
    )

    fig = px.bar(
        chart_data,
        x="Treatment Rate",
        y=group_col,
        orientation="h",
        text="Treatment Rate",
        template=plotly_template(),
        title=f"Treatment Rate by {selected_dimension}",
        custom_data=["Respondent Count"],
    )

    fig.update_traces(
        marker_color=treatment_color,
        marker_line_width=0,
        texttemplate="%{text:.1f}%",
        textposition="outside",
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Treatment rate: <b>%{x:.1f}%</b><br>"
            "Respondents: <b>%{customdata[0]:,}</b>"
            "<extra></extra>"
        ),
    )

    fig.update_layout(
        height=470,
        margin=dict(
            l=20,
            r=75,
            t=65,
            b=40,
        ),
        xaxis=dict(
            range=[0, 100],
            ticksuffix="%",
            title="Treatment Rate (%)",
        ),
        yaxis=dict(
            title="",
        ),
        showlegend=False,
        hoverlabel=dict(
            bgcolor="#151D32",
            font_size=13,
        ),
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displaylogo": False,
            "responsive": True,
            "scrollZoom": True,
            "modeBarButtonsToRemove": [
                "lasso2d",
                "select2d",
            ],
        },
    )

    if not chart_data.empty:
        strongest = chart_data.loc[
            chart_data["Treatment Rate"].idxmax()
        ]

        weakest = chart_data.loc[
            chart_data["Treatment Rate"].idxmin()
        ]

        s1, s2, s3 = st.columns(3)

        with s1:
            st.html(
                f"""
                <div class="spotlight-card">
                    <div class="spotlight-kicker">
                        🏆 Highest treatment rate
                    </div>
                    <div class="spotlight-value">
                        {float(strongest["Treatment Rate"]):.1f}%
                    </div>
                    <div class="spotlight-detail">
                        {str(strongest[group_col])} •
                        {int(strongest["Respondent Count"]):,} respondents
                    </div>
                </div>
                """
            )

        with s2:
            st.html(
                f"""
                <div class="spotlight-card">
                    <div class="spotlight-kicker">
                        📉 Lowest treatment rate
                    </div>
                    <div class="spotlight-value">
                        {float(weakest["Treatment Rate"]):.1f}%
                    </div>
                    <div class="spotlight-detail">
                        {str(weakest[group_col])} •
                        {int(weakest["Respondent Count"]):,} respondents
                    </div>
                </div>
                """
            )

        gap = (
            float(strongest["Treatment Rate"])
            - float(weakest["Treatment Rate"])
        )

        with s3:
            st.html(
                f"""
                <div class="spotlight-card">
                    <div class="spotlight-kicker">
                        ⚖️ Treatment-rate gap
                    </div>
                    <div class="spotlight-value">
                        {gap:.1f} pp
                    </div>
                    <div class="spotlight-detail">
                        Highest group versus lowest group
                    </div>
                </div>
                """
            )

        finding(
            f"💡 The strongest treatment-rate group is "
            f"**{str(strongest[group_col])}** at "
            f"**{float(strongest['Treatment Rate']):.1f}%**. "
            f"Compare the respondent count before interpreting small groups."
        )


else:

    chart_data = profile_data.copy()

    if not chart_data.empty:
        chart_data = chart_data.sort_values(
            "Respondents"
        )

    count_color = count_palettes.get(
        group_col,
        "#A78BFA",
    )

    fig = px.bar(
        chart_data,
        x="Respondents",
        y=group_col,
        orientation="h",
        text="Respondents",
        template=plotly_template(),
        title=f"Respondent Distribution by {selected_dimension}",
    )

    fig.update_traces(
        marker_color=count_color,
        marker_line_width=0,
        texttemplate="%{text:,}",
        textposition="outside",
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Respondents: <b>%{x:,}</b>"
            "<extra></extra>"
        ),
    )

    fig.update_layout(
        height=470,
        margin=dict(
            l=20,
            r=75,
            t=65,
            b=40,
        ),
        xaxis=dict(
            title="Respondents",
        ),
        yaxis=dict(
            title="",
        ),
        showlegend=False,
        hoverlabel=dict(
            bgcolor="#151D32",
            font_size=13,
        ),
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displaylogo": False,
            "responsive": True,
            "scrollZoom": True,
            "modeBarButtonsToRemove": [
                "lasso2d",
                "select2d",
            ],
        },
    )


# Composition views
section_title("🧩 Respondent Profile")


profile_view = st.segmented_control(
    "Profile view",
    options=[
        "👤 Gender",
        "🎂 Age",
        "🏢 Workplace",
    ],
    default="👤 Gender",
    key="demographics_profile_view",
    label_visibility="collapsed",
)


if profile_view is None:
    profile_view = "👤 Gender"


# Render Page Intelligence sidebar after all interactive controls are known
render_demo_sidebar(
    selected_lens,
    selected_dimension,
    group_col,
    profile_data,
    (
        chart_data
        if selected_lens == "Treatment Rate"
        else pd.DataFrame()
    ),
    filtered,
    active_filters,
    profile_view=profile_view,
)


# Gender profile
if profile_view == "👤 Gender":

    gender_data = (
        filtered["Gender"]
        .value_counts()
        .rename_axis("Gender")
        .reset_index(name="Respondents")
    )

    c1, c2 = st.columns([1.15, 1])

    with c1:

        fig = px.pie(
            gender_data,
            names="Gender",
            values="Respondents",
            hole=0.58,
            template=plotly_template(),
            title="Gender Composition",
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
            marker=dict(
                colors=[
                    "#2DD4BF",
                    "#A78BFA",
                    "#F472B6",
                ]
            ),
        )

        fig.update_layout(
            height=410,
            margin=dict(
                l=20,
                r=20,
                t=65,
                b=20,
            ),
            showlegend=False,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
                "displaylogo": False,
                "responsive": True,
            },
        )

    with c2:

        if not gender_data.empty:
            largest = gender_data.iloc[0]

            st.html(
                f"""
                <div class="spotlight-card">
                    <div class="spotlight-kicker">
                        👑 Largest group
                    </div>
                    <div class="spotlight-value">
                        {largest["Gender"]}
                    </div>
                    <div class="spotlight-detail">
                        {int(largest["Respondents"]):,} respondents
                    </div>
                </div>
                """
            )

            st.write("")

            st.caption(
                "Gender values were standardized during data "
                "preparation into Male, Female, and Other."
            )


# Age profile
elif profile_view == "🎂 Age":

    age_data = (
        filtered["Age_Group"]
        .dropna()
        .value_counts()
        .rename_axis("Age Group")
        .reset_index(name="Respondents")
    )

    age_order = [
        "18-24",
        "25-34",
        "35-44",
        "45-54",
        "55-64",
        "65+",
    ]

    age_data["Age Group"] = pd.Categorical(
        age_data["Age Group"],
        categories=age_order,
        ordered=True,
    )

    age_data = age_data.sort_values(
        "Age Group"
    )

    fig = px.bar(
        age_data,
        x="Age Group",
        y="Respondents",
        text="Respondents",
        template=plotly_template(),
        title="Respondent Age Profile",
    )

    fig.update_traces(
        marker_color="#A78BFA",
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
        height=410,
        margin=dict(
            l=20,
            r=25,
            t=65,
            b=45,
        ),
        xaxis_title="Age Group",
        yaxis_title="Respondents",
        showlegend=False,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displaylogo": False,
            "responsive": True,
        },
    )

    st.info(
        "Age groups with very small respondent counts should be "
        "interpreted carefully, especially 55–64 and 65+."
    )


# Workplace profile
else:

    company_data = (
        filtered["Company_Size_Group"]
        .dropna()
        .value_counts()
        .rename_axis("Company Size")
        .reset_index(name="Respondents")
    )

    remote_data = (
        filtered["Remote_Work_Status"]
        .dropna()
        .value_counts()
        .rename_axis("Work Arrangement")
        .reset_index(name="Respondents")
    )

    c1, c2 = st.columns(2)

    with c1:

        fig = px.bar(
            company_data.sort_values(
                "Respondents"
            ),
            x="Respondents",
            y="Company Size",
            orientation="h",
            text="Respondents",
            template=plotly_template(),
            title="Company Size Profile",
        )

        fig.update_traces(
            marker_color="#60A5FA",
            marker_line_width=0,
            texttemplate="%{text:,}",
            textposition="outside",
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Respondents: <b>%{x:,}</b>"
                "<extra></extra>"
            ),
        )

        fig.update_layout(
            height=390,
            margin=dict(
                l=20,
                r=55,
                t=65,
                b=35,
            ),
            xaxis_title="Respondents",
            yaxis_title="",
            showlegend=False,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
                "displaylogo": False,
                "responsive": True,
            },
        )

    with c2:

        fig = px.pie(
            remote_data,
            names="Work Arrangement",
            values="Respondents",
            hole=0.58,
            template=plotly_template(),
            title="Remote Work Composition",
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
            marker=dict(
                colors=[
                    "#F59E0B",
                    "#F472B6",
                ]
            ),
        )

        fig.update_layout(
            height=390,
            margin=dict(
                l=20,
                r=20,
                t=65,
                b=20,
            ),
            showlegend=False,
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
                "displaylogo": False,
                "responsive": True,
            },
        )


# Key takeaway
section_title("🧠 Key Takeaway")


treatment_pct = treatment_rate(filtered)


finding(
    f"📌 In the current filtered view, the overall treatment rate is "
    f"**{treatment_pct:.1f}%**. Demographic differences should be "
    f"interpreted alongside respondent counts and the observational "
    f"nature of the survey."
)


st.markdown(
    """
    <div class="footer-note">
        Source: 2014 Mental Health in Tech Survey •
        Association does not imply causation •
        Results update with the selected filters.
    </div>
    """,
    unsafe_allow_html=True,
)