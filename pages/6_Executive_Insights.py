import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import load_data
from utils.analytics import grouped_treatment_rate
from utils.styling import (
    apply_global_style,
    page_header,
    register_page,
    section_title,
    finding,
    plotly_template,
)

st.set_page_config(
    page_title="Executive Insights",
    page_icon="💡",
    layout="wide",
)

apply_global_style()

# Page styling
st.html(
    """
    <style>
    /* Main page spacing */
    .stMainBlockContainer {
        padding-top: 2.8rem !important;
        padding-bottom: 2.5rem !important;
    }

    [data-testid="stAppViewContainer"] .main .block-container {
        padding-top: 2.8rem !important;
        padding-bottom: 2.5rem !important;
    }

    /* Native Streamlit multipage sidebar navigation */
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

    /* Only the native page navigation is styled here. */

    /* Executive insight cards */
    .insight-card {
        padding: 1rem 1.05rem;
        border: 1px solid rgba(167,139,250,.24);
        border-radius: 14px;
        background: rgba(21,29,50,.72);
        min-height: 148px;
    }

    .insight-card .eyebrow {
        font-size: .72rem;
        font-weight: 800;
        letter-spacing: .04em;
        text-transform: uppercase;
        opacity: .68;
        margin-bottom: .45rem;
    }

    .insight-card .value {
        font-size: 1.8rem;
        font-weight: 850;
        line-height: 1.05;
        margin-bottom: .35rem;
    }

    .insight-card .label {
        font-size: .88rem;
        font-weight: 700;
        margin-bottom: .25rem;
    }

    .insight-card .detail {
        font-size: .76rem;
        line-height: 1.4;
        opacity: .68;
    }

    .action-card {
        padding: .95rem 1rem;
        border-left: 3px solid #2DD4BF;
        border-radius: 10px;
        background: rgba(45,212,191,.055);
        margin-bottom: .55rem;
    }

    .action-card strong {
        font-size: .94rem;
    }

    .action-card p {
        margin: .22rem 0 0 0;
        font-size: .78rem;
        line-height: 1.4;
        opacity: .72;
    }

    /* Keep Streamlit toolbar/menu visible */
    [data-testid="stToolbar"] {
        display: flex !important;
    }
    </style>
    """
)

# Load data
df = load_data()

if df.empty:
    st.error("No data available.")
    st.stop()

# Executive Insights uses the complete survey population.
filtered = df.copy()

# Executive sidepanel
# This is intentionally insight-led rather than a second filter panel.
family_sidebar = grouped_treatment_rate(filtered, "family_history")
family_sidebar_yes = (
    float(
        family_sidebar.loc[
            family_sidebar["family_history"] == "Yes",
            "Treatment Rate",
        ].iloc[0]
    )
    if not family_sidebar.loc[
        family_sidebar["family_history"] == "Yes", "Treatment Rate"
    ].empty
    else None
)
family_sidebar_no = (
    float(
        family_sidebar.loc[
            family_sidebar["family_history"] == "No",
            "Treatment Rate",
        ].iloc[0]
    )
    if not family_sidebar.loc[
        family_sidebar["family_history"] == "No", "Treatment Rate"
    ].empty
    else None
)

work_sidebar = grouped_treatment_rate(filtered, "work_interfere")
work_sidebar = work_sidebar[
    work_sidebar["work_interfere"] != "Not Answered"
].copy()

work_sidebar_often = (
    float(
        work_sidebar.loc[
            work_sidebar["work_interfere"] == "Often",
            "Treatment Rate",
        ].iloc[0]
    )
    if not work_sidebar.loc[
        work_sidebar["work_interfere"] == "Often", "Treatment Rate"
    ].empty
    else None
)
work_sidebar_never = (
    float(
        work_sidebar.loc[
            work_sidebar["work_interfere"] == "Never",
            "Treatment Rate",
        ].iloc[0]
    )
    if not work_sidebar.loc[
        work_sidebar["work_interfere"] == "Never", "Treatment Rate"
    ].empty
    else None
)

family_gap_sidebar = (
    family_sidebar_yes - family_sidebar_no
    if family_sidebar_yes is not None and family_sidebar_no is not None
    else None
)
work_gap_sidebar = (
    work_sidebar_often - work_sidebar_never
    if work_sidebar_often is not None and work_sidebar_never is not None
    else None
)

family_gap_text = (
    f"{family_gap_sidebar:+.1f} pp"
    if family_gap_sidebar is not None
    else "—"
)
work_gap_text = (
    f"{work_gap_sidebar:+.1f} pp"
    if work_gap_sidebar is not None
    else "—"
)
family_detail = (
    f"{family_sidebar_yes:.1f}% with family history vs {family_sidebar_no:.1f}% without."
    if family_sidebar_yes is not None and family_sidebar_no is not None
    else "Comparison unavailable."
)
work_detail = (
    f"{work_sidebar_often:.1f}% for Often vs {work_sidebar_never:.1f}% for Never."
    if work_sidebar_often is not None and work_sidebar_never is not None
    else "Comparison unavailable."
)

with st.sidebar:
    st.html(
        f"""
        <style>
        .exec-brief-panel {{
            box-sizing: border-box;
            width: 100%;
            margin: 0.25rem 0 0.5rem 0;
            padding: 10px;
            border: 1px solid rgba(167,139,250,.55);
            border-radius: 16px;
            background: rgba(21,29,50,.58);
            color: #F5F7FF;
            font-family: inherit;
        }}
        .exec-brief-title {{ display:flex; align-items:center; gap:7px; font-size:.91rem; font-weight:800; line-height:1.15; margin:1px 2px 3px; }}
        .exec-brief-subtitle {{ color:#AAB4CC; font-size:.62rem; line-height:1.25; margin:0 2px 8px; }}
        .exec-divider {{ height:1px; background:rgba(167,139,250,.24); margin:7px 0; }}
        .exec-section-title {{ font-size:.73rem; font-weight:800; line-height:1.15; margin:7px 2px 6px; }}
        .exec-card {{ border:1px solid rgba(167,139,250,.26); border-radius:11px; background:rgba(11,16,32,.34); padding:8px 9px; margin:0 0 6px; }}
        .exec-card.accent {{ border-color:rgba(45,212,191,.48); background:rgba(45,212,191,.08); }}
        .exec-label {{ color:#AAB4CC; font-size:.57rem; line-height:1.15; margin-bottom:3px; }}
        .exec-value {{ color:#FFFFFF; font-size:.96rem; font-weight:850; line-height:1.05; }}
        .exec-detail {{ color:#AAB4CC; font-size:.56rem; line-height:1.25; margin-top:3px; }}
        .exec-action {{ padding:7px 8px; border:1px solid rgba(167,139,250,.22); border-radius:9px; background:rgba(11,16,32,.25); margin-bottom:5px; }}
        .exec-action-title {{ color:#FFFFFF; font-size:.61rem; font-weight:750; line-height:1.15; }}
        .exec-action-text {{ color:#AAB4CC; font-size:.55rem; line-height:1.25; margin-top:3px; }}
        .exec-takeaway {{ padding:8px 9px; border-radius:9px; background:rgba(30,64,112,.72); color:#F5F7FF; font-size:.57rem; line-height:1.28; }}
        .exec-footnote {{ color:#AAB4CC; font-size:.52rem; line-height:1.2; margin:6px 1px 1px; }}
        </style>
        <div class="exec-brief-panel">
            <div class="exec-brief-title">💡 Executive Brief</div>
            <div class="exec-brief-subtitle">Key survey signals and recommended actions.</div>
            <div class="exec-divider"></div>
            <div class="exec-section-title">🔎 Strongest Signals</div>
            <div class="exec-card">
                <div class="exec-label">Family history treatment gap</div>
                <div class="exec-value">{family_gap_text}</div>
                <div class="exec-detail">{family_detail}</div>
            </div>
            <div class="exec-card accent">
                <div class="exec-label">Work interference gap</div>
                <div class="exec-value">{work_gap_text}</div>
                <div class="exec-detail">{work_detail}</div>
            </div>
            <div class="exec-divider"></div>
            <div class="exec-section-title">🎯 What Leaders Should Do</div>
            <div class="exec-action"><div class="exec-action-title">1. Improve access</div><div class="exec-action-text">Make mental-health benefits and care options easy to find and use.</div></div>
            <div class="exec-action"><div class="exec-action-title">2. Support early</div><div class="exec-action-text">Create practical support pathways before difficulties strongly interfere with work.</div></div>
            <div class="exec-action"><div class="exec-action-title">3. Build trust</div><div class="exec-action-text">Clearly explain confidentiality, privacy, and available support.</div></div>
            <div class="exec-divider"></div>
            <div class="exec-section-title">📌 Executive Takeaway</div>
            <div class="exec-takeaway">Treatment behavior varies substantially across key mental-health and workplace factors. The clearest business opportunity is to improve access, early support, and trust.</div>
            <div class="exec-footnote">Observational associations, not causal or clinical conclusions.</div>
        </div>
        """
    )

page_header(
    "💡 Executive Insights",
    "From analysis to business action",
    "Translate the strongest survey relationships into practical workplace actions.",
)

if filtered.empty:
    st.warning("No respondents match the selected filters.")
    st.stop()

# -------------------------------------------------------------------
# Executive snapshot
# -------------------------------------------------------------------

section_title("Executive Snapshot")

total = len(filtered)

treatment_yes = (
    filtered["treatment"].eq("Yes").mean() * 100
    if "treatment" in filtered.columns
    else 0
)

family = grouped_treatment_rate(filtered, "family_history")
family_yes = (
    float(family.loc[family["family_history"] == "Yes", "Treatment Rate"].iloc[0])
    if not family.loc[family["family_history"] == "Yes", "Treatment Rate"].empty
    else None
)
family_no = (
    float(family.loc[family["family_history"] == "No", "Treatment Rate"].iloc[0])
    if not family.loc[family["family_history"] == "No", "Treatment Rate"].empty
    else None
)

work = grouped_treatment_rate(filtered, "work_interfere")
work = work[work["work_interfere"] != "Not Answered"].copy()

work_often = (
    float(work.loc[work["work_interfere"] == "Often", "Treatment Rate"].iloc[0])
    if not work.loc[work["work_interfere"] == "Often", "Treatment Rate"].empty
    else None
)
work_never = (
    float(work.loc[work["work_interfere"] == "Never", "Treatment Rate"].iloc[0])
    if not work.loc[work["work_interfere"] == "Never", "Treatment Rate"].empty
    else None
)

family_gap = family_yes - family_no if family_yes is not None and family_no is not None else None
work_gap = work_often - work_never if work_often is not None and work_never is not None else None

kpi_cols = st.columns(4)

with kpi_cols[0]:
    st.metric(
        "Respondents",
        f"{total:,}",
        help="Number of respondents remaining after the selected sidebar filters.",
    )

with kpi_cols[1]:
    st.metric(
        "Treatment Rate",
        f"{treatment_yes:.1f}%",
        help="Share of filtered respondents who reported receiving treatment.",
    )

with kpi_cols[2]:
    if family_gap is not None:
        st.metric(
            "Family History Gap",
            f"{family_gap:+.1f} pp",
            help="Treatment-rate difference between respondents with and without reported family history.",
        )
    else:
        st.metric("Family History Gap", "—")

with kpi_cols[3]:
    if work_gap is not None:
        st.metric(
            "Work Interference Gap",
            f"{work_gap:+.1f} pp",
            help="Treatment-rate difference between 'Often' and 'Never' work interference.",
        )
    else:
        st.metric("Work Interference Gap", "—")

st.caption(
    "The snapshot reflects the complete survey population."
)

# -------------------------------------------------------------------
# Strongest evidence
# -------------------------------------------------------------------

section_title("Strongest Evidence")

evidence_view = st.segmented_control(
    "Choose an evidence lens",
    ["👨‍👩‍👧 Family History", "💼 Work Interference"],
    default="👨‍👩‍👧 Family History",
    label_visibility="collapsed",
    key="executive_evidence_lens",
)

if evidence_view == "👨‍👩‍👧 Family History":
    left, right = st.columns([1.15, 1])

    with left:
        st.subheader("Family history is a strong treatment signal")

        if family_yes is not None and family_no is not None:
            st.metric(
                "Treatment-rate difference",
                f"{family_gap:.1f} percentage points",
            )
            st.write(
                f"Respondents reporting a family history had a **{family_yes:.1f}%** "
                f"treatment rate, compared with **{family_no:.1f}%** among those "
                "without a reported family history."
            )
            finding(
                "Business implication: family history can be used as an awareness "
                "signal when designing education and support pathways, but it should "
                "not be treated as a diagnosis or causal explanation."
            )
        else:
            st.info("Family-history comparison is not available for the current filters.")

    with right:
        if not family.empty:
            chart = family.copy()
            chart["Treatment Rate"] = chart["Treatment Rate"].astype(float)

            fig = px.bar(
                chart,
                x="family_history",
                y="Treatment Rate",
                text="Treatment Rate",
                labels={
                    "family_history": "Family history",
                    "Treatment Rate": "Treatment rate (%)",
                },
                template=plotly_template(),
            )
            fig.update_traces(
                texttemplate="%{text:.1f}%",
                textposition="outside",
            )
            fig.update_layout(
                height=330,
                margin=dict(l=10, r=10, t=35, b=10),
                yaxis=dict(range=[0, max(100, chart["Treatment Rate"].max() + 10)]),
            )
            st.plotly_chart(
                fig,
                use_container_width=True,
                config={"displayModeBar": True, "displaylogo": False},
                key="executive_family_history_chart",
            )

else:
    left, right = st.columns([1.15, 1])

    with left:
        st.subheader("Work interference separates treatment behavior")

        if work_often is not None and work_never is not None:
            st.metric(
                "Treatment-rate difference",
                f"{work_gap:.1f} percentage points",
            )
            st.write(
                f"Treatment was reported by **{work_often:.1f}%** of respondents "
                f"whose mental health often interfered with work, versus "
                f"**{work_never:.1f}%** among those reporting no interference."
            )
            finding(
                "Business implication: workplace support should focus on reducing "
                "barriers before mental-health difficulties become highly disruptive "
                "to day-to-day work."
            )
        else:
            st.info("Work-interference comparison is not available for the current filters.")

    with right:
        if not work.empty:
            chart = work.copy()
            chart["Treatment Rate"] = chart["Treatment Rate"].astype(float)

            order = ["Never", "Rarely", "Sometimes", "Often"]
            chart["order"] = chart["work_interfere"].map(
                {value: index for index, value in enumerate(order)}
            )
            chart = chart.sort_values("order")

            fig = px.bar(
                chart,
                x="work_interfere",
                y="Treatment Rate",
                text="Treatment Rate",
                labels={
                    "work_interfere": "Work interference",
                    "Treatment Rate": "Treatment rate (%)",
                },
                template=plotly_template(),
            )
            fig.update_traces(
                texttemplate="%{text:.1f}%",
                textposition="outside",
            )
            fig.update_layout(
                height=330,
                margin=dict(l=10, r=10, t=35, b=10),
                yaxis=dict(range=[0, max(100, chart["Treatment Rate"].max() + 10)]),
            )
            st.plotly_chart(
                fig,
                use_container_width=True,
                config={"displayModeBar": True, "displaylogo": False},
                key="executive_work_interference_chart",
            )

# -------------------------------------------------------------------
# Insight explorer
# -------------------------------------------------------------------

section_title("Insight Explorer")

lens = st.selectbox(
    "Explore a business question",
    [
        "Where is the largest treatment gap?",
        "What should workplace leaders prioritize?",
        "What should be communicated to employees?",
    ],
    key="executive_question_lens",
)

if lens == "Where is the largest treatment gap?":
    comparisons = []

    if family_gap is not None:
        comparisons.append(
            {
                "Driver": "Family history",
                "Gap": family_gap,
                "Higher-treatment group": "Reported family history",
            }
        )

    if work_gap is not None:
        comparisons.append(
            {
                "Driver": "Work interference",
                "Gap": work_gap,
                "Higher-treatment group": "Often interferes with work",
            }
        )

    if comparisons:
        comparison_df = pd.DataFrame(comparisons).sort_values(
            "Gap", ascending=False
        )
        strongest = comparison_df.iloc[0]

        st.info(
            f"**{strongest['Driver']}** has the largest observed gap in the "
            f"current filtered population: **{strongest['Gap']:.1f} percentage points**."
        )

        st.dataframe(
            comparison_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Gap": st.column_config.NumberColumn(
                    "Treatment-rate gap",
                    format="%.1f pp",
                )
            },
        )
    else:
        st.info("There are not enough comparison groups under the current filters.")

elif lens == "What should workplace leaders prioritize?":
    st.write(
        "The analysis points toward three practical priorities:"
    )

    priorities = [
        (
            "1",
            "Access",
            "Make mental-health care options and benefits easy to discover and use.",
        ),
        (
            "2",
            "Early support",
            "Create supportive pathways before mental-health difficulties strongly interfere with work.",
        ),
        (
            "3",
            "Trust",
            "Clearly communicate confidentiality, available resources, and how employees can seek help.",
        ),
    ]

    cols = st.columns(3)
    for col, (number, title, description) in zip(cols, priorities):
        with col:
            with st.container(border=True):
                st.markdown(f"### {number}. {title}")
                st.write(description)

else:
    st.write(
        "Employee-facing communication should be practical, confidential, and "
        "easy to act on rather than relying only on awareness messaging."
    )

    communication = [
        "Where employees can find mental-health benefits and care options.",
        "How confidentiality and anonymity are handled.",
        "How to access support without needing to disclose unnecessary personal information.",
        "What workplace resources are available when mental health begins affecting work.",
    ]

    for item in communication:
        st.markdown(f"- {item}")

# -------------------------------------------------------------------
# Action plan
# -------------------------------------------------------------------

section_title("Recommended Action Plan")

recommendations = [
    (
        "Strengthen access to mental-health care",
        "Make confidential care options easier to discover, understand, and access.",
        "Priority",
    ),
    (
        "Improve awareness of available support",
        "Clearly communicate benefits, care options, wellness resources, and help-seeking pathways.",
        "Priority",
    ),
    (
        "Protect and communicate confidentiality",
        "Build trust by explaining how sensitive mental-health information is handled.",
        "Trust",
    ),
    (
        "Equip managers and supervisors",
        "Provide practical guidance for recognizing support needs and responding appropriately.",
        "Culture",
    ),
    (
        "Review practical workplace support",
        "Evaluate wellness programs, leave policies, and resources that can reduce workplace barriers.",
        "Workplace",
    ),
    (
        "Track support gaps over time",
        "Use recurring analysis to identify whether access and workplace-support patterns are improving.",
        "Measurement",
    ),
]

for title, description, category in recommendations:
    with st.container(border=True):
        cols = st.columns([0.14, 0.66, 0.20])

        with cols[0]:
            st.markdown(f"**{category}**")

        with cols[1]:
            st.markdown(f"**{title}**")
            st.caption(description)

        with cols[2]:
            if category in {"Priority", "Trust"}:
                st.info("Recommended")
            else:
                st.caption("Strategic")

# -------------------------------------------------------------------
# Executive interpretation
# -------------------------------------------------------------------

section_title("Executive Interpretation")

with st.container(border=True):
    st.subheader("What the analysis supports")

    interpretation_points = [
        "Treatment behavior is not evenly distributed across respondents.",
        "Family history and work interference show particularly strong observed differences in treatment rates.",
        "Workplace policies and support mechanisms should be treated as access and culture levers rather than assumed causes of treatment behavior.",
        "The findings are observational associations and should not be interpreted as causal conclusions.",
    ]

    for point in interpretation_points:
        st.markdown(f"- {point}")

st.caption(
    "Recommendations are based on observed survey associations. They are intended "
    "for workplace planning and should not be interpreted as clinical advice or causal conclusions."
)
